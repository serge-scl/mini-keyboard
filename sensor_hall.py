# Adafruit CircuitPython 8.2.6 on 2023-09-12; Raspberry Pi Pico with rp2040
# ........................................

"""
Hall effect sensor keyboard controller for Raspberry Pi Pico.

Uses analog hall sensors for top-bottom and left-right movement detection.
A 0.5 second sample interval is used for debugging convenience.
Application window must be activated within a ten-second period to begin text entry.
"""

import asyncio
import board
import analogio
import usb_hid
import time

from adafruit_hid.keyboard import Keyboard
from pk_layout import pyramid_keyboard_layout

# Try to import the touch sensor accessor sens_touch() from sensor_touch.py.
# sens_touch() is expected to return an integer 1..15 for touch addresses or 16 for "no touch".
try:
    from sensor_touch import sens_touch
except Exception as e:
    sens_touch = None
    print("Warning: could not import sens_touch from sensor_touch.py:", e)

# Character mappings for different key positions
TOP_BOTTOM_CHARACTERS = ["'1", "\"2", "(3", "[4", "{5",
                         "$6", "#7", "@8", ";9", "%0",
                         ">+", "<-", "&*", ":/", "!="]
RIGHT_LEFT_CHARACTERS = ["qw", "er", "ty", "ui", "op",
                         "as", "df", "gh", "jk", "l^",
                         "zx", "cv", "bn", "m?", ",."]

# Sensor calibration and thresholds
SENSOR_THRESHOLD = 58500
TB_LABEL = None  # Will be set during autocalibration
LR_LABEL = None  # Will be set during autocalibration
BUFFER_SIZE = 20
SAMPLE_DELAY = 0.5
MIN_MOVEMENT = 100  # Minimum movement to register a key press
CALIBRATION_SAMPLES = 10  # Number of samples to collect during calibration

# Global keyboard device
mkps = Keyboard(usb_hid.devices)

# Async control (can be set from outside to stop loops)
stop_event = asyncio.Event()


class HallBuffer:
    """Buffer for storing sensor readings."""
    
    def __init__(self):
        # initialize buffers with their label sentinel values
        self.tb_hall = [TB_LABEL] if TB_LABEL is not None else []
        self.lr_hall = [LR_LABEL] if LR_LABEL is not None else []
    
    def reset(self):
        """Reset buffers after sending a key."""
        self.tb_hall = [TB_LABEL] if TB_LABEL is not None else []
        self.lr_hall = [LR_LABEL] if LR_LABEL is not None else []


async def autocalibrate_sensors():
    """
    Autocalibrate Hall sensors at startup.
    Waits for no-touch condition (sens_touch() == 16) and then collects
    CALIBRATION_SAMPLES readings from both sensors to establish baseline values.
    
    Returns:
        tuple: (TB_LABEL, LR_LABEL) calibrated values
    """
    global TB_LABEL, LR_LABEL
    
    print("Starting sensor autocalibration...")
    print("Please ensure no keys are being touched.")
    
    if sens_touch is None:
        print("Error: sens_touch unavailable; cannot autocalibrate. Using default values.")
        TB_LABEL = 58501
        LR_LABEL = 58502
        return TB_LABEL, LR_LABEL
    
    # Wait for no-touch condition
    max_wait_attempts = 50  # ~25 seconds at 0.5s per check
    wait_attempts = 0
    
    while wait_attempts < max_wait_attempts:
        try:
            x = sens_touch()
            if x == 16:  # No touch detected
                print("No-touch condition detected. Beginning calibration...")
                break
        except Exception as e:
            print("Error reading touch sensor during wait:", e)
        
        await asyncio.sleep(0.5)
        wait_attempts += 1
    else:
        print("Warning: Timeout waiting for no-touch condition. Proceeding anyway.")
    
    # Collect calibration samples
    tb_samples = []
    lr_samples = []
    
    print(f"Collecting {CALIBRATION_SAMPLES} calibration samples...")
    
    try:
        with analogio.AnalogIn(board.A0) as pin_tb, analogio.AnalogIn(board.A1) as pin_lr:
            for i in range(CALIBRATION_SAMPLES):
                tb_samples.append(pin_tb.value)
                lr_samples.append(pin_lr.value)
                print(f"Sample {i+1}: TB={pin_tb.value}, LR={pin_lr.value}")
                await asyncio.sleep(SAMPLE_DELAY)
    except Exception as e:
        print("Error during sensor calibration:", e)
        TB_LABEL = 58501
        LR_LABEL = 58502
        return TB_LABEL, LR_LABEL
    
    # Calculate average values
    TB_LABEL = sum(tb_samples) // len(tb_samples)
    LR_LABEL = sum(lr_samples) // len(lr_samples)
    
    print(f"Calibration complete!")
    print(f"TB_LABEL (board.A0) = {TB_LABEL}")
    print(f"LR_LABEL (board.A1) = {LR_LABEL}")
    
    return TB_LABEL, LR_LABEL


def send_key(character):
    """
    Send keyboard key based on character.
    
    Args:
        character: single-character string from the keyboard layout mapping
    """
    if character not in pyramid_keyboard_layout:
        print("Character not in layout:", repr(character))
        return
    
    key_code = pyramid_keyboard_layout[character]
    
    if isinstance(key_code, tuple):
        mkps.send(key_code[0], key_code[1])
    else:
        mkps.send(key_code)


async def process_and_send_key(buffer_obj, primary_buffer, secondary_buffer):
    """
    Process accumulated sensor data and send appropriate key according to the
    pyramid two-level rules described:
      - get x from sens_touch(): 1..15 => index 0..14, 16 => no touch (do nothing)
      - get TB and LR character pairs for that index
      - compare middle of primary vs secondary to choose which pair to use
      - within chosen pair, select [0] if min(buffer) < LABEL or [1] if max(buffer) > LABEL
      - send resulting single character via pyramid_keyboard_layout -> mkps.send
    Args:
        buffer_obj: HallBuffer instance (so we can reset both buffers after a send)
        primary_buffer: list of readings for primary axis (this buffer)
        secondary_buffer: list of readings for the other axis
    """
    # need at least some readings
    if len(primary_buffer) <= 1 or len(secondary_buffer) <= 1:
        return

    # If sens_touch is not available, we cannot decide the x position; skip
    if sens_touch is None:
        print("sens_touch unavailable; skipping key send.")
        return

    try:
        x = sens_touch()  # expected 1..15 or 16 for no-touch
    except Exception as e:
        print("Error reading touch sensor:", e)
        return

    # If 16 (no touch), do nothing
    if x == 16:
        return

    # Safety: ensure x in 1..15
    if not (1 <= x <= 15):
        print("Received unexpected touch value:", x)
        return

    idx = x - 1  # convert to 0..14

    # Get pairs
    try:
        tb_pair = TOP_BOTTOM_CHARACTERS[idx]
        lr_pair = RIGHT_LEFT_CHARACTERS[idx]
    except IndexError:
        print("Index out of range for character mappings:", idx)
        return

    # Compute middle values for tilt decision
    middle_primary = sum(primary_buffer) / len(primary_buffer)
    middle_secondary = sum(secondary_buffer) / len(secondary_buffer)

    # Choose which pair by tilt: primary vs secondary
    # If primary middle > secondary middle => use TOP_BOTTOM (primary is TB buffer)
    # If primary middle < secondary middle => use RIGHT_LEFT (primary is TB buffer)
    # The call sites will pass the correct buffers so this comparison works generically.
    if middle_primary > middle_secondary:
        chosen_pair = tb_pair
        # for TB comparison we use TB_LABEL and primary_buffer (because TB is primary here)
        threshold = TB_LABEL
        selected_buffer = primary_buffer
    else:
        chosen_pair = lr_pair
        threshold = LR_LABEL
        selected_buffer = secondary_buffer

    # chosen_pair is a two-character string like "'1" -> char0 and char1
    char_to_send = None

    if min(selected_buffer) < threshold:
        char_to_send = chosen_pair[0]
    elif max(selected_buffer) > threshold:
        char_to_send = chosen_pair[1]

    if char_to_send:
        send_key(char_to_send)
        # reset after sending to avoid duplicates
        buffer_obj.reset()


async def hall_sensor(pin, buffer_obj, primary_buf, secondary_buf):
    """
    Read hall effect sensor and detect key presses.
    
    Args:
        pin: Analog pin to read from
        buffer_obj: HallBuffer instance (so we can reset both buffers after send)
        primary_buf: Primary sensor buffer for this pin
        secondary_buf: Secondary sensor buffer for comparison
    """
    with analogio.AnalogIn(pin) as pin_x:
        while not stop_event.is_set():
            primary_buf.append(pin_x.value)
            
            # Debug print
            print("Primary:", primary_buf, "Secondary:", secondary_buf)
            
            if len(primary_buf) > BUFFER_SIZE:
                # maintain sliding window
                primary_buf.pop(0)
                # process and possibly send a key
                await process_and_send_key(buffer_obj, primary_buf, secondary_buf)
                # continue running (do not stop the whole system)
            
            await asyncio.sleep(SAMPLE_DELAY)


async def main():
    """
    Main async coroutine for running the keyboard controller.
    """
    # Perform autocalibration at startup
    await autocalibrate_sensors()
    
    buffer_hall = HallBuffer()
    
    # Create sensor reading tasks
    hall_tb = asyncio.create_task(
        hall_sensor(board.A0, buffer_hall, buffer_hall.tb_hall, buffer_hall.lr_hall)
    )
    hall_lr = asyncio.create_task(
        hall_sensor(board.A1, buffer_hall, buffer_hall.lr_hall, buffer_hall.tb_hall)
    )
    
    # Run both sensor tasks until stop_event is set externally
    await asyncio.gather(hall_tb, hall_lr)

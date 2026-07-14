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

from adafruit_hid.keyboard import Keyboard
from pk_layout import pyramid_keyboard_layout

# Character mappings for different key positions
TOP_BOTTOM_CHARACTERS = ["'1", "\"2", "(3", "[4", "{5",
                         "$6", "#7", "@8", ";9", "%0",
                         ">+", "<-", "&*", ":/", "!="]
RIGHT_LEFT_CHARACTERS = ["qw", "er", "ty", "ui", "op",
                         "as", "df", "gh", "jk", "l^",
                         "zx", "cv", "bn", "m?", ",."]

# Sensor calibration and thresholds
SENSOR_THRESHOLD = 58500
TB_LABEL = 58501
LR_LABEL = 58502
BUFFER_SIZE = 20
SAMPLE_DELAY = 0.5
MIN_MOVEMENT = 100  # Minimum movement to register a key press

# Global keyboard device
mkps = Keyboard(usb_hid.devices)

# Async control
stop_event = asyncio.Event()


class HallBuffer:
    """Buffer for storing sensor readings."""
    
    def __init__(self):
        self.tb_hall = [TB_LABEL]
        self.lr_hall = [LR_LABEL]
    
    def reset(self):
        """Reset buffers after sending a key."""
        self.tb_hall = [TB_LABEL]
        self.lr_hall = [LR_LABEL]


def select_character(move_h, move_h1, middle_h, middle_h1, label):
    """
    Determine which character to send based on movement and sensor calibration.
    
    Args:
        move_h: Movement range in primary axis
        move_h1: Movement range in secondary axis
        middle_h: Average value in primary axis
        middle_h1: Average value in secondary axis
        label: Sensor type label (TB_LABEL or LR_LABEL)
    
    Returns:
        Tuple of (character, charset) or None if no significant movement detected
    """
    if abs(move_h) <= abs(move_h1) or abs(move_h) < MIN_MOVEMENT:
        return None
    
    # Select character set based on sensor label
    charset = TOP_BOTTOM_CHARACTERS if label == TB_LABEL else RIGHT_LEFT_CHARACTERS
    
    # Choose character based on which direction moved more
    if middle_h > middle_h1:
        return charset[0]
    elif middle_h < middle_h1:
        return charset[1]
    
    return None


def send_key(character):
    """
    Send keyboard key based on character.
    
    Args:
        character: Character from the keyboard layout mapping
    """
    if character not in pyramid_keyboard_layout:
        return
    
    key_code = pyramid_keyboard_layout[character]
    
    if isinstance(key_code, tuple):
        mkps.send(key_code[0], key_code[1])
    else:
        mkps.send(key_code)


async def process_and_send_key(buffer, other_buffer, character_index, label):
    """
    Process accumulated sensor data and send appropriate key.
    
    Args:
        buffer: Primary sensor buffer
        other_buffer: Secondary sensor buffer for comparison
        character_index: Index into character set
        label: Sensor type label
    """
    if len(buffer) <= 1 or len(other_buffer) <= 1:
        return
    
    move_h = max(buffer) - min(buffer)
    move_h1 = max(other_buffer) - min(other_buffer)
    middle_h = sum(buffer) / len(buffer)
    middle_h1 = sum(other_buffer) / len(other_buffer)
    
    character = select_character(move_h, move_h1, middle_h, middle_h1, label)
    
    if character:
        send_key(character)


async def hall_sensor(pin, buffer, other_buffer, character_index, label):
    """
    Read hall effect sensor and detect key presses.
    
    Args:
        pin: Analog pin to read from
        buffer: Primary sensor buffer for this pin
        other_buffer: Secondary sensor buffer for comparison
        character_index: Index into character set
        label: Sensor type label (TB_LABEL or LR_LABEL)
    """
    with analogio.AnalogIn(pin) as pin_x:
        while not stop_event.is_set():
            buffer.append(pin_x.value)
            
            print(f"Buffer: {buffer}, Other: {other_buffer}")
            
            if len(buffer) > BUFFER_SIZE:
                buffer.pop(0)
                await process_and_send_key(buffer, other_buffer, character_index, label)
                stop_event.set()
            
            await asyncio.sleep(SAMPLE_DELAY)


async def main(character_index):
    """
    Main async coroutine for running the keyboard controller.
    
    Args:
        character_index: Index into character set (0-14)
    """
    buffer_hall = HallBuffer()
    
    # Create sensor reading tasks
    hall_tb = asyncio.create_task(
        hall_sensor(board.A0, buffer_hall.tb_hall, buffer_hall.lr_hall, character_index, TB_LABEL)
    )
    hall_lr = asyncio.create_task(
        hall_sensor(board.A1, buffer_hall.lr_hall, buffer_hall.tb_hall, character_index, LR_LABEL)
    )
    
    # Run both sensor tasks
    await asyncio.gather(hall_tb, hall_lr)

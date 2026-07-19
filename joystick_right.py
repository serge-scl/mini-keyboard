import time
import math
import board
import pulseio
import usb_hid
from adafruit_hid.keyboard import Keyboard

# import keyboard layout and touch sensor module (if available)
from pk_layout import pyramid_keyboard_layout

try:
    import sensor_touch as st  # module provides mpr121 and sens_touch()
    sens_touch = st.sens_touch
except Exception as e:
    st = None
    sens_touch = None
    print("Warning: could not import sensor_touch module:", e)

control_command_clock = {'12': 'Shift', '3': '->', '6':'Enter', '9': 'Alt'}

# Pin settings: X - sensor A, Y - sensor B
pin_x = board.GP10
pin_y = board.GP11

pulse_x = pulseio.PulseIn(pin_x, maxlen=2)
pulse_y = pulseio.PulseIn(pin_y, maxlen=2)

# --- CALIBRATION SETTINGS ---
# Run the code, look at the actual percentages in the console at the extremes
# and enter your own values in place of these templates (currently set to 10%-90% with center 50%):
X_MIN, X_CENTER, X_MAX = 10.0, 50.0, 90.0
Y_MIN, Y_CENTER, Y_MAX = 10.0, 50.0, 90.0

DEADZONE = 5.0  # Deadzone in % (ignores small noises around the center)

keyboard = Keyboard(usb_hid.devices)


def get_duty_cycle(pulse_obj):
    """Read PWM duty cycle (%) from pulseio.PulseIn object.

    pulse_obj contains alternating high, low durations; use first two samples.
    """
    if len(pulse_obj) >= 2:
        high = pulse_obj[0]
        low = pulse_obj[1]
        total = high + low
        if total > 0:
            return (high / total) * 100.0
    return None


def map_axis(current_val, axis_min, axis_center, axis_max):
    """Convert PWM percentage to -100..+100 range taking calibration center into account."""
    if current_val is None:
        return 0.0

    current_val = max(axis_min, min(axis_max, current_val))

    if current_val < axis_center:
        raw_val = ((current_val - axis_center) / (axis_center - axis_min)) * 100.0
    else:
        raw_val = ((current_val - axis_center) / (axis_max - axis_center)) * 100.0

    if abs(raw_val) < DEADZONE:
        return 0.0

    return raw_val


def angle_from_xy(x, y):
    """Return angle in degrees [0, 360) with 0 at +X (3 o'clock), increasing CCW."""
    deg = math.degrees(math.atan2(y, x))
    deg = (deg + 360.0) % 360.0
    return deg


def joystick_sector(joy_x, joy_y):
    """Map joystick (x,y) to one of the clock sectors '12','3','6','9' or None.

    Sector centers (degrees): 3 -> 0°, 12 -> 90°, 9 -> 180°, 6 -> 270°
    Tolerance: ±30° (one-hour tolerance)
    """
    # if near center, treat as no sector
    if abs(joy_x) < 15.0 and abs(joy_y) < 15.0:
        return None

    deg = angle_from_xy(joy_x, joy_y)

    # Define ranges (inclusive). Handle wrap-around for 3 o'clock.
    if (deg >= 330.0 or deg <= 30.0):
        return '3'
    if 60.0 <= deg <= 120.0:
        return '12'
    if 150.0 <= deg <= 210.0:
        return '9'
    if 240.0 <= deg <= 300.0:
        return '6'
    return None


def send_key_for_clock(clock_label):
    """Lookup command via control_command_clock -> pyramid_keyboard_layout -> send via USB HID."""
    cmd_label = control_command_clock.get(clock_label)
    if cmd_label is None:
        print("No command mapped for clock", clock_label)
        return

    keycodes = pyramid_keyboard_layout.get(cmd_label)
    if keycodes is None:
        print("No keycodes in layout for command", cmd_label)
        return

    # keycodes may be a single Keycode or a tuple of Keycodes
    if isinstance(keycodes, tuple) or isinstance(keycodes, list):
        keyboard.send(*keycodes)
    else:
        keyboard.send(keycodes)

    print(f"Sent command '{cmd_label}' for clock {clock_label}")


def joystick_touch_active():
    """Return True if left joystick (ELE8 -> 18) is currently touched using mpr121, if available.

    Fallback: if sensor_touch module is not available, return True (can't detect).
    """
    if st is None:
        # No direct sensor module available; fallback to True so joystick logic can run
        return True

    try:
        # mpr121[8] corresponds to joystick 1 (left)
        return bool(st.mpr121[9].value)
    except Exception as e:
        print("Error reading mpr121 directly:", e)
        return False


print("Waiting for left joystick touch (sensor value 18) to activate...")

# Main loop: wait for sens_touch to indicate 18 or [17,18] to start; stop on value 19.
# If sens_touch module isn't available, the joystick loop can still run but can't be auto-started/stopped.
while True:
    # If we have the sens_touch function, use it to wait for activation or stop signal.
    if sens_touch is not None:
        val = sens_touch()
        print("sens_touch returned:", val)

        # Stop condition per your requirement (19)
        if val == 19:
            print("Received stop code 19 from sens_touch — exiting.")
            break

        # Start condition: single 18 or list containing 18
        if val == 18 or (isinstance(val, (list, tuple)) and 18 in val):
            print("Left joystick touch detected — entering joystick tracking.")
        else:
            # Not the left joystick — keep waiting
            continue
    else:
        # sens_touch not available: fall through and try to run if the physical mpr121 indicates touch
        if joystick_touch_active():
            print("mpr121 indicates joystick active — entering joystick tracking.")
        else:
            time.sleep(0.1)
            continue

    # Joystick active loop: read analog PWM and map to 4 sectors.
    previous_sector = None
    try:
        while True:
            duty_x = get_duty_cycle(pulse_x)
            duty_y = get_duty_cycle(pulse_y)

            if duty_x is not None and duty_y is not None:
                joy_x = map_axis(duty_x, X_MIN, X_CENTER, X_MAX)
                joy_y = map_axis(duty_y, Y_MIN, Y_CENTER, Y_MAX)

                # Print for debugging/calibration
                print(
                    f"PWM [X: {duty_x:.1f}%, Y: {duty_y:.1f}%] -> "
                    f"Joystick [X: {joy_x:+.0f}, Y: {joy_y:+.0f}]"
                )

                sector = joystick_sector(joy_x, joy_y)

                if sector is not None and sector != previous_sector:
                    send_key_for_clock(sector)
                    previous_sector = sector
                elif sector is None:
                    previous_sector = None

            # Clear pulse buffers and throttle loop
            pulse_x.clear()
            pulse_y.clear()

            # Check touch sensor to stop: use direct mpr121 read if available (non-blocking)
            if st is not None:
                try:
                    # Stop when joystick is not touched (both ELE8 and ELE9 false)
                    if not st.mpr121[8].value and not st.mpr121[9].value:
                        print("Joystick no longer touched per mpr121 — stopping joystick tracking.")
                        break
                except Exception as e:
                    print("Error reading mpr121 during active loop:", e)

            # If sens_touch available but we prefer not to block, we only used mpr121 direct check above.
            # Sleep for a short time (adjust for responsiveness; 0.05 ~= 20 Hz)
            time.sleep(0.05)

    except KeyboardInterrupt:
        # Allow Ctrl-C while testing / REPL
        print("Interrupted, exiting.")
        break

# End of script
print("joystick_left.py finished.")

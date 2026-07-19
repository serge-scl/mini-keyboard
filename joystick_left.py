import time
import board
import pulseio
from adafruit_hid.keyboard import Keyboard
from pk_layout import pyramid_keyboard_layout

try:
    from sensor_touch import sens_touch
except Exception as e:
    sens_touch = None
    print("Warning: could not import sens_touch from sensor_touch.py:", e)

control_command_clock = {'12':'Shift', '3':'Ctrl', '6':'Del', '9':'<-'}

# Pin settings: X - sensor A, Y - sensor B
pin_x = board.GP15
pin_y = board.GP14

pulse_x = pulseio.PulseIn(pin_x, maxlen=2)
pulse_y = pulseio.PulseIn(pin_y, maxlen=2)

# --- CALIBRATION SETTINGS ---
# Run the code, look at the actual percentages in the console at the extremes
# and enter your own values ​​in place of these templates (currently set to a range of 10%-90% centered at 50%):
X_MIN, X_CENTER, X_MAX = 10.0, 50.0, 90.0
Y_MIN, Y_CENTER, Y_MAX = 10.0, 50.0, 90.0

DEADZONE = 5.0 # Deadzone in % (ignores small noises around the center)


def get_duty_cycle(pulse_obj):
    """Reading the PWM signal"""
    if len(pulse_obj) >= 2:
        high = pulse_obj
        low = pulse_obj
        total = high + low
        if total > 0:
            return (high / total) * 100
    return None


def map_axis(current_val, axis_min, axis_center, axis_max):
    """Convert PWM percentages to the range from -100 to +100, taking into account the center"""
    if current_val is None:
        return 0.0

    # Limit the values ​​to the calibration limits
    current_val = max(axis_min, min(axis_max, current_val))

    # If the joystick is deflected to the negative side
    if current_val < axis_center:
        # Calculation from MIN to CENTER -> convert to the range from -100 to 0
        raw_val = ((current_val - axis_center) / (axis_center - axis_min)) * 100
    else:
        # Calculation from CENTER to MAX -> convert to a range from 0 to 100
        raw_val = ((current_val - axis_center) / (axis_max - axis_center)) * 100

    # Dead Zone Application
    if abs(raw_val) < DEADZONE:
        return 0.0

    return raw_val


print("Move the joystick to check the axes...")

while True:
    duty_x = get_duty_cycle(pulse_x)
    duty_y = get_duty_cycle(pulse_y)

    if duty_x is not None and duty_y is not None:
        # Convert PWM to joystick coordinates
        joy_x = map_axis(duty_x, X_MIN, X_CENTER, X_MAX)
        joy_y = map_axis(duty_y, Y_MIN, Y_CENTER, Y_MAX)

        # Output raw PWM (for calibration) and finished X/Y coordinates
        print(
            f"PWM [X: {duty_x:.1f}%, Y: {duty_y:.1f}%] -> "
            f"Joystick [X: {joy_x:+.0f}, Y: {joy_y:+.0f}]"
        )

    # Reset buffers to receive new pulses
    pulse_x.clear()
    pulse_y.clear()

    time.sleep(0.1) # Polling 10 times per second (for games can be reduced to 0.02)


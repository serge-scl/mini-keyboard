# Adafruit CircuitPython 8.2.6 on 2023-09-12; Raspberry Pi Pico with rp204
# I used a sensor matrix circuit using diodes; it seems that few people have done this before me.
import time
import board
import busio
import adafruit_mpr121

i2c = busio.I2C(board.GP5, board.GP4)
mpr121 = adafruit_mpr121.MPR121(i2c)

# Map of xy coordinate strings to pyramid key numbers (1-15)
# y (rows): 0-2, x (columns): 3-7
map_touch_pyramid = {"03":1, "04":2, "05":3, "06":4, "07":5,
                     "13":6, "14":7, "15":8, "16":9, "17":10,
                     "23":11, "24":12, "25":13, "26":14, "27":15}

def sens_touch():
    """
    Read touch sensor input from pyramid keyboard matrix and joysticks.
    
    Pyramid keyboard (ELE0-ELE7):
      - Polls 8 pins arranged as 3 rows × 5 columns
      - Returns key number (1-15) when pyramid touched, or 16 (no-touch) on timeout
    
    Joysticks (ELE8-ELE9):
      - ELE8 (joystick 1) returns 17 when touched
      - ELE9 (joystick 2) returns 18 when touched
      - Both joysticks touched returns [17, 18]
      - No joystick touched returns 19
    
    Complex combinations:
      - Pyramid + joystick(s) simultaneously: returns pyramid key (1-15) and joystick value(s)
        as a list, e.g., [7, 17] for pyramid key 7 + joystick 1
    """
    previous_pyramid_pressed = None
    previous_joystick_state = set()
    timeout_counter = 0
    
    while True:
        pressed_now = None
        
        # ==================== PYRAMID KEYBOARD POLLING ====================
        # Poll pyramid sensors (ELE0-ELE7)
        # Rows: pins 0-2 (y-axis)
        # Columns: pins 3-7 (x-axis)
        row_pin = None
        col_pin = None
        
        # Check rows (pins 0-2)
        for i in range(3):
            if mpr121[i].value:
                row_pin = i
                break
        
        # Check columns (pins 3-7, for 5 columns)
        for i in range(3, 8):
            if mpr121[i].value:
                col_pin = i
                break
        
        # If both row and column are pressed, we have a valid pyramid touch
        if row_pin is not None and col_pin is not None:
            pressed_now = f"{row_pin}{col_pin}"
        
        # ==================== JOYSTICK POLLING ====================
        # Poll joystick pins (ELE8 and ELE9)
        joystick_pressed = set()
        
        if mpr121[8].value:
            joystick_pressed.add(17)
        
        if mpr121[9].value:
            joystick_pressed.add(18)
        
        # ==================== PROCESS PYRAMID STATE CHANGE ====================
        if pressed_now != previous_pyramid_pressed:
            if pressed_now is not None:
                # Pyramid was just touched
                if pressed_now in map_touch_pyramid:
                    key_num = map_touch_pyramid[pressed_now]
                    
                    # Check if joystick(s) are also pressed
                    if joystick_pressed:
                        result = [key_num] + sorted(list(joystick_pressed))
                        print(f"Complex combination: Pyramid {pressed_now} (Key {key_num}) + Joysticks {joystick_pressed} → {result}")
                        return result
                    else:
                        print(f"Pyramid touched: {pressed_now} → Key {key_num}")
                        return key_num
                else:
                    print(f"Invalid pyramid coordinate: {pressed_now}")
                
                timeout_counter = 0  # Reset on valid touch
            
            previous_pyramid_pressed = pressed_now
        
        # ==================== PROCESS JOYSTICK STATE CHANGE ====================
        if joystick_pressed != previous_joystick_state:
            if joystick_pressed:
                # Joystick(s) just pressed (only if pyramid not pressed)
                if pressed_now is None:
                    result = sorted(list(joystick_pressed))
                    if len(result) == 1:
                        print(f"Joystick touched: {result[0]}")
                        return result[0]
                    else:
                        print(f"Both joysticks touched: {result}")
                        return result
            else:
                # Both joysticks just released (only if pyramid not pressed)
                if pressed_now is None and previous_pyramid_pressed is None:
                    print("Timeout: no touch detected, returning 16 (keyboard no-touch)")
                    return 16
            
            previous_joystick_state = joystick_pressed
        else:
            # No state change—increment timeout if nothing pressed anywhere
            if pressed_now is None and not joystick_pressed:
                timeout_counter += 1
                if timeout_counter > 50:  # Adjust threshold as needed
                    print("Timeout: no touch detected, returning 16 (keyboard no-touch)")
                    return 16  # Return 16 as the keyboard no-touch value
        
        time.sleep(0.1)  # Debounce delay

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
    Read touch sensor input and return key number from map.
    Polls all 8 pins (ELE0-ELE7) arranged as 3 rows × 5 columns.
    Returns key number (1-15) when pyramid touched, or 16 (no-touch) on timeout.
    """
    previous_pressed = None
    timeout_counter = 0
    
    while True:
        pressed_now = None
        
        # Poll all 8 sensors (ELE0-ELE7)
        # Rows: pins 0-2 (y-axis)
        # Columns: pins 3-7 (x-axis)
        row_pin = None
        col_pin = None
        
        # Check rows (pins 0-2)
        for i in range(3):
            if mpr121[i].value:
                row_pin = i
                break
        
        # Check columns (pins 3-8, but only 3-7 for 5 columns)
        for i in range(3, 8):
            if mpr121[i].value:
                col_pin = i
                break
        
        # If both row and column are pressed, we have a valid pyramid touch
        if row_pin is not None and col_pin is not None:
            pressed_now = f"{row_pin}{col_pin}"
        
        # If sensor state changed (new press or release)
        if pressed_now != previous_pressed:
            if pressed_now is not None:
                # Pyramid was just touched
                if pressed_now in map_touch_pyramid:
                    key_num = map_touch_pyramid[pressed_now]
                    print(f"Pyramid touched: {pressed_now} → Key {key_num}")
                    return key_num
                else:
                    print(f"Invalid pyramid coordinate: {pressed_now}")
                
                timeout_counter = 0  # Reset on valid touch
            
            previous_pressed = pressed_now
        else:
            # No state change—increment timeout if nothing pressed
            if pressed_now is None:
                timeout_counter += 1
                if timeout_counter > 50:  # Adjust threshold as needed
                    print("Timeout: no touch detected, returning 16 (no-touch)")
                    return 16  # Return 16 as the no-touch value
        
        time.sleep(0.1)  # Debounce delay

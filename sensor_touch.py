# Adafruit CircuitPython 8.2.6 on 2023-09-12; Raspberry Pi Pico with rp204
# I used a sensor matrix circuit using diodes; it seems that few people have done this before me.
import time
import board
import busio
import adafruit_mpr121

i2c = busio.I2C(board.GP5, board.GP4)
mpr121 = adafruit_mpr121.MPR121(i2c)

map_touch_pyramid = {"03":1, "04":2, "05":3, "06":4, "07":5,
                     "13":6, "14":7, "15":8, "16":9, "17":10,
                     "23":11, "24":12, "25":13, "26":14, "27":15}

def sens_touch():
    """
    Read touch sensor input and return key number from map.
    Returns key number (1-15) when found, or None on timeout.
    """
    previous_pressed = None
    timeout_counter = 0
    
    while True:
        pressed_now = None
        
        # Check which sensor(s) are currently pressed
        for i in range(4):
            if mpr121[i].value:
                pressed_now = str(i)
                break  # Use first detected press in this cycle
        
        # If sensor state changed (new press or release)
        if pressed_now != previous_pressed:
            if pressed_now is not None:
                # Sensor was just pressed
                key_num = f"0{pressed_now}"
                kn = key_num[-2:]
                
                if kn in map_touch_pyramid:
                    print(f"Key pressed: {map_touch_pyramid[kn]}")
                    return map_touch_pyramid[kn]
                else:
                    print(f"Invalid key: {kn}")
                
                timeout_counter = 0  # Reset on valid press
            
            previous_pressed = pressed_now
        else:
            # No state change—increment timeout if nothing pressed
            if pressed_now is None:
                timeout_counter += 1
                if timeout_counter > 50:  # Adjust threshold as needed
                    print("Timeout: no valid key pressed")
                    return None
        
        time.sleep(0.1)  # Debounce delay
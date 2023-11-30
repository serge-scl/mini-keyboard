# Raspberry Pi Pico Keyboard Emulator
# Using CircuitPython
# Using Adafruit USB_HID Librarys


from sensor_hall import main
import asyncio
#import digitalio
#import board
from sensor_touch import sens_touch



# while True:

sens_touch()
st = sens_touch()

print("catch", st)

asyncio.run(main(st))
    

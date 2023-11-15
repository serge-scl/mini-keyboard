# Raspberry Pi Pico Keyboard Emulator
# Using CircuitPython
# Using Adafruit USB_HID Librarys


from sensor_hall import main
import asyncio
import digitalio
import board

# here I plugged in a third hall sensor for hardware stop
pin_y = digitalio.DigitalInOut(board.GP15)
pin_y.switch_to_input(pull=digitalio.Pull.UP)
# stopping can also be done by touching a magnet


#while True:
if pin_y.value:
    asyncio.run(main())
    


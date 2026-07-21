# Raspberry Pi Pico 
# Using CircuitPython
from sensor_touch import sens_toch
import usb_hid
from sensor_hall import main
import asyncio

asyncio.run(main())
    

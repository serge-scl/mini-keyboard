# Raspberry Pi Pico
# Using CircuitPython
# import asyncio
import usb_hid
import time
# find HID device object that you configured (index may vary)
hid_device = usb_hid.devices[0]

value = 1
hid_device.send_report(bytes([0xAA, value]))
time.sleep(0.05)


print("Hello from code", value)


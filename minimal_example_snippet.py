# On CircuitPython device (code.py)
import usb_hid
import time
# find HID device object that you configured (index may vary)
hid_device = usb_hid.devices[0]

async def touch_sensor_poll_loop():
    while True:
        value = read_touch_sensor()  # your sensor code => 0..15 or other
        # Compose report [0xAA, value]
        report = bytes([0xAA, value & 0xFF])
        # If your HID descriptor uses a report ID, include it as first byte:
        # report = bytes([REPORT_ID, 0xAA, value & 0xFF])
        hid_device.send_report(report)
        await sleep_ms(50)  # or time.sleep(0.05) if not async

# On CircuitPython device (code.py)
import usb_hid
import time
# find HID device object that you configured (index may vary)
hid_device = usb_hid.devices[0]

async def touch_sensor_poll_loop():
    while True:
        value = read_touch_sensor()  # your sensor code => 0..15 or other
        # Compose report ([0xAA, value & 0xFF])
        # If your HID descriptor uses a report ID, include it as first byte:
        # report = bytes([REPORT_ID, 0xAA, value & 0xFF])
        """
        ValueError: report length must be 8
        The ValueError happens because the HID device expects reports of exactly 8 bytes, but your code sent only 2.
        Fix: send an 8-byte report (pad with zeros) or build the report the device's descriptor requires.
        Compose report ([0xAA, value & 0xFF] + [0] * 6)
        """      
        report = bytes([0xAA, value & 0xFF] + [0] * 6)
        hid_device.send_report(report)
        await sleep_ms(50)  # or time.sleep(0.05) if not async
        
async def read_touch_sensor():
    sens_cod = 1
    await sleep_ms(750)
    return sens_cod

async def main():
    touch_task1 = asyncio.create_task(touch_sensor_poll_loop())
    touch_task2 = asyncio.create_task(read_touch_sensor())
    await asyncio.gather(touch_task1, touch_task2)
    print("asyncio gather")
    
# asyncio.run(main())
    
    

        


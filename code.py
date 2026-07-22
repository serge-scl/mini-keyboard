# Raspberry Pi Pico 
# Using CircuitPython
import asyncio
import usb_hid
from sensor_touch import sens_touch
from sensor_hall import main

# Import HID keyboard for sending custom reports
from adafruit_hid.keyboard import Keyboard

# Initialize USB HID keyboard
mkps = Keyboard(usb_hid.devices)


async def touch_sensor_poll_loop():
    """
    Poll touch sensor continuously and send values 1–19 via USB HID.
    
    Values returned:
      - 1–15: Pyramid keyboard keys
      - 17–18: Joystick values
      - 16 or 19: No-touch condition
    
    Runs as a separate async task (non-blocking).
    """
    print("Starting touch sensor polling loop...")
    
    while True:
        try:
            # Get value from touch sensor (1–19 or 16 for no-touch)
            touch_value = sens_touch()
            
            if touch_value is not None:
                # Handle list return (complex combinations like [7, 17])
                if isinstance(touch_value, list):
                    for value in touch_value:
                        if 1 <= value <= 19:
                            print(f"Sending touch value: {value}")
                            # Send the raw value as a custom HID report
                            # (not a keycode, just the sensor value)
                            send_sensor_value(value)
                else:
                    # Single value (1–19 or 16)
                    if 1 <= touch_value <= 19:
                        print(f"Sending touch value: {touch_value}")
                        send_sensor_value(touch_value)
                    elif touch_value == 16:
                        print("No touch detected (16)")
        
        except Exception as e:
            print(f"Error in touch sensor poll loop: {e}")
        
        # Small delay to avoid overwhelming the loop
        await asyncio.sleep(0.05)


def send_sensor_value(value):
    """
    Send sensor value (1–19) via USB HID to the computer.
    
    This sends the raw sensor value, NOT a keycode.
    The text_editor.py application on the computer should be
    listening for these custom HID reports.
    
    Args:
        value: Integer from 1 to 19 (sensor ID)
    """
    try:
        # Create a custom HID report with the sensor value
        # Format: [0xAA, value] (0xAA is a marker byte for sensor data)
        report = bytes([0xAA, value])
        
        # Send via USB HID
        usb_hid.devices.send(report)
        print(f"Sent HID report: {report.hex()}")
    
    except Exception as e:
        print(f"Error sending HID report: {e}")


async def main_combined():
    """
    Run both the hall sensor task and touch sensor polling task concurrently.
    """
    # Create the touch sensor polling task (separate thread-like behavior)
    touch_task = asyncio.create_task(touch_sensor_poll_loop())
    
    # Create the hall sensor task from sensor_hall.py
    hall_task = asyncio.create_task(main())
    
    # Run both concurrently
    await asyncio.gather(touch_task, hall_task)


# Run the combined main function
asyncio.run(main_combined())

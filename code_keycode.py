# Raspberry Pi Pico 
# Using CircuitPython
# Starts a background task that reads sensor_touch.sens_toch() repeatedly.
# When sens_toch() returns an integer between 1 and 19 (inclusive), the value
# is sent to the host computer over USB HID as text. If the optional
# `minimal_integration_pattern_copilot` plugin exists and exposes a
# `send_value` or `transmit` function, the value is forwarded to it as well.

from sensor_touch import sens_toch
import usb_hid
from sensor_hall import main as hall_main
import asyncio

# adafruit_hid provides a friendly way to type text via the USB keyboard
# interface. This code will attempt to use KeyboardLayoutUS.write() first
# and fall back to sending individual digit Keycodes if necessary.
try:
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
    from adafruit_hid.keycode import Keycode
    _HAVE_ADAFRUIT_HID = True
except Exception:
    # If adafruit_hid isn't available on the device, we still keep the rest
    # of the logic but won't be able to type to the host.
    _HAVE_ADAFRUIT_HID = False

if _HAVE_ADAFRUIT_HID:
    keyboard = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(keyboard)
    # mapping for fallback digit-by-digit key sending
    _DIGIT_TO_KEYCODE = {
        "0": Keycode.ZERO,
        "1": Keycode.ONE,
        "2": Keycode.TWO,
        "3": Keycode.THREE,
        "4": Keycode.FOUR,
        "5": Keycode.FIVE,
        "6": Keycode.SIX,
        "7": Keycode.SEVEN,
        "8": Keycode.EIGHT,
        "9": Keycode.NINE,
    }


async def touch_reporter(poll_delay: float = 0.05):
    """Background task that polls sens_toch() and forwards results.

    - Runs continuously.
    - For values in the inclusive range [1, 19] it sends the numeric value
      to the host via USB HID and (optionally) to the minimal_integration
      plugin if available.
    """
    # brief startup delay to let other device initialization finish
    await asyncio.sleep(0.1)

    while True:
        try:
            val = sens_toch()
        except Exception:
            # If the sensor read fails, skip this iteration but don't crash.
            val = None

        if isinstance(val, int) and 1 <= val <= 19:
            # 1) Send to host as typed text (e.g. "1", "10", "19")
            if _HAVE_ADAFRUIT_HID:
                try:
                    layout.write(str(val))
                except Exception:
                    # fallback to pressing individual digit keycodes
                    for ch in str(val):
                        kc = _DIGIT_TO_KEYCODE.get(ch)
                        if kc is not None:
                            keyboard.press(kc)
                            keyboard.release_all()
                            # small pause so host registers separate key presses
                            await asyncio.sleep(0.01)

            # 2) Attempt to forward to the optional plugin used by text_editor.py
            # The plugin's API is not known here; try common function names
            # (send_value, transmit) if the module exists.
            try:
                import minimal_integration_pattern_copilot as plugin
                if hasattr(plugin, "send_value"):
                    try:
                        plugin.send_value(val)
                    except Exception:
                        # ignore plugin errors to keep the reporter robust
                        pass
                elif hasattr(plugin, "transmit"):
                    try:
                        plugin.transmit(val)
                    except Exception:
                        pass
            except Exception:
                # plugin not available or import failed — ignore silently
                pass

        await asyncio.sleep(poll_delay)


async def main():
    """Entry point for asyncio: starts the touch_reporter and then runs
    the existing sensor_hall.main() concurrently. The reporter is started
    first so it precedes any keycode handling in sensor_hall.
    """
    # start the background reporter task
    reporter_task = asyncio.create_task(touch_reporter())

    # run the existing sensor_hall main concurrently. If sensor_hall.main()
    # is a long-running coroutine it will run together with the reporter.
    try:
        await hall_main()
    except Exception:
        # If sensor_hall.main raises, keep the reporter running rather than
        # letting the whole program crash.
        pass

    # keep the reporter alive indefinitely (or until the device resets)
    await reporter_task


# Run the asyncio main loop when executed as a script on the device.
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        # On CircuitPython, asyncio.run may raise on soft-reload; swallow
        # exceptions to avoid crashing the REPL.
        pass

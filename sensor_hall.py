# Adafruit CircuitPython 8.2.6 on 2023-09-12; Raspberry Pi Pico with rp2040
# ........................................


"""
I used a 0.5 second sample, which is about ten times slower than what it would be in reality.
 This is convenient for debugging, since the application window must be activated in a ten-second period,
  otherwise text entry may begin in the editor window.
  """

import asyncio
import board
import analogio
import digitalio
# import time
import usb_hid

from adafruit_hid.keyboard import Keyboard

from pk_layout import pyramid_keyboard_layout

top_bottom_characters = ["'1", "\"2", "(3", "[4", "{5",
                         "$6", "#7", "@8", ";9", "%0",
                         ">+", "<-", "&*", ":/", "!="]
right_left_characters = ["qw", "er", "ty", "ui", "op",
                         "as", "df", "gh", "jk", "l^",
                         "zx", "cv", "bn", "m?", ",."]


mkps = Keyboard(usb_hid.devices)

start_stop = True
# I decided for clarity to use analog sensors, and not PWM as planned at the beginning
# the sensors I used here have a narrow sensitivity band and are poorly calibrated,
# but for now this is not important the sensors cover the range from 51000 to 65535
#  I chose the average value of 58500

label_tb = 58501
label_lr = 58502

touch_sensor = 1


class HallBuffer:
    def __init__(self, x, y):
        self.tb_hall = [x]
        self.lr_hall = [y]

async def hall_sensor(x,n, n1):
    
    with analogio.AnalogIn(x) as pin_x:
        while True:
            global start_stop
            if start_stop:
                if len(n) > 20:
                    label = n.pop(0)
                    move_h = max(n) - min(n)
                    move_h1 = max(n) - min(n1)
                    middle_h = sum(n) / len(n)
                    middle_h1 = sum(n1) / len(n1)

                    if abs(move_h) > abs(move_h1):
                        ch = " "
                        level = []
                        if label == label_tb:
                            level = top_bottom_characters[touch_sensor]
                        elif label == label_lr:
                            level = right_left_characters[touch_sensor]

                        if middle_h > middle_h1:
                            ch = level[0]
                        elif middle_h < middle_h1:
                            ch = level[1]

                        key_code = pyramid_keyboard_layout[ch]

                        if isinstance(key_code, tuple) is True:
                            mkps.send(key_code[0], key_code[1])
                            # print(f"mkps.send{key_code[0], key_code[1]}")
                            start_stop = False
                        else:
                            mkps.send(key_code)
                            # print(f"mkps.send{key_code}")
                            start_stop = False
                    else:
                        pass

                else:
                    n.append(pin_x.value)

                    print(n)
                    print(n1)
                await asyncio.sleep(0.5)
            else:
                break

async def main():
    buffer_hall = HallBuffer(label_tb, label_lr)
    hall_tb = asyncio.create_task(hall_sensor(board.A0, buffer_hall.tb_hall, buffer_hall.lr_hall))
    hall_lr = asyncio.create_task(hall_sensor(board.A1, buffer_hall.lr_hall, buffer_hall.tb_hall))
    await asyncio.gather(hall_tb, hall_lr)


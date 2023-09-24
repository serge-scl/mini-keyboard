# Raspberry Pi Pico Keyboard Emulator
# Using CircuitPython
# Using Adafruit USB_HID Librarys
"""
Since in a keyboard simulator the danger of random signals can lead to unpredictable actions,
I made a hard exit from the loop.
The simulation starts as soon as the chip is connected to the computer,
but then stops after break. If you make the next simulation run,
you must activate the application window three seconds in advance,
otherwise the symbol will be printed in the editor itself.
"""

import time
import usb_hid
import random 

from adafruit_hid.keyboard import Keyboard

from pk_layout import pyramid_keyboard_layout

top_bottom_characters = ["'1", "\"2", "(3", "[4", "{5",
                         "$6", "#7", "@8", ";9", "%0",
                         ">+", "<-", "&*", ":/", "!="]
right_left_characters = ["qw", "er", "ty", "ui", "op",
                         "as", "df", "gh", "jk", "l^",
                         "zx", "cv", "bn", "m?", ",."]



time.sleep(3) # activate the text input application

keyboard = Keyboard(usb_hid.devices)

while True:
    toch_sm = random.randint(0, 14)  # capacitive touch sensor IC data simulator
    
    
    hall_tb = random.randint(0,100)  # simulation of a vertical Hall sensor
    hall_lr = random.randint(0,100)  # simulation of a horizontal Hall sensor
    rest_point = 50 # moving grid rest point

    mov_tb = rest_point - hall_tb
    mov_lr = rest_point - hall_lr
    print(mov_tb, mov_lr)
  
    if abs(mov_tb) > abs(mov_lr):
        print('top_bottom')
        
    else:
        print('left_right')
        
    mtb = lambda: 0 if mov_tb > 0 else 1
    mlr = lambda: 0 if mov_lr > 0 else 1
    
    ch_tb = pyramid_keyboard_layout[top_bottom_characters[toch_sm][mtb()]]
    ch_lr  = pyramid_keyboard_layout[right_left_characters[toch_sm][mlr()]]
#    ch = ch_lr
    ch = lambda: ch_tb if abs(mov_tb) > abs(mov_lr) else ch_lr
    print(ch())
    
    if isinstance(ch(), tuple) is True:
        keyboard.send(ch()[0], ch()[1])
    else:
        keyboard.send(ch())

    break # break is  Simulator mode, turns at loop into at algorithm

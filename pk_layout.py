# Raspberry Pi Pico Keyboard Emulator
# Using CircuitPython
# Using Adafruit USB_HID Librarys

from adafruit_hid.keycode import Keycode

pyramid_keyboard_layout = {'a': Keycode.A, 'b': Keycode.B, 's': Keycode.S,
                           '$': (Keycode.SHIFT, Keycode.FOUR), '6': Keycode.SIX,
                           "'":Keycode.QUOTE, '1': Keycode.ONE, '"':(Keycode.SHIFT, Keycode.QUOTE),
                           '(':(Keycode.SHIFT, Keycode.NINE),'3': Keycode.THREE, '2':Keycode.TWO,
                           '[': Keycode.LEFT_BRACKET, '4':Keycode.FOUR, '{': (Keycode.SHIFT, Keycode.LEFT_BRACKET),
                           '5': Keycode.FIVE, 'q': Keycode.Q, 'w': Keycode.W, 'r':Keycode.R, 't':Keycode.T,
                           'y':Keycode.Y, 'u':Keycode.U, 'i':Keycode.I, 'o':Keycode.O, 'p':Keycode.P,
                           '#':(Keycode.SHIFT, Keycode.THREE), '7':Keycode.SEVEN, '@':(Keycode.SHIFT, Keycode.TWO),
                           '8':Keycode.EIGHT, ';':Keycode.SEMICOLON, '9':Keycode.NINE, '%':(Keycode.SHIFT, Keycode.FIVE),
                           '0':Keycode.ZERO, 'd':Keycode.D, 'f':Keycode.F, 'g':Keycode.G, 'h':Keycode.H,
                           'j':Keycode.J, 'k':Keycode.K, 'l':Keycode.L, '^':(Keycode.SHIFT, Keycode.SIX),
                           '>':(Keycode.SHIFT, Keycode.PERIOD), '+':(Keycode.KEYPAD_PLUS), '-':Keycode.MINUS,
                           '<':(Keycode.SHIFT, Keycode.COMMA), '&':(Keycode.SHIFT, Keycode.SEVEN),
                           '*':Keycode.KEYPAD_ASTERISK, ':':(Keycode.SHIFT, Keycode.SEMICOLON),
                           '/':Keycode.KEYPAD_FORWARD_SLASH, '!':(Keycode.SHIFT,Keycode.ONE), '=':Keycode.EQUALS,
                           'z':Keycode.Z, 'x':Keycode.X, 'c':Keycode.C, 'v':Keycode.V, 'n':Keycode.N, 'm':Keycode.M,
                           '?':(Keycode.SHIFT, Keycode.FORWARD_SLASH), ',':Keycode.COMMA, '.':Keycode.PERIOD}

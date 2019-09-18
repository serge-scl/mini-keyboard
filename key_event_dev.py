# signal from device
# arrange top - bottom - 0_X
# arrange left - right X_0

#         "'1", '"2', "(3", "[4", "{5",
#         "$6", "#7", "@8", ";9", "%0",
#         ">+", "<-", "&*", ":/", "!=",

#         "xy", "yx",    "yx",    "xy",
#             yy              yy
#          --,  "sh",    "sh",   "--"
#

#          "QW", "ER", "TY", "UI", "OP",
#         "AS", "DF", "GH", "JK", "L^",
#         "ZX", "CV", "BN", "M?", ",.",

#         "di",  "bb",   "di",    "bb",
#              xx             xx
#         "pw",  "ca",  "ca",    "pw"


class KeyboardString2FD:

    tb0x = ["'1", '"2', "(3", "[4", "{5",
            "$6", "#7", "@8", ";9", "%0",
            ">+", "<-", "&*", ":/", "!=",
            "xy", "yx", "yx", "yy", "xy",  # add fun joystick
            "--", "yy", "sh", "sh", "--"]  # ch - Shift

    lrx0 = ["QW", "ER", "TY", "UI", "OP",
            "AS", "DF", "GH", "JK", "L^",
            "ZX", "CV", "BN", "M?", ",.",
            "di", "bb", "di", "xx", "bb",  # bb -> back-blank  di -> del - ins, xx -> joystick
            "pw", "xx", "ca", "ca", "pw"]  # pw - power  ca -> ctrl- alt 


class KeyboardInv:

    def __init__(self, x):
        self.tbrd = x
        self.tbrd_inv = []

    def invert_key(self):
        for iv in self.tbrd:
            inv = iv[1] + iv[0]
            self.tbrd_inv.append(inv)
        return self.tbrd_inv


ki = KeyboardInv(KeyboardString2FD.lrx0)
kinv = ki.invert_key()


class KeyboardStr2to4FD:

    def __init__(self, x):
        self.tblr = x

    def plus(self):
        return [x[0] for x in self.tblr]

    def minus(self):
        return [x[1] for x in self.tblr]


kbtb0x = KeyboardStr2to4FD(KeyboardString2FD.tb0x)
kbrlx0 = KeyboardStr2to4FD(KeyboardString2FD.lrx0)
kbinvlr = KeyboardInv(KeyboardString2FD.lrx0)
kblrx0 = KeyboardStr2to4FD(kbinvlr.invert_key())

KeyboardPr1 = {"0,1": kbtb0x.plus(), "0,-1": kbtb0x.minus(), "-1,0": kblrx0.minus(), "1,0": kblrx0.plus()}


def text_in(tx):
    a01 = []
    wordp1 = tx.upper()
    for iw in wordp1:
        for itx in KeyboardPr1:
            if iw in KeyboardPr1[itx]:
                js = [int(s) for s in itx.split(",")]
                t_a = KeyboardPr1[itx].index(iw)
                js.append(t_a)
                a01.append(js)
    return a01


texi01 = text_in("am")

# kbd_andr = {"'w1q": [0x004b, 0x0033, 0x0008, 0x002d], '"r2e': [0x004b, 0x002e, 0x0009, 0x0021],
#             "(y3t": [0x00a2, 0x0035, 0x000a, 0x0030], "[i4u": [0x0047, 0x0025, 0x000b, 0x0031],
#             "{p5o": [0x0047, 0x002c, 0x000c, 0x002b], "$s6a": [[0x003b, 0x000b], 0x002f, 0x000d, 0x001d],
#             "#f7d": [0x00cc, 0x0022, 0x000e, 0x0020], "@h8g": [0x00ce, 0x0024, 0x000f, 0x0023],
#             ";k9j": [0x004a, 0x0027, 0x0010, 0x0026], ":^0L": [0x00cb, 0x00c3, 0x0007, 0x0028],
#             "&x+z": [0x00c7, 0x0034, 0x009d, 0x0036], ">v-c": [0x00c6, 0x0032, 0x0045, 0x001f],
#             "<n*b": [0x00c5, 0x002a, 0x009c, 0x001e], "!?/m": [0x00cf, 0x004c, 0x009a, 0x0029],
#             "%.=,": [0x00c4, 0x0038, 0x0046, 0x0037]}


class KeyEvent:
    ACTION_DOWN = 0  # cap touch & tilt 0_X | X-0
    FLAG_TRACKING = 512  # superposition
    ACTION_UP = 1  # Cap touch 0 -> yes
    ACTION_MULTIPLE = 2  # maybe
    FLAG_CANCELED = 32  # no
    KEYCODE_0 = 7
    KEYCODE_1 = 8
    KEYCODE_2 = 9
    KEYCODE_3 = 10
    KEYCODE_4 = 11
    KEYCODE_5 = 12
    KEYCODE_6 = 13
    KEYCODE_7 = 14
    KEYCODE_8 = 15
    KEYCODE_9 = 16
    KEYCODE_PLUS = 81  # +
    KEYCODE_MINUS = 69  # -
    KEYCODE_NUMPAD_MULTIPLY = 155  # *
    KEYCODE_NUMPAD_DIVIDE = 154  # /
    KEYCODE_EQUAL = 70  # =
    KEYCODE_A = 29
    KEYCODE_B = 30
    KEYCODE_C = 31
    KEYCODE_D = 32
    KEYCODE_E = 33
    KEYCODE_ENTER = 66
    KEYCODE_ESCAPE = 111
    KEYCODE_F = 34
    KEYCODE_G = 35
    KEYCODE_H = 36
    KEYCODE_HELP = 259
    KEYCODE_HOME = 3
    KEYCODE_I = 37
    KEYCODE_INSERT = 124
    KEYCODE_J = 38
    KEYCODE_K = 39
    KEYCODE_L = 40
    KEYCODE_LANGUAGE_SWITCH = 204
    KEYCODE_M = 41
    KEYCODE_MENU = 82
    KEYCODE_N = 42
    KEYCODE_O = 43
    KEYCODE_P = 44
    KEYCODE_POWER = 26
    KEYCODE_Q = 45
    KEYCODE_R = 46
    KEYCODE_S = 47
    KEYCODE_SPACE = 62
    KEYCODE_T = 48
    KEYCODE_U = 49
    KEYCODE_V = 50
    KEYCODE_W = 51
    KEYCODE_X = 52
    KEYCODE_Y = 53
    KEYCODE_Z = 54
    KEYCODE_APOSTROPHE = 75  # '
    KEYCODE_POUND = 18  # #
    KEYCODE_AT = 77  # @
    KEYCODE_LEFT_BRACKET = 71  # [
    KEYCODE_COMMA = 55  # ,
    KEYCODE_PERIOD = 56  # .
    KEYCODE_QUERY = 56


Kpr = KeyboardString2FD
Ke0 = KeyEvent
Kinv = KeyboardInv(Kpr.tb0x)


def str_to_keycode(x):
    keybord_code = []
    for ik in x:
        tlt = []
        try:
            ch1 = ik[0]
            ch2 = ik[1]
            body = "Ke0.KEYCODE_"
            tlt.insert(0, eval(body + ch1))
            tlt.insert(1, eval(body + ch2))
        except:
            if ik[0] == ",":
                tlt.insert(0, 55)
                tlt.insert(1, 56)
            elif ik[1] == "?":
                tlt.insert(1, 101)
            else:
                tlt.insert(1, 102)
        finally:
            keybord_code.append(tlt)
    print(keybord_code)


if __name__ == "__main__":
    # print(kbtb0x)
    pass

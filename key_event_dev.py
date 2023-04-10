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

    tb0x = ["'1", "\"2", "(3", "[4", "{5",
            "$6", "#7", "@8", ";9", "%0",
            ">+", "<-", "&*", ":/", "!=",
            "xy", "yx", "yx", "yy", "xy",  # add fun joystick
            "--", "yy", "sh", "sh", "--"]  # ch - Shift

    lrx0 = ["QW", "ER", "TY", "UI", "OP",
            "AS", "DF", "GH", "JK", "L^",
            "ZX", "CV", "BN", "M?", ",.",
            "di", "bb", "di", "xx", "bb",  # bb -> back-blank  di -> del - ins, xx -> joystick
            "pw", "xx", "ca", "ca", "pw"]  # pw - power  ca -> ctrl- alt 




if __name__ == "__main__":
    pass

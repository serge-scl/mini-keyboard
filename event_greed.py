# event in greed keyboard
#...........................................................................................
""" I can't completely imitate the behavior of my pyramid keyboard on a regular keyboard.
 In my device, the keyboard image on the screen will change to highlight the active object as soon as your finger touches the tip of the pyramid.
Thus, the user, looking at the screen, will immediately see at the tip of which of the pyramids his finger is located.
And then use it by tilting the pyramid in one of the four directions to enter the symbol or letter itself.
This is touch typing what  that it's very simple here. On a regular keyboard, learning to touch type is a long and difficult process.
Therefore, it is difficult to imitate this on a regular keyboard.
I decided that entering a number is the same as touching the tip, and subsequent actions already come with Shift. """

from tkinter import *

top_bottom_characters = ["'1", "\"2", "(3", "[4", "{5",
                         "$6", "#7", "@8", ";9", "%0",
                         ">+", "<-", "&*", ":/", "!="]
right_left_characters = ["QW", "ER", "TY", "UI", "OP",
                         "AS", "DF", "GH", "JK", "L^",
                         "ZX", "CV", "BN", "M?", ",."]

font0 = 'Helvetica'
font1 = 'Liberation Serif'
back_ground0 = 'LightCyan2'
activ_bg = 'yellow3'
akitv_text = 'red2'
back_text = 'grey2'
font_sz = 16

root = Tk()
root.title('On Screen Keyboard')

def scan_key(event):
    keyboard(event.char)
    # print(event.char)

def keyboard(ch=''):
    stp = 0
    for out_row in range(3):
        for out_col in range(5):

            step = out_row + out_col + stp

            one_pyramid = [top_bottom_characters[step][0],top_bottom_characters[step][1],
                           right_left_characters[step][0],right_left_characters[step][1]]


            bgr0 = lambda x : activ_bg if x in one_pyramid else back_ground0
            bgr = bgr0(ch)
            stx = back_text
            fgr = font0
            ftz = font_sz


            frm = Frame(root, bg=bgr)
            frm.grid(row=out_row, column=out_col, padx=2, pady=2)

            captch_key = Label(frm,text='x', fg='blue', bg=bgr, height=1, width=2, font=(fgr, ftz))
            top_key = Label(frm,text=one_pyramid[0], fg=stx, bg=bgr, height=1, width=2, font=(fgr, ftz))
            bottom_key = Label(frm,text=one_pyramid[1], fg=stx, bg=bgr, height=1, width=2, font=(fgr, ftz))
            left_key = Label(frm,text=one_pyramid[2], fg=stx, bg=bgr, height=1, width=2, font=(fgr, ftz))
            righ_key = Label(frm,text=one_pyramid[3], fg=stx, bg=bgr, height=1, width=2, font=(fgr, ftz))
            root['bg'] = 'blue'
            captch_key.grid(row=1, column=1)
            top_key.grid(row=0, column=1)
            bottom_key.grid(row=2, column=1)
            left_key.grid(row=1, column=0)
            righ_key.grid(row=1, column=2)
        stp += 4

keyboard()
root.bind('<Key>', scan_key)

if __name__ == '__main__':
    root.mainloop()
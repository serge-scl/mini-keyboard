# greed keyboard 470x273

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
font_sz = 18

def scan_key(event):
    mkps(event.char)
    print(event.char)

root = Tk()
root.title('pyramid keyboard text editor')

root.geometry("900x500")
key_frame = Frame(root, bg="blue", width=470,height=273)
key_frame.pack(side=BOTTOM)

text_frame = Frame(root)
text_frame.pack(side=TOP)

text_editor = Text(text_frame, width=900,height=227)
text_editor.pack()

def mkps(ch=''):
    stp = 0
    for out_row in range(3):
        for out_col in range(5):

            step = out_row + out_col + stp

            one_pyramid = [top_bottom_characters[step][0],top_bottom_characters[step][1],
                           right_left_characters[step][0],right_left_characters[step][1],
                           str.lower(right_left_characters[step][0]), str.lower(right_left_characters[step][1])]

            bgr0=lambda: activ_bg if ch in one_pyramid else back_ground0
            tp_tx =  lambda: akitv_text if ch == one_pyramid[0] else back_text
            bt_tx =  lambda: akitv_text if ch == one_pyramid[1] else back_text
            lf_tx =  lambda: akitv_text if ch == one_pyramid[2] else back_text
            rt_tx =  lambda: akitv_text if ch == one_pyramid[3] else back_text
            tp_fg = font1
            bg_fg =  font1
            lf_fg =  font1
            rt_fg = font1

            frm = Frame(key_frame, bg=bgr0())
            frm.grid(row=out_row, column=out_col, padx=2, pady=2)

            captch_key = Label(frm, text='x', fg='blue', bg=bgr0(), height=1, width=2, font=(font0, font_sz))
            top_key = Label(frm, text=one_pyramid[0], fg=tp_tx(), bg=bgr0(), height=1, width=2, font=(tp_fg, font_sz))
            bottom_key = Label(frm, text=one_pyramid[1], fg=bt_tx(), bg=bgr0(), height=1, width=2,
                               font=(bg_fg, font_sz))
            left_key = Label(frm, text=one_pyramid[2], fg=lf_tx(), bg=bgr0(), height=1, width=2,
                             font=(lf_fg, font_sz))
            righ_key = Label(frm, text=one_pyramid[3], fg=rt_tx(), bg=bgr0(), height=1, width=2,
                             font=(rt_fg, font_sz))
            root['bg'] = 'blue'
            captch_key.grid(row=1, column=1)
            top_key.grid(row=0, column=1)
            bottom_key.grid(row=2, column=1)
            left_key.grid(row=1, column=0)
            righ_key.grid(row=1, column=2)
        stp += 4

mkps()
root.bind('<Key>', scan_key)

if __name__ == '__main__':
    root.mainloop()
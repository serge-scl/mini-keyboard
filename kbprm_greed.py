# keyboard screen display to improve touch typing skills

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
aktiv_text = 'red2'
back_text = 'grey2'
font_sz = 18
font_sz2 = 28


root = Tk()
root.title('On Screen Keyboard')
root["bg"]="blue"
kb_frame = Frame(root, bg= "blue", width=470, height=273)
joyst_frame_l = Frame(root, bg=back_ground0, width= 235, height=150)
joyst_frame_r = Frame(root, bg=back_ground0, width= 235, height=150)

kb_frame.pack(side=TOP)
joyst_frame_l.pack(side=LEFT)
joyst_frame_r.pack(side=RIGHT)

def keyboard3d():
    stp = 0
    for outer_row in range(3):
        for outer_col in range(5):

            step = outer_row + outer_col + stp
            # print(step)

            frm = Frame(kb_frame, bg=back_ground0)
            frm.grid(row=outer_row, column=outer_col, padx=2, pady=2)

            top = top_bottom_characters[step][0]
            bottom = top_bottom_characters[step][1]
            left = right_left_characters[step][0]
            right = right_left_characters[step][1]

            mylbl1 = Label(frm, text= top, height=1, width=2, bg=back_ground0, font=(font0,font_sz))
            mylbl2 = Label(frm, text= left, height=1, width=2, bg=back_ground0,font=(font0,font_sz))
            mylbl3 = Label(frm, text= bottom, height=1, width=2, bg=back_ground0,font=(font0,font_sz))
            mylbl4 = Label(frm, text=right, height=1, width=2, bg=back_ground0,font=(font0,font_sz))
            mylbl5 = Label(frm, text= 'x', height=1, width=2, fg="blue", bg=back_ground0, font=(font0,font_sz))

            mylbl1.grid(row=0, column=1)
            mylbl2.grid(row=1, column=0)
            mylbl3.grid(row=2, column=1)
            mylbl4.grid(row=1, column=2)
            mylbl5.grid(row=1, column=1)

        stp +=4

def joystick():
    back_l = Label(joyst_frame_l,text=" Back", bg=back_ground0, font=(font0, font_sz2))
    shift_l = Label(joyst_frame_l, text="shift", bg=back_ground0, font=(font0, font_sz2))
    strl_l = Label(joyst_frame_l, text="Ctrl", bg=back_ground0, font=(font0, font_sz2))
    dell_l = Label(joyst_frame_l, text="dell", bg=back_ground0, font=(font0, font_sz2))
    joyst_l = Label(joyst_frame_l, text="x", bg=back_ground0, fg="blue", font=(font0, font_sz2))

    alt_r = Label(joyst_frame_r, text=" Alt ", bg=back_ground0, font=(font0, font_sz2))
    shift_r = Label(joyst_frame_r, text="shift", bg=back_ground0, font=(font0, font_sz2))
    blank_r = Label(joyst_frame_r, text="       ", bg=back_ground0, font=(font0, font_sz2))
    enter_r = Label(joyst_frame_r, text="Enter", bg=back_ground0, font=(font0, font_sz2))
    joyst_r = Label(joyst_frame_r, text="x", bg=back_ground0, fg="blue", font=(font0, font_sz2))

    shift_l.grid(row=0, column=1)
    back_l.grid(row=1, column=0)
    strl_l.grid(row=1, column=2)
    dell_l.grid(row=2, column=1)
    joyst_l.grid(row=1, column=1)

    shift_r.grid(row=0, column=1)
    alt_r.grid(row=1, column=0)
    blank_r.grid(row=1, column=2)
    enter_r.grid(row=2, column=1)
    joyst_r.grid(row=1, column=1)



keyboard3d()
joystick()

if __name__ == '__main__':
    root.mainloop()

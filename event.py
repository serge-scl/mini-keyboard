
'''Here I have done event handling for one keyboard pyramid so far.
 The general idea is that when the user just touches the tip of the pyramid with their finger,
the entire pyramid is displayed on the on-screen keyboard. And only after the tip is tilted,
the character entered into the text is highlighted. The idea is the same as the mouse.
 You are not looking at the mouse at your fingertips, you are looking at the cursor on the screen.'''


from tkinter import *

# keyboard layout
top_bottom_characters = ["'1", "\"2", "(3", "[4", "{5",
                         "$6", "#7", "@8", ";9", "%0",
                         ">+", "<-", "&*", ":/", "!="]
right_left_characters = ["QW", "ER", "TY", "UI", "OP",
                         "AS", "DF", "GH", "JK", "L^",
                         "ZX", "CV", "BN", "M?", ",."]

# keyboard palette
font0 = 'Helvetica'
font1 = 'Liberation Serif'
back_ground0 = 'LightCyan2'
activ_bg = 'yellow3'
akitv_text = 'red2'
back_text = 'grey2'
font_sz = 16


num_pyramid = 5  # this is the number of a separate pyramid

one_key_pyramid = [top_bottom_characters[num_pyramid][0],top_bottom_characters[num_pyramid][1],
                   right_left_characters[num_pyramid][0], right_left_characters[num_pyramid][1],
                   str.lower(right_left_characters[num_pyramid][0]), str.lower(right_left_characters[num_pyramid][1])]
def scan_key(event):
    if event.char in one_key_pyramid:
        captch_key['fg']=akitv_text
        captch_key['bg']=activ_bg
        top_key['bg'] =activ_bg
        bottom_key['bg'] =activ_bg
        left_key['bg'] =activ_bg
        righ_key['bg'] =activ_bg
        root['bg'] =activ_bg
        if event.char == one_key_pyramid[4]:
            left_key['fg'] = akitv_text
            left_key['font']=(font1, font_sz)
        elif event.char == one_key_pyramid[5]:
            righ_key['fg']=akitv_text
            righ_key['font']=(font1, font_sz)
        elif event.char ==top_key['text']:
            top_key['fg'] = akitv_text
            top_key['font'] = (font1,font_sz)
        elif event.char == bottom_key['text']:
            bottom_key['fg'] = akitv_text
            bottom_key['font'] = (font1, font_sz)

    else:
        top_key['bg'] =back_ground0
        bottom_key['bg'] =back_ground0
        left_key['bg'] =back_ground0
        righ_key['bg'] =back_ground0
        root['bg'] = back_ground0
        captch_key['fg']='blue'
        captch_key['bg']=back_ground0
        left_key['fg'] = back_text
        righ_key['fg']=back_text
        top_key['fg'] = back_text
        bottom_key['fg'] = back_text
        left_key['font']=(font0,font_sz)
        righ_key['font']=(font0,font_sz)
        top_key['font'] = (font0, font_sz)
        top_key['font'] = (font0, font_sz)
        bottom_key['font'] = (font0, font_sz)
        bottom_key['font'] = (font0, font_sz)


    # print(event.char)
root = Tk()

captch_key = Label(text='x', fg='blue',bg=back_ground0, height=1, width=2, font=(font0, font_sz))
top_key = Label(text=one_key_pyramid[0], bg=back_ground0, height=1, width=2, font=(font0, font_sz))
bottom_key = Label( text=one_key_pyramid[1], bg=back_ground0, height=1, width=2, font=(font0, font_sz))
left_key = Label( text=one_key_pyramid[2],bg=back_ground0, height=1, width=2, font=(font0, font_sz))
righ_key = Label( text=one_key_pyramid[3], bg=back_ground0, height=1, width=2, font=(font0, font_sz))
root['bg'] = back_ground0
captch_key.grid(row=1,column=1)
top_key.grid(row=0, column=1)
bottom_key.grid(row=2, column=1)
left_key.grid(row=1, column=0)
righ_key.grid(row=1, column=2)


root.bind('<Key>', scan_key)

if __name__ == '__main__':
    root.mainloop()

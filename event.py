'''Here I have done event handling for one keyboard pyramid so far.
 The general idea is that when the user just touches the tip of the pyramid with their finger,
 the entire pyramid is displayed on the on-screen keyboard. And only after the tip is tilted,
  the character entered into the text is highlighted. The idea is the same as the mouse.
 You are not looking at the mouse at your fingertips, you are looking at the cursor on the screen.'''
from tkinter import *


top_bottom_characters = ["'1", "\"2", "(3", "[4", "{5",
                         "$6", "#7", "@8", ";9", "%0",
                         ">+", "<-", "&*", ":/", "!="]
right_left_characters = ["QW", "ER", "TY", "UI", "OP",
                         "AS", "DF", "GH", "JK", "L^",
                         "ZX", "CV", "BN", "M?", ",."]


num_pyramid = 5  # this is the number of a separate pyramid

one_key_pyramid = [top_bottom_characters[num_pyramid][0],top_bottom_characters[num_pyramid][1],
                   str.lower(right_left_characters[num_pyramid][0]), str.lower(right_left_characters[num_pyramid][1])]
def scan_key(event):

    if event.char in one_key_pyramid:
        captch_key.config(text = "x", fg='red', bg='yellow')
        top_key['bg'] ='yellow'
        bottom_key['bg'] ='yellow'
        left_key['bg'] ='yellow'
        righ_key['bg'] ='yellow'
        root['bg'] ='yellow'
        # if event.char['text'] == left_key['text']:
        #     left_key['fg'] = 'blue'
    else:
        top_key['bg'] = 'gray70'
        bottom_key['bg'] = 'gray70'
        left_key['bg'] = 'gray70'
        righ_key['bg'] = 'gray70'
        root['bg'] = 'gray70'
        captch_key.config(text='x', fg="blue", bg='gray70')

    # print(event.char)
root = Tk()

captch_key = Label(text='x', fg='blue', height=1, width=2, font=('Helvetica', 16))
top_key = Label(text=one_key_pyramid[0], height=1, width=2, font=('Helvetica', 16))
bottom_key = Label( text=one_key_pyramid[1], height=1, width=2, font=('Helvetica', 16))
left_key = Label( text=one_key_pyramid[2], height=1, width=2, font=('Helvetica', 16))
righ_key = Label( text=one_key_pyramid[3], height=1, width=2, font=('Helvetica', 16))
captch_key.grid(row=1,column=1)
top_key.grid(row=0, column=1)
bottom_key.grid(row=2, column=1)
left_key.grid(row=1, column=0)
righ_key.grid(row=1, column=2)


root.bind('<Key>', scan_key)
# captch_key.bind('<Key>', scan_key)
# top_key.bind('<Key>', scan_key)
# bottom_key.bind('<Key>', scan_key)
# left_key.bind('<Key>', scan_key)
# righ_key.bind('<Key>', scan_key)

if __name__ == '__main__':
    root.mainloop()

from tkinter import *



top_bottom_characters = ["'1", "\"2", "(3", "[4", "{5",
                         "$6", "#7", "@8", ";9", "%0",
                         ">+", "<-", "&*", ":/", "!="]
right_left_characters = ["QW", "ER", "TY", "UI", "OP",
                         "AS", "DF", "GH", "JK", "L^",
                         "ZX", "CV", "BN", "M?", ",."]



root = Tk()
root.title('On Screen Keyboard')
stp = 0
for outer_row in range(3):
    for outer_col in range(5):

        step = outer_row + outer_col + stp
        # print(step)

        frm = Frame(root, bg='LightCyan2')
        frm.grid(row=outer_row, column=outer_col, padx=2, pady=2)

        top = top_bottom_characters[step][0]
        bottom = top_bottom_characters[step][1]
        left = right_left_characters[step][0]
        right = right_left_characters[step][1]

        myLbl1 = Label(frm, text= top, height=2, width=4, bg='LightCyan2', font="Helvetica 18").grid(row=0, column=1)
        myLbl2 = Label(frm, text= left, height=2, width=4, bg='LightCyan2',font="Helvetica 18").grid(row=1, column=0)
        myLbl3 = Label(frm, text= bottom, height=2, width=4, bg='LightCyan2',font="Helvetica 18").grid(row=2, column=1)
        myLbl4 = Label(frm, text=right, height=2, width=4, bg='LightCyan2',font="Helvetica 18").grid(row=1, column=2)
        myLbl5 = Label(frm, text='x', height=2, width=4, fg='red', bg='LightCyan2', font="Helvetica 10").grid(row=1, column=1)
    stp +=4


if __name__ == '__main__':
    root.mainloop()
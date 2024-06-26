# mouse keyboard pyramids MKP
# Serge Sokolov

"""
The feature of my keyboard is that the entered character is determined at two levels by sensors of different types.
 Touching the tip of the pyramid with a finger activates the capacitive touch sensor,
and the tilt of the tip towards a particular symbol is determined by Hall sensors.
A regular button has two states: pressed and released.  I have three conditions.
Touch, movement, release. The advantage of my keyboard is that after the first touch,
when you have not yet selected the desired symbol or letter, you can already receive an on-screen result.
Five columns of pyramids fit perfectly under five fingers.
Learning to touch-type on my keyboard is not much more difficult than learning to work with a computer mouse.
"""

import tkinter as tk
from tkinter import filedialog
import time
# from ttkthemes import ThemedTk
# from pynput.keyboard import Listener


class Kb:
    tb_ch_e = ["'1", "\"2", "(3", "[4", "{5",
               "$6", "#7", "@8", ";9", "%0",
               ">+", "<-", "&*", ":/", "!="]
    rl_ch_e = ["QW", "ER", "TY", "UI", "OP",
               "AS", "DF", "GH", "JK", "L^",
               "ZX", "CV", "BN", "M?", ",."]

    joysticks = ["<-", "shift", "Del", "Ctrl", "Alt", "Shift", "Enter", "->"]

    ch_up_e = [x + y for x, y in zip(tb_ch_e, rl_ch_e)]
    rl_ch_lw_e = list(map(lambda x: x.lower(), rl_ch_e))
    ch_e = [x + y for x, y in zip(ch_up_e, rl_ch_lw_e)]

    font0 = 'Helvetica'
    font1 = 'Liberation Serif'
    bk_gr0 = 'LightCyan2'
    activ_bg = 'yellow3'
    akitv_text = 'red2'
    back_text = 'grey2'
    font_sz = 18

    #  You can easily change the keyboard layout to a local one with the national alphabet.
    #  In this case, my additional keyboard layout is Cyrillic. You can try adding your own alphabet.
    #  60 characters is not a complete limitation,
    #  since when touch typing on the screen you can create something like scrolling,
    #  and then the meaning of the symbols on the pyramids can be reloaded as you work.

    tb_ch_ru = ["'1", "\"2", "(3", "[4", "{5",
                "Х6", "Ю7", "Э8", ";9", "%0",
                ">+", "<-", "&*", ":/", "!="]
    rl_ch_ru = ["ЙЦ", "УК", "ЕН", "ГШ", "ЩЗ",
                "ФЫ", "ВА", "ПР", "ОЛ", "ДЖ",
                "ЯЧ", "СМ", "ИТ", "ЬБ", ",."]

    ch_up_ru = [x + y for x, y in zip(tb_ch_ru, rl_ch_ru)]
    rl_ch_lw_ru = list(map(lambda x: x.lower(), rl_ch_ru))
    ch_ru = [x + y for x, y in zip(ch_up_ru, rl_ch_lw_ru)]


class EditorMKPs:
    def __init__(self):
        self.window0 = tk.Tk()
        self.window0.geometry("300x450")
        self.window0.title("pyramid keyboard editor")
        self.text_area = tk.Text(self.window0, height=10, wrap="word")
        self.kb_frame = tk.Frame(self.window0)
        self.joyst_frames = tk.Frame(self.window0)

        self.text_area.pack(expand=tk.YES, anchor=tk.N)
        self.kb_frame.pack(anchor=tk.CENTER)
        self.joyst_frames.pack(anchor=tk.S)

        self.kbr(Kb.rl_ch_e, Kb.tb_ch_e)
        self.j_com()
        # self.joysticks()
        self.create_menu()
        # self.tip_touch(x=16)
        # self.window0.bind("<Key>", self.scan_key)
        self.window0.bind_all("<Return>", self.scan_com_e)
        self.window0.bind_all('<space>', self.scan_com_sp)
        self.window0.bind_all('<Control_L>', self.scan_com_ct)
        self.window0.bind_all('<Alt_L>', self.scan_com_al)
        self.window0.bind_all('<Shift_L>', self.scan_com_sl)
        self.window0.bind_all('<Shift_R>', self.scan_com_sr)
        self.window0.bind_all("<Delete>", self.scan_com_d)
        self.window0.bind_all('<BackSpace>', self.scan_key_bk)
        self.window0.bind_all('<KeyPress>', self.press_key)
        # self.window0.bind_all('<Return>', self.press_key)
        self.window0.bind_all('<KeyRelease>', self.release_key)
        # self.n_tip = 16

        self.window0.mainloop()

    def scan_com_e(self, event=None):
        self.joystick_r(1)

    def scan_com_sp(self, event=None):
        self.joystick_r(1)

    def scan_key_bk(self, event=None):
        self.joystick_l(1)

    def scan_com_ct(self, event=None):
        self.joystick_l(1)

    def scan_com_al(self, event=None):
        self.joystick_r(1)

    def scan_com_d(self, event=None):
        self.joystick_l(1)

    def scan_com_sl(self, event=None):
        self.joystick_l(1)

    def scan_com_sr(self, event=None):
        self.joystick_r(1)

    def press_key(self, event=None):
        for i in range(15):
            i2 = Kb.ch_e[i]
            # if event.char == "Return":
            #     self.joystick_r()
            if event.char in i2:
                # print(f" number press {i}")
                self.tip_touch(i)
        # print (f"{event.char} - event press")

        # ......................................

        # This point is a basic feature.
        # Touching the tip of the pyramid is the first part of pressing,
        # the second part is moving to the desired symbol.
        # This cannot be simulated on a pushbutton keyboard that has only two states
        # .....................................


    def release_key(self, even=None):
        time.sleep(0.5)
        self.tip_touch(16)
        self.joystick_r()
        self.joystick_l()

        # print(f" release event key")

    # def scan_key(self,event):
    #     for i in range(15):
    #         i2 = Kb.ch_e[i]
    #         if event.char in i2:
    #             print(f" number press {i}")
    #             self.tip_touch(i)
    #     print(f" letter {event.char}")

    def kbr(self, x, y):
        stp = 0

        for out_row in range(3):
            for out_col in range(5):

                prm = tk.Frame(self.kb_frame)
                prm.grid(row=out_row, column=out_col)
                ps = out_row + out_col + stp
                top = y[ps][0]
                btm = y[ps][1]
                lft = x[ps][0]
                rt = x[ps][1]

                tp_ch = tk.Label(prm, text=top)
                lft_ch = tk.Label(prm, text=lft)
                btm_ch = tk.Label(prm, text=btm)
                rt_ch = tk.Label(prm, text=rt)
                # tip = tk.Label(prm, text="x", bg=Kb.bk_gr0)

                tp_ch.grid(row=0, column=1)
                lft_ch.grid(row=1, column=0)
                btm_ch.grid(row=2, column=1)
                rt_ch.grid(row=1, column=2)
                # tip.grid(row=1, column=1)

            stp += 4

    def tip_touch(self, x=16):
        for out_row in range(3):
            for out_col in range(5):
                ns = out_row * 5 + out_col
                tp = tk.Frame(self.kb_frame)
                tp.grid(row=out_row, column=out_col)
                if ns == x:
                    tip = tk.Label(tp, text="X", fg=Kb.akitv_text, bg=Kb.activ_bg)
                else:
                    tip = tk.Label(tp, text="x", bg=Kb.bk_gr0)
                tip.pack()

    def j_com(self):
        back = tk.Label(self.joyst_frames, text=Kb.joysticks[0])
        shift1 = tk.Label(self.joyst_frames, text=Kb.joysticks[1])
        # jst1 = tk.Label(self.joyst_frames, text="x", bg=Kb.bk_gr0)
        dl = tk.Label(self.joyst_frames, text=Kb.joysticks[2])
        clrl = tk.Label(self.joyst_frames, text=Kb.joysticks[3])
        alt = tk.Label(self.joyst_frames, text=Kb.joysticks[4])
        shif2 = tk.Label(self.joyst_frames, text=Kb.joysticks[5])
        # jst2 = tk.Label(self.joyst_frames, text= "x", bg=Kb.bk_gr0)
        enter = tk.Label(self.joyst_frames, text=Kb.joysticks[6])
        blank = tk.Label(self.joyst_frames, text=Kb.joysticks[7])

        back.grid(row=1, column=0)
        shift1.grid(row=0, column=1)
        # jst1.grid(row=1, column=1)
        dl.grid(row=2, column=1)
        clrl.grid(row=1, column=2)
        alt.grid(row=1, column=3)
        shif2.grid(row=0, column=4)
        # jst2.grid(row=1, column=4)
        enter.grid(row=2, column=4)
        blank.grid(row=1, column=5)

    def joystick_l(self, x=0):
        if x == 1:
            jst1 = tk.Label(self.joyst_frames, text="X", fg=Kb.akitv_text, bg=Kb.activ_bg)
            # jst2 = tk.Label(self.joyst_frames, text="x", bg=Kb.bk_gr0)
            jst1.grid(row=1, column=1)
            # jst2.grid(row=1, column=4)
        else:
            jst1 = tk.Label(self.joyst_frames, text="x", bg=Kb.bk_gr0)
            jst1.grid(row=1, column=1)

    def joystick_r(self, x=0):
        if x == 1:
            jst2 = tk.Label(self.joyst_frames, text="X", fg=Kb.akitv_text, bg=Kb.activ_bg)
            # jst1 = tk.Label(self.joyst_frames, text="x", bg=Kb.bk_gr0)
            jst2.grid(row=1, column=4)
            # jst1.grid(row=1, column=1)
        else:
            jst2 = tk.Label(self.joyst_frames, text="x", bg=Kb.bk_gr0)
            jst2.grid(row=1, column=4)


    def create_menu(self):
        menu = tk.Menu(self.window0)
        self.window0.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window0.quit)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            self.window0.title(f"pyramid keyboard editor - {file}")
            self.text_area.delete(1.0, tk.END)
            with open(file, "r") as file_handler:
                self.text_area.insert(tk.INSERT, file_handler.read())

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            with open(file, "w") as file_handler:
                file_handler.write(self.text_area.get(1.0, tk.END))
            self.window0.title(f"pyramid keyboard editor - {file}")


if __name__ == "__main__":
    # print(Kb.ch_e)
    EditorMKPs()

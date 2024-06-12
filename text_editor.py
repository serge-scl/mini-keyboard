# switching keyboard to local layout

import tkinter as tk
from tkinter import filedialog
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
        self.window0.title("pyramid keyboard editor")
        self.text_area = tk.Text(self.window0, wrap="word")
        self.kb_frame = tk.Frame(self.window0)
        self.joyst_frames = tk.Frame(self.window0)

        self.text_area.pack(expand=tk.YES, anchor=tk.N)
        self.kb_frame.pack(anchor=tk.CENTER)
        self.joyst_frames.pack(anchor=tk.S)

        self.kbr(Kb.rl_ch_e,Kb.tb_ch_e)
        self.joysticks()
        self.create_menu()
        self.tip_touch(x=16)
        self.window0.bind("<Key>", self.scan_key)
        self.n_tip = 16

        self.window0.mainloop()


    def scan_key(self,event):
        for i in range(15):
            i2 = Kb.ch_e[i]
            if event.char in i2:
                # print(f" number press {i}")
                self.tip_touch(i)
        # print(f" letter {event.char}")

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

            stp +=4

    def tip_touch(self, x):
        for out_row in range(3):
            for out_col in range(5):
                ns = out_row * 5 + out_col
                if ns == x:
                    tp = tk.Frame(self.kb_frame)
                    tp.grid(row=out_row, column=out_col)
                    tip = tk.Label(tp, text="X", fg=Kb.akitv_text, bg=Kb.activ_bg)
                    tip.pack()
                else:
                    tp = tk.Frame(self.kb_frame)
                    tp.grid(row=out_row, column=out_col)
                    tip = tk.Label(tp, text="x", bg=Kb.bk_gr0)
                    tip.pack()



    def joysticks(self):
        back =tk.Label(self.joyst_frames, text= Kb.joysticks[0])
        shift1 = tk.Label(self.joyst_frames, text=Kb.joysticks[1])
        jst1 = tk.Label(self.joyst_frames, text="x", bg=Kb.bk_gr0)
        dl = tk.Label(self.joyst_frames, text=Kb.joysticks[2])
        clrl = tk.Label(self.joyst_frames, text=Kb.joysticks[3])
        alt = tk.Label(self.joyst_frames, text=Kb.joysticks[4])
        shif2 = tk.Label(self.joyst_frames, text=Kb.joysticks[5])
        jst2 = tk.Label(self.joyst_frames, text= "x", bg=Kb.bk_gr0)
        enter = tk.Label(self.joyst_frames, text=Kb.joysticks[6])
        blank = tk.Label(self.joyst_frames, text=Kb.joysticks[7])

        back.grid(row=1, column=0)
        shift1.grid(row=0, column=1)
        jst1.grid(row=1, column=1)
        dl.grid(row=2, column=1)
        clrl.grid(row=1, column=2)
        alt.grid(row=1, column=3)
        shif2.grid(row=0, column=4)
        jst2.grid(row=1, column=4)
        enter.grid(row=2, column=4)
        blank.grid(row=1, column=5)

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


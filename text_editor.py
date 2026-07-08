# mouse keyboard pyramids MKP
# Serge Sokolov
"""
Refactored version:
- ScrollTxt is a Frame that wraps a tk.Text with scrollbars (clean init, delegates methods).
- PyramidKeyboard is a reusable widget (tk.Frame) that renders a 3x5 pyramid keyboard
  and provides methods to set the active tip without recreating widgets.
- JoystickFrame is a small widget to show left/right joystick/modifier activity.
- Removed blocking time.sleep; replaced with non-blocking after().
- Highlights all 4 directional characters when a pyramid is selected.
"""

import tkinter as tk
from tkinter import filedialog


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


class ScrollTxt(tk.Frame):
    """A Frame containing a Text with vertical and horizontal scrollbars.
    Delegates text methods (get/insert/delete/...) to internal self.text via __getattr__.
    """

    def __init__(self, master=None, **kw):
        super().__init__(master)
        # Create scrollbars
        self.vbar = tk.Scrollbar(self, orient="vertical")
        self.hbar = tk.Scrollbar(self, orient="horizontal")
        # Create text widget with scroll commands connected
        text_kwargs = kw.copy()
        text_kwargs.setdefault('wrap', 'none')
        text_kwargs.update({'yscrollcommand': self.vbar.set, 'xscrollcommand': self.hbar.set})
        self.text = tk.Text(self, **text_kwargs)

        # Layout
        self.vbar.config(command=self.text.yview)
        self.hbar.config(command=self.text.xview)
        self.vbar.pack(side="right", fill="y")
        self.hbar.pack(side="bottom", fill="x")
        self.text.pack(side="left", fill="both", expand=True)

    def __getattr__(self, item):
        # Delegate unknown attributes to the internal Text widget (so users can call .get/.insert/.delete)
        try:
            return getattr(self.text, item)
        except AttributeError:
            raise AttributeError(f"'ScrollTxt' object has no attribute '{item}'")


class PyramidKeyboard(tk.Frame):
    """Reusable pyramid keyboard widget: rows x cols grid.
    Each cell has top/left/bottom/right labels and a center 'tip' label.
    Use set_active(index) to highlight all 4 directional chars + tip, or clear_active().
    """

    def __init__(self, master, rl_chars, tb_chars, rows=3, cols=5, **styles):
        super().__init__(master)
        self.rows = rows
        self.cols = cols
        self.rl_chars = rl_chars
        self.tb_chars = tb_chars
        self.styles = styles

        self.cell_frames = []
        self.cells = []  # list of dicts with label refs
        self._build_grid()

    def _safe_char(self, s, idx, default=""):
        return s[idx] if (s and len(s) > idx) else default

    def _build_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                idx = r * self.cols + c
                frame = tk.Frame(self, bd=1, relief="flat")
                frame.grid(row=r, column=c, padx=2, pady=2)
                # Top / Left / Bottom / Right
                top_ch = self._safe_char(self.tb_chars[idx], 0)
                bot_ch = self._safe_char(self.tb_chars[idx], 1)
                left_ch = self._safe_char(self.rl_chars[idx], 0)
                right_ch = self._safe_char(self.rl_chars[idx], 1)

                tp = tk.Label(frame, text=top_ch)
                lf = tk.Label(frame, text=left_ch)
                bt = tk.Label(frame, text=bot_ch)
                rt = tk.Label(frame, text=right_ch)
                tip = tk.Label(frame, text="x", bg=Kb.bk_gr0)

                tp.grid(row=0, column=1)
                lf.grid(row=1, column=0)
                tip.grid(row=1, column=1)
                rt.grid(row=1, column=2)
                bt.grid(row=2, column=1)

                # Save references in a dict
                self.cells.append({
                    'frame': frame,
                    'top': tp,
                    'left': lf,
                    'bottom': bt,
                    'right': rt,
                    'tip': tip,
                })

        # Optionally apply styles passed in
        if 'font' in self.styles:
            for cell in self.cells:
                for key in ('top', 'left', 'bottom', 'right', 'tip'):
                    cell[key].config(font=self.styles['font'])
        if 'active_bg' in self.styles:
            self.active_bg = self.styles['active_bg']
        else:
            self.active_bg = Kb.activ_bg
        if 'active_fg' in self.styles:
            self.active_fg = self.styles['active_fg']
        else:
            self.active_fg = Kb.akitv_text
        self.clear_active()

    def set_active(self, index):
        """Highlight the entire pyramid cell at index (0..rows*cols-1):
        all 4 directional chars + center tip get active colors.
        If index is None or out of range, clear."""
        if 0 <= index < len(self.cells):
            for i, cell in enumerate(self.cells):
                if i == index:
                    # Highlight all 4 directions + tip with active colors
                    for key in ('top', 'left', 'bottom', 'right', 'tip'):
                        cell[key].config(fg=self.active_fg, bg=self.active_bg)
                    cell['tip'].config(text="X")
                else:
                    # Reset to default state
                    for key in ('top', 'left', 'bottom', 'right'):
                        cell[key].config(fg="black", bg=Kb.bk_gr0)
                    cell['tip'].config(text="x", fg="black", bg=Kb.bk_gr0)
        else:
            self.clear_active()

    def clear_active(self):
        """Clear highlighting from all pyramids."""
        for cell in self.cells:
            for key in ('top', 'left', 'bottom', 'right'):
                cell[key].config(fg="black", bg=Kb.bk_gr0)
            cell['tip'].config(text="x", fg="black", bg=Kb.bk_gr0)


class JoystickFrame(tk.Frame):
    """Frame for joystick/modifier indicators. Create once and toggle states via set_left/set_right."""

    def __init__(self, master, labels=None, **styles):
        super().__init__(master)
        labels = labels or Kb.joysticks
        # create labeled grid similar to original j_com
        self.back = tk.Label(self, text=labels[0])
        self.shift1 = tk.Label(self, text=labels[1])
        self.dl = tk.Label(self, text=labels[2])
        self.clrl = tk.Label(self, text=labels[3])
        self.alt = tk.Label(self, text=labels[4])
        self.shift2 = tk.Label(self, text=labels[5])
        self.enter = tk.Label(self, text=labels[6])
        self.blank = tk.Label(self, text=labels[7])

        # grid placement (same positions as original)
        self.back.grid(row=1, column=0)
        self.shift1.grid(row=0, column=1)
        self.dl.grid(row=2, column=1)
        self.clrl.grid(row=1, column=2)
        self.alt.grid(row=1, column=3)
        self.shift2.grid(row=0, column=4)
        self.enter.grid(row=2, column=4)
        self.blank.grid(row=1, column=5)

        # dynamic indicator labels for left/right joystick positions
        # reuse grid positions instead of creating ephemeral labels
        self.left_indicator = tk.Label(self, text="x", bg=Kb.bk_gr0)
        self.right_indicator = tk.Label(self, text="x", bg=Kb.bk_gr0)
        self.left_indicator.grid(row=1, column=1)
        self.right_indicator.grid(row=1, column=4)

    def set_left(self, active=False):
        if active:
            self.left_indicator.config(text="X", fg=Kb.akitv_text, bg=Kb.activ_bg)
        else:
            self.left_indicator.config(text="x", fg="black", bg=Kb.bk_gr0)

    def set_right(self, active=False):
        if active:
            self.right_indicator.config(text="X", fg=Kb.akitv_text, bg=Kb.activ_bg)
        else:
            self.right_indicator.config(text="x", fg="black", bg=Kb.bk_gr0)


class EditorMKPs:
    def __init__(self):
        self.window0 = tk.Tk()
        self.window0.geometry("300x680")
        self.window0.title("pyramid keyboard editor")
        self.text_area = ScrollTxt(self.window0, undo=True)
        self.kb_frame = tk.Frame(self.window0)
        self.joyst_frames = JoystickFrame(self.window0)

        # Layout
        self.text_area.pack(expand=tk.YES, anchor=tk.N, fill='both')
        self.kb_frame.pack(anchor=tk.CENTER)
        self.joyst_frames.pack(anchor=tk.S)

        # Create reusable pyramid keyboard inside kb_frame
        self.pyramid = PyramidKeyboard(self.kb_frame, Kb.rl_ch_e, Kb.tb_ch_e, font=(Kb.font0, 10),
                                       active_bg=Kb.activ_bg, active_fg=Kb.akitv_text)
        self.pyramid.pack()

        # File menu and bindings
        self.create_menu()

        # Bind keys
        self.window0.bind_all("<Return>", self.scan_com_e)
        self.window0.bind_all('<space>', self.scan_com_sp)
        self.window0.bind_all('<Control_L>', self.scan_com_ct)
        self.window0.bind_all('<Alt_L>', self.scan_com_al)
        self.window0.bind_all('<Shift_L>', self.scan_com_sl)
        self.window0.bind_all('<Shift_R>', self.scan_com_sr)
        self.window0.bind_all("<Delete>", self.scan_com_d)
        self.window0.bind_all('<BackSpace>', self.scan_key_bk)
        self.window0.bind_all('<KeyPress>', self.press_key)
        self.window0.bind_all('<KeyRelease>', self.release_key)

        # Start mainloop
        self.window0.mainloop()

    # joystick helpers: call joystick frame methods
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
        # Map key char to pyramid index; when found highlight entire pyramid cell.
        ch = event.char if event else ''
        for i in range(15):
            i2 = Kb.ch_e[i]
            if ch and ch in i2:
                self.tip_touch(i)
                break

    def release_key(self, event=None):
        # Non-blocking reset after 500 ms to avoid freezing UI.
        def _reset():
            self.tip_touch(16)  # clear pyramid highlighting
            # Toggle both briefly (original behavior called both)
            self.joystick_r()
            self.joystick_l()

        self.window0.after(500, _reset)

    def kbr(self, x, y):
        # Kept for compatibility if other code calls it; now delegates to PyramidKeyboard
        pass

    def tip_touch(self, x=16):
        """Highlight the entire pyramid cell (all 4 directions + tip) at index x.
        If x >= 15, clear highlighting."""
        if 0 <= x < 15:
            self.pyramid.set_active(x)
        else:
            self.pyramid.clear_active()

    def j_com(self):
        # kept for compatibility; joystick frame is already created
        pass

    def joystick_l(self, x=0):
        self.joyst_frames.set_left(active=(x == 1))

    def joystick_r(self, x=0):
        self.joyst_frames.set_right(active=(x == 1))

    def create_menu(self):
        menu = tk.Menu(self.window0)
        self.window0.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window0.quit)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file = filedialog.askopenfilename(defaultextension=".txt",
                                          filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            self.window0.title(f"pyramid keyboard editor - {file}")
            self.text_area.delete(1.0, tk.END)
            with open(file, "r", encoding='utf-8') as file_handler:
                self.text_area.insert(tk.INSERT, file_handler.read())

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            with open(file, "w", encoding='utf-8') as file_handler:
                file_handler.write(self.text_area.get(1.0, tk.END))
            self.window0.title(f"pyramid keyboard editor - {file}")


if __name__ == "__main__":
    EditorMKPs()

from tkinter import BOTH, END, INSERT, Text, ttk

from sprt.theme import Color

_TEXT_STYLE = {
    "background": Color.box_bg,
    "foreground": "black",
    "borderwidth": 0,
    "relief": "flat",
    "highlightthickness": 0,
    "insertbackground": Color.dark_font,
}


class TextField(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, style="Container.TFrame", padding=5)

        self.inner = Text(self, **kwargs, **_TEXT_STYLE)
        self.inner.pack(fill=BOTH, expand=True)

        self.bind("<Configure>", self.__adjust_text_entry_size)

    def __adjust_text_entry_size(self, _):
        self.inner.configure(width=self.cget("width"))

    @property
    def value(self) -> str:
        return self.inner.get("1.0", END)[:-1]

    @value.setter
    def value(self, new_value: str):
        self.inner.insert(INSERT, new_value)

    def clear(self):
        self.inner.delete(1.0, END)

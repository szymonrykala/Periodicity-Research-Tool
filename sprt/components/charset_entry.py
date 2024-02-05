from tkinter import ttk

from sprt.config import DEFAULT_CHARSET

from .text_field import TextField


class CharsetEntry(ttk.Frame):
    def __init__(self, master, height: int = 5, width: int = 10):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="Zbiór znaków:").grid(column=0, row=0, sticky="w")
        ttk.Button(self, text="przywróć", command=self.set_default).grid(column=1, row=0, sticky="e")
        self.entry = TextField(master=self, wrap="char", width=width, height=height)
        self.entry.grid(column=0, columnspan=2, row=1, sticky="nsew")

        self.set_default()

    @property
    def value(self) -> bytes:
        if self.entry.value.startswith("b'"):
            return bytes(eval(self.entry.value))
        else:
            return self.entry.value.encode()

    @value.setter
    def value(self, value: bytes | str):
        self.entry.clear()
        self.entry.value = str(value)

    def set_default(self):
        self.entry.clear()
        self.entry.value = DEFAULT_CHARSET

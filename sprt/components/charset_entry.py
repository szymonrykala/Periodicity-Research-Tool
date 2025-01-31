from tkinter import ttk

from sprt.config import DEFAULT_CHARSET
from sprt.utils.utils import bytes_to_str

from .text_field import TextField


class CharsetEntry(ttk.Frame):
    def __init__(self, master, height: int = 5, width: int = 10):
        super().__init__(master, style="Container.TFrame")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="Zbiór znaków:").grid(column=0, row=0, sticky="w", padx=(5, 0))
        ttk.Button(self, text="przywróć", command=self.set_default, style="Secondary.TButton").grid(
            column=1, row=0, sticky="e"
        )
        self.entry = TextField(master=self, wrap="char", width=width, height=height)
        self.entry.grid(column=0, columnspan=2, row=1, sticky="nsew")

        self.set_default()

    @property
    def value(self) -> str:
        return self.entry.value

    @value.setter
    def value(self, value: bytes | str):
        self.entry.clear()
        self.entry.value = bytes_to_str(value)

    def set_default(self):
        self.entry.clear()
        self.entry.value = DEFAULT_CHARSET

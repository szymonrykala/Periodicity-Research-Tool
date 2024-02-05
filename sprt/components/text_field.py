from tkinter import BOTH, END, INSERT, Text, ttk


class TextField(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.inner = Text(self, **kwargs)
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

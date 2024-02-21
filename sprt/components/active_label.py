from tkinter import BOTH, ttk


class ActiveLabel(ttk.Frame):
    def __init__(self, master, **kwds):
        super().__init__(master)

        self.__i = 0

        self.label = ttk.Label(self, **kwds)
        self.label.pack(fill=BOTH, expand=True)

        self.bind("<Configure>", self.__resize_label)

    def __resize_label(self, event):
        if self.__i % 5 == 0:
            self.label.configure(wraplength=event.width)
        self.__i += 1

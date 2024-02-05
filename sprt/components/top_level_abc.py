from abc import ABC
from random import randint
from tkinter import Toplevel


class TopLevelABC(ABC, Toplevel):
    def __init__(self, title: str, width: int = 800, height: int = 400):
        super().__init__()
        self.set_window_size(width, height)
        self.title(title)
        self.configure(padx=5, pady=5)

    def set_window_size(self, width: int, height: int):
        w, h, ws, hs = (
            width,
            height,
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )

        offset = randint(50, 80)

        x = (ws / 2) - (w / 2) + offset
        y = (hs / 2) - (h / 2) + offset

        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

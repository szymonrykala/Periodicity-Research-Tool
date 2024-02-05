from tkinter import BOTH, PhotoImage, Tk, font

from matplotlib import pyplot

from sprt.components.main_window import MainWindow
from sprt.components.top_level_abc import TopLevelABC
from sprt.config import STATIC_DIR


class App:
    def __init__(self, master: Tk):
        self.master = master
        TopLevelABC.set_window_size(self.master, 800, 600)  # type: ignore
        self.master.minsize(800, 500)
        self.master.title("Periodicity Research Tool")

        self.icon = PhotoImage(file=STATIC_DIR + "app_icon.png")
        self.master.iconphoto(True, self.icon)

        master.protocol("WM_DELETE_WINDOW", self.__on_close)

        self.__styles_setup()
        MainWindow(master=master).pack(fill=BOTH, expand=True)

    def __on_close(self):
        pyplot.close("all")
        self.master.destroy()

    def __styles_setup(self):
        f = font.nametofont("TkDefaultFont")
        f.config(size=f.cget("size") + 2)

from tkinter import BOTH, PhotoImage, Tk, font, ttk

from matplotlib import pyplot

from sprt.components.main_window import MainWindow
from sprt.components.top_level_abc import TopLevelABC
from sprt.config import STATIC_DIR
from sprt.styles import Color


class App:
    def __init__(self, master: Tk):
        self.master = master

        self.__style_setup()
        self.__font_setup()

        TopLevelABC.set_window_size(self.master, 800, 600)  # type: ignore
        self.master.minsize(800, 500)
        self.master.title("Periodicity Research Tool")

        self.icon = PhotoImage(file=STATIC_DIR + "app_icon.png")
        self.master.iconphoto(True, self.icon)

        master.protocol("WM_DELETE_WINDOW", self.__on_close)
        MainWindow(master=master).pack(fill=BOTH, expand=True)

    def __on_close(self):
        pyplot.close("all")
        self.master.destroy()

    def __font_setup(self):
        f = font.nametofont("TkDefaultFont")
        f.config(size=f.cget("size") + 2)

    def __style_setup(self):
        self.master.configure(background=Color.background)
        s = ttk.Style()
        s.theme_use("default")

        # ---- FRAMES ----
        s.configure("TFrame", background=Color.background)
        s.configure("App.TFrame", background=Color.background)
        s.configure("Container.TFrame", background=Color.box_bg, foreground="black")

        s.configure("ListItem.TFrame", background=Color.box_bg)
        s.configure("Selected.ListItem.TFrame", background=Color.primary)
        s.configure("Selected.ListItem.TFrame", background=Color.primary)

        # ---- LABELS ----
        s.configure("TLabel", background=Color.box_bg)
        s.configure("Selected.ListItem.TLabel", background=Color.primary)

        s.configure("TLabelframe", background=Color.background, borderwidth=0)
        s.configure("TLabelframe.Label", background=Color.background, foreground=Color.gray_font)

        # ---- BUTTONS ----
        s.configure(
            "TButton",
            background=Color.primary,
            foreground=Color.light_font,
            borderwidth=0,
        )
        s.map(
            "TButton",
            background=[("pressed", "!disabled", Color.dim), ("active", Color.accent)],
            relief=[("pressed", "!disabled", "sunken")],
        )

        s.configure(
            "Secondary.TButton",
            background=Color.box_bg,
            foreground=Color.dim,
        )
        s.map(
            "Secondary.TButton",
            foreground=[
                ("pressed", "!disabled", Color.accent),
                ("active", Color.accent),
            ],
            background=[],
        )

        # ---- CHECKBOXES ----
        s.configure(
            "TCheckbutton",
            background=Color.box_bg,
            indicatorcolor=Color.background,
            indicatormargin=5,
        )
        s.map("TCheckbutton", background=[("selected", Color.primary)])

        s.configure("Secondary.TCheckbutton", foreground=Color.gray_font)
        s.map(
            "Secondary.TCheckbutton",
            background=[("selected", Color.box_bg)],
            foreground=[("selected", Color.dim)],
        )

        # ---- SCROLLBAR ----
        s.configure(
            "TScrollbar",
            arrowcolor=Color.box_bg,
            arrowsize=-1,
            background=Color.gray,
            bordercolor=Color.box_bg,
            darkcolor=Color.box_bg,
            foreground=Color.box_bg,
            lightcolor=Color.box_bg,
            troughcolor=Color.box_bg,
            relief="flat",
            borderwidth=0,
        )
        s.map(
            "TScrollbar",
            background=[("disabled", Color.box_bg), ("active", Color.primary)],
            relief=[("pressed", "!disabled", "sunken")],
        )

        # ---- SEPARATOR ----
        s.configure("TSeparator", background=Color.gray)

        # ---- TEXT ENTRY ----
        s.configure("TEntry", insertcolor=Color.dark_font)

from abc import ABC, abstractmethod
from io import BytesIO
from tkinter import NSEW, E, ttk

from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from PIL import Image, ImageTk


class BasePlotFrame(ABC, ttk.Frame):
    def __init__(self, master, title: str, xlabel: str, ylabel: str):
        super().__init__(master)
        self._title: str = title
        self._xlabel: str = xlabel
        self._ylabel: str = ylabel

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._fig, self._ax = self.__create_figure()
        self._fig.set_figwidth(12)

        self.__img = None
        self.__img_canvas = ttk.Label(self, text=title)
        self.__img_canvas.grid(column=0, row=1, sticky=NSEW)

        ttk.Button(
            self,
            text="inter",
            command=self.__show_interactive,
            padding=0,
        ).grid(row=0, column=0, sticky=E)

        # self.master.after(500, lambda: self.bind("<Configure>", self.resize))
        # self._resize_counter = 0

    @property
    def ax(self) -> Axes:
        return self._ax

    @property
    def fig(self) -> Figure:
        return self._fig

    def render_chart(self):
        self._draw()
        self.__render_img()
        pyplot.close(self.fig)

    def set_integer_axis(self):
        self.ax.locator_params(axis="both", integer=True, tight=True)
        # for axis in [self.ax.xaxis, self.ax.yaxis]:
        # axis.set_major_locator(ticker.MaxNLocator(integer=True))

    def __create_figure(self):
        fig, ax = pyplot.subplots(squeeze=True)
        ax.set_title(self._title)
        ax.set_xlabel(self._xlabel)
        ax.set_ylabel(self._ylabel)
        ax.grid(True, axis="both")

        return fig, ax

    def __show_interactive(self):
        self._fig, self._ax = self.__create_figure()
        self._draw()
        self._fig.show()

    def __render_img(self):
        buff = BytesIO()
        self.fig.savefig(buff, format="jpg")
        buff.seek(0)

        self.__img = Image.open(buff)
        self.__img.resize(size=(self.winfo_height(), self.winfo_width()))
        self.img_tk = ImageTk.PhotoImage(self.__img)
        self.__img_canvas.configure(image=self.img_tk)

    # def resize(self, event):
    #     if self.__img and self._resize_counter % 10 == 0:
    #         print(event)
    #         img = self.__img.resize(size=(event.width, event.height))
    #         img_tk = ImageTk.PhotoImage(img)
    #         self.__img_canvas.configure(image=img_tk)
    #         self.__img_canvas.image = img_tk
    #     self._resize_counter += 1

    @abstractmethod
    def _draw(self):
        ...

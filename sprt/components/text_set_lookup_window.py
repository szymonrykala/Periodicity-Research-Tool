from concurrent.futures import ThreadPoolExecutor
from functools import cache
from tkinter import BOTH, VERTICAL, X, ttk

from sprt.components import ScrollableFrame, TextField
from sprt.text_generator import RandomText
from sprt.utils import bytes_to_str

from .charts import GroupChart, Histogram
from .top_level_abc import TopLevelABC


class GeneratedTextWindowController:
    def __init__(self, text: RandomText):
        self.text: RandomText = text

    @cache
    def get_groups(self, count: int) -> dict[int, list[str]]:
        out = {}

        for i in range(self.text.length - count + 1):
            chunk = bytes(self.text.text[i : i + count].tolist())
            out.setdefault(chunk, 0)
            out[chunk] += 1

        grouped_by_count = {}
        for k, v in out.items():
            grouped_by_count.setdefault(v, []).append(k)

        return grouped_by_count


class TextSetWindow(TopLevelABC):
    def __init__(self, text: RandomText):
        super().__init__(title="Podgląd zbioru", width=1200, height=800)
        self.__i = 1

        self.controller = GeneratedTextWindowController(text)
        scroll = ScrollableFrame(self, VERTICAL)
        scroll.pack(expand=True, fill=BOTH)

        frame = scroll.inner_frame

        ttk.Label(frame, text=f"Rozkład: {text.distribution}").pack(fill=X)
        ttk.Label(frame, text=f"Zadane parametry: {text.arguments}").pack(fill=X)
        ttk.Label(frame, text=f"Rzeczywiste parametry: mean={text.mean}, stdev={text.stdev}").pack(fill=X)
        ttk.Label(frame, text=f"Ilość znaków: {text.length}").pack(fill=X)
        self.charset_label = ttk.Label(frame, text=f"Wykorzystany zbiór znaków: {text.parsed_charset}")
        self.charset_label.pack(fill=X)

        Histogram(frame, x=text.charset, y=text.density_matrix).pack(fill=X, expand=True)

        self.pack_text_view(frame, text)
        self.pack_group_charts(frame)

        frame.bind("<Configure>", self.__resize_label, add="+")

    def __resize_label(self, event):
        if self.__i % 5 == 0:
            self.charset_label.configure(wraplength=event.width)
        self.__i += 1

    def pack_group_charts(self, frame):
        with ThreadPoolExecutor() as exec:
            groups = range(2, 7, 1)
            jobs = exec.map(self.controller.get_groups, groups)

        for i, data in zip(groups, jobs):
            if len(data) > 1:
                GroupChart(frame, group_size=i, data=data).pack(fill=X)

    def pack_text_view(self, frame, text: RandomText):
        field = TextField(frame)
        content: str

        if text.length > 3_000:
            content = "<maksymalnie 3 000 znaków>\n" + bytes_to_str(text.text[:3000])
        else:
            content = text.parsed_text

        field.value = content
        field.pack(fill=X)

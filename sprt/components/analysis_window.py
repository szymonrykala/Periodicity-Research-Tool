import json
from copy import copy
from dataclasses import asdict
from tkinter import BOTH, VERTICAL, X, filedialog, messagebox, ttk

from sprt.analysis.analysis import PeriodicityAnalysis
from sprt.components import ScrollableFrame
from sprt.components.charts.results_chart import (
    PatternIndexOffsetGroupsChart,
    PatternOccurrencesChart,
)
from sprt.components.text_field import TextField
from sprt.components.top_level_abc import TopLevelABC
from sprt.logger import logger
from sprt.utils import bytes_to_str


class AnalysisWindow(TopLevelABC):
    def __init__(self, master, analysis: PeriodicityAnalysis):
        super().__init__("Wyniki analizy", width=1200, height=800)
        self.analysis = analysis

        scroll = ScrollableFrame(self, VERTICAL)
        scroll.pack(expand=True, fill=BOTH)
        frame = scroll.inner_frame

        for label in (
            ttk.Label(frame, text=f"Analizowany zbiór: {analysis.text_set.name}"),
            ttk.Label(frame, text=f"Rozkład: {analysis.text_set.distribution}"),
            ttk.Label(
                frame,
                text=f"Rzeczywiste parametry: mean={analysis.text_set.mean}, stdev={analysis.text_set.stdev}",
            ),
            ttk.Label(frame, text=f"Ilość znaków: {analysis.text_set.length}"),
        ):
            label.configure(padding=5)
            label.pack(fill=X)

        ttk.Label(
            frame,
            text=f"Wykorzystany zbiór znaków:",
        ).pack(fill=X, ipadx=5)

        f = TextField(frame, height=7)
        f.value = bytes_to_str(analysis.text_set.charset)
        f.pack(fill=X, ipadx=5)

        ttk.Button(
            frame,
            text="Eksportuj dane analizy do JSON",
            command=self.__dump_to_json_file,
            padding=5,
        ).pack(expand=True, fill=X)

        for result in analysis.results:
            pattern_str = bytes_to_str(result.pattern.text)
            if result.index_offset:
                PatternOccurrencesChart(frame, pattern=pattern_str, y=result.indexes).pack(fill=X)

                PatternIndexOffsetGroupsChart(
                    frame,
                    pattern=pattern_str,
                    x=result.index_offset_groups.keys(),
                    y=result.index_offset_groups.values(),
                ).pack(fill=X, pady=5)
            else:
                ttk.Label(
                    frame,
                    text=f"Brak wystąpień dla wzorca: {pattern_str}",
                    padding=5,
                    justify="center",
                ).pack(fill=X, expand=True, anchor="center", ipadx=5, pady=5)

    def __dump_to_json_file(self):
        file = filedialog.asksaveasfile(
            title="zapisz wyniki analizy", filetypes=[("json", ".json")]
        )
        if not file:
            return

        out = []
        for item in copy(self.analysis.results):
            item.pattern = bytes_to_str(item.pattern.text)  # pattern text instead of full object
            out.append(asdict(item))

        content = json.dumps(out)
        file.write(content)
        file.close()

        logger.info(f"Analysis saved to {file.name}")
        messagebox.showinfo("Sukces", "Plik został zapisany!")

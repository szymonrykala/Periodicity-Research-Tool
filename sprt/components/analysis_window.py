from tkinter import BOTH, VERTICAL, X, ttk

from sprt.analysis.analysis import PeriodicityAnalysys
from sprt.components import ScrollableFrame
from sprt.components.charts.results_chart import (
    PatternIndexOffsetGroupsChart,
    PatternOccurencesChart,
)
from sprt.components.top_level_abc import TopLevelABC
from sprt.utils import bytes_to_str


class AnalysisWindow(TopLevelABC):
    def __init__(self, master, analysys: PeriodicityAnalysys):
        super().__init__("Wyniki analizy", width=1200, height=800)

        scroll = ScrollableFrame(self, VERTICAL)
        scroll.pack(expand=True, fill=BOTH)
        frame = scroll.inner_frame

        ttk.Label(frame, text=f"Analizowany zbiór: {analysys.text_set.name}").pack(fill=X)
        ttk.Label(frame, text=f"Rozkład: {analysys.text_set.distribution}").pack(fill=X)
        ttk.Label(
            frame,
            text=f"Rzeczywiste parametry: mean={analysys.text_set.mean}, stdev={analysys.text_set.stdev}",
        ).pack(fill=X)
        ttk.Label(frame, text=f"Ilość znaków: {analysys.text_set.length}").pack(fill=X)
        self.charset_label = ttk.Label(
            frame,
            text=f"Wykorzystany zbiór znaków: {bytes_to_str(analysys.text_set.charset)}",
        )
        self.charset_label.pack(fill=X)

        for result in analysys.results:
            pattern_str = bytes_to_str(result.algorithm.pattern)
            if result.index_offset:
                ttk.Label(
                    frame,
                    text=f"Wzorzec: {pattern_str}",
                    padding=(0, 10, 0, 0),
                ).pack(fill=X, anchor="center")

                PatternOccurencesChart(frame, pattern=pattern_str, y=result.algorithm.value).pack(fill=X)

                PatternIndexOffsetGroupsChart(
                    frame,
                    pattern=pattern_str,
                    x=result.index_offset_groups.keys(),
                    y=result.index_offset_groups.values(),
                ).pack(fill=X)
            else:
                ttk.Label(
                    frame,
                    text=f"Brak wystąpień dla wzorca: {pattern_str}",
                    padding=(0, 10, 0, 0),
                ).pack(fill=X)

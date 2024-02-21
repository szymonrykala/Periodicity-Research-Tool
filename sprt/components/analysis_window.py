from tkinter import BOTH, VERTICAL, X, ttk

from sprt.analysis.analysis import PeriodicityAnalysis
from sprt.components import ScrollableFrame
from sprt.components.charts.results_chart import (
    PatternIndexOffsetGroupsChart,
    PatternOccurrencesChart,
)
from sprt.components.top_level_abc import TopLevelABC
from sprt.utils import bytes_to_str


class AnalysisWindow(TopLevelABC):
    def __init__(self, master, analysis: PeriodicityAnalysis):
        super().__init__("Wyniki analizy", width=1200, height=800)

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

        self.charset_label = ttk.Label(
            frame,
            text=f"Wykorzystany zbiór znaków: {bytes_to_str(analysis.text_set.charset)}",
        )
        self.charset_label.pack(fill=X, ipadx=5)

        for result in analysis.results:
            pattern_str = bytes_to_str(result.algorithm.pattern)
            if result.index_offset:
                PatternOccurrencesChart(frame, pattern=pattern_str, y=result.algorithm.value).pack(
                    fill=X
                )

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

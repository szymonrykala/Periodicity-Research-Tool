from numpy import poly1d, polyfit

from sprt.analysis.time_measure import TextRunResults
from sprt.config import DISPLAY_TREND_LINES

from .base_chart import BasePlotFrame


class AlgorithmTimePerTextSetChart(BasePlotFrame):
    def __init__(
        self,
        master,
        algorithm: str,
        patterns: list[int],
        text_sets_result: TextRunResults,
    ):
        self.x = patterns
        self.ys = text_sets_result

        super().__init__(
            master=master,
            title=f"Średni czas wykonania algorytmu na bazie '{algorithm}' dla zbiorów",
            xlabel="długość wzorca",
            ylabel="czas wykonania [s]",
        )

        self.render_chart()

    def _draw(self):
        self.set_integer_axis("x")
        self.ax.set_ymargin(0.3)
        for text_set, results in self.ys.items():
            self.ax.errorbar(x=self.x, y=results.time, yerr=results.stdev, label=f"{text_set}")

            if DISPLAY_TREND_LINES:
                z = polyfit(self.x, results.time, 2)
                p = poly1d(z)
                self.ax.plot(self.x, p(self.x), label=f"{text_set}")

        self.ax.legend()


class TextSetPerAlgorithmTimeChart(BasePlotFrame):
    def __init__(self, master, text_set_name: str, patterns: list[int], data: TextRunResults):
        self.x = patterns
        self.ys = data

        super().__init__(
            master=master,
            title=f"Średni czas wykonania algorytmów dla zbioru '{text_set_name}'",
            xlabel="długość wzorca",
            ylabel="czas wykonania [s]",
        )

        self.render_chart()

    def _draw(self):
        self.set_integer_axis("x")
        self.ax.set_ymargin(0.4)

        for alg_name, results in self.ys.items():
            self.ax.errorbar(x=self.x, y=results.time, yerr=results.stdev, label=alg_name)

            if DISPLAY_TREND_LINES:
                z = polyfit(self.x, results.time, 2)
                p = poly1d(z)
                self.ax.plot(self.x, p(self.x), label=alg_name)

        self.ax.legend()

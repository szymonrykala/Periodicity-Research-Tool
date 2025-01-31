from typing import Iterable

from matplotlib import pyplot

from .base_chart import BasePlotFrame


class PatternOccurrencesChart(BasePlotFrame):
    def __init__(self, master, pattern: str, y: list[int]):
        self.y = y
        super().__init__(
            master=master,
            title=f"Występowania wzorca '{pattern}'",
            xlabel="kolejne wystąpienia",
            ylabel="miejsce wystąpienia",
        )
        self.set_integer_axis()
        self.render_chart()

    def _draw(self):
        self.ax.plot(tuple(range(1, len(self.y) + 1)), self.y, "o-")
        self.ax.set_ylim(ymin=0)

    def __del__(self):
        pyplot.close(self.fig)


class PatternIndexOffsetGroupsChart(BasePlotFrame):
    def __init__(
        self,
        master,
        pattern: str,
        y: Iterable[int],
        x: Iterable[int],
    ):
        self._y = tuple(y)
        self._x = tuple(x)
        super().__init__(
            master=master,
            title=f"Częstość występowania przesunięć wzorca '{pattern}'",
            xlabel="przesunięcie występowania",
            ylabel="Ilość powtórzeń przesunięcia",
        )
        self.set_integer_axis()
        self.render_chart()

    def _draw(self):
        self.ax.stem(self._x, self._y)
        self.ax.set_xlim(xmin=0)

    def __del__(self):
        pyplot.close(self.fig)

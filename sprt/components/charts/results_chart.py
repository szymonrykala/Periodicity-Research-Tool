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
        self.ax.plot(self.y, "o-")

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
        self.fig.set_figwidth(13)

        self.ax.stem(self._x, self._y)

    def __del__(self):
        pyplot.close(self.fig)

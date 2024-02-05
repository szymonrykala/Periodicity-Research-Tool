from .base_chart import BasePlotFrame


class GroupChart(BasePlotFrame):
    def __init__(self, master, group_size: int, data: dict[int, list[str]]):
        self._data = data
        super().__init__(
            master=master,
            title=f"Ilość wystąpień grup '{group_size}' znakowych",
            xlabel="Liczba wystapień grupy w zbiorze",
            ylabel="Ilość grup",
        )

        self.set_integer_axis()
        self.render_chart()

    def _draw(self):
        x = list(self._data.keys())  # ilość wystąpień
        y = [len(v) for v in self._data.values()]  # grupy które wystąpły daną ilość razy
        self.ax.stem(x, y, "g")
        # self.ax.stem(x, y, width=0.5, color="g")

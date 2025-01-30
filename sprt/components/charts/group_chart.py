import json
from collections import OrderedDict
from tkinter import filedialog, messagebox

from sprt.logger import logger

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

    def _save_data_to_file(self):
        file = filedialog.asksaveasfile(title="zapisz grupy", filetypes=[("json", ".json")])
        if not file:
            return

        content = json.dumps(
            OrderedDict(sorted(self._data.items(), key=lambda i: i[0], reverse=True))
        )

        file.write(content)
        file.close()

        logger.info(f"Data saved to {file.name}")
        messagebox.showinfo("Sukces", "Plik został zapisany!")

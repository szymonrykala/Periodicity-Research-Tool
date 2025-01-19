from numpy import ndarray

from sprt.logger import logger

from .base_chart import BasePlotFrame


class Histogram(BasePlotFrame):
    def __init__(
        self,
        master,
        y: ndarray,  # float
        x: ndarray,  # int
    ):
        self.y = y
        self.x = x
        super().__init__(
            master=master,
            title="Gęstość prawdopodobieństwa wystąpienia znaków",
            xlabel="Znak",
            ylabel="Prawdopodobieństwo",
        )

        self.render_chart()

    def _draw(self):
        xlabels = self.x.tolist()
        try:
            xlabels = tuple(bytes(xlabels).decode(errors="strict"))
        except Exception as e:
            logger.warning(f"histogram xlabels decoding failed: {e}")
            self.ax.set_xlabel("Bajt")

        self.ax.bar(
            x=xlabels,
            height=self.y,
            width=0.5,
            color="g",
        )

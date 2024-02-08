from tkinter import DoubleVar, ttk
from typing import Any, Optional

from sprt.components import SelectableWidget
from sprt.logger import logger
from sprt.text_generator import Distribution
from sprt.utils import validate_digit


class DistributionViewController:
    def __init__(self, distribution: type[Distribution]):
        self.distribution = distribution
        self.params = {k: DoubleVar(value=1.0) for k in self.distribution.parameters.keys()}

    def get_value(self) -> Distribution:
        params = {k: val.get() for k, val in self.params.items()}
        logger.info(f"Creating distribution {self.distribution._name} with {params}")

        return self.distribution(**params)


class DistributionView(SelectableWidget):
    def _set_up(self, item: Any):
        self.configure(style="ListItem.TFrame")
        self.checkbox.grid(row=0, column=0, columnspan=2, sticky="we")

        self.columnconfigure(1, weight=1)
        self.controller = DistributionViewController(item)
        self.__mount()

    @property
    def value(self) -> Optional[Distribution]:
        if self.checkbox.value:
            return self.controller.get_value()

    def __mount(self):
        for i, (name, var) in enumerate(self.controller.params.items()):
            i += 1
            ttk.Label(self, text=name).grid(column=0, row=i, sticky="we")
            ttk.Entry(
                self,
                textvariable=var,
                validatecommand=(self.register(validate_digit), "%S"),
                validate="key",
                width=8,
            ).grid(column=1, row=i, sticky="we")

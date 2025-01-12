from tkinter import EW, NSEW, VERTICAL, IntVar, filedialog, ttk
from typing import Callable, Optional

import numpy

from sprt.components import CharsetEntry, WidgetSelectionList
from sprt.components.distributionView import DistributionView
from sprt.components.top_level_abc import TopLevelABC
from sprt.logger import logger
from sprt.text_generator import Distribution, Generator, RandomText, distributions_dict
from sprt.utils import validate_digit_input

from .random_text_view import GeneratedRandomTextView


class GeneratorWindowController:
    def __init__(self):
        self._generator = Generator()
        self.desired_length = IntVar(value=10_000)

    def import_text_set(self) -> Optional[RandomText]:
        selected_file = filedialog.askopenfile(title="Choose file to import", mode="rb")
        if not selected_file:
            return
        logger.info(f"loading file {selected_file}")
        text = None
        content: numpy.ndarray = numpy.array(tuple(selected_file.read()))  # bytes array
        try:
            text = RandomText.from_json(selected_file.read().decode())
        except Exception as e:
            logger.error(e)
            text = RandomText.from_bytes_or_text(content, name=selected_file.name)
        finally:
            if text:
                logger.info(f"file imported successfully")
                return text
            else:
                logger.warning(f"file import failed")

    def generate_sets(self, charset: bytes, distributions: tuple[Distribution]):
        self._generator.char_set = charset
        length = self.desired_length.get()

        return tuple(self._generator.generate(size=length, distrib=dist) for dist in distributions)


class SetsGeneratorWindow(TopLevelABC):
    def __init__(self, append_main_list_clb: Callable[[RandomText], None]):
        super().__init__("Generowanie zbioru")
        self.minsize(700, 300)
        self.maxsize(900, 400)

        self.configure(padx=5, pady=5)
        self.grid_columnconfigure([0, 1, 2], weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.append_main_list_clb = append_main_list_clb
        self.controller = GeneratorWindowController()

        # --- WYBÓR ROZKŁADU ---
        self.distributions = WidgetSelectionList(
            self,
            list_items=distributions_dict,
            widget_class=DistributionView,
        )
        self.distributions.grid(row=0, rowspan=2, column=0, sticky=NSEW)

        # --- ZBIÓR ZNAKÓW I DŁUGOŚĆ ---
        self.charset = CharsetEntry(self)
        self.charset.grid(column=1, row=0, sticky=NSEW, padx=5)

        params = ttk.Frame(self, style="Container.TFrame", padding=5)
        ttk.Label(params, text="długość:").grid(column=0, row=0)
        ttk.Entry(
            params,
            textvariable=self.controller.desired_length,
            width=10,
            validate="key",
            validatecommand=(self.register(validate_digit_input), "%S"),
        ).grid(column=1, row=0)
        params.grid(column=1, row=1, pady=(5, 0))

        # --- WYGENEROWANE ZBIORY ---
        self.local_list = WidgetSelectionList(
            self,
            widget_class=GeneratedRandomTextView,
            scrollable=VERTICAL,
            check_all=True,
        )
        self.local_list.grid(row=0, rowspan=2, column=2, sticky=NSEW)

        # --- PRZYCISKI ---
        buttons = ttk.Frame(self, style="Container.TFrame", padding=5)
        buttons.grid_columnconfigure([0, 1, 2], weight=1)
        ttk.Button(buttons, text="Importuj", command=self.__handle_import_file).grid(
            column=0, row=0
        )
        ttk.Button(buttons, text="Generuj", command=self.__handle_generate_sets).grid(
            column=1, row=0
        )
        ttk.Button(buttons, text="Zapisz", command=self.__handle_save_selected_sets).grid(
            column=2, row=0
        )
        buttons.grid(column=0, columnspan=3, row=2, pady=(5, 0), sticky=EW)

    def __handle_import_file(self):
        text_set = self.controller.import_text_set()
        if text_set:
            self.charset.value = bytes(text_set.charset.tolist())

            self.local_list.append(text_set)

    def __handle_generate_sets(self):
        sets = self.controller.generate_sets(self.charset.value, self.distributions.selected)  # type: ignore
        for text in sets:
            print(f"{id(text)=}")
            self.local_list.append(text)

    def __handle_save_selected_sets(self):
        for item in self.local_list.selected:
            self.append_main_list_clb(item)

        self.local_list.remove_selected()

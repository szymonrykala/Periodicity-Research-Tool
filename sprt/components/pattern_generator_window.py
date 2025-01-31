import re
from tkinter import EW, NSEW, VERTICAL, IntVar, filedialog, simpledialog, ttk
from typing import Callable, Optional

import numpy

from sprt.components import CharsetEntry, WidgetSelectionList
from sprt.components.top_level_abc import TopLevelABC
from sprt.logger import logger
from sprt.text_generator import Distribution
from sprt.text_generator import Generator as TextGenerator
from sprt.text_generator import RandomText, distributions_dict
from sprt.utils import validate_digit_input

from .distributionView import DistributionView
from .random_text_view import PatternTextView


class PatternParametersController:
    def __init__(self):
        self.repetitions_var = IntVar(value=3)
        self.sets_params_vars = {
            "od": IntVar(value=2),
            "do": IntVar(value=10),
            "krok": IntVar(value=1),
        }

    @property
    def repetitions(self):
        return self.repetitions_var.get()

    @property
    def patterns_range(self):
        return range(
            self.sets_params_vars["od"].get(),
            self.sets_params_vars["do"].get() + 1,
            self.sets_params_vars["krok"].get(),
        )


class PatternParameters(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="Container.TFrame", padding=5)
        self.grid_columnconfigure([0, 1, 2, 3, 4, 5], weight=1)
        self.grid_rowconfigure([0, 1, 2], weight=1)

        self.controller = PatternParametersController()

        ttk.Label(self, text="długość wzorców:").grid(row=0, column=0, columnspan=6, sticky="W")
        i = 0
        for name, var in self.controller.sets_params_vars.items():
            ttk.Label(self, text=name).grid(row=1, column=i, sticky="E")
            ttk.Entry(
                self,
                textvariable=var,
                validatecommand=(self.register(validate_digit_input), "%S"),
                validate="key",
                width=4,
            ).grid(row=1, column=i + 1, sticky="WE")
            i += 2

        ttk.Label(self, text="ilość powtórzeń:").grid(row=2, column=0, columnspan=4, sticky="W")
        ttk.Entry(
            self,
            textvariable=self.controller.repetitions_var,
            validatecommand=(self.register(validate_digit_input), "%S"),
            validate="key",
            width=3,
        ).grid(row=2, column=4, columnspan=2, sticky="WE")

    @property
    def patterns_range(self):
        return self.controller.patterns_range

    @property
    def repetitions(self):
        return self.controller.repetitions


class PatternGeneratorWindowController:
    def __init__(self):
        self._generator = TextGenerator()

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

    def generate_patterns(
        self,
        charset: str,
        distributions: tuple[Distribution],
        length_range: range,
        repeats: int,
    ):
        self._generator.char_set = charset

        patterns = []
        hashes = []
        for length in length_range:
            for _ in range(repeats):
                for dist in distributions:
                    p = self._generator.generate(size=length, distrib=dist)
                    p_hash = hash(p)
                    if p_hash not in hashes:
                        patterns.append(p)
                        hashes.append(p_hash)
        return patterns


class PatternGeneratorWindow(TopLevelABC):
    def __init__(self, append_main_list_clb: Callable[[RandomText], None]):
        super().__init__("Generowanie wzorców")
        self.minsize(700, 300)
        self.maxsize(900, 400)

        self.grid_columnconfigure([0, 1, 2, 3, 4], weight=1)
        self.grid_rowconfigure([0, 1], weight=1)

        self.append_main_list_clb = append_main_list_clb

        self.distributions = WidgetSelectionList(
            self,
            list_items=distributions_dict,
            widget_class=DistributionView,
        )
        self.distributions.grid(row=0, rowspan=2, column=0, sticky=NSEW)

        self.controller = PatternGeneratorWindowController()

        self.charset = CharsetEntry(self)
        self.charset.grid(column=1, columnspan=2, row=0, sticky=NSEW, padx=5)

        self.params = PatternParameters(self)
        self.params.grid(column=1, columnspan=2, row=1, sticky=NSEW, padx=5, pady=(5, 0))

        self.local_list = WidgetSelectionList(
            self,
            widget_class=PatternTextView,
            list_items=[],
            check_all=True,
            scrollable=VERTICAL,
        )
        self.local_list.grid(row=0, rowspan=2, column=3, columnspan=2, sticky=NSEW)

        buttons = ttk.Frame(self, style="Container.TFrame", padding=(0, 5))
        buttons.grid_columnconfigure([0, 1, 2], weight=1)
        ttk.Button(buttons, text="Wprowadź", command=self.__handle_manually_add_pattern).grid(
            column=0, row=0
        )
        ttk.Button(buttons, text="Generuj", command=self.__handle_generate_sets).grid(
            column=1, row=0
        )
        ttk.Button(buttons, text="Zapisz", command=self.__handle_save_selected_sets).grid(
            column=2, row=0
        )
        buttons.grid(column=0, columnspan=5, row=2, sticky=EW, pady=(5, 0))

    def __handle_generate_sets(self):
        sets = self.controller.generate_patterns(
            charset=self.charset.value,
            distributions=self.distributions.selected,  # type: ignore
            length_range=self.params.patterns_range,
            repeats=self.params.repetitions,
        )

        for pattern in sets:
            self.local_list.append(pattern)

    def __handle_save_selected_sets(self):
        for item in self.local_list.selected:
            self.append_main_list_clb(item)

        self.local_list.remove_selected()

    def __handle_manually_add_pattern(self):
        pattern = simpledialog.askstring("Wprowadzanie wzorca", "Wprowadź wzorzec: ", parent=self)
        if not pattern:
            return

        item: RandomText

        if re.match(r"^b'.*'$", pattern):
            item = RandomText.from_bytes(eval(pattern), name="użytkownik")

        else:
            item = RandomText.from_text(pattern, name="użytkownik")

        self.local_list.append(item)
        logger.info(f"user pattern added: '{pattern}'")

from threading import Thread
from tkinter import BOTH, EW, NSEW, VERTICAL, ttk
from typing import Optional

from sprt.algorithms import AlgorithmStore
from sprt.components import SelectionList, WidgetSelectionList
from sprt.db import pattern_db, text_db
from sprt.text_generator import RandomText

from .pattern_generator_window import PatternGeneratorWindow
from .random_text_view import GeneratedRandomTextView, PatternTextView
from .research_panel import ResearchPanel
from .text_set_generator_window import SetsGeneratorWindow


class MainController:
    def __init__(self):
        self.text_db = text_db
        self.pattern_db = pattern_db
        self.__opened_text_set_generator: Optional[SetsGeneratorWindow] = None
        self.__opened_pattern_generator: Optional[PatternGeneratorWindow] = None

    def async_load_patterns(self, patterns_list: WidgetSelectionList):
        def _job():
            self.pattern_db.get_all_async(patterns_list.append)

        Thread(target=_job).start()

    def async_load_text_sets(self, text_sets_list: WidgetSelectionList):
        def _job():
            self.text_db.get_all_async(text_sets_list.append)

        Thread(target=_job).start()

    def open_text_set_generator_window(self, text_sets: WidgetSelectionList):
        def _append_main_list(item: RandomText):
            self.text_db.insert(item)
            text_sets.append(item)

        if not self.__opened_text_set_generator:
            self.__opened_text_set_generator = SetsGeneratorWindow(_append_main_list)
        elif self.__opened_text_set_generator.winfo_exists():
            self.__opened_text_set_generator.focus()
        else:
            self.__opened_text_set_generator = None
            self.open_text_set_generator_window(text_sets)

    def open_pattern_generator_window(self, pattern_sets: WidgetSelectionList):
        def _append_main_list(item: RandomText):
            self.pattern_db.insert(item)
            pattern_sets.append(item)

        if not self.__opened_pattern_generator:
            self.__opened_pattern_generator = PatternGeneratorWindow(_append_main_list)
        elif self.__opened_pattern_generator.winfo_exists():
            self.__opened_pattern_generator.focus()
        else:
            self.__opened_pattern_generator = None
            self.open_pattern_generator_window(pattern_sets)


class MainWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="App.TFrame")
        self.configure(padding=5)
        self.grid_columnconfigure([0, 2], weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=2, pad=5)
        self.grid_rowconfigure(2, weight=1, pad=5)

        self.controller = MainController()

        # --- LISTA ZBIORÓW ---
        l1 = ttk.LabelFrame(self, text="Zapisane zbiory:")
        self.text_sets = WidgetSelectionList(
            l1,
            widget_class=GeneratedRandomTextView,
            scrollable=VERTICAL,
            check_all=True,
            remove_clb=self.controller.text_db.delete,
        )
        self.text_sets.pack(fill=BOTH, expand=True)
        l1.grid(column=0, row=0, sticky=NSEW, padx=(0, 5))

        # --- ALGORYTMY ---
        algorithm_store = AlgorithmStore()
        l2 = ttk.LabelFrame(self, text="Algorytmy:")
        self.algorithms = SelectionList(
            l2,
            list_items=algorithm_store.algorithms_dict,
            # single_select=True,
        )
        self.algorithms.pack(fill=BOTH, expand=True)
        l2.grid(column=1, row=0, sticky="NSEW", padx=(0, 5))

        # --- LISTA WZORCÓW ---
        l3 = ttk.LabelFrame(self, text="Zapisane wzorce:")
        self.patterns_set = WidgetSelectionList(
            l3,
            widget_class=PatternTextView,
            check_all=True,
            scrollable=VERTICAL,
            remove_clb=self.controller.pattern_db.delete,
        )
        self.patterns_set.pack(fill=BOTH, expand=True)
        l3.grid(row=0, column=2, sticky=NSEW)

        # --- PRZYCISKI ---
        buttons = ttk.Frame(self, style="Container.TFrame", padding=5)
        buttons.grid_columnconfigure([0, 2], weight=2)
        buttons.grid_columnconfigure(1, weight=1)

        ttk.Button(
            buttons, text="dodaj zbiory", command=self.__show_text_set_generator_window
        ).grid(column=0, row=0)
        ttk.Button(buttons, text="dodaj wzorce", command=self.__show_pattern_generator_window).grid(
            column=2, row=0
        )
        buttons.grid(column=0, columnspan=3, row=1, sticky=EW, pady=5)

        # --- PANEL BADAŃ ---
        self.research_panel = ResearchPanel(
            self,
            text_set_list=self.text_sets,
            patterns_list=self.patterns_set,
            algorithms_list=self.algorithms,
        )
        self.research_panel.grid(row=2, column=0, columnspan=5, sticky="NSEW", pady=(5, 0))

        self.controller.async_load_patterns(self.patterns_set)
        self.controller.async_load_text_sets(self.text_sets)

    def __show_text_set_generator_window(self):
        self.controller.open_text_set_generator_window(self.text_sets)

    def __show_pattern_generator_window(self):
        self.controller.open_pattern_generator_window(self.patterns_set)

from tkinter import HORIZONTAL, NSEW, ttk

from sprt.analysis import PeriodicityAnalysys
from sprt.components.selection_list import SelectionList, WidgetSelectionList

from .analysis_item_view import AnalysItemView


class ResearchPanelController:
    def __init__(
        self,
        text_set_list: WidgetSelectionList,
        patterns_list: WidgetSelectionList,
        algorithms_list: SelectionList,
        results_list: WidgetSelectionList,
    ):
        self._texts_list = text_set_list
        self._patterns_list = patterns_list
        self._algorithms_list = algorithms_list
        self._results_list = results_list

    def run_analysys(self):
        algorithm = self._algorithms_list.selected
        if algorithm:
            for text_set in self._texts_list.selected:
                analysys = PeriodicityAnalysys(
                    text_set=text_set,
                    algorithm=algorithm[0],
                    patterns=sorted(self._patterns_list.selected, key=self.__sort_patterns),
                )
                analysys.run()
                self._results_list.append(analysys)

    def run_performance_measure(self):
        raise NotImplementedError("ResearchPanelController.run_performance_measure needs to be implemented")

    def delete_selected(self):
        self._results_list.remove_selected()

    def __sort_patterns(self, a):
        return a.length


class ResearchPanel(ttk.LabelFrame):
    def __init__(
        self,
        master,
        text_set_list: WidgetSelectionList,
        patterns_list: WidgetSelectionList,
        algorithms_list: SelectionList,
    ):
        super().__init__(master, text="Panel badań:")
        self.grid_columnconfigure([1, 2], weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buttons_frame = ttk.Frame(self, padding=5, style="Container.TFrame")
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_rowconfigure([0, 1, 2], weight=1)
        self.buttons_frame.grid(column=0, row=0, sticky=NSEW, padx=(0, 5))

        self.results_list = WidgetSelectionList(self, AnalysItemView, scrollable=HORIZONTAL, check_all=True)
        self.results_list.grid(column=1, columnspan=2, row=0, sticky=NSEW)

        self.controller = ResearchPanelController(text_set_list, patterns_list, algorithms_list, self.results_list)

        self.__mount_buttons()

    def __mount_buttons(self):
        ttk.Button(
            self.buttons_frame,
            text="Badaj wybrane",
            command=self.controller.run_analysys,
        ).grid(column=0, row=0, sticky=NSEW, pady=(0, 5))

        ttk.Button(
            self.buttons_frame,
            text="Wydajność",
            command=self.controller.run_performance_measure,
        ).grid(column=0, row=1, sticky=NSEW, pady=(0, 5))

        ttk.Button(
            self.buttons_frame,
            text="usuń wybrane",
            command=self.controller.delete_selected,
        ).grid(column=0, row=2, sticky=NSEW)

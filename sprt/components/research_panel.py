from threading import Thread
from tkinter import HORIZONTAL, NSEW, messagebox, ttk

from sprt.analysis import PeriodicityAnalysis
from sprt.analysis.time_measure import TimeMeasurement
from sprt.components.performance_result_window import PerformanceResultWindow
from sprt.components.selection_list import SelectionList, WidgetSelectionList

from .analysis_item_view import AnalysisItemView
from .progress_window import ProgressWindow


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

        self.__window = None

    def __all_present(self) -> bool:
        return all(
            map(
                len,
                [
                    self._algorithms_list.selected,
                    self._texts_list.selected,
                    self._patterns_list.selected,
                ],
            )
        )

    def run_analysis(self):
        algorithm = self._algorithms_list.selected

        if not self.__all_present():
            messagebox.showinfo(message="Wybierz co najmniej jeden wzorzec, zbiór i algorytm.")
            return

        for text_set in self._texts_list.selected:
            analysis = PeriodicityAnalysis(
                text_set=text_set,
                algorithm=algorithm[0],
                patterns=sorted(self._patterns_list.selected, key=self.__sort_patterns),
            )
            analysis.run_async()
            self._results_list.append(analysis)

    def run_performance_measure(self):
        if self.__window and self.__window.winfo_exists():
            self.__window.focus()
            return
        else:
            self.__window = None

        if not self.__all_present():
            messagebox.showinfo(message="Wybierz co najmniej jeden wzorzec, zbiór i algorytm.")
            return

        measurement = TimeMeasurement(
            algorithms=self._algorithms_list.selected,
            text_sets=self._texts_list.selected,
            patterns=self._patterns_list.selected,
        )
        box = ProgressWindow(measurement.message)
        box.update()
        measurement.ready.trace_add("write", lambda *_: box.winfo_exists() and box.stop())
        measurement.ready.trace_add(
            "write", lambda *_: self._on_performance_measure_finish(measurement, box)
        )
        Thread(target=measurement.run).start()

    def _on_performance_measure_finish(self, measurement: TimeMeasurement, box: ProgressWindow):
        if not measurement.ready.get() or not measurement.results:
            return
        box.destroy()
        del box

        self.__window = PerformanceResultWindow(measurement.results)

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

        self.results_list = WidgetSelectionList(
            self, AnalysisItemView, scrollable=HORIZONTAL, check_all=True
        )
        self.results_list.grid(column=1, columnspan=2, row=0, sticky=NSEW)

        self.controller = ResearchPanelController(
            text_set_list, patterns_list, algorithms_list, self.results_list
        )

        self.__mount_buttons()

    def __mount_buttons(self):
        ttk.Button(
            self.buttons_frame,
            text="Badaj wybrane",
            command=self.controller.run_analysis,
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

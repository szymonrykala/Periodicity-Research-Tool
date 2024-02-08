from tkinter import X, ttk
from typing import Optional

from sprt.analysis.analysis import PeriodicityAnalysys
from sprt.components import SelectableWidget
from sprt.components.analysis_window import AnalysisWindow


class AnalysItemView(SelectableWidget):
    def _set_up(self, item: PeriodicityAnalysys):
        self.item = item
        self.__opened: Optional[AnalysisWindow] = None

        self.configure(padding=5)

        self.checkbox.pack(fill=X)
        self.checkbox.configure(text=item.name)

        ttk.Label(self, text=f"alg: {item.algorithm}", padding=(5, 5, 5, 0)).pack(fill=X)
        ttk.Label(self, text=f"ilość wzorców: {item.patterns_count}", padding=(5, 0, 5, 0)).pack(fill=X)
        self.__state_label = ttk.Label(self, text="przetwarzanie", foreground="red", padding=(5, 0, 5, 5))
        self.button = ttk.Button(self, text="Otwórz", command=self.__handle_open, state="disabled", padding=0)

        ttk.Separator(self).pack(fill=X)
        self.__state_label.pack(fill=X, ipadx=5)
        self.button.pack(expand=True, anchor="center")

        if self.item.ready.get():
            self.__set_ready()
        else:
            self.__state_tracing_clb = item.ready.trace_add("write", self.__set_ready)

    @property
    def value(self):
        if self.checkbox.value:
            return self.item

    def __handle_open(self):
        if not self.__opened:
            self.__opened = AnalysisWindow(self, self.item)
        elif self.__opened.winfo_exists():
            self.__opened.focus()
        else:
            self.__opened = None
            self.__handle_open()

    def __set_ready(self, *_):
        self.__state_label.configure(text="gotowe", foreground="green")
        self.button.configure(state="enabled")
        self.item.ready.trace_remove("write", self.__state_tracing_clb)

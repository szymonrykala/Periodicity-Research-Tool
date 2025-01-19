from tkinter import StringVar, X, ttk

from .top_level_abc import TopLevelABC


class ProgressWindow(TopLevelABC):
    def __init__(self, string_var=None):
        super().__init__(title="", width=250, height=170)
        self.wait_visibility()
        self.grab_set()

        self._text = string_var or StringVar(value="Proszę czekać.")

        self.label = ttk.Label(self, textvariable=self.text, padding=5)
        self.label.pack(fill=X)
        self.label.bind("<Configure>", self.__resize_label)

        self.progress_bar = ttk.Progressbar(
            self, orient="horizontal", length=300, mode="indeterminate"
        )
        self.progress_bar.pack(fill=X, pady=10)
        self.btn = ttk.Button(self, text="Zamknij", state="disabled", command=self.destroy)
        self.btn.pack()
        self.start()

    @property
    def text(self):
        return self._text

    def __resize_label(self, event):
        self.label.configure(wraplength=event.width)

    def start(self):
        self.progress_bar.start(10)

    def stop(self):
        self.progress_bar.stop()
        self.btn.configure(state="normal")

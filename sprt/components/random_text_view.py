from threading import Thread
from tkinter import simpledialog, ttk
from typing import Optional

from PIL import Image, ImageTk

from sprt.components import SelectableWidget
from sprt.components.text_set_lookup_window import TextSetWindow
from sprt.config import STATIC_DIR
from sprt.db import text_db
from sprt.logger import logger
from sprt.text_generator import RandomText

_ICON_SIZE = 17

_eye_icon = Image.open(STATIC_DIR + "eye.png").resize((_ICON_SIZE + round(_ICON_SIZE / 4), _ICON_SIZE))
_edit_icon = Image.open(STATIC_DIR + "edit.png").resize((_ICON_SIZE, _ICON_SIZE))


class PatternTextView(SelectableWidget):
    def _set_up(self, item: RandomText):
        self.pattern = item
        self._eye_icon = ImageTk.PhotoImage(_eye_icon)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox.configure(text=f"{item.name}; l={item.length}")
        self.checkbox.grid(row=0, column=0, sticky="w")

        l = ttk.Label(
            self,
            cursor="hand",
            image=self._eye_icon,
        )
        l.grid(row=0, column=1, sticky="e", padx=(5, 5))
        l.bind("<Button-1>", lambda _: TextSetWindow(item))

    @property
    def value(self) -> Optional[RandomText]:
        if self.checkbox.value:
            return self.pattern


class GeneratedRandomTextView(SelectableWidget):
    def _set_up(self, item: RandomText):
        self._random_text = item
        self._eye_icon = ImageTk.PhotoImage(_eye_icon)
        self._edit_icon = ImageTk.PhotoImage(_edit_icon)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0, 1], weight=1)

        self.checkbox.configure(text=self._random_text.name)
        self.checkbox.grid(row=0, column=0, sticky="w")

        name_edit = ttk.Label(
            self,
            cursor="hand",
            image=self._edit_icon,
        )
        name_edit.grid(row=0, column=1, sticky="e", padx=(0, 7))
        name_edit.bind("<Button-1>", self.__handle_name_change)

        lookup = ttk.Label(
            self,
            cursor="hand",
            image=self._eye_icon,
        )
        lookup.grid(row=0, column=2, sticky="e")
        lookup.bind("<Button-1>", lambda _: TextSetWindow(self._random_text))

        ttk.Label(
            self,
            text=f"l={self._random_text.length}; mean={self._random_text.mean}; stdev={self._random_text.stdev}",
            font=(15,),
        ).grid(row=1, column=0, columnspan=3, sticky="w")

    @property
    def value(self) -> Optional[RandomText]:
        if self.checkbox.value:
            return self._random_text

    def __handle_name_change(self, _):
        new_name = simpledialog.askstring("Zmiana nazwy", "Podaj nową nazwę: ")
        if not new_name:
            return
        logger.info(f"Updating name of {self._random_text.name}, {self._random_text.id}")
        self._random_text.name = new_name
        self.checkbox.configure(text=new_name)

        Thread(target=text_db.update, args=(self._random_text,)).start()

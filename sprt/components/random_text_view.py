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

_EYE_ICON = Image.open(STATIC_DIR.joinpath("eye.png")).resize(
    (_ICON_SIZE + round(_ICON_SIZE / 4), _ICON_SIZE)
)
_EDIT_ICON = Image.open(STATIC_DIR.joinpath("edit.png")).resize((_ICON_SIZE, _ICON_SIZE))


class PatternTextView(SelectableWidget):
    def _set_up(self, item: RandomText):
        self.configure(style="ListItem.TFrame")

        self.pattern = item
        self._eye_icon = ImageTk.PhotoImage(_EYE_ICON)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox.configure(text=f"l={item.length}; {self.pattern.parsed_text}")
        self.checkbox.grid(row=0, column=0, sticky="we")

        self.eye_icon_label = ttk.Label(
            self,
            cursor="hand",
            image=self._eye_icon,
        )
        self.eye_icon_label.grid(row=0, column=1, sticky="e", padx=(5, 5))
        self.eye_icon_label.bind("<Button-1>", lambda _: TextSetWindow(item))

    @property
    def value(self) -> Optional[RandomText]:
        if self.checkbox.value:
            return self.pattern

    def _on_select(self):
        super()._on_select()
        self.configure(style="Selected.ListItem.TFrame")
        self.eye_icon_label.configure(style="Selected.ListItem.TLabel")

    def _on_deselect(self):
        super()._on_deselect()
        self.eye_icon_label.configure(style="TLabel")


class GeneratedRandomTextView(SelectableWidget):
    def _set_up(self, item: RandomText):
        self.configure(style="ListItem.TFrame")

        self._random_text = item
        self._eye_icon = ImageTk.PhotoImage(_EYE_ICON)
        self._edit_icon = ImageTk.PhotoImage(_EDIT_ICON)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0, 1], weight=1)

        self.checkbox.configure(text=self._random_text.name)
        self.checkbox.grid(row=0, column=0, sticky="WE")

        self.name_edit_icon = ttk.Label(
            self,
            cursor="hand",
            image=self._edit_icon,
            compound="image",
        )
        self.name_edit_icon.grid(
            row=0,
            column=1,
            sticky="e",
        )
        self.name_edit_icon.bind("<Button-1>", self.__handle_name_change)

        self.eye_icon = ttk.Label(self, cursor="hand", image=self._eye_icon, compound="image")
        self.eye_icon.grid(row=0, column=2, sticky="e", padx=5)
        self.eye_icon.bind("<Button-1>", lambda _: TextSetWindow(self._random_text))

        self.params_label = ttk.Label(
            self,
            text=f"l={self._random_text.length}; mean={self._random_text.mean}; stdev={self._random_text.stdev}",
            font=(15,),
        )
        self.params_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=5)

    @property
    def value(self) -> Optional[RandomText]:
        if self.checkbox.value:
            return self._random_text

    def _on_select(self):
        super()._on_select()
        for widget in (self, self.eye_icon, self.params_label, self.name_edit_icon):
            widget.configure(style="Selected.ListItem.TLabel")

    def _on_deselect(self):
        super()._on_deselect()
        for label in (self.eye_icon, self.params_label, self.name_edit_icon):
            label.configure(style="TLabel")

    def __handle_name_change(self, _):
        new_name = simpledialog.askstring("Zmiana nazwy", "Podaj nową nazwę: ")
        if not new_name:
            return
        logger.info(f"Updating name of {self._random_text.name}, {self._random_text.id}")
        self._random_text.name = new_name
        self.checkbox.configure(text=new_name)

        Thread(target=text_db.update, args=(self._random_text,)).start()

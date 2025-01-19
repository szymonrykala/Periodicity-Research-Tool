from abc import ABC, abstractmethod
from tkinter import BOTH, HORIZONTAL, LEFT, E, N, S, W, Widget, X, Y, ttk
from typing import Any, Callable, Optional

from sprt.logger import logger

from .checkbox import Checkbox
from .scrollable_frame import ScrollableFrame

_PADDING = (0, 4)


class SelectableWidget(ABC, ttk.Frame):
    def __init__(self, master, text: str, item: Any, **kwargs):
        opt = {
            "padding": 3,
        }
        opt.update(**kwargs)
        super().__init__(master, **opt)
        self._checkbox = Checkbox(
            self, text=text, onvalue=item, offvalue=None, command=self.__handle_toggle
        )
        self._set_up(item)
        self.__initial_style = self.cget("style")

    @property
    def checkbox(self):
        return self._checkbox

    @property
    def value(self):
        raise NotImplementedError()

    def __handle_toggle(self):
        if self.checkbox.value:
            self._on_select()  # update of checkibox is first
        else:
            self._on_deselect()

    def _on_select(self): ...

    def _on_deselect(self):
        self.configure(style=self.__initial_style)  # revert the style

    def select(self):
        return self.checkbox.select()

    def deselect(self):
        return self.checkbox.deselect()

    @abstractmethod
    def _set_up(self, item: Any): ...


class SelectionListController:
    def __init__(self, checkboxes: list[Checkbox | SelectableWidget]):
        self.items: list[Checkbox | SelectableWidget] = checkboxes
        self._old_selected = 0

        if self.items:
            self.items[self._old_selected].select()

    def assert_single_select(self):
        newly_selected = self._old_selected
        for i, item in enumerate(self.items):
            if item.value and i != self._old_selected:
                newly_selected = i
                break

        if newly_selected != self._old_selected:
            logger.debug("selection list change detected")
            self.items[self._old_selected].deselect()
            self._old_selected = newly_selected


class SelectionList(ttk.Frame):
    def __init__(
        self,
        master,
        scrollable: Optional[str] = None,
        list_items: list | dict[str, Any] = [],
        single_select: bool = False,
        **kwargs,
    ):
        """
        sroclable=HORIZONTAL|VERTICAL
        """

        if "remove_clb" in kwargs:
            self.__remove_clb: Callable[[Any], None] = kwargs["remove_clb"]
            del kwargs["remove_clb"]
        else:
            self.__remove_clb = lambda x: None

        options = {
            "style": "Container.TFrame",
            "padding": 10,
        }
        options.update(**kwargs)
        super().__init__(master, **options)

        self.__empty_label: Optional[Widget] = None
        self.__single_select = single_select
        self.__selected_last: Optional[Checkbox | SelectableWidget] = None

        self.scroll_direction = scrollable
        if scrollable:
            scroll = ScrollableFrame(self, scrollable, style="Container.TFrame")
            self._container = ttk.Frame(scroll.inner_frame, style="Container.TFrame")
            self._container.pack(fill=BOTH, expand=True)
            scroll.pack(fill=BOTH, expand=True)
        else:
            self._container = ttk.Frame(self, style="Container.TFrame")
            self._container.pack(fill=BOTH, expand=True, anchor=N)

        self.controller = SelectionListController([])

        self.__mount_empty_label()
        self._mount_items(list_items)

    @property
    def selected(self) -> tuple[Any, ...]:
        return tuple(w.value for w in self._container.pack_slaves() if w.value)  # type: ignore

    def __mount_empty_label(self):
        if not self.__empty_label:
            self.__empty_label = ttk.Label(self, text="brak ...")
            self.__empty_label.pack(fill=X, side="top", before=self._container)

    def _single_select_clb(self):
        if self.__selected_last is not None:
            self.__selected_last.deselect()

        for widget in self._container.pack_slaves():
            if widget.value:
                self.__selected_last = widget

    def _mount_items(self, list_items: list | dict[str, Any]):
        if isinstance(list_items, list):
            for item in list_items:
                self.append(item)
        elif isinstance(list_items, dict):
            for name, item in list_items.items():
                self.append(item, name=name)

    def _append(self, item: Any, name: str):
        c = Checkbox(self._container, text=name, onvalue=item, offvalue=None)

        if self.__single_select:
            c.configure(command=self._single_select_clb)

        c.pack(fill=X, expand=True, anchor="n", pady=2)

    def append(self, item: Any, name: str = "usnet"):
        if self.__empty_label:
            self.__empty_label.pack_forget()
            self.__empty_label = None

        self._append(item, name=name)

    def remove_selected(self):
        for widget in self._container.pack_slaves():
            if widget.value:
                self.__remove_clb(widget.value)

                widget.pack_forget()
                widget.destroy()
                del widget

        if not self._container.pack_slaves():
            self.__mount_empty_label()


class WidgetSelectionList(SelectionList):
    def __init__(
        self,
        master,
        widget_class: type[SelectableWidget],
        list_items: list | dict[str, Any] = [],
        check_all: bool = False,
        scrollable: Optional[str] = None,
        **kwargs,
    ):
        """
        scrollable=HORIZONTAL|VERTICAL
        """
        self.__widget_class = widget_class
        self.select_all_check = None
        super().__init__(
            master,
            list_items=list_items,
            single_select=False,
            scrollable=scrollable,
            **kwargs,
        )

        if check_all:
            controls = ttk.Frame(self, style="Container.TFrame")
            controls.grid_columnconfigure([0, 1], weight=1)
            controls.grid_rowconfigure(0, weight=1)
            self.select_all_check = Checkbox(
                controls,
                text="zaznacz wszystkie",
                command=self.__handle_check_all,
                padding=_PADDING,
                style="Secondary.TCheckbutton",
            )
            ttk.Button(
                controls,
                text="usuń",
                command=self.remove_selected,
                style="Secondary.TButton",
                padding=0,
                width=8,
                cursor="hand",
            ).grid(column=1, row=0, sticky=E)
            self.select_all_check.grid(column=0, row=0, sticky=W)
            controls.pack(fill=X, anchor=S)

    def __handle_check_all(self):
        if self.select_all_check.value:
            for checkbox_widget in self._container.pack_slaves():
                checkbox_widget.select()
        else:
            for checkbox_widget in self._container.pack_slaves():
                checkbox_widget.deselect()

    def _append(self, item: Any, name: str):
        w = self.__widget_class(master=self._container, text=name, item=item, padding=_PADDING)

        if self.select_all_check and self.select_all_check.value:
            w.select()

        self.controller.items.append(w)

        if self.scroll_direction == HORIZONTAL:
            w.pack(fill=Y, expand=True, side=LEFT, anchor="w", padx=2)
        else:
            w.pack(fill=X, expand=True, anchor="n", pady=2)

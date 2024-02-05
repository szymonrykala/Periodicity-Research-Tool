from abc import abstractmethod
from tkinter import BOTH, HORIZONTAL, LEFT, SW, N, Widget, X, Y, ttk
from typing import Any, Optional

from sprt.logger import logger

from .checkbox import Checkbox
from .scrollable_frame import ScrollableFrame

_PADDING = (0, 4)


class SelectableWidget(ttk.Frame):
    def __init__(self, master, text: str, item: Any, **kwargs):
        super().__init__(master, **kwargs)
        self._checkbox = Checkbox(self, text=text, onvalue=item, offvalue=None)
        self._set_up(item)

    @property
    def checkbox(self):
        return self._checkbox

    @property
    def value(self):
        raise NotImplementedError()

    def select(self):
        return self.checkbox.select()

    def deselect(self):
        return self.checkbox.deselect()

    @abstractmethod
    def _set_up(self, item: Any):
        ...


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
        super().__init__(master, **kwargs)

        self.__empty_label: Optional[Widget] = None
        self.__single_select = single_select
        self.__selected_last: Optional[Checkbox | SelectableWidget] = None

        self.scroll_direction = scrollable
        if scrollable:
            scroll = ScrollableFrame(self, scrollable)
            self._container = ttk.Frame(scroll.inner_frame)
            self._container.pack(fill=BOTH, expand=True)
            scroll.pack(fill=BOTH, expand=True)
        else:
            self._container = ttk.Frame(self)
            self._container.pack(fill=BOTH, expand=True, anchor=N)

        self.controller = SelectionListController([])

        self.__mount_empty_label()
        self._mount_items(list_items)

    @property
    def selected(self) -> tuple[Any, ...]:
        return tuple(w.value for w in self._container.pack_slaves() if w.value)  # type: ignore

    def __mount_empty_label(self):
        if not self.__empty_label:
            self.__empty_label = ttk.Label(self, text="brak zbiorów ...")
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
        c.configure(padding=_PADDING)

        if self.__single_select:
            c.configure(command=self._single_select_clb)

        c.pack(fill=X, expand=True, anchor="n")

    def append(self, item: Any, name: str = "usnet"):
        if self.__empty_label:
            self.__empty_label.pack_forget()
            self.__empty_label = None

        self._append(item, name=name)

    def remove_selected(self):
        for widget in self._container.pack_slaves():
            if widget.value:
                widget.pack_forget()
                widget.destroy()

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
        sroclable=HORIZONTAL|VERTICAL
        """
        self.__widget_class = widget_class
        super().__init__(
            master,
            list_items=list_items,
            single_select=False,
            scrollable=scrollable,
            **kwargs,
        )

        if check_all:
            self.__all_checked = False
            self.select_all_check = Checkbox(
                self,
                text="zaznacz wszystkie",
                command=self.__handle_check_all,
                padding=_PADDING,
            )
            self.select_all_check.pack(fill=X, anchor=SW)

    def __handle_check_all(self):
        self.__all_checked = not self.__all_checked

        if self.__all_checked is True:
            for chckbox_widget in self._container.pack_slaves():
                chckbox_widget.select()
        else:
            for chckbox_widget in self._container.pack_slaves():
                chckbox_widget.deselect()

    def _append(self, item: Any, name: str):
        w = self.__widget_class(master=self._container, text=name, item=item, padding=_PADDING)
        self.controller.items.append(w)

        if self.scroll_direction == HORIZONTAL:
            w.pack(fill=Y, expand=True, side=LEFT, anchor="w")
        else:
            w.pack(fill=X, expand=True, anchor="n")

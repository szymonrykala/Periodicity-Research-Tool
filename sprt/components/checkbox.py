from tkinter import IntVar, ttk


class Checkbox(ttk.Checkbutton):
    def __init__(self, master, onvalue: object = True, offvalue=None, **kwargs):
        self.__var = IntVar(value=0)
        self.__on_value = onvalue
        self.__off_value = offvalue
        self.__command = kwargs.get("command", lambda: None)
        kwargs.update(variable=self.__var, cursor="hand")

        super().__init__(master, **kwargs)

    @property
    def value(self):
        if bool(self.__var.get()):
            return self.__on_value
        return self.__off_value

    def select(self):
        self.__var.set(1)
        self.__command()
        # self.invoke()

    def deselect(self):
        self.__var.set(0)
        self.__command()
        # self.invoke()

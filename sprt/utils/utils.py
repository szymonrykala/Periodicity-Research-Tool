from tkinter import Toplevel

from numpy import ndarray


def bytes_to_str(value: list | ndarray | str) -> str:
    if isinstance(value, ndarray):
        value = value.tolist()
    elif isinstance(value, str):
        return value

    b = bytes(value)  # type: ignore
    try:
        return b.decode(errors="strict")
    except UnicodeDecodeError:
        return str(b)


def validate_digit(value: str):
    return value.isdigit() or value in "."


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        if issubclass(cls, Toplevel):
            cls._instances[cls].focus()

        return cls._instances[cls]

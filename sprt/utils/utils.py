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


def validate_digit_input(value: str) -> bool:
    return value.isdigit() or value in "."

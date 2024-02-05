import sys
from logging import Formatter, StreamHandler, getLogger

from sprt import config


def get_logger(name: str = config.LOGGER_NAME):
    logger = getLogger(name)

    h = StreamHandler(sys.stdout)
    f = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    h.setFormatter(f)
    logger.addHandler(h)

    logger.setLevel(config.LOGGING_LEVEL)

    return logger


logger = get_logger()

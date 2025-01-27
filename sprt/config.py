import string
from logging import getLevelNamesMapping
from pathlib import Path

from matplotlib import use

from sprt.utils import get_env

use("TkAgg")


LOGGER_NAME = get_env("LOGGER_NAME", "SPRT")
LOGGING_LEVEL = getLevelNamesMapping()[get_env("LOGGING_LEVEL", "INFO").upper()]
DEFAULT_CHARSET = get_env("DEFAULT_CHARSET", string.ascii_letters + string.digits)
SINGLE_CHAR_SAMPLES_COUNT = get_env("SINGLE_CHAR_SAMPLES_COUNT", 200)

# seconds
TIME_MEASURE_MEAN_COUNT = get_env("TIME_MEASURE_MEAN_COUNT", 5)
ENV_STABLE_WAIT_TIME = get_env("ENV_STABLE_WAIT_TIME", 30)
ENV_TIME_DEVIATION_THRESHOLD = get_env("ENV_TIME_DEVIATION_THRESHOLD", 0.005)
ENV_TIME_DEVIATION_REPEATS = get_env("ENV_TIME_DEVIATION_REPEATS", 5)

cwd = Path(__file__).parent

DB_FILE = get_env("DB_FILE", "/tmp/sprt_database.sqlite")
STATIC_DIR = cwd.joinpath("static")

DISPLAY_TREND_LINES = get_env("DISPLAY_TREND_LINES", False)

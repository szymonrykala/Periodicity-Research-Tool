import string
from logging import DEBUG, INFO
from pathlib import Path

from matplotlib import use

use("TkAgg")

LOGGER_NAME = "SPRT"
LOGGING_LEVEL = INFO
DEFAULT_CHARSET = string.ascii_letters + string.digits
SINGLE_CHAR_SAMPLES_COUNT = 200

# seconds
TIME_MEASURE_MEAN_COUNT = 5
ENV_STABLE_WAIT_TIME = 30
ENV_TIME_DEVIATION_THRESHOLD = 0.005
ENV_TIME_DEVIATION_REPEATS = 5

cwd = Path(__file__).parent

DB_FILE = "/tmp/sprt_database.sqlite"
STATIC_DIR = cwd.joinpath("static")

DISPLAY_TREND_LINES = False

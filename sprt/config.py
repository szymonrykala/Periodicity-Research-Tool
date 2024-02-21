import string
from logging import DEBUG, INFO

from matplotlib import use

use("TkAgg")

LOGGER_NAME = "SPRT"
LOGGING_LEVEL = INFO
DEFAULT_CHARSET = string.ascii_letters + string.digits
SINGLE_CHAR_SAMPLES_COUNT = 30
RANDOM_GENERATOR_SEED = 1

TIME_MEASURE_MEAN_COUNT = 5
ENV_STABLE_WAIT_TIME = 30  # seconds
ENV_TIME_DEVIATION_THRESHOLD = 0.0015

DB_FILE = "sprt/static/prt_database.db"
STATIC_DIR = "sprt/static/"

DISPLAY_TREND_LINES = False

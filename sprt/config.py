import string
from logging import DEBUG

from matplotlib import use

use("TkAgg")

LOGGER_NAME = "SPRT"
LOGGING_LEVEL = DEBUG
DEFAULT_CHARSET = string.ascii_letters + string.digits
SINGLE_CHAR_SAMPLES_COUNT = 30
RANDOM_GENERATOR_SEED = 1

DB_FILE = "sprt/static/prt_database.db"
STATIC_DIR = "sprt/static/"

import pkgutil
from configparser import ConfigParser


def load_config():
    cfp = ConfigParser()
    cfp.read_string(pkgutil.get_data("quotesbot", "config.ini").decode("utf-8"))
    return cfp


config = load_config()

DB_TEST_HOST = config.get("DB", "HOST")
DB_TEST_PORT = config.getint("DB", "PORT")
DB_TEST_USER = config.get("DB", "USER")
DB_TEST_PASS = config.get("DB", "PASS")

VLAD_PERSONAL_DB_HOST = config.get("VLAD_DB", "HOST")
VLAD_PERSONAL_DB_PORT = config.getint("VLAD_DB", "PORT")
VLAD_PERSONAL_DB_NAME = config.get("VLAD_DB", "NAME")
VLAD_PERSONAL_DB_USER = config.get("VLAD_DB", "USER")
VLAD_PERSONAL_DB_PASS = config.get("VLAD_DB", "PASS")


BOT_TOKEN = config.get("TELEGRAM", "TOKEN")
CHAT_ID = config.getint("TELEGRAM", "CHAT_ID")


DB_CONNECTION_INFO = (
    f"postgresql+psycopg2://{DB_TEST_USER}:"
    f"{DB_TEST_PASS}@{DB_TEST_HOST}:"
    f"{DB_TEST_PORT}/parsers"
)

HASH_DB_CONNECTION_INFO = (
    f"postgresql+psycopg2://{DB_TEST_USER}:"
    f"{DB_TEST_PASS}@{DB_TEST_HOST}:"
    f"{DB_TEST_PORT}/yandex-market-prices"
)

VLAD_PERSONAL_CONNECTION_INFO = (
    f"mysql+pymysql://{VLAD_PERSONAL_DB_USER}:"
    f"{VLAD_PERSONAL_DB_PASS}@{VLAD_PERSONAL_DB_HOST}:"
    f"{VLAD_PERSONAL_DB_PORT}/{VLAD_PERSONAL_DB_NAME}"
)

import utils
import pathlib


secrets=utils.load_secrets()
DB_PATH=pathlib.Path(__file__).absolute().parent.parent.joinpath("db").joinpath("mydb.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
NEWS_API_URL="https://newsapi.org/v2/everything"
STABILITYKEY="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"
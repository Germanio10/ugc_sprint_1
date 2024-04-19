import logging
import sys
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("etl_mongo")
logger.setLevel(logging.INFO)

fh = RotatingFileHandler("logs/etl_logs.log", maxBytes=20_000_000, backupCount=5)
sh = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)

fh.setFormatter(formatter)
sh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(sh)

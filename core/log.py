import logging
from pathlib import Path
from settings import APP_ENV
from logging.handlers import RotatingFileHandler

log_dir = "storage/logs"
Path(log_dir).mkdir(parents=True, exist_ok=True)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(f"{log_dir}/app.log", maxBytes=5_000_000, backupCount=5)
file_handler.setFormatter(formatter)

class AppOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.name.startswith("app")

file_handler.addFilter(AppOnlyFilter())

level = logging.WARNING if APP_ENV == "production" else logging.DEBUG
logging.basicConfig(level=level, handlers=[stream_handler, file_handler])

logger = logging.getLogger("app")

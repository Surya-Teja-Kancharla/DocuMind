import logging
from pathlib import Path

LOG_DIR = Path("backend/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def setup_logger():
    logger = logging.getLogger("documind")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Console logging (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File logging
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

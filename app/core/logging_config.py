import logging
import sys
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

def setup_logging():
    # 1. Create a custom logger
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    # 2. Create formatters (The 'output template')
    # This looks like: 2023-10-27 10:00:00 - INFO - main.py - Message
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # 3. Create a File Handler (Like a Serilog Sink)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    # 4. Create a Console Handler (So you still see logs in the terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 5. Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Initialize it
logger = setup_logging()
Logging setup
import logging
import sys

def setup_logging(debug: bool = False, log_file: str = None):
    level = logging.DEBUG if debug else logging.INFO
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(level=level, format="%(message)s", handlers=handlers)

def get_logger(name: str):
    return logging.getLogger(name)

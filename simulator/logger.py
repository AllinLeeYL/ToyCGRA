import logging, sys

formatter = logging.Formatter("%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

class LevelFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    Rather than use actual contextual information, we just use random
    data in this demo.
    """

    def __init__(self, name: str = "", level: int = logging.WARNING) -> None:
        super().__init__(name)
        self.level = level

    def filter(self, record):
        if record.levelno < self.level:
            return False
        else:
            return True

def setup_logger(filename: str, log_level: int = logging.DEBUG):
    logger.setLevel(logging.DEBUG)
    # stream
    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(formatter)
    stream.setLevel(logging.INFO)
    logger.addHandler(stream)
    # file
    file = logging.FileHandler(filename, mode='w', encoding='utf-8')
    file.setLevel(log_level)
    file.setFormatter(formatter)
    logger.addHandler(file)
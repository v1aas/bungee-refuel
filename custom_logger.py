import logging
from colorlog import ColoredFormatter

class CustomLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        logging.addLevelName(25, "SUCCESS")

    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(25):
            self._log(25, msg, args, **kwargs)

logging.setLoggerClass(CustomLogger)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_format = (
    "%(asctime)s:%(levelname)s:%(message)s"
)
colored_formatter = ColoredFormatter(
    "%(log_color)s" + log_format,
    datefmt='%H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'white',
        'SUCCESS': 'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(colored_formatter)
logger.addHandler(stream_handler)
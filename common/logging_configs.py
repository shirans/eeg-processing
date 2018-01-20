from logging.config import dictConfig
import coloredlogs, logging

DEFAULT_CONFIGS = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'f': {'format':
                  '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
              'datefmt': '%H:%M:%S',
              }
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
    },
    root={
        'handlers': ['h'],
        'level': logging.WARN,
    },
)
coloredlogs.install(level='DEBUG')
coloredlogs.install(level='INFO')


def getMyLogger(name):
    dictConfig(DEFAULT_CONFIGS)
    get_logger = logging.getLogger(name)
    get_logger.setLevel(level=logging.INFO)
    return get_logger

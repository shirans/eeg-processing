import logging
from logging.config import dictConfig

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
        'level': logging.DEBUG,
    },
)


def getMyLogger(name):
    dictConfig(DEFAULT_CONFIGS)
    return logging.getLogger(name)
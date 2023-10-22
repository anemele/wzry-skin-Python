import logging.config

import rtoml

from .constants import FILE_LOGGER_CONFIG

with open(FILE_LOGGER_CONFIG, 'r') as fp:
    logging.config.dictConfig(rtoml.load(fp))
logger = logging.getLogger('log')

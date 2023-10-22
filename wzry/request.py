import requests

from .constants import DEFAULT_TIMEOUT, HEADERS
from .logger import logger

_session = requests.Session()


def get(url: str):
    logger.info(f'Get {url}')
    res = _session.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    return res

import requests
from fake_useragent import FakeUserAgent

DEFAULT_TIMEOUT = 5

_session = requests.Session()
_session.headers.update(
    {
        'User-Agent': FakeUserAgent().random,
        'Referer': 'https://pvp.qq.com/',
    }
)


def get(url: str):
    return _session.get(url, timeout=DEFAULT_TIMEOUT)

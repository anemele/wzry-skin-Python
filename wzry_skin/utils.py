import time
from functools import wraps
from pathlib import Path

from .constants import DEFAULD_SAVEPATH, FILE_SAVEPATH
from .log import logger


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        delta = time.perf_counter() - start
        logger.info(f'used time {delta:.3f}s')

        return result

    return wrapper


def mkdir(path: Path):
    if not path.exists():
        path.mkdir()
        logger.info(f'mkdir {path}')


def get_rootpath():
    if FILE_SAVEPATH.exists():
        with open(FILE_SAVEPATH) as fp:
            rootpath = Path(fp.read().strip())
        try:
            mkdir(rootpath)
            return rootpath
        except Exception as e:
            logger.error(e)
    rootpath = DEFAULD_SAVEPATH
    mkdir(rootpath)
    return rootpath

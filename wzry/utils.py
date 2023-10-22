import os
import os.path
import time
from dataclasses import dataclass
from functools import wraps

from .constants import DEFAULD_SAVEPATH, FILE_SAVEPATH
from .logger import logger


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        delta = time.perf_counter() - start
        logger.info(f'Used time {delta:.3f}s')

        return result

    return wrapper


def mkdir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f'mkdir {path}')


def get_rootpath():
    if os.path.exists(FILE_SAVEPATH):
        with open(FILE_SAVEPATH) as fp:
            rootpath = fp.read().strip()
        if not os.path.exists(rootpath):
            try:
                mkdir(rootpath)
                return rootpath
            except Exception as e:
                logger.error(e)
                rootpath = DEFAULD_SAVEPATH
    else:
        rootpath = DEFAULD_SAVEPATH
    mkdir(rootpath)
    return rootpath


@dataclass
class Hero:
    ename: int
    cname: str
    title: str

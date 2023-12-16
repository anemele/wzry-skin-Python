import json
from concurrent.futures import ThreadPoolExecutor, wait
from dataclasses import dataclass
from pathlib import Path
from queue import Queue

from .constants import API_HEROLIST
from .log import logger
from .parser import get_heropage, get_skinlist, get_skinurl
from .request import get
from .utils import get_rootpath, mkdir, timeit


@dataclass
class Hero:
    ename: int
    cname: str
    title: str


def get_hero_data():
    response = get(API_HEROLIST)
    for item in json.loads(response.content):
        yield Hero(item['ename'], item['cname'], item['title'])


def get_skin_data(q: Queue, hero: Hero):
    url = get_heropage(hero_id=hero.ename)
    res = get(url)
    skinlist = get_skinlist(res.content)
    q.put((skinlist, hero))


def download_skin(q: Queue, url: str, save_path: Path):
    res = get(url)
    # 非 200 认为请求 404，即该英雄没有更多皮肤了
    if res.status_code != 200:
        return
    q.put((res.content, save_path))


def write_skin(content: bytes, save_path: Path):
    save_path.write_bytes(content)
    logger.info(f'saved {save_path}')


def thread1():
    queue = Queue()
    with ThreadPoolExecutor() as executor:
        for hero in get_hero_data():
            executor.submit(get_skin_data, queue, hero)
    return queue


def thread2(q: Queue):
    rootpath = get_rootpath()

    queue = Queue()
    with ThreadPoolExecutor() as executor:
        while not q.empty():
            skinlist: list[str]
            hero: Hero
            skinlist, hero = q.get()

            savepath = rootpath / f'{hero.cname}_{hero.title}'
            mkdir(savepath)

            for i, skin in enumerate(skinlist):
                img_save_path = savepath / f'{i+1}_{skin}.jpg'
                if img_save_path.exists():
                    continue
                url = get_skinurl(hero_id=hero.ename, skin_id=i + 1)
                executor.submit(download_skin, queue, url, img_save_path)

    return queue


@timeit
def main():
    q1 = thread1()
    q2 = thread2(q1)

    futures = []
    with ThreadPoolExecutor() as executor:
        while not q2.empty():
            c, s = q2.get()
            task = executor.submit(write_skin, c, s)
            futures.append(task)
    wait(futures)
    logger.info('done.')

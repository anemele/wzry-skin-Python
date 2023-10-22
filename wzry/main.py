import json
import os.path
from concurrent.futures import ThreadPoolExecutor, wait
from queue import Queue
from typing import List

from lxml.etree import HTML

from .constants import (
    API_HEROLIST,
    API_HEROPAGE,
    API_SKINURL,
    REGEX_SKINLIST,
    XPATH_SKINLIST,
)
from .logger import logger
from .request import get
from .utils import Hero, get_rootpath, mkdir, timeit


def get_hero_data():
    response = get(API_HEROLIST)
    for item in json.loads(response.content):
        yield Hero(item['ename'], item['cname'], item['title'])


def get_skin_data(q: Queue, hero: Hero):
    url = API_HEROPAGE.format(hero_id=hero.ename)
    res = get(url)
    html = HTML(res.content) # type: ignore
    skinlist = html.xpath(XPATH_SKINLIST)
    if len(skinlist) == 1:
        skinlist = REGEX_SKINLIST.findall(skinlist[0])
    q.put((skinlist, hero))


def download_skin(q: Queue, url: str, save_path: str):
    res = get(url)
    # 非 200 认为请求 404，即该英雄没有更多皮肤了
    if res.status_code != 200:
        return
    q.put((res.content, save_path))


def write_skin(content: bytes, save_path: str):
    with open(save_path, 'wb') as fp:
        fp.write(content)
    logger.info(f'Saved {save_path}')


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
            skinlist, hero = q.get()
            savepath = os.path.join(rootpath, f'{hero.cname}_{hero.title}')
            mkdir(savepath)
            for i, skin in enumerate(skinlist):
                img_save_path = os.path.join(savepath, f'{i+1}_{skin}.jpg')
                if os.path.exists(img_save_path):
                    continue
                url = API_SKINURL.format(hero_id=hero.ename, skin_id=i + 1)
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
    logger.info('Done!')

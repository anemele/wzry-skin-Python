import json
import os.path
from concurrent.futures import ThreadPoolExecutor, wait
from typing import List, Union

from lxml.etree import HTML

from .constants import (API_HEROLIST, API_HEROPAGE, API_SKINURL,
                        REGEX_SKINLIST, XPATH_SKINLIST)
from .logger import logger
from .request import get
from .utils import Hero, get_rootpath, mkdir, timeit


def get_hero_data():
    response = get(API_HEROLIST)
    for item in json.loads(response.content):
        yield Hero(item['ename'], item['cname'], item['title'])


def get_skin_data(hero_id: Union[int, str]) -> List[str]:
    url = API_HEROPAGE.format(hero_id=hero_id)
    res = get(url)
    html = HTML(res.content)
    skinlist = html.xpath(XPATH_SKINLIST)
    if len(skinlist) == 1:
        skinlist = REGEX_SKINLIST.findall(skinlist[0])
    return skinlist


def job(url: str, save_path: str):
    res = get(url)
    # 非 200 认为请求 404，即该英雄没有更多皮肤了
    if res.status_code != 200:
        return
    with open(save_path, 'wb') as fp:
        fp.write(res.content)
    logger.info(f'下载成功：{save_path}')


@timeit
def main():
    with ThreadPoolExecutor() as executor:
        futures = []
        rootpath = get_rootpath()
        for hero in get_hero_data():
            savepath = os.path.join(rootpath, f'{hero.cname}_{hero.title}')
            mkdir(savepath)
            for i, skin in enumerate(get_skin_data(hero.ename)):
                img_save_path = os.path.join(savepath, f'{i+1}_{skin}.jpg')
                if os.path.exists(img_save_path):
                    # logger.info(f'已存在：{img_save_path}')
                    continue
                url = API_SKINURL.format(hero_id=hero.ename, skin_id=i + 1)
                futures.append(executor.submit(job, url, img_save_path))
    wait(futures)
    logger.info('全部下载完成！')

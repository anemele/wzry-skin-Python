import asyncio
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

import aiofiles
import aiohttp
from fake_useragent import FakeUserAgent

from .parser import get_heropage, get_skinlist, get_skinurl
from .utils import get_rootpath, mkdir, timeit

FAU = FakeUserAgent()

logging.basicConfig(
    format='[%(levelname)s] %(message)s',
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger(__file__)


def _random_ua():
    return {
        'User-Agent': FAU.random,
        'Referer': 'https://pvp.qq.com/',
    }


@dataclass
class Hero:
    ename: int
    cname: str
    title: str


API_HEROLIST = 'http://pvp.qq.com/web201605/js/herolist.json'


async def get_hero_data():
    async with aiohttp.ClientSession(headers=_random_ua()) as session:
        async with session.get(API_HEROLIST) as response:
            logger.debug(f'{API_HEROLIST}: {response.status}')
            content = await response.read()
    for item in json.loads(content):
        yield Hero(item['ename'], item['cname'], item['title'])


async def get_skin_data(session: aiohttp.ClientSession, hero: Hero):
    url = get_heropage(hero_id=hero.ename)
    async with session.get(url) as response:
        logger.debug(f'{url}: {response.status}')
        content = await response.read()
    return get_skinlist(content)


async def download_skin(session: aiohttp.ClientSession, url: str, savepath: Path):
    async with session.get(url) as response:
        # 非 200 认为请求 404，即该英雄没有更多皮肤了
        logger.debug(f'{url}: {response.status}')
        if response.status != 200:
            return
        content = await response.read()

    async with aiofiles.open(savepath, 'wb') as fp:
        await fp.write(content)
    logger.info(f'saved {savepath}')


async def get_hero_skin():
    async with aiohttp.ClientSession(headers=_random_ua()) as session:
        async for hero in get_hero_data():
            yield hero, await get_skin_data(session, hero),


async def main():
    rootpath = get_rootpath()

    async with aiohttp.ClientSession(headers=_random_ua()) as session:
        async for hero, skins in get_hero_skin():
            savepath = rootpath / f'{hero.cname}_{hero.title}'
            mkdir(savepath)

            tasks = []
            i = 0
            async for skin in skins:
                i += 1
                img_save_path = savepath / f'{i}_{skin}.jpg'
                if img_save_path.exists():
                    logger.debug(f'exists {img_save_path}')
                    continue
                url = get_skinurl(hero_id=hero.ename, skin_id=i)
                task = download_skin(session, url, img_save_path)
                tasks.append(task)
            await asyncio.gather(*tasks)


@timeit
def run():
    asyncio.run(main())
    logger.info('done.')

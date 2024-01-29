import re

from lxml.etree import HTML

XPATH_SKINLIST = '//div[@class="pic-pf"]/ul/@data-imgname'
REGEX_SKINLIST = re.compile(r'\s*(.+?)\s*(?:(?:&\d+\|)|(?:&\d+)|\|)')


def get_heropage(hero_id: int):
    return f'https://pvp.qq.com/web201605/herodetail/{hero_id}.shtml'


def get_skinurl(hero_id: int, skin_id: int):
    # SKIN_SIZE = ('big', 'mobile', 'small')
    return (
        'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'
        f'{hero_id}/{hero_id}-bigskin-{skin_id}.jpg'
    )


async def get_skinlist(content: bytes):
    html = HTML(content)  # type: ignore
    skinlist = html.xpath(XPATH_SKINLIST)
    if len(skinlist) == 0:
        return
    skinlist = skinlist[0]
    for it in REGEX_SKINLIST.finditer(skinlist):
        yield it.group(1)

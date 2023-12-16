import re

from lxml.etree import HTML

API_HEROPAGE = 'https://pvp.qq.com/web201605/herodetail/{hero_id}.shtml'
API_SKINURL = (
    'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'
    '{hero_id}/{hero_id}-bigskin-{skin_id}.jpg'
)
# SKIN_SIZE = ('big', 'mobile', 'small')


XPATH_SKINLIST = '//div[@class="pic-pf"]/ul/@data-imgname'
REGEX_SKINLIST = re.compile(r'\s*(.+?)\s*(?:(?:&\d+\|)|(?:&\d+)|\|)')


def get_heropage(hero_id: int):
    return API_HEROPAGE.format(hero_id=hero_id)


def get_skinurl(hero_id: int, skin_id: int):
    return API_SKINURL.format(hero_id=hero_id, skin_id=skin_id)


def get_skinlist(content: bytes) -> list[str]:
    html = HTML(content)  # type: ignore
    skinlist = html.xpath(XPATH_SKINLIST)
    if len(skinlist) == 1:
        skinlist = REGEX_SKINLIST.findall(skinlist[0])
    return skinlist

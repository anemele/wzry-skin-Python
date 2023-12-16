from lxml.etree import HTML

from .constants import API_HEROPAGE, API_SKINURL, REGEX_SKINLIST, XPATH_SKINLIST


def get_heropage(hero_id: int):
    return API_HEROPAGE.format(hero_id=hero_id)


def get_skinurl(hero_id: int, skin_id: int):
    return API_SKINURL.format(hero_id=hero_id, skin_id=skin_id)


def get_skinlist(content: bytes) -> list:
    html = HTML(content)  # type: ignore
    skinlist = html.xpath(XPATH_SKINLIST)
    if len(skinlist) == 1:
        skinlist = REGEX_SKINLIST.findall(skinlist[0])
    return skinlist

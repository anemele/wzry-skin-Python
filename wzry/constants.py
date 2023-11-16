import re
from pathlib import Path

API_HEROLIST = 'http://pvp.qq.com/web201605/js/herolist.json'
API_HEROPAGE = 'https://pvp.qq.com/web201605/herodetail/{hero_id}.shtml'
API_SKINURL = (
    'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'
    '{hero_id}/{hero_id}-bigskin-{skin_id}.jpg'
)
# SKIN_SIZE = ('big', 'mobile', 'small')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 2.2.2) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/53.0.855.0 Safari/534.1',
    'Referer': 'https://pvp.qq.com/',
}
DEFAULT_TIMEOUT = 5

XPATH_SKINLIST = '//div[@class="pic-pf"]/ul/@data-imgname'
REGEX_SKINLIST = re.compile(r'\s*(.+?)\s*(?:(?:&\d+\|)|(?:&\d+)|\|)')

FILE_LOGGER_CONFIG = 'logging.toml'
FILE_SAVEPATH = Path('savepath.txt')
DEFAULD_SAVEPATH = Path('./wzry-skin')

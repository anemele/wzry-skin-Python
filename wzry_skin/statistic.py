from pathlib import Path

from .utils import get_rootpath

# 皮肤数量统计
STATISTIC_RESULT = Path('statistic.txt')
# 从大到小排列（False 是从小到大排列，即皮肤少的在前）
STATISTIC_REVERSE = False
# 本地保存目录
SAVE_PATH = get_rootpath()


def _count_files(path: Path):
    count = -1
    for count, _ in enumerate(path.iterdir()):
        pass
    return path.name, count + 1


def get_data():
    data = map(_count_files, SAVE_PATH.iterdir())
    sorted_data = sorted(data, key=lambda x: x[1], reverse=STATISTIC_REVERSE)

    return sorted_data


def dump_data():
    data = [f'{k}:{v}' for k, v in get_data()]
    STATISTIC_RESULT.write_text('\n'.join(data), encoding='utf-8')

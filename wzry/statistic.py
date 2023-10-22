import os

from .utils import get_rootpath

# 皮肤数量统计
STATISTIC_RESULT = 'statistic.txt'
# 从大到小排列（False 是从小到大排列，即皮肤少的在前）
STATISTIC_REVERSE = False
# 本地保存目录
SAVE_PATH = get_rootpath()


def get_data():
    data = dict()
    for p in os.listdir(SAVE_PATH):
        tmp = os.path.join(SAVE_PATH, p)
        data[p] = len(os.listdir(tmp))

    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=STATISTIC_REVERSE)

    return sorted_data


def res_data(data):
    ret = []
    for k, v in data:
        it = f'{k}:{v}'
        ret.append(it)
    return ret


def dump_data():
    data = get_data()
    data = res_data(data)
    with open(STATISTIC_RESULT, 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(data))

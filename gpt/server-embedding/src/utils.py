#!/usr/bin/env python
# encoding: utf-8

import logging
import hashlib
import time
import uuid

import env

logger = logging.getLogger(__name__)

# 成功
SUCCESS = 0
# 错误
SERVER_ERROR = 500

# 无权限
NOT_AUTH = 300

# 数据不存在
NOT_EXIST = 400


def resp_not_exist():
    return {'code': NOT_EXIST, 'msg': '数据不存在', 'data': None}


def resp_success(data=None):
    return {'code': SUCCESS, 'msg': 'OK', 'data': data}


def resp_error(msg='服务出错'):
    return {'code': SERVER_ERROR, 'msg': msg, 'data': None}


def resp_auth():
    return {'code': NOT_AUTH, 'msg': 'not auth', 'data': False}


def parse_int(v):
    try:
        n = int(v)
        return True, n
    except Exception:
        return False, None


def check_list_dict(data):
    if not isinstance(data, list):
        return False
    for i in data:
        if not isinstance(i, dict):
            return False
    return True


def parse_digit(v):
    if str(v).isdigit():
        return True, int(v)
    return False, None


def valid_short_id(fid):
    if isinstance(fid, str) and len(fid) == 8:
        return True
    return False


def parse_float(v):
    try:
        n = float(v)
        return True, round(n, 2)
    except Exception:
        return False, None


def gen_uuid():
    return uuid.uuid1().hex[::-1]


def filemd5(fname: str) -> str:
    """文件md5"""
    with open(fname, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def today():
    """获取今天日期"""
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def cur_time_str():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


array = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
         "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
         "w", "x", "y", "z",
         "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
         "W", "X", "Y", "Z"
         ]


def gen_short_id() -> object:
    id = str(uuid.uuid4()).replace("-", '')  # 注意这里需要用uuid4
    buffer = []
    for i in range(0, 8):
        start = i * 4
        end = i * 4 + 4
        val = int(id[start:end], 16)
        buffer.append(array[val % 62])
    return "".join(buffer)


def gen_long_id():
    return uuid.uuid4().hex


def test():
    id_set = set()  # 用于存放生成的唯一id
    count = 0  # 用于统计出现重复的次数
    index = []  # 记录第几次调用生成8位id出现重复
    for i in range(0, 20000000):
        id = gen_short_id()
        if id in id_set:
            count += 1
            index.append(str(i + 1))
        else:
            id_set.add(id)
        if i % 10000 == 0:
            print(
                'id：%s, 运行第 %s 次, 重复数:%s , 重复率:%s, 出现重复次序 %s' % (
                    id, i + 1, count, count / (i + 1) * 100, ','.join(index)))


def gen_static_url(path):
    return f"{env.STATIC_PATH}{path}"


def format_price(price: int):
    tmp = price / 100
    format = "%.2f" % tmp
    return format


if __name__ == '__main__':
    for i in range(10):
        print(gen_short_id())

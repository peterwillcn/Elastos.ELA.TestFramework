#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/13 3:05 PM
# author: liteng

from src.core.wallet import keytool
from src.tools import serialize


def hello():
    return "hello", "world"


if __name__ == '__main__':

    balance = dict()

    balance["a"] = 1
    balance["b"] = 2
    balance["c"] = 3
    balance["d"] = 4

    keys = balance.values()
    a = list(keys)

    for key in keys:
        print(key)

    print(type(keys))

    print(type(a))

    print(a[0])








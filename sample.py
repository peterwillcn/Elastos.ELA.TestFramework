#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/13 3:05 PM
# author: liteng

import random
from decimal import Decimal
from elasdk.wallet.account import Account
from elasdk.wallet.keystore import Keystore


def hello():
    return "hello", "world"


if __name__ == '__main__':

    a = Account()
    data = str.encode("hello")

    k = Keystore(a, "123")
    print(k)
    k.save_to_file("./")

    k2 = Keystore("./keystore.dat", "12")








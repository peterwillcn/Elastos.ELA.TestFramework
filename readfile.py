#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/6/28 4:10 PM
# author: liteng


from src.core.wallet import keytool


if __name__ == '__main__':

    with open("./datas/code.avm", "rb") as f:
        content = f.read()

    print(content)
    print(content.hex())

    con_hash = keytool.sha256_hash(content, 1)
    con_160 = keytool.ripemd160_hash(con_hash, 1)
    print("before: ", con_160.hex())
    con_160 = con_160[::-1]

    print(con_160.hex())

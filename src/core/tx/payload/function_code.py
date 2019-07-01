#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/6/28 10:33 AM
# author: liteng

import struct

from src.tools import serialize


class FunctionCode(object):

    TYPE_SIGNATURE = 0
    TYPE_BOOLEAN = 1
    TYPE_INTEGER = 2
    TYPE_HASH160 = 3
    TYPE_HASH160_2 = 0xab
    TYPE_HASH256 = 4
    TYPE_BYTE_ARRAY = 5
    TYPE_PUBLIC_KEY = 6
    TYPE_STRING = 7
    TYPE_OBJECT = 8
    TYPE_HASH168 = 9
    TYPE_ARRAY = 0x10
    TYPE_VOID = 0xff

    def __init__(self, code=None, params_type=None, return_type=8):
        self.code = code
        self.params_type = params_type
        self.return_type = return_type
        self.code_hash = ""

    def serialize(self, r: bytes):
        r = serialize.write_var_bytes(r, self.code)
        r = serialize.write_var_bytes(r, bytes(self.params_type))
        r += struct.pack("<B", self.return_type)

        return r


if __name__ == '__main__':

    code_hash = "1c7779c302193ebc1523a7fe627497a31808fede95"
    code_hash_bytes = bytes.fromhex(code_hash)[1:]
    r = code_hash_bytes[::-1]
    print("code hash: ", code_hash_bytes.hex())
    print("reverse h: ", r.hex())
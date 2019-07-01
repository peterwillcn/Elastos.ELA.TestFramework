#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/2 10:21 AM
# author: liteng


class Payload(object):

    DEFAULT_VERSION = 0x00

    def __init__(self, version: int):
        self.version = version

    def data(self, version: int):
        return None

    def serialize(self, r: bytes, version: int):
        return None

    def deserialize(self, r: bytes, version: int):
        return None

    def __repr__(self):
        return ""


if __name__ == '__main__':

    program_hash = "21cd3ce7d81cef33d7522133bdaa20050b37084869"

    program2 = program_hash[2:]

    print("program1: ", program_hash)
    print("program2: ", program2)



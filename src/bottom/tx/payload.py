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



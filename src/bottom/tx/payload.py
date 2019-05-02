#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/2 10:21 AM
# author: liteng


class Payload(object):

    def __init__(self):
        pass

    def data(self, r: bytes):
        pass

    def serialize(self, r: bytes, version: int):
        pass

    def deserialize(self, r: bytes, version: int):
        pass
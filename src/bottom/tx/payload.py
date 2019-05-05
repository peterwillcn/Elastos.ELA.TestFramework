#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/2 10:21 AM
# author: liteng


class Payload(object):

    def data(self, r: bytes):
        return None

    def serialize(self, r: bytes, version: int):
        return None

    def deserialize(self, r: bytes, version: int):
        return None

    def __repr__(self):
        return ""



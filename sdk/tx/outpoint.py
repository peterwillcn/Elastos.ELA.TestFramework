#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 2:18 PM
# author: liteng

import struct


class OutPoint(object):
    def __init__(self, tx_id: bytes, n: int):
        self.tx_id = tx_id
        self.index = n

    def deserialize(self, f):
        pass

    def serialize(self):
        r = b""
        r += self.tx_id
        r += struct.pack("<H", self.index)
        return r

    def __repr__(self):
        return "OutPoint{" + "\n\t" \
                + "tx_hash: " + self.tx_id.hex() + "\n\t" \
                + "index: " + str(self.index) + "\n" \
                + "}"





#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 2:18 PM
# author: liteng

import struct

from src.middle.tools import util

from src.bottom.wallet import keytool


class OutPoint(object):
    def __init__(self, hash="", n=0):
        self.hash = hash
        self.index = n

    def deserialize(self, f):
        hash = util.deser_uint256(f)
        self.hash = hex(hash)[2:]
        self.index = struct.unpack("<I", f.read(4))[0]

    def serialize(self):
        r = b""
        r += bytes.fromhex(self.hash)
        r += struct.pack("<H", self.index)
        return r

    def __repr__(self):
        return "OutPoint(hash=%s index=%i)" % (self.hash, self.index)





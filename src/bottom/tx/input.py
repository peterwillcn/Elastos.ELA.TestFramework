#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 2:17 PM
# author: liteng

import struct

from src.bottom.wallet import keytool
from src.bottom.tx.outpoint import OutPoint


class Input(object):
    def __init__(self, outpoint=None, sequence=0):
        if outpoint is None:
            self.previous = OutPoint()
        else:
            self.previous = outpoint
        self.sequence = sequence

    def deserialize(self, f):
        self.previous.deserialize(f)
        self.sequence = struct.unpack("<I", f.read(4))[0]

    def serialize(self):
        r = b""
        r += self.previous.serialize()
        r += struct.pack("<I", self.sequence)
        return r

    def __repr__(self):
        return "Input(previous=%s sequence=%i)" % (repr(self.previous), self.sequence)


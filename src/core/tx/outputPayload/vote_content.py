#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/5 5:14 PM
# author: liteng

import struct

from src.tools import serialize
from src.tools.log import Logger


class VoteContent(object):
    DELEGATE = 0x00
    CRC = 0x01
    CRC_PROPOSAL = 0x02
    CRC_IMPEACHMENT = 0x03

    def __init__(self, vote_type: int, candidates: list):
        self.vote_type = vote_type
        self.candidates = candidates

    def serialize(self, version: int):
        if self.candidates is None or len(self.candidates) == 0:
            Logger.error("candidates list is empty!")
            return None
        r = b""
        r += struct.pack("<B", self.vote_type)
        r += serialize.write_var_uint(len(self.candidates))
        for candidate in self.candidates:
            r += candidate.serialize(version)
        return r

    def deserialize(self, version: int):
        pass

    def __repr__(self):
        return "VoteContent {\n\t" \
               + "vote_type: {}".format(self.vote_type) + "\n\t" \
               + "candidates: {}".format(self.candidates) + "\n" \
               + "}"

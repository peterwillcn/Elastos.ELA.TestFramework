#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/5 5:14 PM
# author: liteng

import struct

from sdk.common import util, serialize
from sdk.common.log import Logger


class VoteContent(object):

    TYPE_DELEGATE = 0x00
    TYPE_CRC = 0x01

    def __init__(self, vote_type: int, candidates: list):
        self.tag = util.tag_from_path(__file__, VoteContent.__name__)
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
            r = serialize.write_var_bytes(r, candidate)

        return r

    def deserialize(self, version: int):
        pass

    def __repr__(self):
        return "VoteContent {\n\t" \
                + "vote_type: {}".format(self.vote_type) + "\n\t" \
                + "candidates: {}".format(self.candidates) + "\n" \
                + "}"
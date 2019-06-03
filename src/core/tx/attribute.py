#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 2:11 PM
# author: liteng

import struct

from elasdk.common import serialize


class Attribute(object):

    NONCE = 0x00
    SCRIPT = 0x20
    MEMO = 0x81
    DESCRIPTION = 0x90
    DESCRIPTION_URL = 0x91
    CONFIRMATIONS = 0X92

    def __init__(self, usage=0, data=None):
        self.usage = usage
        self.data = data

    @staticmethod
    def get_attribute_usage(usage: int):
        if usage == 0x00:
            return "Nonce"
        elif usage == 0x20:
            return "Script"
        elif usage == 0x81:
            return "Memo"
        elif usage == 0x90:
            return "Description"
        elif usage == 0x91:
            return "DescriptionUrl"
        elif usage == 0x92:
            return "Confirmations"

    def is_valid_attribute_type(self, usage: int):
        if usage == self.NONCE or usage == self.SCRIPT or usage == self.MEMO or usage == self.DESCRIPTION \
                or usage == self.DESCRIPTION_URL or usage == self.CONFIRMATIONS:
            return True
        return False

    def serialize(self):
        if not self.is_valid_attribute_type(self.usage):
            return None

        r = b""
        r += struct.pack("<B", self.usage)
        if self.data is None:
            r = serialize.write_var_bytes(r, bytes(0))
        else:
            r = serialize.write_var_bytes(r, self.data)

        return r

    def deserialize(self):
        pass

    def __repr__(self):
        if self.data is None:
            arg1 = ""
        else:
            arg1 = self.data.hex()

        return "Attribute {" + "\n\t" \
                + "usage: " + str(self.usage) + "\n\t" \
                + "data: " + arg1 + "\n" \
                + "}"




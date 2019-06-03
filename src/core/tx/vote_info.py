#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/5 5:31 PM
# author: liteng

import struct

from src.tools import serialize
from src.tools.log import Logger

from src.core.tx.vote_content import VoteContent
from src.core.tx.output_payload import OutputPayload


class VoteInfo(OutputPayload):

    def __init__(self, version: int, vote_contents: list):
        self.version = version
        self.contents = vote_contents

    def data(self):
        return None

    def serialize(self):
        if self.contents is None or len(self.contents) == 0:
            Logger.error("contents is invalid")
            return None

        r = b""
        r += struct.pack("<B", self.version)
        r += serialize.write_var_uint(len(self.contents))
        for content in self.contents:
            r += content.serialize(self.version)

        return r

    def deserialize(self):
        pass

    def get_version(self):
        return self.version

    def validate(self):
        if self.version != 0:
            Logger.error("invalid vote version")
            return False

        type_list = list()
        for content in self.contents:
            if content.vote_type in type_list:
                Logger.error("{} duplicate vote type")
                return False
            type_list.append(content.vote_type)

            if content.vote_type != VoteContent.TYPE_DELEGATE:
                Logger.error("{} invalid vote type")

            if len(content.candidates) == 0 or len(content.candidates) > 36:
                Logger.error("{} invalid vote candidates")
                return False

            candidates_list = list()
            for candidate in content.candidates:
                if candidate in candidates_list:
                    Logger.error("{} duplicate candidate")
                    return False
                candidates_list.append(candidate)

        return True

    def __repr__(self):
        return "VoteInfo {\n\t" \
                + "version: {}".format(self.version) + "\n\t" \
                + "contents: {}".format(self.contents) + "\n" \
                + "}"
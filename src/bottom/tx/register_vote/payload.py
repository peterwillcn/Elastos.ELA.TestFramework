#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/3 4:49 PM
# author: liteng

from src.middle.tools import util


class Payload(object):
    def __init__(self, private_key: str, owner_public_key: str, node_public_key: str,
                 nickname: str, url: str, location: int, net_address: str):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.private_key = private_key
        self.owner_public_key = owner_public_key
        self.node_public_key = node_public_key
        self.nickname = nickname
        self.url = url
        self.location = location
        self.net_address = net_address
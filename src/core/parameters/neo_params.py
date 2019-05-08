#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:42 AM
# author: liteng

from src.tools import util, constant


class NeoParams(object):
    def __init__(self, config: dict):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.magic = constant.CONFIG_MAGIC_NEO
        self.spv_magic = constant.CONFIG_MAGIC_ELA
        self.enable = config["enable"]
        self.number = config["number"]
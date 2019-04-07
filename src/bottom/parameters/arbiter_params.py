#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:42 AM
# author: liteng

from src.middle.tools import util
from src.middle.tools import constant


class ArbiterParams(object):
    def __init__(self, config: dict):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.magic = constant.CONFIG_MAGIC_ARBITER
        self.enable = config["enable"]
        self.number = config["number"]
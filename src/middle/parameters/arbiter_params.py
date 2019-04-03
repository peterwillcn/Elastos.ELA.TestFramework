#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:42 AM
# author: liteng


class ArbiterParams(object):
    def __init__(self, config: dict):
        self.tag = "[src.middle.parameters.arbiter_params.ArbiterParams]"
        self.enable = config["enable"]
        self.number = config["number"]
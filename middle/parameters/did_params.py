#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:42 AM
# author: liteng


class DidParams(object):
    def __init__(self, config: dict):
        self.enable = config["enable"]
        self.number = config["number"]
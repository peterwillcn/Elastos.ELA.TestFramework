#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:40 AM
# author: liteng


class ElaParams(object):

    def __init__(self, config: dict):
        self.enable = config["enable"]
        self.number = config["number"]
        self.password = config["password"]
        self.crc_number = config["crc_number"]
        self.config_heights = config["heights"]
        self.pre_connect_offset = config["pre_connect_offset"]


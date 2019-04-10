#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:40 AM
# author: liteng

from src.middle.tools import util
from src.middle.tools import constant


class ElaParams(object):

    def __init__(self, config: dict):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.magic = constant.CONFIG_MAGIC_ELA
        self.enable = config["enable"]
        self.arbiter_enable = config["arbiter_enable"]
        self.number = config["number"]
        self.password = config["password"]
        self.crc_number = config["crc_number"]
        self.print_level = config["print_level"]
        self.auto_mining = config["auto_mining"]
        self.instant_block = config["instant_block"]
        self.pre_connect_offset = config["pre_connect_offset"]
        self.check_address_height = config["check_address_height"]
        self.vote_start_height = config["vote_start_height"]
        self.crc_dpos_height = config["crc_dpos_height"]
        self.public_dpos_height = config["public_dpos_height"]
        self.max_inactivate_rounds = config["max_inactivate_rounds"]

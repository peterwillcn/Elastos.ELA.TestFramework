#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:40 AM
# author: liteng


class ElaParams(object):

    def __init__(self, config: dict):
        self.enable = config["enable"]
        self.arbiter_enable = config["arbiter_enable"]
        self.number = config["number"]
        self.password = config["password"]
        self.crc_number = config["crc_number"]
        self.auto_mining = config["auto_mining"]
        self.instant_block = config["instant_block"]
        self.foundation_address = config["foundation_address"]
        self.miner_address = config["miner_address"]
        self.pre_connect_offset = config["pre_connect_offset"]
        self.check_address_height = config["check_address_height"]
        self.vote_start_height = config["vote_start_height"]
        self.crc_dpos_height = config["crc_dpos_height"]
        self.public_dpos_height = config["public_dpos_height"]


#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:42 AM
# author: liteng

from src.tools import util, constant

from src.core.parameters.ela_params import ElaParams


class ArbiterParams(object):
    def __init__(self, config: dict, ela_params: ElaParams):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.magic = constant.CONFIG_MAGIC_ARBITER
        self.spv_magic = constant.CONFIG_MAGIC_ELA
        self.enable = config["enable"]
        self.number = config["number"]
        self.active_net = config["active_net"]
        self.pow_chain = config["pow_chain"]
        self.print_level = config["print_level"]
        self.spv_print_level = config["spv_print_level"]
        self.crc_number = ela_params.crc_number
        self.crc_dpos_only_height = ela_params.crc_dpos_height
        self.side_chain_genesis_hash = ""
        self.recharge_address = ""
        self.withdraw_address = ""
        self.side_info = dict()
        self.password = ela_params.password
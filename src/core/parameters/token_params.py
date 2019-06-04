#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:42 AM
# author: liteng

from src.tools import util, constant


class TokenParams(object):
    def __init__(self, config: dict):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.magic = constant.CONFIG_MAGIC_TOKEN
        self.spv_magic = constant.CONFIG_MAGIC_ELA
        self.enable = config["enable"]
        self.number = config["number"]
        self.active_net = config["active_net"]
        self.mining_enable = config["mining_enable"]
        self.disable_dns = config["disable_dns"]
        self.log_level = config["log_level"]
        self.spv_disable_dns = config["spv_disable_dns"]
        self.rest_port_enable = config["rest_port_enable"]
        self.ws_port_enable = config["ws_port_enable"]
        self.rpc_port_enable = config["rpc_port_enable"]
        self.instant_block = config["instant_block"]
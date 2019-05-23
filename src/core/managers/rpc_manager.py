#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/9 5:03 PM
# author: liteng

import time

from src.core.services import rpc
from src.core.managers.node_manager import NodeManager

from src.tools import util
from src.tools.log import Logger


class RpcManager(object):

    def __init__(self, node_manager: NodeManager):
        self.tag = util.tag_from_path(__file__, RpcManager.__name__)
        self.node_manager = node_manager
        self.params = self.node_manager.params
        self.node_info_dict = dict()
        self.normal_dpos_pubkeys = list()

    def mining_blocks_ready(self, foundation_address):
        time.sleep(3)
        rpc.discrete_mining(110)
        balance = rpc.get_balance_by_address(foundation_address)
        Logger.debug("{} foundation address value: {}".format(self.tag, balance))

    def get_arbiter_names(self, category: str):
        public_key_nickname = self.node_info_dict
        arbiters = rpc.get_arbiters_info()[category]
        current_nicknames = list()
        for public_key in arbiters:
            current_nicknames.append(public_key_nickname[public_key])

        return current_nicknames

    def init_normal_dpos_public_keys(self):
        public_keys_list = list()
        nodes = self.node_manager.ela_nodes[1: self.params.ela_params.crc_number * 3 + 1]
        for node in nodes:
            public_keys_list.append(node.node_account.public_key())

        self.normal_dpos_pubkeys = public_keys_list

    def init_pubkey_nodes(self):
        pubkey_node_name = dict()
        for node in self.node_manager.ela_nodes:
            Logger.debug("{} node name: {}".format(self.tag, node.name))
            pubkey_node_name[node.node_account.public_key()] = node.name
        if len(pubkey_node_name.keys()) == 0:
            Logger.debug("pubkey node name length: {}".format(len(pubkey_node_name)))
            exit(0)
        self.node_info_dict = pubkey_node_name

    def show_arbiter_info(self):
        arbiters_nicknames = self.get_arbiter_names("arbiters")
        arbiters_nicknames.sort()
        next_arbiter_nicknames = self.get_arbiter_names("nextarbiters")
        next_arbiter_nicknames.sort()
        Logger.info("current arbiters nicknames: {}".format(arbiters_nicknames))
        Logger.info("next    arbiters nicknames: {}".format(next_arbiter_nicknames))

    def check_nodes_height(self):
        Logger.debug("{} check the all nodes whether have the same height".format(self.tag))
        time.sleep(3)
        heights = list()

        for node in self.node_manager.ela_nodes:
            if not node.running:
                continue

            height = rpc.get_block_count(node.rpc_port)
            Logger.debug("{} node{} height\t{}".format(self.tag, node.index, height))
            heights.append(height)

        global h0
        h0 = heights[0]

        for h in heights[1:]:
            if h != h0:
                return False

        return True


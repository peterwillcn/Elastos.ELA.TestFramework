#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 2:48 PM
# author: liteng

import time

from src.middle.common.log import Logger
from src.middle.parameters.params import Parameter

from src.bottom.nodes.node_manager import NodeManager
from src.bottom.services.rpc import RPC
from src.bottom.services.rest import REST
from src.bottom.services.jar import JarService
from src.bottom.tx.transaction import Transaction
from src.bottom.tx.assist import Assist


class Overall(object):

    def __init__(self, top_config, project_root_path: str):
        self.tag = "[src.middle.overall.Overall]"
        self.params = Parameter(top_config)
        self.check_params()
        self.jar_server = JarService(project_root_path)
        self.rpc = RPC()
        self.rest = REST()
        self.assist = Assist(self.rpc, self.rest)
        self.tx = Transaction(self.jar_server, self.assist, self.params.ela_params.number)

        self.node_manager = NodeManager(self.rpc, self.params, project_root_path)

    def deploy_node(self):
        ret = False

        config_update_content = dict()
        config_update_content["ela"] = dict()
        config_update_content["arbiter"] = dict()
        config_update_content["did"] = dict()
        config_update_content["token"] = dict()
        config_update_content["neo"] = dict()

        if self.params.ela_params.enable:
            ret = self.node_manager.deploy_node("ela",  self.params.ela_params.number, config_update_content)
        if self.params.arbiter_params.enable:
            ret = self.node_manager.deploy_node("arbiter", self.params.arbiter_params.number, config_update_content)
        if self.params.did_params.enable:
            ret = self.node_manager.deploy_node("did", self.params.did_params.number, config_update_content)
        if self.params.token_params.enable:
            ret = self.node_manager.deploy_node("token", self.params.token_params.number, config_update_content)
        if self.params.neo_params.enable:
            ret = self.node_manager.deploy_node("neo", self.params.neo_params.number, config_update_content)

        return ret

    def start_node(self):
        ret = False

        if self.params.ela_params.enable:
            ret = self.node_manager.start_nodes()
        time.sleep(4)

        self.rpc.discrete_mining(101)
        Logger.debug("{} mining 101 blocks on success!".format(self.tag))
        foundation_value = self.rpc.get_balance_by_address(self.node_manager.foundation_address)
        Logger.debug("{} The value of foundation address is {}".format(self.tag, foundation_value))

        return ret

    def stop_node(self):
        if self.params.ela_params.enable:
            self.node_manager.stop_nodes()

    def recharge_tap_wallet(self, amount):
        ret = self.tx.ordinary_single_sign(
            input_keystore=self.node_manager.keystore_manager.special_key_stores[0],
            output_addresses=[self.node_manager.tap_address],
            amount=amount,
            fee=100
        )
        tap_value = self.rpc.get_balance_by_address(self.node_manager.tap_address)
        Logger.debug("{} tap address value: {} ELAs".format(self.tag, tap_value))
        return ret

    def recharge_producer_wallet(self, amount):
        addresses = list()
        for keystore in self.node_manager.keystore_manager.owner_key_stores:
            addresses.append(keystore.address)

        ret = self.transfer_money(addresses, amount)

        for i in range(len(addresses)):
            value = self.rpc.get_balance_by_address(addresses[i])
            Logger.debug("{} producers {} wallet balance: {}".format(self.tag, i, value))
        return ret

    def register_producers_candidates(self):
        for i in range(self.params.ela_params.crc_number, self.params.ela_params.number):
            ret = self.tx.register_a_producer(self.node_manager.ela_nodes[i])
            if not ret:
                return False
        return True

    def vote_producers_candidates(self):
        for i in range(self.params.ela_params.crc_number, self.params.ela_params.number):
            ret = self.tx.vote_a_producer(
                self.node_manager.ela_nodes[i],
                self.tx.register_producers_list[i - self.params.ela_params.crc_number]
            )
            if not ret:
                return False
        return True

    def transfer_money(self, addresses: list, amount: int):
        ret = self.tx.ordinary_single_sign(
            input_keystore=self.node_manager.keystore_manager.special_key_stores[2],
            output_addresses=addresses,
            amount=amount,
            fee=100,
        )
        return ret

    def check_params(self):
        if self.params.ela_params.number < 3 * self.params.ela_params.crc_number:
            Logger.error("{} ela node number should be >= 3 * crc number, please check your config.json, exit...")
            time.sleep(1)
            exit(-1)




#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/5 5:42 PM
# author: liteng

from src.middle.tools import util
from src.middle.tools import constant
from src.middle.tools.log import Logger
from src.middle.managers.node_manager import NodeManager

from src.bottom.tx.transaction import Transaction
from src.bottom.parameters.params import Parameter


class TransactionManager(object):
    def __init__(self, params: Parameter, node_manager: NodeManager):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.params = params
        self.node_manager = node_manager
        self.tx = Transaction(self.node_manager.service_manager)

    def recharge_tap_keystore(self, amount):
        ret = self.tx.ordinary_single_sign(
            input_keystore=self.node_manager.keystore_manager.special_key_stores[0],
            output_addresses=[self.node_manager.tap_address],
            amount=amount,
            fee=100
        )
        tap_value = self.node_manager.service_manager.rpc.get_balance_by_address(self.node_manager.tap_address)
        Logger.debug("{} tap address value: {} ELAs".format(self.tag, tap_value))
        return ret

    def recharge_arbiter_keystore(self, amount):
        addresses = list()
        for keystore in self.node_manager.keystore_manager.arbiter_stores:
            addresses.append(keystore.address)

        ret = self.transfer_money(addresses, amount)

        for i in range(len(addresses)):
            value = self.node_manager.service_manager.rpc.get_balance_by_address(addresses[i])
            Logger.debug("{} arbiter {} wallet balance {}".format(self.tag, i, value))
        return ret

    def recharge_producer_keystore(self, amount):
        addresses = list()
        for keystore in self.node_manager.keystore_manager.owner_key_stores:
            addresses.append(keystore.address)

        ret = self.transfer_money(addresses, amount)

        for i in range(len(addresses)):
            value = self.node_manager.service_manager.rpc.get_balance_by_address(addresses[i])
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
                self.node_manager.keystore_manager.owner_key_stores[i],
                self.tx.register_producers_list[i - self.params.ela_params.crc_number],
                (self.params.ela_params.number - i) * constant.TO_SELA
            )
            if not ret:
                return False
        return True

    def transfer_money(self, addresses: list, amount: int):
        ret = self.tx.ordinary_single_sign(
            input_keystore=self.node_manager.keystore_manager.special_key_stores[4],
            output_addresses=addresses,
            amount=amount,
            fee=100,
        )
        return ret


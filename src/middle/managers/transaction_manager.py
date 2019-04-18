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
        self.general_producer_public_keys = list()
        self.candidate_public_keys = list()

    def recharge_tap_keystore(self, amount):
        ret = self.tx.ordinary_single_sign(
            input_keystore=self.node_manager.keystore_manager.special_key_stores[0],
            output_addresses=[self.node_manager.tap_address],
            amount=amount
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
            Logger.debug("{} arbiter {} wallet balance: {}".format(self.tag, i, value))
        return ret

    def recharge_sub_keystore(self, amount):
        addresses = list()
        for keystore in self.node_manager.keystore_manager.sub_key_stores:
            addresses.append(keystore.address)

        ret = self.transfer_money(addresses, amount)

        for i in range(len(addresses)):
            value = self.node_manager.service_manager.rpc.get_balance_by_address(addresses[i])
            Logger.debug("{} sub {} wallet balance: {}".format(self.tag, i, value))

        return ret

    def recharge_producer_keystore(self, amount=10000 * constant.TO_SELA):
        addresses = list()
        for keystore in self.node_manager.keystore_manager.owner_key_stores:
            addresses.append(keystore.address)

        ret = self.transfer_money(addresses, amount)
        if not ret:
            Logger.error("{} recharge producer keystore failed, exit...".format(self.tag))
            exit(-1)
        for i in range(len(addresses)):
            value = self.node_manager.service_manager.rpc.get_balance_by_address(addresses[i])
            Logger.debug("{} producers {} wallet balance: {}".format(self.tag, i, value))
        return ret

    def cross_chain_transaction(self, recharge: bool):
        if recharge:
            ret = self.tx.cross_chain_transaction(
                input_keystore=self.node_manager.keystore_manager.special_key_stores[4],
                lock_address=self.params.arbiter_params.recharge_address,
                output_address=self.node_manager.keystore_manager.special_key_stores[5].address,
                amount=200 * constant.TO_SELA,
                port=self.node_manager.ela_nodes[0].rpc_port
            )

            if not ret:
                Logger.info("{} cross chain recharge failed".format(self.tag))
                return False

        else:
            ret = self.tx.cross_chain_transaction(
                input_keystore=self.node_manager.keystore_manager.special_key_stores[5],
                lock_address=self.params.arbiter_params.withdraw_address,
                output_address=self.node_manager.keystore_manager.special_key_stores[4].address,
                amount=100 * constant.TO_SELA,
                port=self.node_manager.did_nodes[0].rpc_port
            )

            if not ret:
                Logger.info("{} cross chain withdraw failed".format(self.tag))
                return False

        return True

    def register_producers_candidates(self):
        num = 0
        for i in range(self.params.ela_params.crc_number + 1, self.params.ela_params.number + 1):
            ela_node = self.node_manager.ela_nodes[i]
            public_key = ela_node.node_keystore.public_key.hex()
            ret = self.tx.register_a_producer(ela_node)
            if not ret:
                return False
            num += 1
            if num <= self.params.ela_params.crc_number * 2:
                self.general_producer_public_keys.append(public_key)
            else:
                self.candidate_public_keys.append(public_key)

        Logger.info("{} general register public keys size: {}".format(self.tag, len(self.general_producer_public_keys)))
        Logger.info("{} general register public keys: {}".format(self.tag, self.general_producer_public_keys))
        Logger.info("{} candidate public keys size: {}".format(self.tag, len(self.candidate_public_keys)))
        Logger.info("{} candidate public keys: {}".format(self.tag, self.candidate_public_keys))
        return True

    def update_produces_candidates(self):
        for i in range(len(self.tx.register_producers_list)):
            producer = self.tx.register_producers_list[i]
            payload = producer.payload
            payload.nickname = "arbiter-" + str(i)
            ret = self.tx.update_a_producer(producer, payload)
            if not ret:
                return False
        return True

    def cancel_producers_candidates(self):
        for producer in self.tx.register_producers_list:
            ret = self.tx.cancel_a_producer(producer)
            if not ret:
                return False
        self.node_manager.service_manager.rpc.discrete_mining(2200)
        return True

    def redeem_producers_candidates(self):
        print("cancel producers size: ", len(self.tx.cancel_producers_list))
        for producer in self.tx.cancel_producers_list:
            ret = self.tx.redeem_a_producer(producer)
            if not ret:
                return False
        return True

    def vote_producers_candidates(self):
        for i in range(self.params.ela_params.crc_number, self.params.ela_params.number):
            ret = self.tx.vote_a_producer(
                vote_keystore=self.node_manager.keystore_manager.owner_key_stores[i],
                producer=self.tx.register_producers_list[i - self.params.ela_params.crc_number],
                vote_amount=(self.params.ela_params.number - i) * constant.TO_SELA
            )
            if not ret:
                return False
        return True

    def transfer_money(self, addresses: list, amount: int):
        ret = self.tx.ordinary_single_sign(
            input_keystore=self.node_manager.keystore_manager.special_key_stores[4],
            output_addresses=addresses,
            amount=amount
        )
        return ret


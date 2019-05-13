#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/5 5:42 PM
# author: liteng


import time


from src.core.tx import txbuild
from src.core.tx.transaction import Transaction
from src.core.services import rpc
from src.core.wallet.keystore import KeyStore
from src.core.nodes.ela import ElaNode
from src.core.tx.producer import Producer
from src.core.parameters.params import Parameter
from src.core.managers.node_manager import NodeManager
from src.core.tx.payload.producer_info import ProducerInfo

from src.tools import util
from src.tools import constant
from src.tools.log import Logger


class TransactionManager(object):

    def __init__(self, node_manager: NodeManager):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.node_manager = node_manager
        self.params = self.node_manager.params
        self.fee = 10000
        self.register_producers_list = list()
        self.cancel_producers_list = list()
        self.general_producer_public_keys = list()
        self.candidate_public_keys = list()
        self.tap_key_store = self.node_manager.keystore_manager.tap_key_store

    def transfer_asset(self, input_keystore: KeyStore, output_addresses: list, amount: int):

        # create transfer asset tx
        tx = txbuild.create_transaction(
            keystore=input_keystore,
            output_addresses=output_addresses,
            amount=amount,
            fee=self.fee,
            output_lock=0
        )

        if tx is None:
            return False
        # single sign this tx
        tx = txbuild.single_sign_transaction(input_keystore, tx)

        # return the result
        ret = self._handle_tx_result(tx)

        return ret

    def transfer_cross_chain_asset(self, input_keystore: KeyStore, lock_address: str, cross_address: str,
                                   amount: int, port=rpc.DEFAULT_PORT):
        tx = txbuild.create_cross_chain_asset(
            keystore=input_keystore,
            lock_address=lock_address,
            cross_chain_address=cross_address,
            amount=amount,
            port=port
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(input_keystore, tx)

        Logger.debug("cross chain asset transaction: \n{}".format(tx))
        ret = self._handle_tx_result(tx, port)

        return ret

    def register_producer(self, node: ElaNode):

        producer = Producer(node)
        tx = producer.register()

        if tx is None:
            return False

        ret = self._handle_tx_result(tx)
        if ret:
            self.register_producers_list.append(producer)

        return ret

    def update_producer(self, producer: Producer, producer_info: ProducerInfo):
        tx = producer.update(producer_info)

        print(tx)
        if tx is None:
            return False

        ret = self._handle_tx_result(tx)

        return ret

    def cancel_producer(self, producer: Producer):
        tx = producer.cancel()

        if tx is None:
            return False

        ret = self._handle_tx_result(tx)

        if ret:
            self.cancel_producers_list.append(producer)
        return ret

    def redeem_producer(self, producer: Producer):
        tx = producer.redeem()

        if tx is None:
            return False

        ret = self._handle_tx_result(tx)

        return ret

    def activate_producer(self, producer: Producer):
        tx = producer.activate()

        if tx is None:
            return False

        ret = self._handle_tx_result(tx)

        return ret

    def vote_producer(self, keystore: KeyStore, amount: int, candidates: list):

        candidates_list = list()
        for producer in candidates:
            candidates_list.append(producer.node.owner_keystore.public_key)

        tx = txbuild.create_vote_transaction(
            keystore=keystore,
            cancadites_list=candidates_list,
            amount=amount,
            fee=10000
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(keystore, tx)

        ret = self._handle_tx_result(tx)

        return ret

    def recharge_necessary_keystore(self, input_keystore: KeyStore, keystores: list, amount: int):
        addresses = list()
        for keystore in keystores:
            addresses.append(keystore.address)

        ret = self.transfer_asset(input_keystore, addresses, amount)

        if ret:
            rpc.discrete_mining(1)
        else:
            Logger.error("{} recharge necessary keystore failed".format(self.tag))
            return False

        for i in range(len(addresses)):
            value = rpc.get_balance_by_address(addresses[i])
            Logger.debug("{} arbiter {} wallet balance: {}".format(self.tag, i, value))
        return ret

    def cross_chain_transaction(self, side_node_type: str, recharge: bool):
        if side_node_type is None or side_node_type is "":
            return False

        global cross_key_store
        global side_port
        global result

        if side_node_type is "did":
            side_port = 10036
            cross_key_store = self.node_manager.keystore_manager.special_key_stores[5]
        elif side_node_type is "token":
            side_port = 10046
            cross_key_store = self.node_manager.keystore_manager.special_key_stores[5]

        if recharge:

            balance1 = rpc.get_balance_by_address(cross_key_store.address)

            ret = self.transfer_cross_chain_asset(
                input_keystore=self.tap_key_store,
                lock_address=self.params.arbiter_params.side_info[side_node_type][constant.SIDE_RECHARGE_ADDRESS],
                cross_address=cross_key_store.address,
                amount=200 * constant.TO_SELA,
            )

            if not ret:
                Logger.info("{} cross chain recharge failed".format(self.tag))
                return False

            Logger.debug("{} cross chain transaction on success".format(self.tag))

            current_height = rpc.get_block_count()
            while True:
                main_height = rpc.get_block_count()
                side_height = rpc.get_block_count(side_port)

                Logger.debug("{} main height: {}, side height: {}".format(self.tag, main_height, side_height))

                if main_height - current_height > 7:
                    time.sleep(2)

                if main_height - current_height > 10:
                    break

                rpc.discrete_mining(1)
                time.sleep(1)

            balance2 = rpc.get_balance_by_address(cross_key_store.address)

            result = float(balance2) - float(balance1) > float(200 - 3 * 10000) / constant.TO_SELA

        else:

            balance1 = rpc.get_balance_by_address(self.tap_key_store.address)
            ret = self.transfer_cross_chain_asset(
                input_keystore=cross_key_store,
                lock_address=self.params.arbiter_params.withdraw_address,
                cross_address=self.tap_key_store.address,
                amount=100 * constant.TO_SELA,
                port=side_port
            )

            if not ret:
                Logger.info("{} cross chain withdraw failed".format(self.tag))
                return False

            Logger.debug("{} cross chain transaction on success".format(self.tag))

            current_height = rpc.get_block_count(side_port)
            while True:
                main_height = rpc.get_block_count()
                side_height = rpc.get_block_count(side_port)

                Logger.debug("{} main height: {}, side height: {}".format(self.tag, main_height, side_height))

                if side_height - current_height > 10:
                    break

                rpc.discrete_mining(1)
                time.sleep(3)

            balance2 = rpc.get_balance_by_address(self.tap_key_store.address)

            result = float(balance2) - float(balance1) > float(100 - 3 * 10000) / constant.TO_SELA

        return result

    def register_producers_candidates(self):
        num = 0

        global result
        result = False
        for i in range(
                self.params.ela_params.crc_number + 1,
                self.params.ela_params.number - round(self.params.ela_params.later_start_number / 2) + 1
        ):
            ela_node = self.node_manager.ela_nodes[i]
            public_key = ela_node.node_keystore.public_key.hex()
            ret = self.register_producer(ela_node)
            if not ret:
                return False
            rpc.discrete_mining(7)

            status = rpc.producer_status(public_key)
            Logger.debug("After mining 7 blocks, register status: {}".format(status))
            result = status == "Active"
            if not result:
                Logger.error("{} register producer {} failed".format(self.tag, ela_node.name))
                break
            num += 1
            if num <= self.params.ela_params.crc_number * 2:
                self.general_producer_public_keys.append(public_key)
            else:
                self.candidate_public_keys.append(public_key)
            Logger.info("{} register node-{} to be a producer on success!\n".format(self.tag, i))

        return result

    def register_producers(self, start: int, end: int, without_mining=False):
        num = 0
        for i in range(start, end):
            ela_node = self.node_manager.ela_nodes[i]
            public_key = ela_node.node_keystore.public_key.hex()
            ret = self.register_producer(ela_node)
            if not ret:
                return False

            current_height = rpc.get_block_count()
            last_height = current_height
            while True:
                rpc.discrete_mining(1)
                current_height = rpc.get_block_count()
                Logger.debug("{} current height: {}".format(self.tag, current_height))
                if current_height - 6 > last_height:
                    break
                time.sleep(1)

            num += 1
            if num <= self.params.ela_params.crc_number * 2:
                self.general_producer_public_keys.append(public_key)
            else:
                self.candidate_public_keys.append(public_key)
            Logger.info("{} register node-{} to be a producer on success!\n".format(self.tag, i))
        return True

    def update_produces_candidates(self):
        for i in range(len(self.register_producers_list)):
            producer = self.register_producers_list[i]
            payload = producer.info
            payload.nickname = "arbiter-" + str(i)
            ret = self.update_producer(producer, payload)
            if not ret:
                return False
            rpc.discrete_mining(1)
        return True

    def cancel_producers_candidates(self):
        global result
        for producer in self.register_producers_list:
            ret = self.cancel_producer(producer)
            if not ret:
                return False
            rpc.discrete_mining(1)
            status = rpc.producer_status(producer.node.owner_keystore.public_key.hex())
            result = status is "Cancelled"
        return result

    def redeem_producers_candidates(self):
        print("cancel producers size: ", len(self.cancel_producers_list))
        for producer in self.cancel_producers_list:
            ret = self.redeem_producer(producer)
            if not ret:
                return False
            rpc.discrete_mining(1)
        return True

    def vote_producers_candidates(self):
        for i in range(
                self.params.ela_params.crc_number + 1,
                self.params.ela_params.number - round(self.params.ela_params.later_start_number / 2) + 1
        ):
            producer = self.register_producers_list[i - self.params.ela_params.crc_number - 1]
            vote_amount = (self.params.ela_params.number - i + 1) * constant.TO_SELA
            ret = self.vote_producer(
                keystore=self.node_manager.keystore_manager.node_key_stores[i],
                amount=vote_amount,
                candidates=[producer],
            )
            if not ret:
                return False
            rpc.discrete_mining(1)
            Logger.info("{} vote node-{} {} Elas on success!\n".format(self.tag, i, vote_amount))
        return True

    def vote_producers(self, start: int, end: int):
        for i in range(start, end):
            producer = self.register_producers_list[i - self.params.ela_params.crc_number - 1]
            vote_amount = (self.params.ela_params.number - i + 1) * constant.TO_SELA
            ret = self.vote_producer(
                keystore=self.node_manager.keystore_manager.node_key_stores[i],
                amount=vote_amount,
                candidates=[producer]
            )
            if not ret:
                return False
            Logger.info("{} vote node-{} {} Elas on success!\n".format(self.tag, i, vote_amount))
            rpc.discrete_mining(1)
        return True

    def _handle_tx_result(self, tx: Transaction, port=rpc.DEFAULT_PORT):

        # Logger.debug("{} {}".format(self.tag, tx))

        r = tx.serialize()
        response = rpc.send_raw_transaction(r.hex(), port)
        if isinstance(response, dict):
            Logger.error("{} rpc response: {}".format(self.tag, response))
            Logger.error("rpc send raw transaction failed")
            return False

        # response return on success, response is tx hash, but we should reverse it at first
        reverse_res = util.bytes_reverse(bytes.fromhex(response)).hex()
        Logger.debug("{} tx hash : {}".format(self.tag, tx.hash()))
        Logger.debug("{} response: {}".format(self.tag, reverse_res))

        return tx.hash() == reverse_res


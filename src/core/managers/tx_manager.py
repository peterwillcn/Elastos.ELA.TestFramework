#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/5 5:42 PM
# author: liteng


import time


from src.core.tx import txbuild
from src.core.tx.producer import Producer
from src.core.tx.transaction import Transaction
from src.core.services import rpc
from src.core.nodes.ela import ElaNode
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
        self.rpc_port = rpc.DEFAULT_PORT
        self.register_producers_list = list()
        self.cancel_producers_list = list()

        self.tap_account = self.node_manager.keystore_manager.tap_account

    def transfer_asset(self, input_private_key: str, output_addresses: list, amount: int):

        # create transfer asset tx
        tx = txbuild.create_transaction(
            input_private_key=input_private_key,
            output_addresses=output_addresses,
            amount=amount,
            rpc_port=self.rpc_port
        )

        if tx is None:
            return False
        # single sign this tx
        tx = txbuild.single_sign_transaction(input_private_key, tx)

        # return the result
        ret = self.handle_tx_result(tx)

        return ret

    def transfer_cross_chain_asset(self, input_private_key: str, lock_address: str, cross_address: str,
                                   amount: int, recharge: bool, port=rpc.DEFAULT_PORT):
        tx = txbuild.create_cross_chain_transaction(
            input_private_key=input_private_key,
            lock_address=lock_address,
            cross_chain_address=cross_address,
            amount=amount,
            recharge=recharge,
            rpc_port=port
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.warn("cross chain asset transaction: \n{}".format(tx))
        ret = self.handle_tx_result(tx, port)

        return ret

    def register_producer(self, node: ElaNode):

        producer = Producer(
            input_private_key=node.owner_account.private_key(),
            node=node,
            nick_name=node.name,
            url="http://elastos.org",
            location=0,
            net_address="127.0.0.1:" + str(node.arbiter_node_port)
        )
        tx = producer.register(self.rpc_port)

        if tx is None:
            return False

        ret = self.handle_tx_result(tx)
        if ret:
            self.register_producers_list.append(producer)

        return ret

    def update_producer(self, producer: Producer, producer_info: ProducerInfo):
        tx = producer.update(producer_info, self.rpc_port)

        print(tx)
        if tx is None:
            return False

        ret = self.handle_tx_result(tx)

        return ret

    def cancel_producer(self, producer: Producer):
        tx = producer.cancel(self.rpc_port)

        if tx is None:
            return False

        ret = self.handle_tx_result(tx)

        if ret:
            self.cancel_producers_list.append(producer)
        return ret

    def redeem_producer(self, producer: Producer):
        tx = producer.redeem(4999 * constant.TO_SELA, self.rpc_port)

        if tx is None:
            return False

        ret = self.handle_tx_result(tx)

        return ret

    def active_producer(self, producer: Producer):
        tx = producer.active()

        if tx is None:
            return False

        ret = self.handle_tx_result(tx)

        return ret

    def vote_producer(self, input_private_key: str, amount: int, candidates: list):

        candidates_list = list()
        for producer in candidates:
            candidates_list.append(producer.owner_account().public_key())

        tx = txbuild.create_vote_transaction(
            input_private_key=input_private_key,
            candidates_list=candidates_list,
            amount=amount,
            rpc_port=self.rpc_port
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(input_private_key, tx)

        ret = self.handle_tx_result(tx)

        return ret

    def recharge_necessary_keystore(self, input_private_key: str, accounts: list, amount: int):
        addresses = list()
        for a in accounts:
            addresses.append(a.address())

        ret = self.transfer_asset(input_private_key, addresses, amount)

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

        global cross_address
        global side_port
        global result
        global balance_port
        global cross_input_key

        if side_node_type is "did":
            side_port = 10136
            cross_did_account = self.node_manager.keystore_manager.cross_did_account
            cross_address = cross_did_account.address()
            cross_input_key = cross_did_account.private_key()

        elif side_node_type is "token":
            side_port = 10146
            cross_token_account = self.node_manager.keystore_manager.cross_token_account
            cross_address = cross_token_account.address()
            cross_input_key = cross_token_account.private_key()

        elif side_node_type is "neo":
            side_port = 10156
            cross_neo_account = self.node_manager.keystore_manager.cross_neo_account
            cross_address = cross_neo_account.address()
            cross_input_key = cross_neo_account.private_key()

        if recharge:
            port = self.rpc_port
            balance_port = side_port
            input_private_key = self.tap_account.private_key()
            lock_address = self.params.arbiter_params.side_info[side_node_type][constant.SIDE_RECHARGE_ADDRESS]
            amount = 200 * constant.TO_SELA

        else:
            port = side_port
            balance_port = self.rpc_port
            input_private_key = cross_input_key
            lock_address = self.params.arbiter_params.side_info[side_node_type][constant.SIDE_WITHDRAW_ADDRESS]
            cross_address = self.tap_account.address()
            amount = 100 * constant.TO_SELA

        balance1 = rpc.get_balance_by_address(cross_address, balance_port)

        ret = self.transfer_cross_chain_asset(
            input_private_key=input_private_key,
            lock_address=lock_address,
            cross_address=cross_address,
            amount=amount,
            recharge=recharge,
            port=port
        )

        if not ret:
            Logger.error("{} transfer cross chain asset failed".format(self.tag))
            return False

        side_height_begin = rpc.get_block_count(side_port)

        while True:
            main_height = rpc.get_block_count()
            side_height = rpc.get_block_count(side_port)

            Logger.debug("{} main height: {}, side height: {}".format(self.tag, main_height, side_height))

            if side_height - side_height_begin > 10:
                break

            rpc.discrete_mining(1)
            time.sleep(3)

        balance2 = rpc.get_balance_by_address(cross_address, balance_port)
        Logger.debug("{} recharge balance1: {}".format(self.tag, balance1))
        Logger.debug("{} recharge balance2: {}".format(self.tag, balance2))

        if isinstance(balance1, dict):
            before_balance = list(balance1.values())[0]
        else:
            before_balance = balance1

        if isinstance(balance2, dict):
            after_balance = list(balance2.values())[0]
        else:
            after_balance = balance2

        result = (float(after_balance) - float(before_balance)) * constant.TO_SELA > float(amount - 3 * 10000)
        Logger.debug("{} recharge result: {}".format(self.tag, result))

        return result

    def register_producers_candidates(self):

        global result
        result = False
        for i in range(
                self.params.ela_params.crc_number + 1,
                self.params.ela_params.number - round(self.params.ela_params.later_start_number / 2) + 1
        ):
            ela_node = self.node_manager.ela_nodes[i]
            public_key = ela_node.node_account.public_key()
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

            Logger.info("{} register node-{} to be a producer on success!\n".format(self.tag, i))

        return result

    def register_producers(self, start: int, end: int, without_mining=False):
        for i in range(start, end):
            ela_node = self.node_manager.ela_nodes[i]
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
                input_private_key=producer.node_account().private_key(),
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
                input_private_key=producer.node_account().private_key(),
                amount=vote_amount,
                candidates=[producer]
            )
            if not ret:
                return False
            Logger.info("{} vote node-{} {} Elas on success!\n".format(self.tag, i, vote_amount))
            rpc.discrete_mining(1)
        return True

    def handle_tx_result(self, tx: Transaction, port=rpc.DEFAULT_PORT):

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
        Logger.debug("{} reverse:  {}".format(self.tag, response))

        return tx.hash() == reverse_res


#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 2:33 PM
# author: liteng

import time


from src.middle.tools import util
from src.middle.tools import constant
from src.middle.tools.log import Logger
from src.middle.managers.service_manager import ServiceManager

from src.bottom.nodes.ela import ElaNode
from src.bottom.services import rpc2
from src.bottom.tx.assist import Assist
from src.bottom.tx.register_vote.payload import Payload
from src.bottom.tx.register_vote.voter import Voter
from src.bottom.tx.register_vote.producer import Producer
from src.bottom.tx.process_producer import ProcessProducer
from src.bottom.tx.transaction import Transaction
from src.bottom.tx.input import Input
from src.bottom.tx.outpoint import OutPoint
from src.bottom.tx.output import Output
from src.bottom.tx import txbuild
from src.bottom.wallet.keystore import KeyStore


class Deal(object):

    def __init__(self, service_manager: ServiceManager):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.jar_service = service_manager.jar_service
        self.assist = Assist(service_manager.rpc, service_manager.rest)
        self.fee = 10000
        self.register_producers_list = []
        self.update_producers_list = []
        self.cancel_producers_list = []
        self.redeem_producers_list = list()
        self.voter_list = list()
        self.vote_producers_list = list()

    def transfer_asset(self, input_keystore: KeyStore, output_addresses: list, amount: int):
        tx = txbuild.create_transaction(
            keystore=input_keystore,
            output_addresses=output_addresses,
            amount=amount,
            fee=self.fee,
            output_lock=0
        )

        tx = txbuild.single_sign_transaction(input_keystore, tx)
        tx.hash()

        r = tx.serialize()
        response = rpc2.send_raw_transaction(r.hex())
        if isinstance(response, dict):
            Logger.error("rpc send raw transaction failed")
            return False
        reverse_res = util.bytes_reverse(bytes.fromhex(response)).hex()
        Logger.debug("{} tx hash : {}".format(self.tag, tx.hash()))
        Logger.debug("{} response: {}".format(self.tag, reverse_res))

        return tx.hash() == reverse_res

    def vote_producer(self, keystore: KeyStore, amount: int, candidates_list):
        tx = txbuild.create_vote_transaction(
            keystore=keystore,
            cancadites_list=candidates_list,
            amount=amount,
            fee=10000
        )

        tx = txbuild.single_sign_transaction(keystore, tx)
        Logger.debug("vote transaction: \n{}".format(tx))
        r = tx.serialize()

        resp = rpc2.send_raw_transaction(r.hex())
        if isinstance(resp, dict):
            Logger.error("rpc send raw transaction failed")
            return False

        response = util.bytes_reverse(bytes.fromhex(resp)).hex()
        Logger.debug("tx hash : {}".format(tx.hash()))
        Logger.debug("response: {}".format(response))

        return tx.hash() == response

    def ordinary_single_sign(self, input_keystore, output_addresses: list, amount: int, mode="privatekey"):
        inputs, utxos_value = self.assist.gen_inputs_utxo_value(
            input_keystore=input_keystore,
            amount=amount,
            mode=mode
        )

        outputs = self.assist.gen_usual_outputs(
            output_addresses=output_addresses,
            change_address=input_keystore.address,
            utxo_value=utxos_value,
            amount=amount
        )

        jar_response = self.jar_service.gen_tx(inputs, outputs)
        raw_data = jar_response["rawtx"]
        txid = jar_response["txhash"].lower()
        resp = self.assist.rpc.send_raw_transaction(data=raw_data)
        result = util.assert_equal(txid, resp)
        if not result:
            Logger.error("{} Ordinary single sign transaction txid is not equal resp".format(self.tag))
            return result

        self.assist.rpc.discrete_mining(1)
        return True

    def ordinary_multi_sign(self):
        pass

    def cross_chain_transaction(self, input_keystore: KeyStore, lock_address, output_address, amount, port: int):
        balance1 = 0
        balance2 = 0
        if port == self.assist.rpc.DEFAULT_PORT:
            Logger.info("{} before cross transaction input address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(input_keystore.address, port)
            ))

            balance1 = self.assist.rpc.get_balance_by_address(output_address, port + 20)
            Logger.info("{} before cross transaction output address address: {} ELAs".format(
                self.tag,
                balance1
            ))
        else:
            Logger.info("{} before cross transaction input address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(input_keystore.address, port)
            ))

            balance1 = self.assist.rpc.get_balance_by_address(output_address, port - 20)
            Logger.info("{} before cross transaction output address address: {} ELAs".format(
                self.tag,
                balance2
            ))

        inputs, utxo_value = self.assist.gen_inputs_utxo_value(
            input_keystore=input_keystore,
            amount=amount,
            deposit_address="",
            port=port
        )

        outputs = self.assist.gen_usual_outputs(
            output_addresses=[lock_address],
            amount=amount,
            change_address=input_keystore.address,
            utxo_value=utxo_value
        )

        private_key_sign = self.assist.gen_private_sign(input_keystore.private_key.hex())

        cross_chain_asset = self.assist.gen_cross_chain_asset(
            address=output_address,
            amount=amount,
            utxo_value=utxo_value
        )

        jar_response = self.jar_service.gen_cross_chain_transaction(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=private_key_sign,
            crosschainasset=cross_chain_asset
        )

        raw_data = jar_response["rawtx"]
        txid = jar_response["txhash"].lower()
        resp = self.assist.rpc.send_raw_transaction(data=raw_data, port=port)
        Logger.info("{} jar txid = {}".format(self.tag, txid))
        Logger.info("{} rpc resp = {}".format(self.tag, resp))
        result = util.assert_equal(txid, resp)
        if not result:
            Logger.error("{} Ordinary single sign transaction txid is not equal resp".format(self.tag))
            return result

        if port == self.assist.rpc.DEFAULT_PORT:
            for i in range(15):
                self.assist.rpc.discrete_mining(1)
                Logger.info("{} main chain height: {}, side chain height: {}".format(
                    self.tag,
                    self.assist.rpc.get_block_count(),
                    self.assist.rpc.get_block_count(port + 20)
                ))
                if i > 7:
                    time.sleep(2)
                time.sleep(1)

        else:
            for i in range(20):
                self.assist.rpc.discrete_mining(1)
                Logger.info("{} main chain height: {}, side chain height: {}".format(
                    self.tag,
                    self.assist.rpc.get_block_count(),
                    self.assist.rpc.get_block_count(port)
                ))
                time.sleep(3)

        if port == self.assist.rpc.DEFAULT_PORT:
            Logger.info("{} after cross transaction input address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(input_keystore.address, port)
            ))

            balance2 = self.assist.rpc.get_balance_by_address(output_address, port + 20)
            Logger.info("{} after cross transaction output address address: {} ELAs".format(
                self.tag,
                balance2
            ))
        else:
            Logger.info("{} after cross transaction input address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(input_keystore.address, port)
            ))

            balance2 = self.assist.rpc.get_balance_by_address(output_address, port - 20)
            Logger.info("{} after cross transaction output address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(output_address, port - 20)
            ))

        print("balance2: {}".format(balance2))
        print("balance1: {}".format(balance1))
        print("amount: {}".format(amount))

        return float(balance2) - float(balance1) > float(amount - 3 * 10000) / constant.TO_SELA

    def register_a_producer(self, node: ElaNode, without_mining=False):
        producer = Producer(node, self.jar_service, self.assist)
        if without_mining:
            ret = producer.register_without_mining()
            if ret:
                self.register_producers_list.append(producer)
            Logger.debug("register a producer without mining blocks: {}".format(ret))
        else:
            ret = producer.register()
            if ret:
                self.register_producers_list.append(producer)
                Logger.debug("{} node {} has registered a producer!".format(self.tag, node.index))

        return ret

    def update_a_producer(self, producer: Producer, payload: Payload):
        producer.payload = payload
        ret = producer.update()
        if ret:
            self.update_producers_list.append(producer)
            Logger.info("{} node {} has updated a producer!".format(self.tag, producer.node.index))

        return ret

    def cancel_a_producer(self, producer: Producer):
        ret = producer.cancel()
        if ret:
            self.cancel_producers_list.append(producer)
            Logger.info("{} node {} has cancelled a producer!".format(self.tag, producer.node.index))

        return ret

    def redeem_a_producer(self, producer: Producer):
        ret = producer.redeem()
        if ret:
            self.redeem_producers_list.append(producer)
            Logger.info("{} node {} has redeemed a producer!".format(self.tag, producer.node.index))
        return ret

    def activate_a_producer(self, producer: Producer):
        ret = producer.activate()
        if ret:
            Logger.debug("{} node {} has activated a producer!".format(self.tag, producer.node.index))
        return ret

    def vote_a_producer(self, vote_keystore: KeyStore, producer: Producer, vote_amount: int):
        voter = Voter(vote_keystore, self.jar_service, self.assist)

        ret = voter.vote([producer], vote_amount)
        Logger.debug("{} register_vote result: {}".format(self.tag, ret))
        return ret

    def vote_producers(self, vote_keystore: KeyStore, producers: list, vote_amount: int):
        voter = Voter(vote_keystore, self.jar_service, self.assist)

        ret = voter.vote(producers, vote_amount)
        Logger.debug("{} register_vote result: {}".format(self.tag, ret))
        return ret

    def create_transaction(self, inputs: list, outputs: list):
        pass

    @staticmethod
    def create_activate_producer_transaction(node_key_store: KeyStore):
        pub_key = node_key_store.public_key
        pri_key = node_key_store.private_key

        activate_producer = ProcessProducer(pub_key, pri_key)

        tx = Transaction()
        tx.version = Transaction.TX_VERSION_09
        tx.tx_type = Transaction.ACTIVATE_PRODUCER
        tx.payload = activate_producer
        tx.attributes = None
        tx.inputs = None
        tx.outputs = None
        tx.programs = list()
        tx.lock_time = 0

        return tx










#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 2:33 PM
# author: liteng

import time

from src.middle.tools import util
from src.middle.tools.log import Logger
from src.middle.managers.service_manager import ServiceManager

from src.bottom.nodes.ela import ElaNode
from src.bottom.tx.assist import Assist
from src.bottom.tx.register_vote.payload import Payload
from src.bottom.tx.register_vote.voter import Voter
from src.bottom.tx.register_vote.producer import Producer
from src.bottom.wallet.keystore import KeyStore


class Transaction(object):

    def __init__(self, service_manager: ServiceManager):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.jar_service = service_manager.jar_service
        self.assist = Assist(service_manager.rpc, service_manager.rest)
        self.fee = 100
        self.register_producers_list = []
        self.update_producers_list = []
        self.cancel_producers_list = []
        self.redeem_producers_list = list()
        self.voter_list = list()
        self.vote_producers_list = list()

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

        Logger.info("{} port: {}".format(self.tag, port))

        if port == self.assist.rpc.DEFAULT_PORT:
            Logger.info("{} before cross transaction input address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(input_keystore.address, port)
            ))

            Logger.info("{} before cross transaction output address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(output_address, port + 20)
            ))
        else:
            Logger.info("{} before cross transaction input address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(input_keystore.address, port)
            ))

            Logger.info("{} before cross transaction output address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(output_address, port - 20)
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
                    time.sleep(8)
                time.sleep(1)

        else:
            for i in range(10):
                self.assist.rpc.discrete_mining(1)
                Logger.info("{} main chain height: {}, side chain height: {}".format(
                    self.tag,
                    self.assist.rpc.get_block_count(),
                    self.assist.rpc.get_block_count(port)
                ))
                time.sleep(10)

        if port == self.assist.rpc.DEFAULT_PORT:
            Logger.info("{} after cross transaction input address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(input_keystore.address, port)
            ))

            Logger.info("{} after cross transaction output address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(output_address, port + 20)
            ))
        else:
            Logger.info("{} after cross transaction input address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(input_keystore.address, port)
            ))

            Logger.info("{} after cross transaction output address address: {} ELAs".format(
                self.tag,
                self.assist.rpc.get_balance_by_address(output_address, port - 20)
            ))

        return True

    def register_a_producer(self, node: ElaNode):
        producer = Producer(node, self.jar_service, self.assist)
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
        self.voter_list.append(voter)

        ret = voter.vote([producer], vote_amount)
        if ret:
            self.vote_producers_list.append({"voter": voter, "producer": producer})
        Logger.debug("{} register_vote result: {}".format(self.tag, ret))
        return ret









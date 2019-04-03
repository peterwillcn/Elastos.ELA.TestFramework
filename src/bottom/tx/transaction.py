#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 2:33 PM
# author: liteng

from src.middle.common import util
from src.middle.common.log import Logger

from src.bottom.nodes.ela import ElaNode
from src.bottom.tx.assist import Assist
from src.bottom.tx.vote.payload import Payload
from src.bottom.tx.vote.voter import Voter
from src.bottom.tx.vote.producer import Producer
from src.bottom.services.jar import JarService


class Transaction(object):

    def __init__(self, jar_service: JarService, assist: Assist):
        self.tag = "[src.bottom.tx.transaction.Transaction]"
        self.jar_service = jar_service
        self.assist = assist
        self.fee = 100
        self.register_producers_list = list()
        self.update_producers_list = list()
        self.cancel_producers_list = list()
        self.redeem_producers_list = list()
        self.voter_list = list()
        self.vote_producers_list = list()

    def ordinary_single_sign(self, input_keystore, output_addresses, amount, fee=100, mode="privatekey"):
        inputs, utxos_value = self.assist.gen_inputs_utxos_value(input_keystore=input_keystore,
                                                                 amount=amount, fee=fee, mode=mode)
        outputs = self.assist.gen_single_sign_outputs(output_addresses, input_keystore.address, utxos_value, amount)
        jar_response = self.jar_service.create_transaction(inputs, outputs)
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

    def recharge_coin(self):
        pass

    def withdraw_coin(self):
        pass

    def register_a_producer(self, node: ElaNode):
        producer = Producer(node, self.jar_service, self.assist)
        ret = producer.register()
        if ret:
            self.register_producers_list.append(producer)

        return ret

    def update_a_producer(self, producer: Producer, payload: Payload):
        producer.payload = payload
        ret = producer.update()
        if ret:
            self.update_producers_list.append(producer)

        return ret

    def cancel_a_producer(self, producer: Producer):
        ret = producer.cancel()
        if ret:
            self.cancel_producers_list.append(producer)

        return ret

    def redeem_a_producer(self, producer: Producer):
        pass

    def vote_a_producer(self, vote_node: ElaNode, producer: Producer):
        voter = Voter(vote_node, [producer], self.jar_service, self.assist)
        self.voter_list.append(voter)

        ret = voter.vote()
        if ret:
            self.vote_producers_list.append({"voter": voter, "producer": producer})

        return ret







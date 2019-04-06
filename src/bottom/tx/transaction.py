#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 2:33 PM
# author: liteng

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
            Logger.debug("{} node {} has registered a producer!".format(self.tag, node.index))

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

    def vote_a_producer(self, vote_keystore: KeyStore, producer: Producer, vote_amount: int):
        voter = Voter(vote_keystore, self.jar_service, self.assist)
        self.voter_list.append(voter)

        ret = voter.vote([producer], vote_amount)
        if ret:
            self.vote_producers_list.append({"voter": voter, "producer": producer})
        Logger.debug("{} register_vote result: {}".format(self.tag, ret))
        return ret









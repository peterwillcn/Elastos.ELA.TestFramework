#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 2:33 PM
# author: liteng

from logs.log import Logger
from core.deal.assist import Assist
from core.service.rpc import RPC
from core.service.rest import REST
from core.service.jar import JarService


class Transaction(object):

    def __init__(self, jar_service: JarService, rpc: RPC, rest: REST):
        self.tag = '[core.deal.transaction.Transaction]'
        self.jar_service = jar_service
        self.rpc = rpc
        self.rest = rest
        self.assist = Assist(self.rpc)

    def ordinary_single_sign(self, input_keystore, output_addresses, amount, fee=100, mode='address'):
        inputs, utxos_value = self.assist.gen_inputs_utxos_value(input_keystore, amount, fee, mode)
        Logger.debug('{} ordinary single sign inputs: {}'.format(self.tag, inputs))
        Logger.debug('{} utxos value: {}'.format(self.tag, utxos_value))
        outputs = self.assist.gen_single_sign_outputs(output_addresses, input_keystore.address, utxos_value, amount)
        Logger.debug('{} outputs: {}'.format(self.tag, outputs))
        jar_response = self.jar_service.create_transaction(inputs, outputs)
        raw_data = jar_response["rawtx"]
        txid = jar_response["txhash"].lower()
        resp = self.rpc.send_raw_transaction(data=raw_data)
        result = resp == txid
        if not result:
            Logger.error('{} Ordinary single sign transaction txid is not equal resp'.format(self.tag))
            return result

        self.rpc.discrete_mining(1)
        return True

    def ordinary_multi_sign(self):
        pass

    def recharge_coin(self):
        pass

    def withdraw_coin(self):
        pass

    def register_producer(self):
        pass

    def update_producer(self):
        pass

    def vote_producer(self):
        pass

    def cancel_producer(self):
        pass

    def redeem_producer(self):
        pass
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 2:31 PM
# author: liteng

from core.service.rpc import RPC
from logs.log import Logger
from decimal import Decimal


class Assist(object):

    def __init__(self, rpc: RPC):
        self.tag = '[core.deal.assist.Assist]'
        self.rpc = rpc

    def collect_utxos_by_keystore(self, input_keystore, assetid=None):
        utxos_resp = self.rpc.list_unspent_utxos(addresses=input_keystore.address, assetid=assetid)
        if not utxos_resp:
            Logger.error('{} gen unspent utxos response: {}'.format(self.tag, utxos_resp))
            exit(-1)

        utxos = []
        for utxo in utxos_resp:
            utxos.append({'txid': utxo['txid'], 'index': utxo['vout'], 'amount': utxo['amount'],
                          'address': utxo['address'], 'privatekey': input_keystore.private_key.hex()})
        return utxos

    @staticmethod
    def get_utxos_amount(utxos):
        amount = 0
        if not isinstance(utxos, list):
            utxos = [utxos]
        for utxo in utxos:
            amount += float(utxo['amount']) * 100000000
        return int(amount)

    def get_enough_value_for_amount(self, utxos, amount, fee, utxo_value=0, index=-1, quantity=0):
        if amount < 0:
            Logger.error('{} Invalid argument amount: {}'.format(self.tag, amount))
            exit(-1)

        if utxo_value <= amount + fee and amount >= 0:
            index += 1
            utxo_value += self.get_utxos_amount(utxos[index])
            quantity += 1
            return self.get_enough_value_for_amount(utxos, amount, fee, utxo_value, index, quantity)

        else:
            return {'value': utxo_value, 'quantity': quantity}

    def gen_inputs_utxos_value(self, input_keystore, amount: int, fee=100, mode='address'):
        invalid_utxos = self.collect_utxos_by_keystore(input_keystore)
        value_quantity = self.get_enough_value_for_amount(utxos=invalid_utxos, amount=amount, fee=fee)
        utxos_value = value_quantity['value']
        utxos_quantitiy = value_quantity['quantity']
        inputs = []
        for utxo in invalid_utxos[0:utxos_quantitiy]:
            inputs.append({"txid": utxo["txid"], "vout": utxo["index"], mode: utxo[mode]})
        return inputs, utxos_value

    def gen_normal_outputs(self, addresses: list, amount: int, change_address: str, utxo_value: int, fee=100):
        if utxo_value < ((amount + fee) * len(addresses) + 1):
            Logger.error('{} utxo is not enough!'.format(self.tag))
            return None
        else:
            change_value = utxo_value - (amount + fee) * len(addresses)
            change_value = str(Decimal(str(change_value)) / Decimal(100000000))
            amount = str(Decimal(str(amount)) / Decimal(100000000))
            output = []
            for addr in addresses:
                output.append({"address": addr, "amount": amount})
            if not float(change_value) == 0:
                output.append({"address": change_address, "amount": change_value})
            return output

    def gen_single_sign_outputs(self, output_addresses, change_address, utxos_value: int, amount: int):
        outputs = self.gen_normal_outputs(
            addresses=output_addresses,
            amount=amount,
            change_address=change_address,
            utxo_value=utxos_value,
        )
        return outputs
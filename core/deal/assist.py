#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 2:31 PM
# author: liteng

from logs.log import Logger
from decimal import Decimal
from core.service.rpc import RPC
from core.service.rest import REST


class Assist(object):

    def __init__(self, rpc: RPC, rest: REST):
        self.tag = '[core.deal.assist.Assist]'
        self.rpc = rpc
        self.rest = rest

    def _collect_utxos_by_keystore(self, input_keystore, deposit_address: str):
        if deposit_address != '':
            utxos_resp = self.rpc.list_unspent_utxos(addresses=deposit_address, assetid='None')
        else:
            utxos_resp = self.rpc.list_unspent_utxos(addresses=input_keystore.address, assetid='None')
        if not utxos_resp:
            Logger.error('{} gen unspent utxos response: {}'.format(self.tag, utxos_resp))
            exit(-1)

        utxos = []
        for utxo in utxos_resp:
            utxos.append({'txid': utxo['txid'], 'index': utxo['vout'], 'amount': utxo['amount'],
                          'address': utxo['address'], 'privatekey': input_keystore.private_key.hex()})
        return utxos

    def _get_utxos_amount(self, utxos):
        amount = 0
        if not isinstance(utxos, list):
            utxos = [utxos]
        for utxo in utxos:
            amount += float(utxo['amount']) * 100000000
        return int(amount)

    def _get_enough_value_for_amount(self, utxos, amount, fee, utxo_value=0, index=-1, quantity=0):
        if amount < 0:
            Logger.error('{} Invalid argument amount: {}'.format(self.tag, amount))
            exit(-1)

        if utxo_value <= amount + fee and amount >= 0:
            index += 1
            utxo_value += self._get_utxos_amount(utxos[index])
            quantity += 1
            return self._get_enough_value_for_amount(utxos, amount, fee, utxo_value, index, quantity)

        else:
            return {'value': utxo_value, 'quantity': quantity}

    def gen_inputs_utxos_value(self, input_keystore, amount: int, deposit_address='', fee=100, mode='address'):
        invalid_utxos = self._collect_utxos_by_keystore(input_keystore, deposit_address)
        value_quantity = self._get_enough_value_for_amount(utxos=invalid_utxos, amount=amount, fee=fee)
        utxos_value = value_quantity['value']
        utxos_quantitiy = value_quantity['quantity']
        inputs = []
        for utxo in invalid_utxos[0:utxos_quantitiy]:
            inputs.append({"txid": utxo["txid"], "vout": utxo["index"], mode: utxo[mode]})
        return inputs, utxos_value

    def _gen_normal_outputs(self, addresses: list, amount: int, change_address: str, utxo_value: int, fee=100):
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
        outputs = self._gen_normal_outputs(
            addresses=output_addresses,
            amount=amount,
            change_address=change_address,
            utxo_value=utxos_value,
        )
        return outputs

    def gen_private_sign(self, privatekey):
        output = []
        output.append({"privatekey": privatekey})
        return output

    def gen_register_producer_output(self, deposit_address: str, amount: int, change_address: str, utxo_value: int,
                                     fee=10000):
        if utxo_value < amount + fee + 1:
            Logger.error('{} utxo value is not enough!'.format(self.tag))
            return None

        else:
            change_value = utxo_value - fee - amount
            change_value = str(Decimal(str(change_value)) / Decimal(100000000))
            amount = str(Decimal(str(amount)) / Decimal(100000000))
            output = []
            output.append({"address": deposit_address, "amount": amount})
            if change_value != 0:
                output.append({"address": change_address, "amount": change_value})
        return output

    def gen_update_producer_output(self, address: str, utxo_value: int, fee=100):
        if utxo_value < fee + 1:
            Logger.error('{} utxo value is not enough?!'.format(self.tag))
            return None

        else:
            change_value = utxo_value - fee
            change_value = str(Decimal(str(change_value)) / Decimal(100000000))
            outputs = []
            outputs.append({"address": address, "amount": change_value})
        return outputs

    def gen_cancel_producer_output(self, address: str, utxo_value: int, fee=100):
        if utxo_value < fee + 1:
            Logger.error('{} utxo value is not enough!'.format(self.tag))
            return None

        else:
            change_value = utxo_value - fee
            change_value = str(Decimal(str(change_value)) / Decimal(100000000))
            outputs = []
            outputs.append({"address": address, "amount": change_value})
        return outputs

    def gen_redeem_producer_output(self, address: str, utxo_value: int, fee=10000):
        if utxo_value < fee + 1:
            Logger.error('{} utxo value is not enough!'.format(self.tag))
            return None

        else:
            change_value = utxo_value - fee
            change_value = str(Decimal(str(change_value)) / Decimal(100000000))
            outputs = []
            outputs.append({"address": address, "amount": change_value})
        return outputs

    def gen_vote_outputs_contents_candidates(self, candidate_publickeys):
        candidates = []
        for publickey in candidate_publickeys:
            candidates.append({"publickey": publickey})
        if len(candidates) == 0:
            return None

        return candidates

    def gen_vote_outputs_contents(self, votetype: int, candidates):
        contents = []
        contents.append({"votetype": votetype, "candidates": candidates})
        return contents

    def gen_vote_outputs(self, vote_address: str, change_address: str, utxos_value: int, vote_amount: int, outputtype: int,
                         version: int, contents, fee=100):
        if utxos_value < fee + 1 + vote_amount:
            Logger.error('{} utxo value is not enough!'.format(self.tag))
            return None

        else:
            change_value = utxos_value - fee - vote_amount
            change_value = str(Decimal(str(change_value)) / Decimal(100000000))
            amount = str(Decimal(str(vote_amount)) / Decimal(100000000))
            output = []
            output.append({"address": vote_address, "amount": amount, "outputtype": outputtype,
                           "version": version, "contents": contents})
            if not float(change_value) == 0:
                output.append({"address": change_address, "amount": change_value})
            return output


    def gen_register_producer_payload(self, privatekey, owner_publickey, node_publickey,
                                      nickname, url, location, address):
        return {
                "privatekey": privatekey,
                "ownerpublickey": owner_publickey,
                "nodepublickey": node_publickey,
                "nickname": nickname,
                "url": url,
                "location": location,
                "address": address,
            }

    def gen_update_producer_payload(self, privatekey, owner_publickey, node_publickey,
                                    nickname, url, location, address):
        return {
                "privatekey": privatekey,
                "ownerpublickey": owner_publickey,
                "nodepublickey": node_publickey,
                "nickname": nickname,
                "url": url,
                "location": location,
                "address": address
            }

    def gen_cancel_producer_payload(self, privatekey, publickey):
        return {"privatekey": privatekey, "publickey": publickey}
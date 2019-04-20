#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 2:31 PM
# author: liteng

from decimal import Decimal

from src.middle.tools import util
from src.middle.tools import constant
from src.middle.tools.log import Logger

from src.bottom.services.rpc import RPC
from src.bottom.services.rest import REST
from src.bottom.wallet.keystore import KeyStore


class Assist(object):

    def __init__(self, rpc: RPC, rest: REST):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.rpc = rpc
        self.rest = rest

    def collect_unspent_utxos(self, address: str, private_key: str, port: int):
        utxos_response = self.rpc.list_unspent_utxos(addresses=address, assetid="None", port=port)

        if not utxos_response:
            Logger.error("{} gen unspent utxos response: {}".format(self.tag, utxos_response))
            exit(-1)

        unspend_utxos = list()
        for utxo in utxos_response:
            if "txtype" in utxo.keys() and utxo["txtype"] == 0 and utxo["confirmations"] <= 100:
                continue
            unspend_utxos.append(
                {
                    "txid": utxo["txid"],
                    "index": utxo["vout"],
                    "amount": utxo["amount"],
                    "address": utxo["address"],
                    "privatekey": private_key
                }
            )
        return unspend_utxos

    def collect_enough_utxos(self, unspect_utxos, amount, fee):
        if amount < 0 or fee < 0:
            Logger.error("{} Invalid argument amount: {} {}".format(self.tag, amount, fee))
            exit(-1)

        utxo_value = 0
        index = -1
        while utxo_value <= (amount + fee):
            index += 1
            utxo_value += int(float(unspect_utxos[index]["amount"]) * constant.TO_SELA)
            Logger.debug("### {} index = {}, utxo_value = {}, amount + fee = {}".format(self.tag, index, utxo_value,
                                                                                        amount + fee))
        return {"value": utxo_value, "quantity": index + 1}

    def gen_inputs_utxo_value(self, input_keystore: KeyStore, amount: int, deposit_address="",
                              fee=10000, mode="address", port=RPC.DEFAULT_PORT):
        if deposit_address != "":
            unspent_utxos = self.collect_unspent_utxos(deposit_address, "", port)
        else:
            unspent_utxos = self.collect_unspent_utxos(input_keystore.address, input_keystore.private_key.hex(), port)
        # value_quantity = self._get_enough_value_for_amount(utxos=invalid_utxos, amount=amount, fee=fee)
        value_quantity = self.collect_enough_utxos(unspent_utxos, amount, fee)
        utxo_value = value_quantity["value"]
        utxos_quantitiy = value_quantity["quantity"]
        inputs = []
        for utxo in unspent_utxos[0:utxos_quantitiy]:
            inputs.append({"txid": utxo["txid"], "vout": utxo["index"], mode: utxo[mode]})
        return inputs, utxo_value

    def gen_usual_outputs(self, output_addresses: list, amount: int, change_address: str, utxo_value: int, fee=10000):
        if utxo_value < amount * len(output_addresses) + fee + 1:
            Logger.error("{} utxo is not enough!".format(self.tag))
            return None
        else:
            change_value = utxo_value - amount * len(output_addresses) - fee
            change_value = str(Decimal(str(change_value)) / Decimal(constant.TO_SELA))
            amount = str(Decimal(str(amount)) / Decimal(constant.TO_SELA))
            output = list()
            if float(amount):
                for addr in output_addresses:
                    output.append({"address": addr, "amount": amount})
            if float(change_value):
                output.append({"address": change_address, "amount": change_value})
            return output

    @staticmethod
    def gen_private_sign(privatekey):
        output = list()
        output.append({"privatekey": privatekey})
        return output

    def gen_cross_chain_asset(self, address: str, amount: int, utxo_value: int, fee=10000):
        if utxo_value < amount + fee + 1:
            Logger.error("{} utxo is not enough!".format(self.tag))
            return None
        asset = list()
        amount = str(Decimal(amount - 10000) / Decimal(constant.TO_SELA))
        asset.append({"address": address, "amount": amount})
        return asset
            
    @staticmethod
    def gen_vote_outputs_contents_candidates(candidate_publickeys):
        candidates = list()
        for publickey in candidate_publickeys:
            candidates.append({"publickey": publickey})
        if len(candidates) == 0:
            return None

        return candidates

    @staticmethod
    def gen_vote_outputs_contents(votetype: int, candidates):
        contents = list()
        contents.append({"votetype": votetype, "candidates": candidates})
        return contents

    def gen_vote_outputs(self, vote_address: str, change_address: str, utxo_value: int, vote_amount: int, outputtype: int,
                         version: int, contents, fee=100):
        if utxo_value < fee + 1 + vote_amount:
            Logger.error("{} utxo value is not enough!".format(self.tag))
            return None

        else:
            change_value = utxo_value - fee - vote_amount
            change_value = str(Decimal(str(change_value)) / Decimal(constant.TO_SELA))
            amount = str(Decimal(str(vote_amount)) / Decimal(constant.TO_SELA))
            output = list()
            output.append({"address": vote_address, "amount": amount, "outputtype": outputtype,
                           "version": version, "contents": contents})
            if not float(change_value) == 0:
                output.append({"address": change_address, "amount": change_value})
            return output

    @staticmethod
    def gen_register_producer_payload(privatekey, owner_publickey, node_publickey,
                                      nickname, url, location, netaddress):
        return {
                "privatekey": privatekey,
                "ownerpublickey": owner_publickey,
                "nodepublickey": node_publickey,
                "nickname": nickname,
                "url": url,
                "location": location,
                "netaddress": netaddress,
            }


    @staticmethod
    def gen_update_producer_payload(privatekey, owner_publickey, node_publickey,
                                    nickname, url, location, netaddress):
        return {
                "privatekey": privatekey,
                "ownerpublickey": owner_publickey,
                "nodepublickey": node_publickey,
                "nickname": nickname,
                "url": url,
                "location": location,
                "netaddress": netaddress
            }

    @staticmethod
    def gen_cancel_producer_payload(privatekey, owner_publickey):
        return {"privatekey": privatekey, "ownerpublickey": owner_publickey}
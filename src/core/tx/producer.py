#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/3 4:49 PM
# author: liteng

from elasdk.common import util
from elasdk.tx.payload.producer_info import ProducerInfo
from elasdk.tx import txbuild
from elasdk.wallet.account import Account


class Producer(object):

    def __init__(self, input_private_key: str, owner_private_key: str, node_private_key: str,
                 nick_name: str, url: str, location: int, net_address: str):
        self.input_private_key = input_private_key
        self.input = Account(input_private_key)
        self.utxo_value = 0
        self.fee = 10000
        self.state = ""
        self.deposit_amount = 5000 * util.TO_SELA
        self.info = self._producer_info(owner_private_key, node_private_key, nick_name, url, location, net_address)

    @staticmethod
    def _producer_info(owner_private_key: str, node_private_key: str, nick_name: str, url: str,
                       location: int, net_address: str):
        info = ProducerInfo(
            owner_private_key=owner_private_key,
            node_private_key=node_private_key,
            nickname=nick_name,
            url=url,
            location=location,
            net_address=net_address
        )
        return info

    def producer_info(self):
        return self.info

    def input_account(self):
        return self.input

    def owner_account(self):
        return self.producer_info().owner_account

    def node_account(self):
        return self.producer_info().node_account

    def register(self, rpc_port: int):
        tx = txbuild.create_register_transaction(
            input_private_key=self.input_private_key,
            amount=self.deposit_amount,
            payload=self.info,
            rpc_port=rpc_port
        )

        if tx is None:
            return None

        tx = txbuild.single_sign_transaction(self.input_private_key, tx)

        return tx

    def update(self, producer_info: ProducerInfo, rpc_port):
        tx = txbuild.create_update_transaction(
            input_private_key=self.input_private_key,
            payload=producer_info,
            rpc_port=rpc_port
        )

        if tx is None:
            return None
        producer_info.gen_signature()
        tx = txbuild.single_sign_transaction(self.input_private_key, tx)

        return tx

    def cancel(self, rpc_port: int):
        tx = txbuild.create_cancel_transaction(
            input_private_key=self.input_private_key,
            payload=self.producer_info(),
            rpc_port=rpc_port
        )

        if tx is None:
            return None

        tx = txbuild.single_sign_transaction(self.input_private_key, tx)

        return tx

    def redeem(self, amount: int, rpc_port: int):

        tx = txbuild.create_redeem_transaction(
            payload=self.producer_info(),
            output_address=self.input.address(),
            amount=amount,
            rpc_port=rpc_port
        )

        if tx is None:
            return None

        tx = txbuild.single_sign_transaction(self.producer_info().owner_account.private_key(), tx)

        return tx

    def active(self):

        # note activate producer transaction needn't to sign the whole transaction
        tx = txbuild.create_active_transaction(self.node_account().private_key(), self.node_account().public_key())

        if tx is None:
            return None

        return tx

    def __repr__(self):
        return self.producer_info().__repr__()




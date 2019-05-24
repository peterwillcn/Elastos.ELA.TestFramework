#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/3 4:49 PM
# author: liteng

from sdk.common import util
from sdk.common.log import Logger

from sdk.tx.payload.producer_info import ProducerInfo
from sdk.tx import txbuild
from sdk.wallet.account import Account


class Producer(object):

    def __init__(self, input_private_key: str, owner_private_key: str, node_private_key: str,
                 nick_name: str, url: str, location: int, net_address: str):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.input_private_key = input_private_key
        self.input_account = Account(input_private_key)
        self.utxo_value = 0
        self.fee = 10000
        self.state = ""
        self.deposit_amount = 5000 * util.TO_SELA
        self.info = self._producer_info(owner_private_key, node_private_key, nick_name, url, location, net_address)

    def _producer_info(self, owner_private_key: str, node_private_key: str, nick_name: str, url: str,
                       location: int, net_address: str):
        info = ProducerInfo(
            owner_private_key=owner_private_key,
            node_private_key=node_private_key,
            nickname=nick_name,
            url=url,
            location=location,
            net_address=net_address
        )
        Logger.debug("{} generate register producer payload: {}".format(self.tag, info))
        return info

    def get_payload(self):
        return self.info

    def input_private_key(self):
        return self.input_private_key

    def input_public_key(self):
        return self.input_account.public_key()

    def owner_private_key(self):
        return self.get_payload().owner_account.private_key()

    def owner_public_key(self):
        return self.get_payload().owner_account.public_key()

    def node_private_key(self):
        return self.get_payload().node_account.private_key()

    def node_public_key(self):
        return self.get_payload().node_account.public_key()

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
            payload=self.get_payload(),
            rpc_port=rpc_port
        )

        if tx is None:
            return None

        tx = txbuild.single_sign_transaction(self.input_private_key, tx)

        return tx

    def redeem(self, amount: int, rpc_port: int):

        tx = txbuild.create_redeem_transaction(
            payload=self.get_payload(),
            output_address=self.input_account.address(),
            amount=amount,
            rpc_port=rpc_port
        )

        if tx is None:
            return None

        tx = txbuild.single_sign_transaction(self.get_payload().owner_account.private_key(), tx)

        return tx

    def activate(self):

        # note activate producer transaction needn't to sign the whole transaction
        tx = txbuild.create_activate_producer(self.get_payload())

        if tx is None:
            return None

        return tx




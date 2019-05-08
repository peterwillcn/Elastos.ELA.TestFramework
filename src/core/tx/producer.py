#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/3 4:49 PM
# author: liteng

from src.tools import util, constant
from src.tools.log import Logger

from src.core.nodes.ela import ElaNode
from src.core.services import rpc
from src.core.wallet import keytool
from src.core.tx.payload.producer_info import ProducerInfo
from src.core.tx import txbuild


class Producer(object):

    def __init__(self, node: ElaNode):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.node = node
        self.utxo_value = 0
        self.fee = 10000
        self.state = ""
        self.deposit_address = keytool.gen_deposit_address(self.node.owner_keystore.program_hash)
        self.output_address = self.node.owner_keystore.address
        self.deposit_amount = 5000 * constant.TO_SELA
        self.info = self._producer_info()

    def _producer_info(self):
        info = ProducerInfo(
            private_key=self.node.owner_keystore.private_key,
            owner_public_key=self.node.owner_keystore.public_key,
            node_public_key=self.node.node_keystore.public_key,
            nickname="PRO-{:0>3d}".format(self.node.index),
            url="https://elastos.org",
            location=0,
            net_address="127.0.0.1:" + str(self.node.reset_port(self.node.index, "ela", "arbiter_node_port"))
        )
        return info

    def register(self):
        tx = txbuild.create_register_transaction(
            keystore=self.node.owner_keystore,
            output_addresses=[self.deposit_address],
            amount=self.deposit_amount,
            payload=self.info
        )

        if tx is None:
            return None

        tx = txbuild.single_sign_transaction(self.node.owner_keystore, tx)

        return tx

    def update(self, producer_info: ProducerInfo):
        tx = txbuild.create_update_transaction(
            keystore=self.node.owner_keystore,
            payload=producer_info,
        )

        if tx is None:
            return None
        producer_info.gen_signature()
        tx = txbuild.single_sign_transaction(self.node.owner_keystore, tx)

        return tx

    def cancel(self):
        tx = txbuild.create_cancel_transaction(self.node.owner_keystore)

        if tx is None:
            return None

        tx = txbuild.single_sign_transaction(self.node.owner_keystore, tx)

        return tx

    def redeem(self):

        tx = txbuild.create_redeem_transaction(self.node.owner_keystore, amount=4999 * constant.TO_SELA)

        if tx is None:
            return None

        tx = txbuild.single_sign_transaction(self.node.owner_keystore, tx)

        return tx

    def activate(self):

        # note activate producer transaction needn't to sign the whole transaction
        tx = txbuild.create_activate_producer(self.node.node_keystore)

        if tx is None:
            return None

        return tx


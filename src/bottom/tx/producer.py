#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/3 4:49 PM
# author: liteng

from src.middle.tools import constant
from src.middle.tools import util
from src.middle.tools.log import Logger

from src.bottom.nodes.ela import ElaNode
from src.bottom.services import rpc2
from src.bottom.wallet import keytool
from src.bottom.tx.producer_info import ProducerInfo
from src.bottom.tx import txbuild


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

    def register(self, before_h1: bool):
        tx = txbuild.create_register_transaction(
            keystore=self.node.owner_keystore,
            output_addresses=[self.deposit_address],
            amount=self.deposit_amount,
            payload=self.info
        )

        tx = txbuild.single_sign_transaction(self.node.owner_keystore, tx)

        r = tx.serialize()
        tx.hash()
        Logger.debug("{} {}".format(self.tag, tx))
        Logger.debug("{} tx serialize: {}".format(self.tag, r.hex()))

        resp = rpc2.send_raw_transaction(r.hex())
        Logger.debug("{} resp: {}".format(self.tag, resp))
        if type(resp) is not dict:
            resp = util.bytes_reverse(bytes.fromhex(resp)).hex()
        if before_h1:
            rpc2.discrete_mining(6)
        else:
            rpc2.discrete_mining(1)
        return resp == tx.hash()

    def update(self):
        tx = txbuild.create_update_transaction(
            keystore=self.node.owner_keystore,
            payload=self.info,
        )

        tx = txbuild.single_sign_transaction(self.node.owner_keystore, tx)

        r = tx.serialize()
        tx.hash()
        Logger.debug("{} {}".format(self.tag, tx))
        Logger.debug("{} tx serialize: {}".format(self.tag, r.hex()))

        resp = rpc2.send_raw_transaction(r.hex())
        Logger.debug("{} resp: {}".format(self.tag, resp))
        if type(resp) is not dict:
            resp = util.bytes_reverse(bytes.fromhex(resp)).hex()
        rpc2.discrete_mining(1)

        return resp == tx.hash()

    def cancel(self):
        tx = txbuild.create_cancel_transaction(self.node.owner_keystore)
        tx = txbuild.single_sign_transaction(self.node.owner_keystore, tx)

        r = tx.serialize()
        resp = rpc2.send_raw_transaction(r.hex())
        Logger.debug("{} resp: {}".format(self.tag, resp))
        if isinstance(resp, dict):
            Logger.error("{} send raw transaction error".format(self.tag))
            return False

        response = util.bytes_reverse(bytes.fromhex(resp)).hex()
        rpc2.discrete_mining(1)
        Logger.debug("{} tx hash : {}".format(self.tag, tx.hash()))
        Logger.debug("{} response: {}".format(self.tag, response))

        return tx.hash() == response

    def redeem(self):

        tx = txbuild.create_redeem_transaction(self.node.owner_keystore, amount=200 * constant.TO_SELA)
        tx = txbuild.single_sign_transaction(self.node.owner_keystore, tx)
        Logger.debug("{} redeem transaction: \n{}".format(self.tag, tx))
        r = tx.serialize()
        resp = rpc2.send_raw_transaction(r.hex())
        Logger.debug("{} resp: {}".format(self.tag, resp))

        if isinstance(resp, dict):
            Logger.error("{} send raw transaction error".format(self.tag))
            return False

        response = util.bytes_reverse(bytes.fromhex(resp)).hex()
        rpc2.discrete_mining(1)
        Logger.debug("{} tx hash : {}".format(self.tag, tx.hash()))
        Logger.debug("{} response: {}".format(self.tag, response))

        return tx.hash() == response

    def activate(self):

        # note activate producer transaction needn't to sign the whole transaction
        tx = txbuild.create_activate_producer(self.node.node_keystore)

        r = tx.serialize()

        resp = rpc2.send_raw_transaction(r.hex())
        Logger.debug("{} resp: {}".format(self.tag, resp))

        if isinstance(resp, dict):
            Logger.error("{} send raw transaction error".format(self.tag))
            return False

        response = util.bytes_reverse(bytes.fromhex(resp)).hex()
        rpc2.discrete_mining(1)
        Logger.debug("{} tx hash : {}".format(self.tag, tx.hash()))
        Logger.debug("{} response: {}".format(self.tag, response))

        return resp == tx.hash()

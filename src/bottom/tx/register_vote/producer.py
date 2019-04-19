#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/3 4:49 PM
# author: liteng

import time

from src.middle.tools import constant
from src.middle.tools import util
from src.middle.tools.log import Logger

from src.bottom.nodes.ela import ElaNode
from src.bottom.services.jar import JarService
from src.bottom.tx.assist import Assist
from src.bottom.tx.register_vote.payload import Payload


class Producer(object):

    PRODUCER_REGISTER = "Register Producer"
    PRODUCER_UPDATE = "Update Producer"
    PRODUCER_CANCEL = "Cancel producer"
    PRODUCER_REDEEM = "Redeem Producer"
    PRODUCER_ACTIVATE = "Activate Producer"

    def __init__(self, node: ElaNode, jar_service: JarService, assist: Assist):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.node = node
        self.jar_service = jar_service
        self.assist = assist
        self.utxo_value = 0
        self.fee = 10000
        self.registered = False
        self.canceled = False
        self.updated = False
        self.redeemed = False
        self.output_address = self.node.owner_keystore.address
        self.deposit_amount = 5000 * constant.TO_SELA
        self.payload = self._init_payload()
        self.deposit_address = jar_service.gen_pledge_address(self.node.owner_keystore.public_key.hex())
        self.privatekeysign = self.assist.gen_private_sign(self.node.owner_keystore.private_key.hex())

    def _init_payload(self):
        payload = Payload(
            private_key=self.node.owner_keystore.private_key.hex(),
            owner_public_key=self.node.owner_keystore.public_key.hex(),
            node_public_key=self.node.node_keystore.public_key.hex(),
            nickname="Producer-" + str(self.node.index),
            url="https://elastos.org",
            location=0,
            net_address="127.0.0.1:" + str(self.node.reset_port(self.node.index, "ela", "arbiter_node_port"))
        )
        return payload

    def _inputs(self, category: str):
        deposit_address = ""
        amount = 0
        if category == self.PRODUCER_REDEEM:
            deposit_address = self. deposit_address
            amount = self.deposit_amount - self.fee - 1
        elif category == self.PRODUCER_REGISTER:
            amount = self.deposit_amount

        inputs, utxo_value = self.assist.gen_inputs_utxo_value(
            self.node.owner_keystore,
            amount,
            deposit_address=deposit_address
        )
        self.utxo_value = utxo_value
        Logger.debug("{} {} amount: {}".format(self.tag, category, amount))
        Logger.debug("{} {} inputs: {}".format(self.tag, category, inputs))
        Logger.debug("{} {} utxo_value: {}".format(self.tag, category, utxo_value))
        return inputs

    def _outputs(self, category: str):

        if category == self.PRODUCER_REGISTER:
            outputs = self.assist.gen_usual_outputs(
                output_addresses=[self.deposit_address],
                amount=self.deposit_amount,
                change_address=self.output_address,
                utxo_value=self.utxo_value
            )

        else:
            outputs = self.assist.gen_usual_outputs(
                output_addresses=[self.output_address],
                amount=0,
                change_address=self.output_address,
                utxo_value=self.utxo_value
            )

        Logger.debug("{} outputs: {}".format(category, outputs))
        return outputs

    def _payload(self, category: str):
        load = None
        if category == self.PRODUCER_REGISTER:

            load = self.assist.gen_register_producer_payload(
                privatekey=self.payload.private_key,
                owner_publickey=self.payload.owner_public_key,
                node_publickey=self.payload.node_public_key,
                nickname=self.payload.nickname,
                url=self.payload.url,
                location=self.payload.location,
                netaddress=self.payload.net_address
            )

        elif category == self.PRODUCER_UPDATE:
            load = self.assist.gen_update_producer_payload(
                privatekey=self.payload.private_key,
                owner_publickey=self.payload.owner_public_key,
                node_publickey=self.payload.node_public_key,
                nickname=self.payload.nickname,
                url=self.payload.url,
                location=self.payload.location,
                netaddress=self.payload.net_address
            )

        elif category == self.PRODUCER_CANCEL or self.PRODUCER_ACTIVATE:
            load = self.assist.gen_cancel_producer_payload(
                privatekey=self.payload.private_key,
                owner_publickey=self.payload.owner_public_key
            )

        Logger.debug("{} payload: {}".format(category, load))
        return load

    def register(self):
        result = False
        category = self.PRODUCER_REGISTER
        inputs = self._inputs(category)
        outputs = self._outputs(category)
        load = self._payload(category)
        register_resp = self.jar_service.gen_register_producer_tx(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=self.privatekeysign,
            payload=load
        )

        tran_raw = register_resp["rawtx"]
        tran_txid = register_resp["txhash"].lower()
        sendraw_resp = self.assist.rpc.send_raw_transaction(data=tran_raw)
        compare = util.assert_equal(sendraw_resp, tran_txid)
        if not compare:
            return result

        self.assist.rpc.discrete_mining(6)

        producer_status_resp = self.assist.rpc.producer_status(self.node.owner_keystore.public_key.hex())
        Logger.debug("{} producers status: {}".format(self.PRODUCER_REGISTER, producer_status_resp))

        if producer_status_resp == "Activate":
            self.registered = True
            result = True

        return result

    def register_without_mining(self):
        category = self.PRODUCER_REGISTER
        inputs = self._inputs(category)
        outputs = self._outputs(category)
        load = self._payload(category)
        register_resp = self.jar_service.gen_register_producer_tx(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=self.privatekeysign,
            payload=load
        )

        tran_raw = register_resp["rawtx"]
        tran_txid = register_resp["txhash"].lower()
        sendraw_resp = self.assist.rpc.send_raw_transaction(data=tran_raw)
        result = util.assert_equal(sendraw_resp, tran_txid)

        return result

    def update(self):
        result = False
        category = self.PRODUCER_UPDATE
        inputs = self._inputs(category)
        outputs = self._outputs(category)
        load = self._payload(category)

        update_resp = self.jar_service.gen_update_producer_tx(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=self.privatekeysign,
            payload=load)

        tran_raw = update_resp["rawtx"]
        tran_txid = update_resp["txhash"].lower()
        sendraw_resp = self.assist.rpc.send_raw_transaction(tran_raw)
        compare = util.assert_equal(sendraw_resp, tran_txid)
        if not compare:
            return result

        self.assist.rpc.discrete_mining(2)

        producer_status_resp = self.assist.rpc.producer_status(self.node.owner_keystore.public_key.hex())
        Logger.debug("{} producers status: {}".format(category, producer_status_resp))
        if producer_status_resp == "Activate":
            result = True
            self.updated = True

        return result

    def cancel(self):
        result = False

        category = self.PRODUCER_CANCEL
        inputs = self._inputs(category)
        outputs = self._outputs(category)
        load = self._payload(category)

        cancel_resp = self.jar_service.gen_cancel_producer_tx(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=self.privatekeysign,
            payload=load
        )

        tran_raw = cancel_resp["rawtx"]
        tran_txid = cancel_resp["txhash"].lower()
        sendraw_resp = self.assist.rpc.send_raw_transaction(data=tran_raw)

        compare = util.assert_equal(send_resp=sendraw_resp, jar_txid=tran_txid)
        if compare:
            result = True

        self.assist.rpc.discrete_mining(2)
        producer_status_resp = self.assist.rpc.producer_status(
            publickey=self.node.owner_keystore.public_key.hex()
        )
        Logger.debug("{} producer status: {}".format(category, producer_status_resp))

        if producer_status_resp == "Canceled":
            self.canceled = True

        return result

    def redeem(self):
        result = False
        category = self.PRODUCER_REDEEM
        balance1 = self.get_deposit_balance()
        inputs = self._inputs(category)
        outputs = self._outputs(category)

        redeem_resp = self.jar_service.gen_return_deposit_coint_tx(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=self.privatekeysign
        )

        tran_raw = redeem_resp["rawtx"]
        tran_txid = redeem_resp["txhash"].lower()
        sendraw_resp = self.assist.rpc.send_raw_transaction(data=tran_raw)
        compare = util.assert_equal(send_resp=sendraw_resp, jar_txid=tran_txid)
        if compare:
            result = True

        self.assist.rpc.discrete_mining(1)
        balance2 = self.get_deposit_balance()
        balance3 = self.assist.rpc.get_balance_by_address(self.node.owner_keystore.address)
        Logger.debug("{} balance1 = {}, balance2 = {}, balance3 = {}".format(self.PRODUCER_REDEEM,
                                                                            balance1, balance2, balance3))
        return result

    def activate(self):
        result = False
        category = self.PRODUCER_ACTIVATE
        inputs = self._inputs(category)
        outputs = self._outputs(category)
        payload = self._payload(category)

        activate_resp = self.jar_service.gen_activate_producer_tx(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=self.privatekeysign,
            payload=payload
        )

        tran_raw = activate_resp["rawtx"]
        tran_txid = activate_resp["txhash"].lower()

        sendraw_resp = self.assist.rpc.send_raw_transaction(data=tran_raw)
        Logger.warn("{} jar txid: {}".format(self.tag, tran_txid))
        Logger.warn("{} rpc txid: {}".format(self.tag, sendraw_resp))
        compare = util.assert_equal(send_resp=sendraw_resp, jar_txid=tran_txid)
        if compare:
            result = True
            height1 = self.assist.rpc.get_block_count()
            while True:
                self.assist.rpc.discrete_mining(1)
                time.sleep(1)
                height2 = self.assist.rpc.get_block_count()
                Logger.debug("{} height1 = {}, height2 = {}".format(self.tag, height1, height2))
                if height2 - height1 > 6:
                    break
        return result

    def get_deposit_balance(self):
        balance = self.assist.rpc.get_balance_by_address(
            address=self.deposit_address
        )
        Logger.debug("{} deposit balance: {}".format(self.tag, balance))
        return balance
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 2:33 PM
# author: liteng

from middle import util, constant
from bottom.logs.log import Logger
from bottom.tx.assist import Assist
from bottom.services.jar import JarService
from bottom.wallet.keystore import KeyStore


class Payload(object):
    def __init__(self, privatekey: str, owner_publickey: str, node_publickey: str,
                 nickname: str, url: str, location: int, address: str):
        self.tag = "[bottom.tx.transaction.Payload]"
        self.privatekey = privatekey
        self.owner_publickey = owner_publickey
        self.node_publickey = node_publickey
        self.nickname = nickname
        self.url = url
        self.location = location
        self.address = address


class Transaction(object):

    def __init__(self, jar_service: JarService, assist: Assist):
        self.tag = "[bottom.tx.transaction.Transaction]"
        self.jar_service = jar_service
        self.assist = assist
        self.fee = 100
        self.utxos_value = 0
        self.TO_SELA = 100000000

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


class Producer(Transaction):

    def __init__(self, keystore: KeyStore, payload: Payload, jar_service: JarService, assist: Assist):
        Transaction.__init__(self, jar_service=jar_service, assist=assist)
        self.tag = "Producer"
        self.keystore = keystore
        self.owner_publickey = keystore.public_key.hex()
        self.owner_privatekey = keystore.private_key.hex()
        self.payload = payload
        self.registered = False
        self.canceled = False
        self.updated = False
        self.redeemed = False
        self.output_address = keystore.address
        self.deposit_amount = 5000 * self.TO_SELA
        self.deposit_address = jar_service.gen_deposit_address(self.owner_publickey)
        self.privatekeysign = self.assist.gen_private_sign(self.owner_privatekey)

    def _inputs(self, category: str):
        deposit_address = ""
        amount = self.fee
        if category == constant.PRODUCER_REDEEM:
            deposit_address = self.deposit_address
            amount = self.deposit_amount - self.fee - 1
        elif category == constant.PRODUCER_REGISTER:
            amount = self.deposit_amount

        inputs, utxos_value = self.assist.gen_inputs_utxos_value(self.keystore, amount, deposit_address=deposit_address)
        self.utxos_value = utxos_value
        Logger.debug("{} inputs: {}".format(category, inputs))
        return inputs

    def _outputs(self, category: str):
        outputs = None
        if category == constant.PRODUCER_REGISTER:
            outputs = self.assist.gen_register_producer_output(
                deposit_address=self.deposit_address,
                amount=self.deposit_amount,
                change_address=self.output_address,
                utxo_value=self.utxos_value,
                fee=self.fee
            )
        elif category == constant.PRODUCER_UPDATE:
            outputs = self.assist.gen_update_producer_output(
                address=self.output_address,
                utxo_value=self.utxos_value,
                fee=self.fee
            )
        elif category == constant.PRODUCER_CANCEL:
            outputs = self.assist.gen_cancel_producer_output(
                address=self.output_address,
                utxo_value=self.utxos_value,
                fee=self.fee
            )
        elif category == constant.PRODUCER_REDEEM:
            outputs = self.assist.gen_redeem_producer_output(
                address=self.output_address,
                utxo_value=self.utxos_value,
                fee=self.fee
            )
        Logger.debug("{} outputs: {}".format(category, outputs))
        return outputs

    def _payload(self, category: str):
        load = None
        if category == constant.PRODUCER_REGISTER:

            load = self.assist.gen_register_producer_payload(
                privatekey=self.payload.privatekey,
                owner_publickey=self.payload.owner_publickey,
                node_publickey=self.payload.node_publickey,
                nickname=self.payload.nickname,
                url=self.payload.url,
                location=self.payload.location,
                address=self.payload.address
            )

        elif category == constant.PRODUCER_UPDATE:
            load = self.assist.gen_update_producer_payload(
                privatekey=self.payload.privatekey,
                owner_publickey=self.payload.owner_publickey,
                node_publickey=self.payload.node_publickey,
                nickname=self.payload.nickname,
                url=self.payload.url,
                location=self.payload.location,
                address=self.payload.address
            )

        elif category == constant.PRODUCER_CANCEL:
            load = self.assist.gen_cancel_producer_payload(
                privatekey=self.payload.privatekey,
                publickey=self.payload.owner_publickey
            )

        Logger.debug("{} payload: {}".format(category, load))
        return load

    def register(self):
        result = False
        category = constant.PRODUCER_REGISTER
        inputs = self._inputs(category)
        outputs = self._outputs(category)
        load = self._payload(category)
        register_resp = self.jar_service.register_producer_transaction(
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

        producer_status_resp = self.assist.rpc.producer_status(self.keystore.public_key.hex())
        Logger.debug("{} producers status: {}".format(constant.PRODUCER_REGISTER, producer_status_resp))

        if producer_status_resp == 1:
            self.registered = True
            result = True

        return result

    def update(self):
        result = False
        category = constant.PRODUCER_UPDATE
        inputs = self._inputs(category)
        outputs = self._outputs(category)
        load = self._payload(category)

        update_resp = self.jar_service.update_producer_transaction(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=self.privatekeysign,
            payload=load)

        tran_raw = update_resp["rawtx"]
        tran_txid = update_resp["txhash"].lower()
        sendraw_resp = self.assist.rpc.send_raw_transaction(tran_raw)
        print("tran_txid =    ", tran_txid)
        print("sendraw_resp = ", sendraw_resp)
        compare = util.assert_equal(sendraw_resp, tran_txid)
        if not compare:
            return result

        self.assist.rpc.discrete_mining(2)

        producer_status_resp = self.assist.rpc.producer_status(self.keystore.public_key.hex())
        Logger.debug("{} producers status: {}".format(category, producer_status_resp))
        if producer_status_resp == 1:
            result = True
            self.updated = True

        return result

    def cancel(self):
        result = False
        category = constant.PRODUCER_CANCEL
        inputs = self._inputs(category)
        outputs = self._outputs(category)
        load = self._payload(category)

        cancel_resp = self.jar_service.cancel_producer_transaction(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=self.privatekeysign,
            payload=load)

        tran_raw = cancel_resp["rawtx"]
        tran_txid = cancel_resp["txhash"].lower()
        sendraw_resp = self.assist.rpc.send_raw_transaction(data=tran_raw)

        compare = util.assert_equal(arg1=sendraw_resp, arg2=tran_txid)
        if compare:
           result = True

        self.assist.rpc.discrete_mining(2)
        producer_status_resp = self.assist.rpc.producer_status(
            publickey=self.keystore.public_key.hex())
        Logger.debug("{} producer status: {}".format(category, producer_status_resp))

        if producer_status_resp == 0:
            self.canceled = True

        return result

    def redeem(self):
        result = False
        category = constant.PRODUCER_REDEEM
        balance1 = self.get_deposit_balance()
        inputs = self._inputs(category)
        outputs = self._outputs(category)

        redeem_resp = self.jar_service.redemption_producer_transaction(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=self.privatekeysign
        )

        tran_raw = redeem_resp["rawtx"]
        tran_txid = redeem_resp["txhash"].lower()
        sendraw_resp = self.assist.rpc.send_raw_transaction(data=tran_raw)
        compare = util.assert_equal(arg1=sendraw_resp, arg2=tran_txid)
        if compare:
            result = True

        self.assist.rpc.discrete_mining(1)
        balance2 = self.get_deposit_balance()
        balance3 = self.assist.rpc.get_balance_by_address(self.keystore.address)
        Logger.info("{} balance1 = {}, balance2 = {}, balance3 = {}".format(constant.PRODUCER_REDEEM,
                                                                            balance1, balance2, balance3))
        return result

    def get_deposit_balance(self):
        balance = self.assist.rpc.get_balance_by_address(
            address=self.deposit_address
        )
        Logger.debug("{} deposit balance: {}".format(self.tag, balance))
        return balance


class Voter(Transaction):
    def __init__(self, keystore: KeyStore, candidates: [Producer], jar_service: JarService, assist: Assist):
        Transaction.__init__(self, jar_service=jar_service, assist=assist)
        self.tag = "Vote Producer"
        self.keystore = keystore
        self.candidates = candidates
        self.vote_amount = 1 * self.TO_SELA
        self.vote_type = 0
        self.vote_version = 0
        self.vote_output_type = 1
        self.utxos_value = 0
        self.output_address = keystore.address

    def _inputs(self):
        inputs, utxos_value = self.assist.gen_inputs_utxos_value(self.keystore, self.vote_amount)
        self.utxos_value = utxos_value
        Logger.debug("{} inputs: {}".format(self.tag, inputs))
        return inputs

    def _outputs(self):
        if len(self.candidates) == 0:
            return []

        candidate_publickeys = []
        for candidate in self.candidates:
            candidate_publickeys.append(candidate.keystore.public_key.hex())

        candidates = self.assist.gen_vote_outputs_contents_candidates(candidate_publickeys)
        contents = self.assist.gen_vote_outputs_contents(votetype=self.vote_type, candidates=candidates)
        outputs = self.assist.gen_vote_outputs(
            vote_address=self.output_address,
            change_address=self.output_address,
            utxos_value=self.utxos_value,
            vote_amount=self.vote_amount,
            outputtype=self.vote_output_type,
            version=self.vote_version,
            contents=contents
        )
        Logger.debug("{} inputs: {}".format(self.tag, outputs))
        return outputs

    def _privatekeysign(self):
        privatekeysign = self.assist.gen_private_sign(self.keystore.private_key.hex())
        Logger.debug("{} privatekeysign: {}".format(self.tag, privatekeysign))
        print("[Vote Producer] privatekeysign: ", privatekeysign)
        return privatekeysign

    def vote(self):
        result = False

        inputs = self._inputs()
        outputs = self._outputs()
        privatekeysign = self._privatekeysign()

        vote_resp = self.jar_service.vote_transaction(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=privatekeysign
        )

        tran_raw = vote_resp["rawtx"]
        tran_txid = vote_resp["txhash"].lower()
        sendraw_resp = self.assist.rpc.send_raw_transaction(data=tran_raw)

        compare = util.assert_equal(arg1=sendraw_resp, arg2=tran_txid)
        if not compare:
            return result

        self.assist.rpc.discrete_mining(2)

        vote_amount = self.get_vote_amount()
        Logger.debug("{} vote amount: {} ELA".format(self.tag, vote_amount))
        print("[Vote producer] vote_amount = ", vote_amount)
        if vote_amount == float(self.vote_amount):
            result = True
        return result

    def get_vote_amount(self):
        vote_status_resp = self.assist.rpc.vote_status(
            address=self.keystore.address
        )
        return float(vote_status_resp["voting"]) * self.TO_SELA
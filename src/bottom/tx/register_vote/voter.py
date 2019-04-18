#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/3 4:49 PM
# author: liteng

from src.middle.tools import constant
from src.middle.tools import util
from src.middle.tools.log import Logger

from src.bottom.services.jar import JarService
from src.bottom.tx.assist import Assist
from src.bottom.wallet.keystore import KeyStore
from src.bottom.tx.register_vote.producer import Producer


class Voter(object):
    def __init__(self, keystore: KeyStore, jar_service: JarService, assist: Assist):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.keystore = keystore
        self.jar_service = jar_service
        self.assist = assist
        self.vote_type = 0
        self.vote_version = 0
        self.vote_output_type = 1
        self.utxo_value = 0
        self.output_address = self.keystore.address

    def _inputs(self, vote_amount: int):
        inputs, utxos_value = self.assist.gen_inputs_utxo_value(self.keystore, vote_amount)
        self.utxo_value = utxos_value
        Logger.debug("{} inputs: {}".format(self.tag, inputs))
        return inputs

    def _outputs(self, producers: [Producer], vote_amount: int):
        if len(producers) == 0:
            return []

        candidate_publickeys = []
        for producer in producers:
            candidate_publickeys.append(producer.node.owner_keystore.public_key.hex())

        candidates = self.assist.gen_vote_outputs_contents_candidates(candidate_publickeys)
        contents = self.assist.gen_vote_outputs_contents(votetype=self.vote_type, candidates=candidates)
        outputs = self.assist.gen_vote_outputs(
            vote_address=self.output_address,
            change_address=self.output_address,
            utxo_value=self.utxo_value,
            vote_amount=vote_amount,
            outputtype=self.vote_output_type,
            version=self.vote_version,
            contents=contents
        )
        Logger.debug("{} inputs: {}".format(self.tag, outputs))
        return outputs

    def _privatekeysign(self):
        privatekeysign = self.assist.gen_private_sign(self.keystore.private_key.hex())
        Logger.debug("{} privatekeysign: {}".format(self.tag, privatekeysign))
        return privatekeysign

    def vote(self, producers: [Producer], vote_amount: int):

        inputs = self._inputs(vote_amount)
        outputs = self._outputs(producers, vote_amount)
        privatekeysign = self._privatekeysign()

        vote_resp = self.jar_service.gen_vote_tx(
            inputs=inputs,
            outputs=outputs,
            privatekeysign=privatekeysign
        )

        tran_raw = vote_resp["rawtx"]
        tran_txid = vote_resp["txhash"].lower()
        sendraw_resp = self.assist.rpc.send_raw_transaction(data=tran_raw)

        compare = util.assert_equal(send_resp=sendraw_resp, jar_txid=tran_txid)
        if not compare:
            return False

        self.assist.rpc.discrete_mining(1)

        return True

    def get_vote_amount(self):
        vote_status_resp = self.assist.rpc.vote_status(
            address=self.keystore.address
        )
        Logger.debug("{} register_vote status response: {}".format(self.tag, vote_status_resp))
        return float(vote_status_resp["voting"]) * constant.TO_SELA
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/3 4:49 PM
# author: liteng

from src.middle.common import constant
from src.middle.common import util
from src.middle.common.log import Logger

from src.bottom.nodes.ela import ElaNode
from src.bottom.services.jar import JarService
from src.bottom.tx.assist import Assist
from src.bottom.tx.vote.producer import Producer


class Voter(object):
    def __init__(self, node: ElaNode, candidates: [Producer], jar_service: JarService, assist: Assist, number: int):
        self.tag = "[src.bottom.tx.vote.voter.Voter]"
        self.node = node
        self.candidates = candidates
        self.jar_service = jar_service
        self.assist = assist
        self.ela_number = number
        self.vote_amount = (self.ela_number - self.node.index) * constant.TO_SELA
        self.vote_type = 0
        self.vote_version = 0
        self.vote_output_type = 1
        self.utxos_value = 0
        self.output_address = self.node.owner_keystore.address

    def _inputs(self):
        inputs, utxos_value = self.assist.gen_inputs_utxos_value(self.node.owner_keystore, self.vote_amount)
        self.utxos_value = utxos_value
        Logger.debug("{} inputs: {}".format(self.tag, inputs))
        return inputs

    def _outputs(self):
        if len(self.candidates) == 0:
            return []

        candidate_publickeys = []
        for candidate in self.candidates:
            candidate_publickeys.append(candidate.node.owner_keystore.public_key.hex())

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
        privatekeysign = self.assist.gen_private_sign(self.node.owner_keystore.private_key.hex())
        Logger.debug("{} privatekeysign: {}".format(self.tag, privatekeysign))
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
        Logger.debug("{} vote amount: {} SELA".format(self.tag, vote_amount))
        Logger.debug("{} self amount: {} SELA".format(self.tag, float(self.vote_amount)))

        if (vote_amount - float(self.vote_amount)) < 0.000001:
            result = True
        return result

    def get_vote_amount(self):
        vote_status_resp = self.assist.rpc.vote_status(
            address=self.node.owner_keystore.address
        )
        Logger.debug("{} vote status response: {}".format(self.tag, vote_status_resp))
        return float(vote_status_resp["voting"]) * constant.TO_SELA
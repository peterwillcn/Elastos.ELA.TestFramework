#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/5 5:42 PM
# author: liteng


import time
from src.core.tx import txbuild
from src.core.tx.outputPayload.candidate_votes import CandidateVotes
from src.core.tx.outputPayload.vote_content import VoteContent
from src.core.tx.payload.crc_proposal import CRCProposal
from src.core.tx.payload.crc_proposal_review import CRCProposalReview
from src.core.tx.payload.crc_proposal_tracking import CRCProposalTracking
from src.core.tx.payload.crc_proposal_withdraw import CRCProposalWithdraw
from src.core.tx.producer import Producer
from src.core.tx.transaction import Transaction
from src.core.services import rpc
from src.core.nodes.ela import ElaNode
from src.core.wallet.account import Account

from src.core.managers.node_manager import NodeManager
from src.core.tx.payload.producer_info import ProducerInfo
from src.core.tx.payload.cr_info import CRInfo
from src.core.tx.payload.un_register_cr import UnRegisterCR
from src.core.tx.payload.neo_contract_deploy import NeoDeployContract
from src.core.tx.payload.neo_contract_invoke import NeoInvokeContract
from src.tools import util
from src.tools import constant
from src.tools.log import Logger


class TxManager(object):

    def __init__(self, port: int):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.fee = 10000
        self.rpc_port = port
        self.register_cr_list = list()
        self.cancel_producers_list = list()
        self.crc_proposal_list = list()

    def transfer_asset(self, input_private_key: str, output_addresses: list, amount: int, side_chain: bool):

        # create transfer asset tx
        tx = txbuild.create_transaction(
            input_private_key=input_private_key,
            output_addresses=output_addresses,
            amount=amount,
            rpc_port=self.rpc_port,
            side_chain=side_chain
        )

        if tx is None:
            return False
        # single sign this tx
        tx = txbuild.single_sign_transaction(input_private_key, tx)
        # Logger.debug("transaction:\n{} ".format(tx))
        # return the result
        ret = self.handle_tx_result(tx, self.rpc_port)

        return ret

    def transfer_abnormal_asset(self, input_private_key: str, output_addresses: list, amount: int, attributes=None):

        # create transfer asset tx
        tx = txbuild.create_abnormal_transaction(
            input_private_key=input_private_key,
            output_addresses=output_addresses,
            amount=amount,
            rpc_port=self.rpc_port,
            attributes=attributes
        )

        if tx is None:
            return False
        # single sign this tx
        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.debug("transaction:\n{} ".format(tx))
        # return the result
        ret = self.handle_tx_result(tx, self.rpc_port)

        return ret

    def transfer_cross_chain_asset(self, input_private_key: str, lock_address: str, cross_address: str,
                                   amount: int, recharge: bool, port=rpc.DEFAULT_PORT):
        tx = txbuild.create_cross_chain_transaction(
            input_private_key=input_private_key,
            lock_address=lock_address,
            cross_chain_address=cross_address,
            amount=amount,
            recharge=recharge,
            rpc_port=port
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.debug("cross chain asset transaction: \n{}".format(tx))
        ret = self.handle_tx_result(tx, port)

        return ret

    def transfer_multi_cross_chain_asset(self, input_private_key: str, lock_address: str,
                                         cross_address: str, tx_count: int, amount: int,
                                         recharge: bool, port: int):
         account = Account(input_private_key)
         response = rpc.list_unspent_utxos(account.address(), port=port)
         if not response or isinstance(response, dict):
            Logger.error("get utxos return error: {}".format(response))
            return False
         utxos = response
         if len(utxos) < tx_count:
            Logger.error("utxo is not enough")
            return False
        
         for i in range(tx_count):
            current_utxos = list()
            utxo = utxos[i]
            current_utxos.append(utxo)
            Logger.info("current cross chain index: {}".format(i))
            tx = txbuild.create_cross_chain_transaction_by_utxo(
                input_private_key=input_private_key,
                lock_address=lock_address,
                cross_chain_address=cross_address,
                amount=amount,
                recharge=recharge,
                utxos=current_utxos
            )

            if tx is None:
               return False

            tx = txbuild.single_sign_transaction(input_private_key, tx)
            Logger.debug("cross chain asset transaction: \n{}".format(tx))
            ret = self.handle_tx_result(tx, port)

         return ret

    def crc_proposal_review(self, input_private_key: str, amount: int, crc_proposal_review: CRCProposalReview,
                            port=rpc.DEFAULT_PORT):

        tx = txbuild.create_crc_proposal_review_transaction(
            input_private_key=input_private_key,
            amount=amount,
            payload=crc_proposal_review,
            rpc_port=port
        )

        if tx is None:
            return False
        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.debug("crc proposal review transaction:\n{} ".format(tx))
        ret = self.handle_tx_result(tx, port)
        return ret

    def crc_proposal_withdraw(self, input_address: str, amount: int, crc_proposal_withdraw: CRCProposalWithdraw,
                              output_address: str, port=rpc.DEFAULT_PORT):

        tx = txbuild.create_crc_proposal_withdraw_transaction(
            input_address=input_address,
            amount=amount,
            payload=crc_proposal_withdraw,
            rpc_port=port,
            output_address=output_address
        )

        if tx is None:
            return False
        Logger.debug("crc proposal withdraw transaction:\n{} ".format(tx))
        ret = self.handle_tx_result(tx, port)
        return ret

    def crc_proposal_tracking(self, input_private_key: str, amount: int, crc_proposal_tracking: CRCProposalTracking,
                              port=rpc.DEFAULT_PORT):

        tx = txbuild.create_crc_proposal_tracking_transaction(
            input_private_key=input_private_key,
            amount=amount,
            payload=crc_proposal_tracking,
            rpc_port=port
        )

        if tx is None:
            return False
        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.debug("crc proposal tracking transaction:\n{} ".format(tx))
        ret = self.handle_tx_result(tx, port)
        return ret

    def crc_proposal(self, input_private_key: str, amount: int, crc_proposal: CRCProposal, port=rpc.DEFAULT_PORT):

        tx = txbuild.create_crc_proposal_transaction(
            input_private_key=input_private_key,
            amount=amount,
            payload=crc_proposal,
            rpc_port=port
        )

        if tx is None:
            return False
        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.debug("crc proposal transaction:\n{} ".format(tx))
        ret = self.handle_tx_result(tx, port)
        return ret

    def register_cr(self, input_private_key: str, amount: int, cr_info: CRInfo, port=rpc.DEFAULT_PORT):

        tx = txbuild.create_cr_register_transaction(
            input_private_key=input_private_key,
            amount=amount,
            payload=cr_info,
            rpc_port=port
        )

        if tx is None:
            return False
        tx.payload_version = cr_info.CR_INFO_DID_VERSION
        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.debug("register cr transaction:\n{} ".format(tx))
        ret = self.handle_tx_result(tx, port)
        return ret

    def update_cr(self, input_private_key: str, cr_info: CRInfo, port=rpc.DEFAULT_PORT):
        tx = txbuild.create_cr_update_transaction(
            input_private_key=input_private_key,
            update_payload=cr_info,
            rpc_port=port
        )

        if tx is None:
            return False

        tx.payload_version = cr_info.CR_INFO_DID_VERSION
        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.debug("update cr transaction:\n{}".format(tx))
        ret = self.handle_tx_result(tx, port)

        return ret

    def unregister_cr(self, input_private_key: str, register_private_key: str, port=rpc.DEFAULT_PORT):
        un_register_cr = UnRegisterCR(register_private_key)

        tx = txbuild.create_cr_cancel_transaction(
            input_private_key=input_private_key,
            payload=un_register_cr,
            rpc_port=port
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.debug("ungister cr transaction:\n{}".format(tx))
        ret = self.handle_tx_result(tx, port)

        return ret

    def redeem_cr(self, crc_info: CRInfo, return_address: str, amount: int, port=rpc.DEFAULT_PORT):
        tx = txbuild.create_cr_redeem_transaction(
            payload=crc_info,
            output_address=return_address,
            amount=amount,
            rpc_port=port
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(crc_info.account.private_key(), tx)
        Logger.debug("redeem cr transaction:\n{}".format(tx))
        ret = self.handle_tx_result(tx, port)

        return ret

    def register_producer(self, node: ElaNode):
        producer = Producer(
            input_private_key=node.owner_account.private_key(),
            node=node,
            nick_name=node.name,
            url="http://elastos.org",
            location=0,
            net_address="127.0.0.1:" + str(node.arbiter_node_port)
        )
        tx = producer.register(self.rpc_port)

        if tx is None:
            return False

        ret = self.handle_tx_result(tx, self.rpc_port)
        return ret

    def update_producer(self, producer: Producer, producer_info: ProducerInfo):
        tx = producer.update(producer_info, self.rpc_port)

        print(tx)
        if tx is None:
            return False

        ret = self.handle_tx_result(tx, self.rpc_port)

        return ret

    def cancel_producer(self, producer: Producer):
        tx = producer.cancel(self.rpc_port)

        if tx is None:
            return False

        ret = self.handle_tx_result(tx, self.rpc_port)

        return ret

    def redeem_producer(self, producer: Producer):
        tx = producer.redeem(4999 * constant.TO_SELA, self.rpc_port)

        if tx is None:
            return False

        ret = self.handle_tx_result(tx, self.rpc_port)

        return ret

    def active_producer(self, producer: Producer):
        tx = producer.active()

        if tx is None:
            return False

        ret = self.handle_tx_result(tx, self.rpc_port)

        return ret

    def vote_producer(self, input_private_key: str, amount: int, candidates: list):
        vote_content = VoteContent(VoteContent.DELEGATE, candidates)
        tx = txbuild.create_vote_transaction(
            input_private_key=input_private_key,
            candidates_list=candidates,
            amount=amount,
            rpc_port=self.rpc_port,
            vote_content=vote_content
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.info("vote producer transaction:\n{} ".format(tx))
        ret = self.handle_tx_result(tx, self.rpc_port)

        return ret

    def vote_cr(self, input_private_key: str, amount: int, candidates: list):
        vote_content = VoteContent(VoteContent.CRC, candidates)
        tx = txbuild.create_vote_transaction(
            input_private_key=input_private_key,
            candidates_list=candidates,
            amount=amount,
            rpc_port=self.rpc_port,
            vote_content=vote_content
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.info("vote cr transaction:\n{} ".format(tx))
        ret = self.handle_tx_result(tx, self.rpc_port)

        return ret

    def vote_proposal(self, input_private_key: str, amount: int, candidates: list):
        candidates_list = list()
        for crc_proposal in candidates:
            candidates_list.append(CandidateVotes(crc_proposal.hash, amount))
        vote_content = VoteContent(VoteContent.CRC_PROPOSAL, candidates_list)
        tx = txbuild.create_vote_transaction(
            input_private_key=input_private_key,
            candidates_list=candidates_list,
            amount=amount,
            rpc_port=self.rpc_port,
            vote_content=vote_content
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(input_private_key, tx)
        Logger.info("vote cr proposal transaction:\n{} ".format(tx))
        ret = self.handle_tx_result(tx, self.rpc_port)

        return ret

    def deploy_neo_contract(self, input_private_key: str, output_addresses: list, payload: NeoDeployContract,
                            amount: int, rpc_port: int):
        tx = txbuild.deploy_contract_transaction(
            input_private_key=input_private_key,
            output_addresses=output_addresses,
            payload=payload,
            amount=amount,
            rpc_port=rpc_port,
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(input_private_key, tx)

        ret = self.handle_tx_result(tx, rpc_port)

        return ret

    def invoke_neo_contract(self, input_private_key: str, output_addresses: list, payload: NeoInvokeContract,
                            amount: int, rpc_port: int):
        tx = txbuild.invoke_contract_transaction(
            input_private_key=input_private_key,
            output_addresses=output_addresses,
            payload=payload,
            amount=amount,
            rpc_port=rpc_port
        )

        if tx is None:
            return False

        tx = txbuild.single_sign_transaction(input_private_key, tx)

        ret = self.handle_tx_result(tx, rpc_port)

        return ret

    def recharge_necessary_keystore(self, input_private_key: str, accounts: list, amount: int):
        addresses = list()
        for a in accounts:
            addresses.append(a.address())

        ret = self.transfer_asset(input_private_key, addresses, amount)

        if ret:
            rpc.discrete_mining(1)
        else:
            Logger.error("{} recharge necessary keystore failed".format(self.tag))
            return False

        for i in range(len(addresses)):
            value = rpc.get_balance_by_address(addresses[i])
            Logger.debug("{} arbiter {} wallet balance: {}".format(self.tag, i, value))
        return ret

    def cross_chain_transaction(self, side_node_type: str, recharge: bool, target_address=""):
        if side_node_type is None or side_node_type is "":
            return False

        global cross_address
        global side_port
        global result
        global balance_port
        global cross_input_key

        if side_node_type is "did":
            side_port = 10136
            cross_did_account = self.node_manager.keystore_manager.cross_did_account
            cross_address = cross_did_account.address()
            cross_input_key = cross_did_account.private_key()

        elif side_node_type is "token":
            side_port = 10146
            cross_token_account = self.node_manager.keystore_manager.cross_token_account
            cross_address = cross_token_account.address()
            cross_input_key = cross_token_account.private_key()

        elif side_node_type is "neo":
            side_port = 10156
            cross_neo_account = self.node_manager.keystore_manager.cross_neo_account
            if target_address == "":
                cross_address = cross_neo_account.address()
            else:
                cross_address = target_address
            cross_input_key = cross_neo_account.private_key()

        if recharge:
            port = self.rpc_port
            balance_port = side_port
            input_private_key = self.tap_account.private_key()
            lock_address = self.params.arbiter_params.side_info[side_node_type][constant.SIDE_RECHARGE_ADDRESS]
            amount = 1000 * constant.TO_SELA

        else:
            port = side_port
            balance_port = self.rpc_port
            input_private_key = cross_input_key
            lock_address = self.params.arbiter_params.side_info[side_node_type][constant.SIDE_WITHDRAW_ADDRESS]
            cross_address = self.tap_account.address()
            amount = 300 * constant.TO_SELA

        balance1 = rpc.get_balance_by_address(cross_address, balance_port)

        ret = self.transfer_cross_chain_asset(
            input_private_key=input_private_key,
            lock_address=lock_address,
            cross_address=cross_address,
            amount=amount,
            recharge=recharge,
            port=port
        )

        if not ret:
            Logger.error("{} transfer cross chain asset failed".format(self.tag))
            return False

        side_height_begin = rpc.get_block_count(side_port)
        while True:
            main_height = rpc.get_block_count()
            side_height = rpc.get_block_count(side_port)

            Logger.debug("{} main height: {}, side height: {}".format(self.tag, main_height, side_height))

            if side_height - side_height_begin > 10:
                break

            rpc.discrete_mining(1)
            time.sleep(3)

        balance2 = rpc.get_balance_by_address(cross_address, balance_port)
        Logger.debug("{} recharge balance1: {}".format(self.tag, balance1))
        Logger.debug("{} recharge balance2: {}".format(self.tag, balance2))

        if isinstance(balance1, dict):
            before_balance = list(balance1.values())[0]
        else:
            before_balance = balance1

        if isinstance(balance2, dict):
            after_balance = list(balance2.values())[0]
        else:
            after_balance = balance2

        result = (float(after_balance) - float(before_balance)) * constant.TO_SELA > float(amount - 3 * 10000)
        Logger.debug("{} recharge result: {}".format(self.tag, result))

        return result

    def register_producers_candidates(self):
        global result
        result = False
        for i in range(
                self.params.ela_params.crc_number + 1,
                self.params.ela_params.number - round(self.params.ela_params.later_start_number / 2) + 1
        ):
            ela_node = self.node_manager.ela_nodes[i]
            public_key = ela_node.node_account.public_key()
            ret = self.register_producer(ela_node)
            if not ret:
                return False
            rpc.discrete_mining(7)

            status = rpc.producer_status(public_key)
            Logger.debug("After mining 7 blocks, register status: {}".format(status))
            result = status == "Active"
            if not result:
                Logger.error("{} register producer {} failed".format(self.tag, ela_node.name))
                break

            Logger.info("{} register node-{} to be a producer on success!\n".format(self.tag, i))

        return result

    def register_producers(self, start: int, end: int, without_mining=False):
        for i in range(start, end):
            ela_node = self.node_manager.ela_nodes[i]
            ret = self.register_producer(ela_node)
            if not ret:
                return False

            current_height = rpc.get_block_count()
            last_height = current_height
            while True:
                rpc.discrete_mining(1)
                current_height = rpc.get_block_count()
                Logger.debug("{} current height: {}".format(self.tag, current_height))
                if current_height - 6 > last_height:
                    break
                time.sleep(1)

            Logger.info("{} register node-{} to be a producer on success!\n".format(self.tag, i))
        return True

    def update_produces_candidates(self):
        for i in range(len(self.register_producers_list)):
            producer = self.register_producers_list[i]
            payload = producer.info
            payload.nickname = "arbiter-" + str(i)
            ret = self.update_producer(producer, payload)
            if not ret:
                return False
            rpc.discrete_mining(1)
        return True

    def cancel_producers_candidates(self):
        global result
        for producer in self.register_producers_list:
            ret = self.cancel_producer(producer)
            if not ret:
                return False
            rpc.discrete_mining(1)
            status = rpc.producer_status(producer.node.owner_keystore.public_key.hex())
            result = status is "Cancelled"
        return result

    def redeem_producers_candidates(self):
        for producer in self.cancel_producers_list:
            ret = self.redeem_producer(producer)
            if not ret:
                return False
            rpc.discrete_mining(1)
        return True

    def vote_crc_proposal_candidates(self):
        for i in range(len(self.crc_proposal_list)):
            proposal = self.crc_proposal_list[i]
            vote_amount = (self.params.ela_params.crc_number - i + 1) * constant.TO_SELA
            ret = self.vote_proposal(
                input_private_key=self.tap_account.private_key(),
                amount=vote_amount,
                candidates=[proposal])
            if not ret:
                return False
            rpc.discrete_mining(1)
            Logger.info("{} vote crc proposal:{} on success!\n".format(self.tag, proposal.hash, vote_amount))
        return True

    def vote_producers(self, start: int, end: int):
        for i in range(start, end):
            producer = self.register_producers_list
            vote_amount = constant.TO_SELA
            ret = self.vote_producer(
                input_private_key=self.private_key,
                amount=vote_amount,
                candidates=[producer]
            )
            if not ret:
                return False
            Logger.info("{} vote node-{} {} Elas on success!\n".format(self.tag, i, vote_amount))
            rpc.discrete_mining(1)
        return True

    def handle_tx_result(self, tx: Transaction, port):
        # Logger.debug("{} {}".format(self.tag, tx))

        r = tx.serialize()
        response = rpc.send_raw_transaction(r.hex(), port)
        if isinstance(response, dict):
            Logger.error("{} rpc response: {}".format(self.tag, response))
            Logger.error("rpc send raw transaction failed")
            return False

        tx_hash = util.bytes_reverse(bytes.fromhex(tx.hash())).hex()
        Logger.debug("{} tx hash : {}".format(self.tag, tx_hash))
        Logger.debug("{} response: {}".format(self.tag, response))

        return tx_hash

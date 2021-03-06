#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/4 11:44 AM
# author: liteng
import time
from decimal import Decimal

from src.core.tx.payload.crc_proposal import CRCProposal
from src.core.tx.payload.crc_proposal_review import CRCProposalReview
from src.core.tx.payload.crc_proposal_tracking import CRCProposalTracking
from src.core.tx.payload.crc_proposal_withdraw import CRCProposalWithdraw
from src.tools import util, serialize
from src.tools.log import Logger

from src.core.services import rpc
from src.core.tx.input import Input
from src.core.tx.output import Output
from src.core.tx.program import Program
from src.core.tx.outputPayload.vote_output import VoteOutput
from src.core.tx.attribute import Attribute
from src.core.tx.transaction import Transaction
from src.core.tx.outputPayload.vote_content import VoteContent
from src.core.tx.output_payload import OutputPayload
from src.core.tx.payload.payload import Payload
from src.core.tx.payload.producer_info import ProducerInfo
from src.core.tx.payload.process_producer import ProcessProducer
from src.core.tx.payload.cross_chain_asset import TransferCrossChainAsset
from src.core.tx.payload.neo_contract_deploy import NeoDeployContract
from src.core.tx.payload.neo_contract_invoke import NeoInvokeContract

from src.core.tx.payload.cr_info import CRInfo
from src.core.tx.payload.un_register_cr import UnRegisterCR

from src.core.wallet import keytool
from src.core.wallet.account import Account


def create_abnormal_transaction(input_private_key: str, output_addresses: list, amount: int, rpc_port: int, attributes=None):
    account = Account(input_private_key)
    # check output
    if output_addresses is None or len(output_addresses) == 0:
        Logger.error("Invalid output addresses")
        return None

    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=output_addresses,
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs
    inputs, change_outputs = create_normal_inputs(account.address(), total_amount, rpc_port)

    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    if attributes is None:
        attributes = list()
        attribute = Attribute(
            usage=Attribute.NONCE,
            data=bytes("attributes".encode())
        )
        attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.TRANSFER_ASSET
    tx.payload = Payload(Payload.DEFAULT_VERSION)
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_transaction(input_private_key: str, output_addresses: list, amount: int, rpc_port: int, side_chain: bool):
    account = Account(input_private_key)
    # check output
    if output_addresses is None or len(output_addresses) == 0:
        Logger.error("Invalid output addresses")
        return None

    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=output_addresses,
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs
    inputs, change_outputs = create_normal_inputs(account.address(), total_amount, rpc_port)

    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    if not side_chain :
        tx.version = Transaction.TX_VERSION_09
    else:
        tx.version = Transaction.TX_VERSION_DEFAULT

    tx.tx_type = Transaction.TRANSFER_ASSET
    tx.payload = Payload(Payload.DEFAULT_VERSION)
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx

def create_cross_chain_transaction(input_private_key: str, lock_address: str, cross_chain_address: str, amount: int,
                                   recharge: bool, rpc_port: int, utxo_index=-1):
    if lock_address is None or lock_address is "":
        Logger.error("Invalid lock address")
        return None

    if cross_chain_address is None or cross_chain_address is "":
        Logger.error("Invalid cross chain address")
        return None

    account = Account(input_private_key)
    # create outputs:
    outputs, total_amount = create_normal_outputs(
        output_addresses=[lock_address],
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs:
    inputs, change_outputs = create_normal_inputs(
        account.address(), total_amount, rpc_port, utxo_index)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    cross_chain_asset = TransferCrossChainAsset()
    cross_chain_asset.cross_chain_addresses = [cross_chain_address]
    cross_chain_asset.output_indexes = [0]
    cross_chain_asset.cross_chain_amounts = [amount - 10000]

    tx = Transaction()
    if recharge:
        tx.version = Transaction.TX_VERSION_09
    else:
        tx.version = Transaction.TX_VERSION_DEFAULT

    # Logger.debug("transaction version {}".format(tx.version))
    tx.tx_type = Transaction.TRANSFER_CROSS_CHAIN_ASSET
    tx.payload = cross_chain_asset
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_cross_chain_transaction_by_utxo(input_private_key: str, lock_address: str, cross_chain_address: str, amount: int,
                                   recharge: bool, utxos: list):
    if lock_address is None or lock_address is "":
        Logger.error("Invalid lock address")
        return None

    if cross_chain_address is None or cross_chain_address is "":
        Logger.error("Invalid cross chain address")
        return None

    account = Account(input_private_key)
    # create outputs:
    outputs, total_amount = create_normal_outputs(
        output_addresses=[lock_address],
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs:
    inputs, change_outputs = create_normal_inputs_by_utxo(
        account.address(), total_amount, utxos)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    cross_chain_asset = TransferCrossChainAsset()
    cross_chain_asset.cross_chain_addresses = [cross_chain_address]
    cross_chain_asset.output_indexes = [0]
    cross_chain_asset.cross_chain_amounts = [amount - 10000]

    tx = Transaction()
    if recharge:
        tx.version = Transaction.TX_VERSION_09
    else:
        tx.version = Transaction.TX_VERSION_DEFAULT

    # Logger.debug("transaction version {}".format(tx.version))
    tx.tx_type = Transaction.TRANSFER_CROSS_CHAIN_ASSET
    tx.payload = cross_chain_asset
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx

def create_register_transaction(input_private_key: str, amount: int, payload: ProducerInfo, rpc_port: int):
    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=[payload.get_deposit_address()],
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs
    account = Account(input_private_key)
    inputs, change_outputs = create_normal_inputs(account.address(), total_amount, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.REGISTER_PRODUCER
    tx.payload_version = 0
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_cr_register_transaction(input_private_key: str, amount: int, payload: CRInfo, rpc_port: int):
    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=[payload.get_deposit_address()],
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs
    account = Account(input_private_key)
    inputs, change_outputs = create_normal_inputs(account.address(), total_amount, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.REGISTER_CR
    tx.payload_version = 0
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_crc_proposal_review_transaction(input_private_key: str, amount: int, payload: CRCProposalReview,
                                           rpc_port: int):
    # create outputs
    account = Account(input_private_key)
    outputs, total_amount = create_normal_outputs(
        output_addresses=[account.address()],
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs
    inputs, change_outputs = create_normal_inputs(account.address(), total_amount, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.CRC_PROPOSAL_REVIEW
    tx.payload_version = 0
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_crc_proposal_withdraw_transaction(input_address: str, amount: int, payload: CRCProposalWithdraw,
                                             rpc_port: int, output_address: str):
    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=[output_address],
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs
    inputs, change_outputs = create_normal_inputs(input_address, total_amount, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.CRC_PROPOSAL_WITHDRAW
    tx.payload_version = 0
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_crc_proposal_tracking_transaction(input_private_key: str, amount: int, payload: CRCProposalTracking,
                                             rpc_port: int):
    # create outputs
    account = Account(input_private_key)
    outputs, total_amount = create_normal_outputs(
        output_addresses=[account.address()],
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs
    inputs, change_outputs = create_normal_inputs(account.address(), total_amount, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.CRC_PROPOSAL_TRACKING
    tx.payload_version = 0
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_crc_proposal_transaction(input_private_key: str, amount: int, payload: CRCProposal, rpc_port: int):
    # create outputs
    account = Account(input_private_key)
    outputs, total_amount = create_normal_outputs(
        output_addresses=[account.address()],
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs
    inputs, change_outputs = create_normal_inputs(account.address(), total_amount, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.CRC_PROPOSAL
    tx.payload_version = 0
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_update_transaction(input_private_key: str, payload: ProducerInfo, rpc_port: int):
    # create inputs
    account = Account(input_private_key)
    inputs, change_outputs = create_normal_inputs(account.address(), util.TX_FEE, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None

    # create outputs
    outputs = list()
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    payload.gen_signature()

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.UPDATE_PRODUCER
    tx.payload_version = 0
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_cr_update_transaction(input_private_key: str, update_payload: CRInfo, rpc_port: int):
    # create inputs
    account = Account(input_private_key)
    inputs, change_outputs = create_normal_inputs(account.address(), util.TX_FEE, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None

    # create outputs
    outputs = list()
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    # update_payload.gen_signature()

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.UPDATE_CR
    tx.payload_version = 0
    tx.payload = update_payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_cancel_transaction(input_private_key: str, payload: ProducerInfo, rpc_port: int):
    # create inputs
    account = Account(input_private_key)
    inputs, change_outputs = create_normal_inputs(account.address(), util.TX_FEE, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None

    # create outputs
    outputs = list()
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    payload = ProcessProducer(bytes.fromhex(payload.owner_account.public_key()),
                              bytes.fromhex(payload.owner_account.private_key()))
    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.CANCEL_PRODUCER
    tx.payload_version = 0
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_cr_cancel_transaction(input_private_key: str, payload: UnRegisterCR, rpc_port: int):
    # create inputs
    account = Account(input_private_key)
    inputs, change_outputs = create_normal_inputs(account.address(), util.TX_FEE, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None

    # create outputs
    outputs = list()
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.UN_REGISTER_CR
    tx.payload_version = 0
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_redeem_transaction(payload: ProducerInfo, output_address: str, amount: int, rpc_port: int):
    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=[output_address],
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs

    deposit_address = payload.get_deposit_address()
    inputs, change_outputs = create_normal_inputs(deposit_address, total_amount, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(payload.owner_account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.RETURN_DEPOSIT_CHAIN
    tx.payload_version = 0
    tx.payload = Payload(Payload.DEFAULT_VERSION)
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_cr_redeem_transaction(payload: CRInfo, output_address: str, amount: int, rpc_port: int):
    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=[output_address],
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs

    deposit_address = payload.get_deposit_address()
    inputs, change_outputs = create_normal_inputs(deposit_address, total_amount, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(payload.account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.RETURN_CR_DEPOSIT_COIN
    tx.payload_version = 0
    tx.payload = Payload(Payload.DEFAULT_VERSION)
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_active_transaction(node_private_key: str, node_public_key: str):
    pub_key = bytes.fromhex(node_public_key)
    pri_key = bytes.fromhex(node_private_key)
    activate_producer = ProcessProducer(pub_key, pri_key)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.ACTIVATE_PRODUCER
    tx.payload = activate_producer
    tx.attributes = []
    tx.inputs = []
    tx.outputs = []
    tx.programs = list()
    tx.lock_time = 0

    return tx


def create_vote_transaction(input_private_key: str, candidates_list: list, amount: int, rpc_port: int, vote_content):
    # check output
    if candidates_list is None or len(candidates_list) == 0:
        Logger.error("Invalid output addresses")
        return None

    # candidates_bytes_list = list()
    #
    # for candidate in candidates_list:
    #     candidates_bytes_list.append(bytes.fromhex(candidate))

    # create outputs
    account = Account(input_private_key)
    outputs = create_vote_output(account.address(), amount, vote_content)

    # create inputs
    total_amount = amount + util.TX_FEE
    inputs, change_outputs = create_normal_inputs(account.address(), total_amount, rpc_port)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_09
    tx.tx_type = Transaction.TRANSFER_ASSET
    tx.payload = Payload(Payload.DEFAULT_VERSION)
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_normal_inputs_by_utxo(address: str, total_amount: int, utxos: list):
    global total_amount_global
    global response
    total_amount_global = total_amount

    inputs = list()
    change_outputs = list()
    program_hash = keytool.address_to_program_hash(address)

    for utxo in utxos:
        txid = util.bytes_reverse(bytes.fromhex(utxo["txid"]))
        index = utxo["vout"]
        input = Input(txid, index)
        inputs.append(input)

        amount = int(Decimal(utxo["amount"]) * util.TO_SELA)

        if amount < total_amount_global:
            # total_amount -= amount
            total_amount_global -= amount
        elif amount == total_amount_global:
            total_amount_global = 0
            break
        elif amount > total_amount_global:
            change = Output(
                value=amount - total_amount_global,
                output_lock=0,
                program_hash=program_hash,
                output_type=Output.OT_NONE,
                output_payload=OutputPayload()
            )
            change_outputs.append(change)
            total_amount_global = 0
            break

    if total_amount_global > 0:
        Logger.error("Available token is not enough!")
        return None, None

    return inputs, change_outputs

def create_normal_inputs(address: str, total_amount: int, rpc_port: int, utxo_index=-1):
    global total_amount_global
    global response
    total_amount_global = total_amount

    response = rpc.list_unspent_utxos(address, port=rpc_port)
    if not response or isinstance(response, dict):
        Logger.error("get utxos return error: {}".format(response))
        return None, None
    utxos = response
    if utxo_index >= 0 and len(utxos) >= utxo_index+1:
        utxo = utxos[utxo_index]
        utxos = list()
        utxos.append(utxo)

    inputs = list()
    change_outputs = list()

    program_hash = keytool.address_to_program_hash(address)

    for utxo in utxos:
        txid = util.bytes_reverse(bytes.fromhex(utxo["txid"]))
        index = utxo["vout"]
        input = Input(txid, index)
        inputs.append(input)

        amount = int(Decimal(utxo["amount"]) * util.TO_SELA)

        if amount < total_amount_global:
            # total_amount -= amount
            total_amount_global -= amount
        elif amount == total_amount_global:
            total_amount_global = 0
            break
        elif amount > total_amount_global:
            change = Output(
                value=amount - total_amount_global,
                output_lock=0,
                program_hash=program_hash,
                output_type=Output.OT_NONE,
                output_payload=OutputPayload()
            )
            change_outputs.append(change)
            total_amount_global = 0
            break

    if total_amount_global > 0:
        Logger.error("Available token is not enough!")
        return None, None

    return inputs, change_outputs


def create_normal_outputs(output_addresses: list, amount: int, fee: int, output_lock: int):
    total_amount = 0
    outputs = list()
    total_amount += fee

    global program_hash
    for address in output_addresses:
        if address == "0000000000000000000000000000000000":
            program_hash = bytes(21)
        else:
            program_hash = keytool.address_to_program_hash(address)

        output = Output(
            value=amount,
            output_lock=output_lock,
            program_hash=program_hash,
            output_type=Output.OT_NONE,
            output_payload=OutputPayload()
        )
        total_amount += amount
        outputs.append(output)

    return outputs, total_amount


def create_vote_output(output_address: str, amount: int, vote_content):
    outputs = list()
    program_hash = keytool.address_to_program_hash(output_address)

    # create output paylaod
    vote_info = VoteOutput(VoteOutput.VOTE_PRODUCER_AND_CR_VERSION, [vote_content])

    output = Output(
        value=amount,
        output_lock=0,
        program_hash=program_hash,
        output_type=Output.OT_VOTE,
        output_payload=vote_info,
    )

    outputs.append(output)

    return outputs


def deploy_contract_transaction(input_private_key: str, output_addresses: list, payload: NeoDeployContract, amount: int,
                                rpc_port: int):
    account = Account(input_private_key)
    # check output
    if output_addresses is None or len(output_addresses) == 0:
        Logger.error("Invalid output addresses")
        return None

    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=output_addresses,
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs
    inputs, change_outputs = create_normal_inputs(account.address(), total_amount, rpc_port)

    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_DEFAULT
    tx.tx_type = Transaction.DEPLOY
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def invoke_contract_transaction(input_private_key: str, output_addresses: list, payload: NeoInvokeContract, amount: int,
                                rpc_port: int):
    account = Account(input_private_key)
    # check output
    if output_addresses is None or len(output_addresses) == 0:
        Logger.error("Invalid output addresses")
        return None

    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=output_addresses,
        amount=amount,
        fee=util.TX_FEE,
        output_lock=0
    )

    # create inputs
    inputs, change_outputs = create_normal_inputs(account.address(), total_amount, rpc_port)

    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = bytes.fromhex(account.redeem_script())
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    tx = Transaction()
    tx.version = Transaction.TX_VERSION_DEFAULT
    tx.tx_type = Transaction.INVOKE
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def single_sign_transaction(input_private_key: str, tx: Transaction):
    data = tx.serialize_unsigned()
    signature = keytool.ecdsa_sign(bytes.fromhex(input_private_key), data)
    r = b""
    r = serialize.write_var_bytes(r, signature)
    tx.programs[0].parameter = r
    tx.hash()
    return tx


if __name__ == '__main__':
    pass

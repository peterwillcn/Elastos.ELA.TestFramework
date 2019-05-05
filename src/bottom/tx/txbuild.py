#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/4 11:44 AM
# author: liteng

from decimal import Decimal

from src.middle.tools import util
from src.middle.tools import constant
from src.middle.tools.log import Logger

from src.bottom.services import rpc2
from src.bottom.tx import serialize
from src.bottom.tx.input import Input
from src.bottom.tx.output import Output
from src.bottom.tx.program import Program
from src.bottom.tx.payload import Payload
from src.bottom.tx.attribute import Attribute
from src.bottom.tx.transaction import Transaction
from src.bottom.tx.producer_info import ProducerInfo
from src.bottom.tx.output_payload import OutputPayload
from src.bottom.tx.vote_content import VoteContent
from src.bottom.tx.vote_info import VoteInfo
from src.bottom.tx.process_producer import ProcessProducer
from src.bottom.wallet import keytool
from src.bottom.wallet.keystore import KeyStore


def create_transaction(keystore: KeyStore, output_addresses: list, amount: int, fee=10000, output_lock=0):
    # check output
    if output_addresses is None or len(output_addresses) == 0:
        Logger.error("Invalid output addresses")
        return None

    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=output_addresses,
        amount=amount,
        fee=fee,
        output_lock=output_lock
    )

    # create inputs
    inputs, change_outputs = create_normal_inputs(keystore.address, total_amount)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = keystore.sign_script
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


def create_register_transaction(keystore: KeyStore, output_addresses: list, amount: int,
                                payload: ProducerInfo, fee=10000, output_lock=0):
    # check output
    if output_addresses is None or len(output_addresses) == 0:
        Logger.error("Invalid output addresses")
        return None

    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=output_addresses,
        amount=amount,
        fee=fee,
        output_lock=output_lock
    )

    # create inputs
    inputs, change_outputs = create_normal_inputs(keystore.address, total_amount)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = keystore.sign_script
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


def create_update_transaction(keystore: KeyStore, payload: ProducerInfo):

    # create inputs
    fee = 10000
    inputs, change_outputs = create_normal_inputs(keystore.address, fee)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None

    # create outputs
    outputs = list()
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = keystore.sign_script
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
    tx.tx_type = Transaction.UPDATE_PRODUCER
    tx.payload_version = 0
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_cancel_transaction(owner_keystore: KeyStore):

    # create inputs
    fee = 10000
    inputs, change_outputs = create_normal_inputs(owner_keystore.address, fee)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None

    # create outputs
    outputs = list()
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = owner_keystore.sign_script
    program = Program(code=redeem_script, params=None)
    programs.append(program)

    # create attributes
    attributes = list()
    attribute = Attribute(
        usage=Attribute.NONCE,
        data=bytes("attributes".encode())
    )
    attributes.append(attribute)

    payload = ProcessProducer(owner_keystore.public_key, owner_keystore.private_key)
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


def create_redeem_transaction(keystore: KeyStore, amount: int):

    # create outputs
    outputs, total_amount = create_normal_outputs(
        output_addresses=[keystore.address],
        amount=amount,
        fee=10000,
        output_lock=0
    )

    # create inputs

    deposit_address = keytool.gen_deposit_address(keystore.program_hash)
    inputs, change_outputs = create_normal_inputs(deposit_address, total_amount)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = keystore.sign_script
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


def create_activate_producer(keystore: KeyStore):
    pub_key = keystore.public_key
    pri_key = keystore.private_key
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


def create_vote_transaction(keystore: KeyStore, cancadites_list: list, amount: int, fee=10000):
    # check output
    if cancadites_list is None or len(cancadites_list) == 0:
        Logger.error("Invalid output addresses")
        return None

    # create outputs
    outputs = create_vote_output(keystore.address, amount, cancadites_list)

    # create inputs
    total_amount = amount + fee
    inputs, change_outputs = create_normal_inputs(keystore.address, total_amount)
    if inputs is None or change_outputs is None:
        Logger.error("Create normal inputs failed")
        return None
    outputs.extend(change_outputs)

    # create program
    programs = list()
    redeem_script = keystore.sign_script
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


def create_normal_inputs(address: str, total_amount: int):
    global total_amount_global
    total_amount_global = total_amount
    total_amount_format = str(Decimal(str(total_amount_global)) / Decimal(constant.TO_SELA))
    response = rpc2.get_utxos_by_amount(address, total_amount_format)
    if isinstance(response, dict):
        Logger.debug("rpc return error: {}".format(response))
    utxos = response

    inputs = list()
    change_outputs = list()

    program_hash = keytool.address_to_program_hash(address)

    for utxo in utxos:
        txid = util.bytes_reverse(bytes.fromhex(utxo["txid"]))
        index = utxo["vout"]
        input = Input(txid, index)
        inputs.append(input)

        amount = int(Decimal(utxo["amount"]) * constant.TO_SELA)

        if amount < total_amount_global:
            total_amount -= amount
        elif amount == total_amount:
            total_amount_global = 0
            break
        elif amount > total_amount:
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

    for address in output_addresses:
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


def create_vote_output(output_address: str, amount: int, candidates_list: list):

    outputs = list()
    program_hash = keytool.address_to_program_hash(output_address)

    # create output paylaod
    vote_content = VoteContent(VoteContent.TYPE_DELEGATE, candidates_list)
    vote_info = VoteInfo(0, [vote_content])

    output = Output(
        value=amount,
        output_lock=0,
        program_hash=program_hash,
        output_type=Output.OT_VOTE,
        output_payload=vote_info,
    )

    outputs.append(output)

    return outputs


def single_sign_transaction(keystore: KeyStore, tx: Transaction):
    data = tx.serialize_unsigned()
    signature = keytool.ecdsa_sign(keystore.private_key, data)
    r = b""
    r = serialize.write_var_bytes(r, signature)
    tx.programs[0].parameter = r
    return tx


if __name__ == '__main__':

    pass

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/4 11:44 AM
# author: liteng

import sys
import random
from decimal import Decimal

from src.middle.tools import util
from src.middle.tools import constant
from src.middle.tools.log import Logger

from src.bottom.services import rpc2
from src.bottom.tx.input import Input
from src.bottom.tx.output import Output
from src.bottom.tx.program import Program
from src.bottom.tx.payload import Payload
from src.bottom.tx.attribute import Attribute
from src.bottom.tx.transaction import Transaction
from src.bottom.tx.output_payload import OutputPayload
from src.bottom.tx import serialize
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
    inputs, change_outputs = create_normal_inputs(keystore, total_amount)
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
    tx.payload = Payload()
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = 0
    tx.programs = programs

    return tx


def create_normal_inputs(keystore: KeyStore, total_amount: int):
    global total_amount_global
    total_amount_global = total_amount
    total_amount_format = str(Decimal(str(total_amount_global)) / Decimal(constant.TO_SELA))
    response = rpc2.get_utxos_by_amount(keystore.address, total_amount_format)
    if isinstance(response, dict):
        Logger.debug("rpc return error: {}".format(response))
    utxos = response

    inputs = list()
    change_outputs = list()

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
                program_hash=keystore.program_hash,
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


def single_sign_transaction(keystore: KeyStore, tx: Transaction):
    data = tx.serialize_unsigned()
    signature = keytool.ecdsa_sign(keystore.private_key, data)
    r = b""
    r = serialize.write_var_bytes(r, signature)
    tx.programs[0].parameter = r
    return tx


if __name__ == '__main__':

    pass

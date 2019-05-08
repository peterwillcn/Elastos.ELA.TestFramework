#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 10:15 AM
# author: liteng

import struct

from src.tools import util, serialize
from src.tools.log import Logger

from src.core.wallet import keytool
from src.core.tx.attribute import Attribute
from src.core.tx.input import Input
from src.core.tx.output import Output
from src.core.tx.program import Program
from src.core.tx.payload.payload import Payload
from src.core.tx.output_payload import OutputPayload


class Transaction(object):

    TX_VERSION_DEFAULT = 0x00
    TX_VERSION_09 = 0x09

    COIN_BASE = 0x00
    REGISTER_ASSET = 0x01
    TRANSFER_ASSET = 0x02
    RECORD = 0x03
    DEPLOY = 0x04

    SIDE_CHAIN_POW = 0x05
    RECHARGE_TO_SIDE_CHAIN = 0x06
    WITHDRAW_FROM_SIDE_CHAIN = 0x07
    TRANSFER_CROSS_CHAIN_ASSET = 0x08

    REGISTER_PRODUCER = 0x09
    CANCEL_PRODUCER = 0x0a
    UPDATE_PRODUCER = 0x0b
    RETURN_DEPOSIT_CHAIN = 0x0c
    ACTIVATE_PRODUCER = 0x0d

    ILLEGAL_PROPOSAL_EVIDENCE = 0x0e
    ILLEGAL_VOTE_EVIDENCE = 0x0f
    ILLEGAL_BLOCK_EVIDENCE = 0x10
    ILLEGAL_SIDE_CHAIN_EVIDENCE = 0x11
    INACTIVE_ARBITRATORS = 0x12

    UPDATE_VERSION = 0x13

    def __init__(self):
        self.version = 0
        self.tx_type = 0
        self.payload_version = 0
        self.payload = None
        self.attributes = None
        self.inputs = None
        self.outputs = None
        self.lock_time = 0
        self.programs = None
        self.fee = 0
        self.fee_per_kb = 0
        self.tx_hash = ""

    def __repr__(self):
        return "Transaction {" + "\n\t" \
                + "version: " + str(self.version) + "\n\t" \
                + "tx_type: " + str(self.tx_type) + "\n\t" \
                + "payload_version: " + str(self.payload_version) + "\n\t" \
                + "payload: {}".format(self.payload) + "\n\t"\
                + "attributes: {}".format(self.attributes) + "\n\t" \
                + "inputs: {}".format(self.inputs) + "\n\t" \
                + "outputs: {}".format(self.outputs) + "\n\t" \
                + "lock_time: " + str(self.lock_time) + "\n\t" \
                + "programs: {}".format(self.programs) + "\n\t" \
                + "fee: " + str(self.fee) + "\n\t" \
                + "fee_per_kb: " + str(self.fee_per_kb) + "\n\t" \
                + "tx_hash: " + self.tx_hash + "\n" \
                + "}"

    def serialize(self):
        r = self.serialize_unsigned()
        r += serialize.write_var_uint(len(self.programs))

        for program in self.programs:
            r += program.serialize()

        return r

    # serialize the Transaction data without contracts
    def serialize_unsigned(self):
        # version
        r = b""
        if self.version >= self.TX_VERSION_09:
            r += struct.pack(">B", self.version)

        # tx type
        r += struct.pack(">B", self.tx_type)

        # payload version
        r += struct.pack(">B", self.payload_version)

        # payload
        if self.payload is None:
            Logger.error("Transaction payload is None")
            return None

        if self.payload.data(self.payload_version) is not None:
            r += self.payload.data(self.payload_version)

        # attributes
        if self.attributes is not None:
            r += serialize.write_var_uint(len(self.attributes))
            for attribute in self.attributes:
                r += attribute.serialize()

        # inputs
        if self.inputs is not None:
            r += serialize.write_var_uint(len(self.inputs))
            for input in self.inputs:
                r += input.serialize()

        # outputs
        if self.outputs is not None:
            r += serialize.write_var_uint(len(self.outputs))
            for output in self.outputs:
                r += output.serialize(self.version)

        # lock_time
        r += struct.pack("<I", self.lock_time)

        return r

    def hash(self):
        if self.tx_hash is not "":
            return self.tx_hash
        r = self.serialize_unsigned()
        tx_hash_str = keytool.sha256_hash(r, 2).hex()
        self.tx_hash = tx_hash_str
        return tx_hash_str

    @staticmethod
    def get_tx_type(tx_type: int):
        if tx_type == 0x00:
            return "COIN_BASE"
        elif tx_type == 0x01:
            return "REGISTER_ASSET"
        elif tx_type == 0x02:
            return "TRANSFER_ASSET"
        elif tx_type == 0x03:
            return "RECORD"
        elif tx_type == 0x04:
            return "DEPLOY"
        elif tx_type == 0x05:
            return "SIDE_CHAIN_POW"
        elif tx_type == 0x06:
            return "RECHARGE_TO_SIDE_CHAIN"
        elif tx_type == 0x07:
            return "WITHDRAW_FROM_SIDE_CHAIN"
        elif tx_type == 0x08:
            return "TRANSFER_CROSS_CHAIN_ASSET"
        elif tx_type == 0x09:
            return "REGISTER_PRODUCER"
        elif tx_type == 0x0a:
            return "CANCEL_PRODUCER"
        elif tx_type == 0x0b:
            return "UPDATE_PRODUCER"
        elif tx_type == 0x0c:
            return "RETURN_DEPOSIT_CHAIN"
        elif tx_type == 0x0d:
            return "ACTIVATE_PRODUCER"
        elif tx_type == 0x0e:
            return "ILLEGAL_PROPOSAL_EVIDENCE"
        elif tx_type == 0x0f:
            return "ILLEGAL_VOTE_EVIDENCE"
        elif tx_type == 0x10:
            return "ILLEGAL_BLOCK_EVIDENCE"
        elif tx_type == 0x11:
            return "ILLEGAL_SIDE_CHAIN_EVIDENCE"
        elif tx_type == 0x12:
            return "INACTIVE_ARBITRATORS"
        elif tx_type == 0x13:
            return "UPDATE_VERSION"


if __name__ == '__main__':
    txid = "16c90c1e3a45cdf11f39fe0aa9f5eaea8fd0e6ab8bf5830c8cec4029c5964498"
    index = 2
    tx_id = util.bytes_reverse(bytes.fromhex(txid))
    input = Input(tx_id, index)
    inputs = list()
    inputs.append(input)

    outputs = list()
    address = "EUrmyVjtQkUijfffapHM6tJrw7EN2vUHxp"
    program_hash = keytool.address_to_program_hash(address)
    amount = 123
    output_lock = 0
    output = Output(
        value=amount,
        output_lock=output_lock,
        program_hash=program_hash,
        output_type=Output.OT_NONE,
        output_payload=OutputPayload()
    )
    outputs.append(output)

    programs = list()
    redeem_script = bytes.fromhex("2102d5b81d2f002b1ace56f6da5a35322df75544d71699af31bd30cfbfd348a61e15ac")
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

    r = tx.serialize()
    r2 = tx.serialize_unsigned()

    print(tx)
    print("transaction serial: ", r.hex())
    print("tx serial unsigned: ", r2.hex())


#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 10:15 AM
# author: liteng

import struct

from src.middle.tools.log import Logger

from src.bottom.wallet import keytool
from src.bottom.tx.attribute import Attribute
from src.bottom.tx.input import Input
from src.bottom.tx.output import Output
from src.bottom.tx.outpoint import OutPoint
from src.bottom.tx.program import Program
from src.bottom.tx.active_producer import ActiveProducer
from src.bottom.tx import serialize


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
                + "attributes: ".format(self.attributes) + "\n\t" \
                + "inputs: ".format(self.inputs) + "\n\t" \
                + "outputs: ".format(self.outputs) + "\n\t" \
                + "lock_time: " + str(self.lock_time) + "\n\t" \
                + "programs: ".format(self.programs) + "\n\t" \
                + "fee: " + str(self.fee) + "\n\t" \
                + "fee_per_kb: " + str(self.fee_per_kb) + "\n\t" \
                + "tx_hash: " + self.tx_hash + "\n\t" \
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

        r += self.payload.data(self.payload_version)

        # attributes
        r += serialize.write_var_uint(len(self.attributes))
        for attribute in self.attributes:
            r += attribute.serialize()

        # inputs
        r += serialize.write_var_uint(len(self.inputs))
        for input in self.inputs:
            r += input.serialize()

        # outputs
        r += serialize.write_var_uint(len(self.outputs))
        for output in self.outputs:
            r += output.serialize(self.version)

        # lock_time
        r += struct.pack("<I", self.lock_time)

        return r

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

    version = Transaction.TX_VERSION_DEFAULT
    tx_type = Transaction.ACTIVATE_PRODUCER
    payload_version = 0x00

    public_key_str = "02517f74990da8de27d0bc7c516c45ecbb9b2aa6a4d4d5ab552b537e638fcfe45f"
    node_public_key = bytes.fromhex(public_key_str)
    signature = keytool.sha256_hash(node_public_key, 2)
    ap = ActiveProducer(node_public_key, signature)

    payload = ap

    usage = 0x81
    r = struct.pack("B", usage)
    data = bytes([1, 2, 3])
    attribute = Attribute(usage, data)

    attributes = [attribute]

    hash = keytool.sha256_hash(bytes("hello".encode("utf-8")), 2)
    index = 21

    op = OutPoint(hash.hex(), index)
    print(op)
    serial = op.serialize()
    input = Input(op, 100)

    inputs = [input]

    value = 12
    output_lock = 567
    output_type = 11
    asset_id = keytool.sha256_hash("assetid".encode(), 2)
    program_hash = keytool.sha256_hash("programhash".encode(), 2)[:21]
    output = Output(
        asset_id=asset_id,
        value=value,
        output_lock=output_lock,
        program_hash=program_hash,
        output_type=output_type,
        output_payload=None
    )

    outputs = [output]
    lock_time = 99

    p = Program(bytes([1, 2]), bytes([3, 4, 5]))

    programs = [p]
    fee = 100
    fee_per_kb = 10

    tx = Transaction()
    tx.version = version
    tx.tx_type = tx_type
    tx.payload_version = payload_version
    tx.payload = payload
    tx.attributes = attributes
    tx.inputs = inputs
    tx.outputs = outputs
    tx.lock_time = lock_time
    tx.programs = programs
    tx.fee = fee
    tx.fee_per_kb = fee_per_kb

    s = tx.serialize()

    print(tx)
    print("tx serial: ", s.hex())
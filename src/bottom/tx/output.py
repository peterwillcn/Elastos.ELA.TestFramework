#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 3:33 PM
# author: liteng

import struct
# from src.bottom.tx.transaction import Transaction
from src.bottom.wallet import keytool


class Output(object):
    def __init__(self, asset_id=None, value=0, output_lock=0, program_hash=None, output_type=0, output_payload=None):

        self.asset_id = asset_id
        self.value = value
        self.output_lock = output_lock
        self.program_hash = program_hash
        self.type = output_type
        self.output_payload = output_payload

    def deserialize(self, f):
        pass

    def serialize(self, tx_version):
        r = b""
        r += self.asset_id
        r += struct.pack("<q", self.value)
        r += struct.pack("<I", self.output_lock)
        r += self.program_hash

        if tx_version >= 0x09:
            r += struct.pack("<B", self.type)
            r += self.output_payload.serialize()
        return r

    def __repr__(self):
        return "Output {" + "\n\t" \
                + "asset_id: " + self.asset_id.hex() + "\n\t" \
                + "value: " + str(self.value) + "\n\t" \
                + "output_lock: " + str(self.output_lock) + "\n\t" \
                + "program_hash: " + self.program_hash.hex() + "\n\t" \
                + "type: " + str(self.type) + "\n\t" \
                + "output_payload: " + "" + "\n" \
                + "}"


if __name__ == '__main__':

    value = 12
    value_serial = struct.pack("q", value)
    print("value serial: ", value_serial.hex())

    output_lock = 567
    lock_serial = struct.pack("I", output_lock)
    print("lock  serial: ", lock_serial.hex())

    output_type = 11
    type_serial = struct.pack("B", output_type)
    print("output type serial: ", type_serial.hex())

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

    r = output.serialize(0x00)

    print("output: ", output)
    print("output serial: ", r.hex())
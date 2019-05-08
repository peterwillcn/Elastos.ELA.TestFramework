#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 3:33 PM
# author: liteng

import struct

from src.tools import util
from src.core.wallet import keytool
from src.core.tx.output_payload import OutputPayload


class Output(object):

    ASSET_ID = "a3d0eaa466df74983b5d7c543de6904f4c9418ead5ffd6d25814234a96db37b0"
    OT_NONE = 0
    OT_VOTE = 1
    OT_MAPPING = 2

    def __init__(self, value=0, output_lock=0, program_hash=None, output_type=0, output_payload=None):

        self.asset_id = util.bytes_reverse(bytes.fromhex(self.ASSET_ID))
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
            if self.output_payload.serialize() is not None:
                r += self.output_payload.serialize()
        return r

    def __repr__(self):
        return "Output {" + "\n\t" \
                + "asset_id: " + self.asset_id.hex() + "\n\t" \
                + "value: " + str(self.value) + "\n\t" \
                + "output_lock: " + str(self.output_lock) + "\n\t" \
                + "program_hash: " + self.program_hash.hex() + "\n\t" \
                + "type: " + str(self.type) + "\n\t" \
                + "output_payload: {}".format(self.output_payload) + "\n" \
                + "}"


if __name__ == '__main__':

    address = "EUrmyVjtQkUijfffapHM6tJrw7EN2vUHxp"
    program_hash2 = "218064296606c4d98600133d76c26eb037d62522fd"
    program_hash = keytool.address_to_program_hash(address)
    print("program Hash: ", program_hash.hex())
    amount = 123
    output_lock = 0
    output = Output(
        value=amount,
        output_lock=output_lock,
        program_hash=program_hash,
        output_type=Output.OT_NONE,
        output_payload=OutputPayload()
    )

    r = output.serialize(0x09)
    print("output serial: ", r.hex())
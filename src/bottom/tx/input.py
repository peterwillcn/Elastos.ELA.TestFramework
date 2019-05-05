#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 2:17 PM
# author: liteng

import struct

from src.middle.tools import util

from src.bottom.services.rpc import RPC
from src.bottom.wallet import keytool
from src.bottom.tx.outpoint import OutPoint


class Input(object):
    def __init__(self, tx_id: bytes, index: int, sequence=0):
        self.previous = OutPoint(tx_id, index)
        self.sequence = sequence

    def deserialize(self, f):
        self.previous.deserialize(f)
        self.sequence = struct.unpack("<I", f.read(4))[0]

    def serialize(self):
        r = b""
        r += self.previous.serialize()
        r += struct.pack("<I", self.sequence)
        return r

    def __repr__(self):
        return "Input{" + "\n\t" \
                + "previous: {}".format(repr(self.previous)) + "\n\t" \
                + "sequence: {}".format(self.sequence) + "\n" \
                + "}"


if __name__ == '__main__':

    # txid = "16c90c1e3a45cdf11f39fe0aa9f5eaea8fd0e6ab8bf5830c8cec4029c5964498"
    # index = 2
    # tx_id = util.bytes_reverse(bytes.fromhex(txid))
    # input = Input(tx_id, index)
    #
    # r = input.serialize()
    # print(input)
    # print("input serial: ", r.hex())

    rpc = RPC()
    address = "EKpcRUrdJz1cs5zKNDj5WDXsv3TVN9qqco"
    # address2 = "ETJSRdS4fTh89bdHmWbfSt7HAXpwweqykB"
    amount = 10.0001
    response = rpc.get_utxos_by_amount(address, str(amount))
    print("type: ", type(response))
    print("response: {}".format(response))
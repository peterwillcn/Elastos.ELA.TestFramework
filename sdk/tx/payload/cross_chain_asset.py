#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/7 11:34 AM
# author: liteng

import struct

from sdk.common.log import Logger

from sdk.common import serialize
from sdk.tx.payload.payload import Payload


class TransferCrossChainAsset(Payload):

    def __init__(self):
        Payload.__init__(self, Payload.DEFAULT_VERSION)
        self.cross_chain_addresses = list()
        self.output_indexes = list()
        self.cross_chain_amounts = list()

    def data(self, version: int):
        r = b""
        r = self.serialize(r, version)
        return r

    def serialize(self, r: bytes, version: int):
        if len(self.cross_chain_addresses) != len(self.output_indexes) or \
                len(self.cross_chain_addresses) != len(self.cross_chain_addresses):
            Logger.error("Invalid cross chain asset")
            return None

        r += serialize.write_var_uint(len(self.cross_chain_addresses))

        for i in range(len(self.cross_chain_addresses)):
            r = serialize.write_var_bytes(r, bytes(self.cross_chain_addresses[i].encode()))
            r += serialize.write_var_uint(self.output_indexes[i])
            r += struct.pack("<q", self.cross_chain_amounts[i])

        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def __repr__(self):

        return "TransferCrossChainAsset {" + "\n\t" \
                + "cross_chain_addresses: {}".format(self.cross_chain_addresses) + "\n\t" \
                + "output_indexes: {}".format(self.output_indexes) + "\n\t" \
                + "cross_chain_amounts: {}".format(self.cross_chain_amounts) + "\n" \
                + "}"


if __name__ == '__main__':

    cross_asset = TransferCrossChainAsset()
    cross_asset.cross_chain_addresses = ["EZRm8DiVGwSRXuCofehywZWAa3feJfESVu"]
    cross_asset.output_indexes = [0]
    cross_asset.cross_chain_amounts = [19999990000]

    r = cross_asset.data(cross_asset.version)

    print("cross asset: \n{}".format(cross_asset))
    print("cross asset serial: {}".format(r.hex()))
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/2 11:48 AM
# author: liteng


from src.core.tx.payload.payload import Payload
from src.tools import serialize
from src.core.wallet import keytool


class ProcessProducer(Payload):

    PROCESS_PRODUCER_VERSION = 0x00

    def __init__(self, pub_key=None, pri_key=None, signature=None):
        Payload.__init__(self, self.PROCESS_PRODUCER_VERSION)
        self.public_key = pub_key
        self.private_key = pri_key
        if pub_key is not None and pri_key is not None:
            self.signature = self.set_signature()

    def data(self, version):
        r = b""
        r = self.serialize(r, version)
        return r

    def serialize(self, r: bytes, version: int):
        r = self.serialize_unsigned(r, version)
        r = serialize.write_var_bytes(r, self.signature)
        return r

    def serialize_unsigned(self, r: bytes, version: int):
        r = serialize.write_var_bytes(r, self.public_key)
        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def set_signature(self):
        data = b""
        data = self.serialize_unsigned(data, self.PROCESS_PRODUCER_VERSION)
        return keytool.ecdsa_sign(self.private_key, data)

    def __repr__(self):
        if self.public_key is None:
            arg1 = ""
        else:
            arg1 = self.public_key.hex()

        if self.private_key is None:
            arg2 = ""
        else:
            arg2 = self.private_key.hex()

        if self.signature is None:
            arg3 = ""
        else:
            arg3 = self.signature.hex()

        return "ProcessProducer{\n\t" \
                + "node_public_key: {}".format(arg1) + "\n\t" \
                + "node_private_key: {}".format(arg2) + "\n\t" \
                + "signature: {}".format(arg3) + "\n" \
                + "}"



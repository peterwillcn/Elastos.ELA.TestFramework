#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/2 11:48 AM
# author: liteng


from src.bottom.tx.payload import Payload
from src.bottom.tx import serialize
from src.bottom.wallet import keytool


class ActiveProducer(Payload):

    def __init__(self, node_public_key=None, signature=None):
        Payload.__init__(self)
        self.node_public_key = node_public_key
        self.signature = signature

    def data(self, version):
        r = b""
        r = self.serialize(r, version)
        return r

    def serialize(self, r: bytes, version: int):
        r = self.serialize_unsigned(r, version)
        r = serialize.write_var_bytes(r, self.signature)
        return r

    def serialize_unsigned(self, r: bytes, version: int):
        r = serialize.write_var_bytes(r, self.node_public_key)
        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def __repr__(self):

        return "ActiveProducer {\n\tnode_public_key: " + self.node_public_key.hex() + \
               "\n\tsignature: " + self.signature.hex() + "\n}"


if __name__ == '__main__':

    public_key_str = "02517f74990da8de27d0bc7c516c45ecbb9b2aa6a4d4d5ab552b537e638fcfe45f"
    node_public_key = bytes.fromhex(public_key_str)
    signature = keytool.sha256_hash(node_public_key, 2)

    ap = ActiveProducer(node_public_key, signature)
    print(ap)

    r = ap.data(0x09)
    print("active producer serial: ", r.hex())

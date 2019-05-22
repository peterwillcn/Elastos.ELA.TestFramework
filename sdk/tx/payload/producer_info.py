#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/5 11:24 AM
# author: liteng

import struct

from sdk.common import serialize

from sdk.tx.payload.payload import Payload
from sdk.wallet import keytool
from sdk.wallet.account import Account


class ProducerInfo(Payload):

    def __init__(self, owner_private_key: str, node_private_key: str, nickname: str, url: str, location: int,
                 net_address: str):
        Payload.__init__(self, self.DEFAULT_VERSION)
        self.owner_account = Account(owner_private_key)
        self.node_account = Account(node_private_key)
        self.nickname = nickname
        self.url = url
        self.location = location
        self.net_address = net_address
        self.signature = self.gen_signature()

    def gen_signature(self):
        r = b""
        r = self.serialize_unsigned(r, self.version)
        signature = keytool.ecdsa_sign(bytes.fromhex(self.owner_account.private_key()), r)
        self.signature = signature
        return signature

    def data(self, version):
        r = b""
        r = self.serialize(r, version)

        return r

    def serialize(self, r: bytes, version: int):
        r = self.serialize_unsigned(r, version)
        if self.signature is not None:
            r = serialize.write_var_bytes(r, self.signature)

        return r

    def serialize_unsigned(self, r: bytes, version=0):
        r = serialize.write_var_bytes(r, bytes.fromhex(self.owner_account.public_key()))
        r = serialize.write_var_bytes(r, bytes.fromhex(self.node_account.public_key()))
        r = serialize.write_var_bytes(r, bytes(self.nickname.encode()))
        r = serialize.write_var_bytes(r, bytes(self.url.encode()))
        r += struct.pack("<Q", self.location)
        r = serialize.write_var_bytes(r, bytes(self.net_address.encode()))
        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def deserialize_unsigned(self, r: bytes, version: int):
        pass

    def get_deposit_address(self):
        return self.owner_account.deposit_address()

    def __repr__(self):
        return "ProducerInfo {" + "\n\t" \
                + "owner_public_key: {}".format(self.owner_account.public_key()) + "\n\t" \
                + "node_public_key : {}".format(self.node_account.public_key()) + "\n\t" \
                + "nickname: {}".format(self.nickname) + "\n\t" \
                + "url: {}".format(self.url) + "\n\t" \
                + "location: {}".format(self.location) + "\n\t" \
                + "net_address: {}".format(self.net_address) + "\n" \
                + "}"







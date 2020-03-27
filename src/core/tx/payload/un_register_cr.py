#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/8/2 12:36 PM
# author: liteng

from src.tools import serialize
from src.core.wallet import keytool
from src.core.tx.payload.payload import Payload
from src.core.wallet.account import Account


class UnRegisterCR(Payload):

    def __init__(self, register_private_key: str):
        Payload.__init__(self, self.DEFAULT_VERSION)
        self.account = Account(register_private_key)
        self.cid = self.account.cid()
        self.signature = None
        self.gen_signature()
        self.serialize_data = None

    def gen_signature(self):
        r = b""
        r = self.serialize_unsigned(r, self.version)
        signature = keytool.ecdsa_sign(bytes.fromhex(self.account.private_key()), r)
        self.signature = signature

    def data(self, version: int):
        r = b""
        if self.serialize_data is not None:
            return self.serialize_data

        r = self.serialize(r, self.version)
        self.serialize_data = r
        return r

    def serialize(self, r: bytes, version: int):
        r = self.serialize_unsigned(r, self.version)
        if self.signature is not None:
            r = serialize.write_var_bytes(r, self.signature)
        return r

    def serialize_unsigned(self, r: bytes, version: int):
        r += bytes.fromhex(self.cid)

        return r

    def deserialize(self, r: bytes, version: int):
        pass

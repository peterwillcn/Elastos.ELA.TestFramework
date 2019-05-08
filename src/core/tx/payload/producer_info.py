#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/5 11:24 AM
# author: liteng

import struct

from src.tools import util, serialize
from src.tools.log import Logger

from src.core.tx.payload.payload import Payload
from src.core.wallet import keytool


class ProducerInfo(Payload):

    def __init__(self, private_key: bytes, owner_public_key: bytes, node_public_key: bytes,
                 nickname: str, url: str, location: int, net_address: str):
        Payload.__init__(self, self.DEFAULT_VERSION)
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.private_key = private_key
        self.owner_public_key = owner_public_key
        self.node_public_key = node_public_key
        self.nickname = nickname
        self.url = url
        self.location = location
        self.net_address = net_address
        self.signature = self.gen_signature()

    def gen_signature(self):
        r = b""
        r = self.serialize_unsigned(r, self.version)
        signature = keytool.ecdsa_sign(self.private_key, r)
        Logger.debug("{} len signature: {}".format(self.tag, len(signature)))
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
        r = serialize.write_var_bytes(r, self.owner_public_key)
        r = serialize.write_var_bytes(r, self.node_public_key)
        r = serialize.write_var_bytes(r, bytes(self.nickname.encode()))
        r = serialize.write_var_bytes(r, bytes(self.url.encode()))
        r += struct.pack("<Q", self.location)
        r = serialize.write_var_bytes(r, bytes(self.net_address.encode()))
        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def deserialize_unsigned(self, r: bytes, version: int):
        pass

    def __repr__(self):
        return "ProducerInfo {" + "\n\t" \
                + "owner_public_key: {}".format(self.owner_public_key.hex()) + "\n\t" \
                + "node_public_key : {}".format(self.node_public_key.hex()) + "\n\t" \
                + "nickname: {}".format(self.nickname) + "\n\t" \
                + "url: {}".format(self.url) + "\n\t" \
                + "location: {}".format(self.location) + "\n\t" \
                + "net_address: {}".format(self.net_address) + "\n" \
                + "}"


if __name__ == '__main__':

    private_key = "579701507deb7b1917e26ce213d7c53b24d60e552f777db5fbdc3d0970ebef82"
    owner_public_key = "03d758bcf43cd1a61920b8982e251f74a1f477aad187aaa5fcd38eb33c823a3d3e"
    node_public_key = "02d33b5c12970fe3fda9adc5de4e94349fe18b6e96aff4fd779379d76884f4bfca"
    nickname = "RPO-001"
    url = "http://elastos.org"
    location = 1
    net_address = "127.0.0.1:10014"

    pro_info = ProducerInfo(
        private_key=bytes.fromhex(private_key),
        owner_public_key=bytes.fromhex(owner_public_key),
        node_public_key=bytes.fromhex(node_public_key),
        nickname=nickname,
        url=url,
        location=location,
        net_address=net_address
    )

    print(pro_info)

    r = b""
    print("type r: ", type(r))
    r = pro_info.serialize_unsigned(r, 0)
    print("pro info serial unsigned: ", r.hex())





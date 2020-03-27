
import struct

from src.tools import serialize
from src.tools.log import Logger

from src.core.wallet.account import Account
from src.core.tx.payload.payload import Payload
from src.core.wallet import keytool


class CRInfo(Payload):
    CR_INFO_VERSION = 0x00
    CR_INFO_DID_VERSION = 0x01

    def __init__(self, private_key: str, nickname: str, url: str, location: int):
        Payload.__init__(self, self.DEFAULT_VERSION)
        self.account = Account(private_key)
        self.nickname = nickname
        self.url = url
        self.location = location
        self.code = self.account.redeem_script()
        self.cid = self.account.cid()
        self.did = self.account.did()
        self.signature = None
        self.gen_signature()
        self.serialize_data = None

    def data(self, version: int):
        if self.serialize_data is not None:
            return self.serialize_data
        r = b""
        r = self.serialize(r, self.version)
        self.serialize_data = r
        return r

    def serialize(self, r: bytes, version: int):
        r = self.serialize_unsigned(r, version)

        if self.signature is not None:
            r = serialize.write_var_bytes(r, self.signature)

        return r

    def serialize_unsigned(self, r: bytes, version=0):
        r = serialize.write_var_bytes(r, bytes.fromhex(self.code))
        r += bytes.fromhex(self.cid)
        r += bytes.fromhex(self.did)
        r = serialize.write_var_bytes(r, bytes(self.nickname.encode()))
        r = serialize.write_var_bytes(r, bytes(self.url.encode()))
        r += struct.pack("<Q", self.location)

        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def get_deposit_address(self):
        return self.account.deposit_address()

    def gen_signature(self):
        r = b""
        r = self.serialize_unsigned(r, self.version)
        signature = keytool.ecdsa_sign(bytes.fromhex(self.account.private_key()), r)
        self.signature = signature
        return signature

    def __repr__(self):
        return "CRInfo {" + "\n\t" \
               + "code: {}".format(self.code) + "\n\t" \
               + "cid : {}".format(keytool.create_address(bytes.fromhex(self.cid))) + "\n\t" \
               + "did : {}".format(keytool.create_address(bytes.fromhex(self.did))) + "\n\t" \
               + "nickname: {}".format(self.nickname) + "\n\t" \
               + "url: {}".format(self.url) + "\n\t" \
               + "location: {}".format(self.location) + "\n\t" \
               + "signature: {}".format(self.signature.hex()) + "\n" \
               + "}"


if __name__ == '__main__':
    sig = "10e04ca9c43999fe7479ce0249c34f1f82aa97f073b667f08a49cdd0afa5663f93f16acb0f26a04500597d0eb62f4c50ab225e9af3c03c81a899fedd2f22ce6f"

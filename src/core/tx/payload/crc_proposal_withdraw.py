import struct

from src.tools import serialize
from src.tools.log import Logger

from src.core.wallet.account import Account
from src.core.tx.payload.payload import Payload
from src.core.wallet import keytool


class CRCProposalWithdraw(Payload):

    def __init__(self, private_key: str, proposal_hash: bytes):
        Payload.__init__(self, self.DEFAULT_VERSION)
        self.account = Account(private_key)
        self.proposal_hash = proposal_hash
        self.sponsor_public_key = bytes.fromhex(self.account.public_key())
        self.sign = None
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
        r = serialize.write_var_bytes(r, self.sign)
        return r

    def serialize_unsigned(self, r: bytes, version=0):
        r += self.proposal_hash
        r = serialize.write_var_bytes(r, self.sponsor_public_key)
        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def gen_signature(self):
        r = b""
        r = self.serialize_unsigned(r, self.version)
        self.sign = keytool.ecdsa_sign(bytes.fromhex(self.account.private_key()), r)
        return r

    def __repr__(self):
        return "CRCProposalWithdraw {" + "\n\t" \
               + "proposal_hash: {}".format(self.proposal_hash.hex()) + "\n\t" \
               + "sponsor_public_key : {}".format(self.sponsor_public_key.hex()) + "\n\t" \
               + "sign: {}".format(self.sign.hex()) + "\n\t" \
               + "}"

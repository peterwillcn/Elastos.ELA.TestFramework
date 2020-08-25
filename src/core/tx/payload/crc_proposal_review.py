
import struct

from src.tools import serialize
from src.tools.log import Logger

from src.core.wallet.account import Account
from src.core.tx.payload.payload import Payload
from src.core.wallet import keytool


class CRCProposalReview(Payload):
    APPROVE = 0x00
    REJECT = 0x01
    ABSTAIN = 0x02

    def __init__(self, private_key: str, proposal_hash: bytes, vote_result: int, opinion_hash: bytes):
        Payload.__init__(self, self.DEFAULT_VERSION)
        self.account = Account(private_key)
        self.proposal_hash = proposal_hash
        self.vote_result = vote_result
        self.opinion_hash = opinion_hash
        self.did = bytes.fromhex(self.account.did())
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
        r += struct.pack("<B", self.vote_result)
        r += self.opinion_hash
        r += self.did
        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def gen_signature(self):
        r = b""
        r = self.serialize_unsigned(r, self.version)
        self.sign = keytool.ecdsa_sign(bytes.fromhex(self.account.private_key()), r)
        return r

    def __repr__(self):
        return "CRCProposalReview {" + "\n\t" \
               + "privateKey: {}".format(self.account.private_key()) + "\n\t" \
               + "proposalHash: {}".format(self.proposal_hash.hex()) + "\n\t" \
               + "voteResult : {}".format(self.vote_result) + "\n\t" \
               + "crOpinionHash: {}".format(self.opinion_hash.hex()) + "\n\t" \
               + "did : {}".format(keytool.create_address(self.did)) + "\n\t" \
               + "sign: {}".format(self.sign.hex()) + "\n\t" \
               + "}"

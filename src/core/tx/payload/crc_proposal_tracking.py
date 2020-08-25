import struct

from src.tools import serialize
from src.tools.log import Logger

from src.core.wallet.account import Account
from src.core.tx.payload.payload import Payload
from src.core.wallet import keytool


class CRCProposalTracking(Payload):
    COMMON = 0x00
    PROGRESS = 0x01
    REJECTED = 0x02
    TERMINATED = 0x03
    PROPOSAL_LEADER = 0x04
    FINALIZED = 0x05

    DEFAULT = 0x00

    def __init__(self, secretary_private_key: str, leader_private_key: str, new_leader_private_key,
                 tracking_type: int, proposal_hash: bytes,
                 document_hash: bytes, stage: int, secretary_opinion_hash: bytes):
        Payload.__init__(self, self.DEFAULT_VERSION)
        self.secretary_general_account = Account(secretary_private_key)
        self.leader_account = Account(leader_private_key)
        self.new_leader_account = None
        self.proposal_hash = proposal_hash
        self.document_hash = document_hash
        self.stage = stage
        self.leader_public_key = bytes.fromhex(self.leader_account.public_key())
        self.new_leader_public_key = None
        self.proposal_tracking_type = tracking_type
        self.secretary_opinion_hash = secretary_opinion_hash
        self.secretary_general_sign = None
        self.leader_sign = None
        self.new_leader_sign = None
        self._get_new_leader_account(new_leader_private_key)
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
        r = serialize.write_var_bytes(r, self.leader_sign)
        if self.new_leader_sign is not None:
            r = serialize.write_var_bytes(r, self.new_leader_sign)
        else:
            r += struct.pack("<B", CRCProposalTracking.DEFAULT)
        r += struct.pack("<B", self.proposal_tracking_type)
        r += self.secretary_opinion_hash
        r = serialize.write_var_bytes(r, self.secretary_general_sign)
        return r

    def serialize_unsigned(self, r: bytes, version=0):
        r += self.proposal_hash
        r += self.document_hash
        r += serialize.write_var_uint(self.stage)
        r = serialize.write_var_bytes(r, self.leader_public_key)
        if self.new_leader_public_key is not None:
            r = serialize.write_var_bytes(r, self.new_leader_public_key)
        else:
            r += struct.pack("<B", CRCProposalTracking.DEFAULT)
        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def gen_signature(self):
        r = b""
        r = self.serialize_unsigned(r, self.version)
        self.leader_sign = keytool.ecdsa_sign(bytes.fromhex(self.leader_account.private_key()), r)
        r = serialize.write_var_bytes(r, self.leader_sign)
        if self.new_leader_account is not None:
            self.new_leader_sign = keytool.ecdsa_sign(bytes.fromhex(self.new_leader_account.private_key()), r)
            r = serialize.write_var_bytes(r, self.new_leader_sign)
        else:
            self.new_leader_sign = None
            r += struct.pack("<B", CRCProposalTracking.DEFAULT)
        r += struct.pack("<B", self.proposal_tracking_type)
        r += self.secretary_opinion_hash
        self.secretary_general_sign = keytool.ecdsa_sign(bytes.fromhex(self.secretary_general_account.private_key()), r)
        return r

    def _get_new_leader_account(self, new_leader_private_key):
        if new_leader_private_key is not None:
            self.new_leader_account = Account(new_leader_private_key)
            self.new_leader_public_key = bytes.fromhex(self.new_leader_account.public_key())

    def __repr__(self):
        return "CRCProposalTracking {" + "\n\t" \
               + "SecretaryGeneralPrivateKey: {}".format(self.secretary_general_account.private_key()) + "\n\t" \
               + "proposalTrackingType: {}".format(self.proposal_tracking_type) + "\n\t" \
               + "proposalHash: {}".format(self.proposal_hash.hex()) + "\n\t" \
               + "documentHash : {}".format(self.document_hash) + "\n\t" \
               + "stage : {}".format(self.stage) + "\n\t" \
               + "leaderPublicKey: {}".format(self.leader_public_key.hex()) + "\n\t" \
               + "newLeaderPublicKey: {}".format(self.new_leader_public_key) + "\n\t" \
               + "leaderSign: {}".format(self.leader_sign.hex()) + "\n\t" \
               + "newLeaderSign: {}".format(self.new_leader_sign) + "\n\t" \
               + "secretaryOpinionHash: {}".format(self.secretary_opinion_hash) + "\n\t" \
               + "secretaryGeneralSign: {}".format(self.secretary_general_sign.hex()) + "\n\t" \
               + "}"

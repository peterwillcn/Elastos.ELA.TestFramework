import struct

from src.tools import serialize

from src.core.wallet.account import Account
from src.core.tx.payload.payload import Payload
from src.core.wallet import keytool


class CRCProposal(Payload):
    NORMAL = 0x0000
    ELIP = 0x0100
    FLOW_ELIP = 0x0101
    INFO_ELIP = 0x0102
    MAIN_CHAIN_UPGRADE_CODE = 0x0200
    SIDE_CHAIN_UPGRADE_CODE = 0x0300
    REGISTER_SIDE_CHAIN = 0x0301
    SECRETARY_GENERAL = 0x0400
    CHANGE_SPONSOR = 0x0401
    CLOSE_PROPOSAL = 0x0402
    DAPP_CONSENSUS = 0x0500
    WRONG = 0x4321

    def __init__(self, private_key: str, cr_private_key: str, proposal_type: int, category_data: str,
                 draft_hash: bytes, budget: list, recipient: bytes):
        Payload.__init__(self, self.DEFAULT_VERSION)
        self.account = Account(private_key)
        self.cr_account = Account(cr_private_key)
        self.proposal_type = proposal_type
        self.category_data = category_data
        self.draft_hash = draft_hash
        self.budget = budget
        self.recipient = recipient
        self.sign = None
        self.cr_sponsor_did = bytes.fromhex(self.cr_account.did())
        self.cr_sign = None
        self.gen_signature()
        self.hash = self.gen_hash()
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
        r += self.cr_sponsor_did
        r = serialize.write_var_bytes(r, self.cr_sign)
        return r

    def serialize_unsigned(self, r: bytes, version=0):
        r += struct.pack("<H", self.proposal_type)
        r = serialize.write_var_bytes(r, bytes(self.category_data.encode()))
        r = serialize.write_var_bytes(r, bytes.fromhex(self.account.public_key()))
        r += self.draft_hash
        r += serialize.write_var_uint(len(self.budget))
        for budget in self.budget:
            r += budget.serialize(version)
        r += self.recipient
        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def get_deposit_address(self):
        return self.account.deposit_address()

    def gen_signature(self):
        r = b""
        r = self.serialize_unsigned(r, self.version)
        self.sign = keytool.ecdsa_sign(bytes.fromhex(self.account.private_key()), r)
        r = serialize.write_var_bytes(r, self.sign)
        r += self.cr_sponsor_did
        self.cr_sign = keytool.ecdsa_sign(bytes.fromhex(self.cr_account.private_key()), r)
        return r

    def gen_hash(self):
        r = b""
        r = self.serialize(r, 0)
        return keytool.sha256_hash(r, 2)

    def __repr__(self):
        return "CRCProposal {" + "\n\t" \
               + "proposal_type: {}".format(self.proposal_type) + "\n\t" \
               + "category_data : {}".format(self.category_data) + "\n\t" \
               + "sponsor_public_key : {}".format(self.account.public_key()) + "\n\t" \
               + "draft_hash: {}".format(self.draft_hash.hex()) + "\n\t" \
               + "budgets: {}".format(self.budget) + "\n\t" \
               + "recipient: {}".format(keytool.create_address(self.recipient)) + "\n\t" \
               + "sign: {}".format(self.sign.hex()) + "\n\t" \
               + "cr_sponsor_did: {}".format(keytool.create_address(self.cr_sponsor_did)) + "\n\t" \
               + "cr_sign: {}".format(self.cr_sign.hex()) + "\n\t" \
               + "hash: {}".format(self.hash.hex()) + "\n\t" \
               + "}"

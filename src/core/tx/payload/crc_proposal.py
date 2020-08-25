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
    CHANGE_SPONSOR_OWNER = 0x0401
    CLOSE_PROPOSAL = 0x0402
    DAPP_CONSENSUS = 0x0500
    WRONG = 0x4321

    def __init__(self, private_key: str, cr_private_key: str, proposal_type: int, category_data: str,
                 draft_hash: bytes, budget=None, recipient=None, target_proposal_hash=None, new_recipient=None,
                 secretary_general_private_key=None, new_owner_private_key=None):
        Payload.__init__(self, self.DEFAULT_VERSION)
        self.account = Account(private_key)
        self.cr_account = Account(cr_private_key)
        self.secretary_general_account = None
        self.new_owner_account = None
        self.proposal_type = proposal_type
        self.category_data = category_data
        self.draft_hash = draft_hash
        self.target_proposal_hash = target_proposal_hash
        self.new_owner_public_key = None
        self.budget = budget
        self.recipient = recipient
        self.new_recipient = None
        self.secretary_general_public_key = None
        self.secretary_general_did = None
        self.sign = None
        self.new_owner_signature = None
        self.secretary_general_signature = None
        self._gen_secretary_general_account(secretary_general_private_key)
        self._gen_new_owner_account(new_owner_private_key)
        self.cr_council_member_did = bytes.fromhex(self.cr_account.did())
        self.cr_council_member_sign = None
        self._gen_signature()
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
        if self.proposal_type is self.SECRETARY_GENERAL:
            return self.serialize_secretary_general(r, version)
        elif self.proposal_type is self.CHANGE_SPONSOR_OWNER:
            return self.serialize_change_proposal_owner(r, version)
        elif self.proposal_type is self.CLOSE_PROPOSAL:
            return self.serialize_close_proposal(r, version)
        else:
            return self.serialize_normal_or_elip(r, version)

    def serialize_normal_or_elip(self, r: bytes, version: int):
        r = self.serialize_unsigned_normal_or_elip(r, version)
        r = serialize.write_var_bytes(r, self.sign)
        r += self.cr_council_member_did
        r = serialize.write_var_bytes(r, self.cr_council_member_sign)
        return r

    def serialize_secretary_general(self, r: bytes, version: int):
        r = self.serialize_unsigned_secretary_genera(r, version)
        r = serialize.write_var_bytes(r, self.sign)
        r = serialize.write_var_bytes(r, self.secretary_general_signature)
        r += self.cr_council_member_did
        r = serialize.write_var_bytes(r, self.cr_council_member_sign)
        return r

    def serialize_change_proposal_owner(self, r: bytes, version: int):
        r = self.serialize_unsigned_change_proposal_owner(r, version)
        r = serialize.write_var_bytes(r, self.sign)
        r = serialize.write_var_bytes(r, self.new_owner_signature)
        r += self.cr_council_member_did
        r = serialize.write_var_bytes(r, self.cr_council_member_sign)
        return r

    def serialize_close_proposal(self, r: bytes, version: int):
        r = self.serialize_unsigned_close_proposal(r, version)
        r = serialize.write_var_bytes(r, self.sign)
        r += self.cr_council_member_did
        r = serialize.write_var_bytes(r, self.cr_council_member_sign)
        return r

    def serialize_unsigned_normal_or_elip(self, r: bytes, version=0):
        r += struct.pack("<H", self.proposal_type)
        r = serialize.write_var_bytes(r, bytes(self.category_data.encode()))
        r = serialize.write_var_bytes(r, bytes.fromhex(self.account.public_key()))
        r += self.draft_hash
        r += serialize.write_var_uint(len(self.budget))
        for budget in self.budget:
            r += budget.serialize(version)
        r += self.recipient
        return r

    def serialize_unsigned_secretary_genera(self, r: bytes, version=0):
        r += struct.pack("<H", self.proposal_type)
        r = serialize.write_var_bytes(r, bytes(self.category_data.encode()))
        r = serialize.write_var_bytes(r, bytes.fromhex(self.account.public_key()))
        r += self.draft_hash
        r = serialize.write_var_bytes(r, self.secretary_general_public_key)
        r += self.secretary_general_did
        return r

    def serialize_unsigned_change_proposal_owner(self, r: bytes, version=0):
        r += struct.pack("<H", self.proposal_type)
        r = serialize.write_var_bytes(r, bytes(self.category_data.encode()))
        r = serialize.write_var_bytes(r, bytes.fromhex(self.account.public_key()))
        r += self.draft_hash
        r += self.target_proposal_hash
        r += self.new_recipient
        r = serialize.write_var_bytes(r, self.new_owner_public_key)
        return r

    def serialize_unsigned_close_proposal(self, r: bytes, version=0):
        r += struct.pack("<H", self.proposal_type)
        r = serialize.write_var_bytes(r, bytes(self.category_data.encode()))
        r = serialize.write_var_bytes(r, bytes.fromhex(self.account.public_key()))
        r += self.draft_hash
        r += self.target_proposal_hash
        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def _gen_secretary_general_account(self, private_key):
        if private_key is not None:
            self.secretary_general_account = Account(private_key)
            self.secretary_general_public_key = bytes.fromhex(self.secretary_general_account.public_key())
            self.secretary_general_did = bytes.fromhex(self.secretary_general_account.did())

    def _gen_new_owner_account(self, private_key):
        if private_key is not None:
            self.new_owner_account = Account(private_key)
            self.new_owner_public_key = bytes.fromhex(self.new_owner_account.public_key())
            self.new_recipient = bytes.fromhex(self.new_owner_account.did())

    def get_deposit_address(self):
        return self.account.deposit_address()

    def _gen_signature(self):
        r = b""
        if self.proposal_type is self.SECRETARY_GENERAL:
            r = self.serialize_unsigned_secretary_genera(r, self.version)
            self.sign = keytool.ecdsa_sign(bytes.fromhex(self.account.private_key()), r)
            self.secretary_general_signature = keytool.ecdsa_sign(
                bytes.fromhex(self.secretary_general_account.private_key()), r)
            r = serialize.write_var_bytes(r, self.sign)
            r = serialize.write_var_bytes(r, self.secretary_general_signature)
            r += self.cr_council_member_did
            self.cr_council_member_sign = keytool.ecdsa_sign(bytes.fromhex(self.cr_account.private_key()), r)
            return r
        elif self.proposal_type is self.CHANGE_SPONSOR_OWNER:
            r = self.serialize_unsigned_change_proposal_owner(r, self.version)
            self.sign = keytool.ecdsa_sign(bytes.fromhex(self.account.private_key()), r)
            self.new_owner_signature = keytool.ecdsa_sign(bytes.fromhex(self.new_owner_account.private_key()), r)
            r = serialize.write_var_bytes(r, self.sign)
            r = serialize.write_var_bytes(r, self.new_owner_signature)
            r += self.cr_council_member_did
            self.cr_council_member_sign = keytool.ecdsa_sign(bytes.fromhex(self.cr_account.private_key()), r)
            return r
        elif self.proposal_type is self.CLOSE_PROPOSAL:
            r = self.serialize_unsigned_close_proposal(r, self.version)
            self.sign = keytool.ecdsa_sign(bytes.fromhex(self.account.private_key()), r)
            r = serialize.write_var_bytes(r, self.sign)
            r += self.cr_council_member_did
            self.cr_council_member_sign = keytool.ecdsa_sign(bytes.fromhex(self.cr_account.private_key()), r)
            return r
        else:
            r = self.serialize_unsigned_normal_or_elip(r, self.version)
            self.sign = keytool.ecdsa_sign(bytes.fromhex(self.account.private_key()), r)
            r = serialize.write_var_bytes(r, self.sign)
            r += self.cr_council_member_did
            self.cr_council_member_sign = keytool.ecdsa_sign(bytes.fromhex(self.cr_account.private_key()), r)
            return r

    def gen_hash(self):
        r = b""
        r = self.serialize(r, 0)
        return keytool.sha256_hash(r, 2)

    def __repr__(self):
        if self.proposal_type is self.SECRETARY_GENERAL:
            return "CRCProposalSecretaryGeneral {" + "\n\t" \
                   + "privateKey: {}".format(self.proposal_type) + "\n\t" \
                   + "crCouncilMemberDid: {}".format(self.proposal_type) + "\n\t" \
                   + "proposalType: {}".format(self.proposal_type) + "\n\t" \
                   + "categoryData : {}".format(self.category_data) + "\n\t" \
                   + "sponsorPublicKey : {}".format(self.account.public_key()) + "\n\t" \
                   + "draftHash: {}".format(self.draft_hash.hex()) + "\n\t" \
                   + "secretaryGeneralPublicKey: {}".format(self.secretary_general_public_key.hex()) + "\n\t" \
                   + "secretaryGeneralDid: {}".format(keytool.create_address(self.secretary_general_did)) + "\n\t" \
                   + "sign: {}".format(self.sign.hex()) + "\n\t" \
                   + "secretaryGeneralSignature: {}".format(self.secretary_general_signature.hex()) + "\n\t" \
                   + "crCouncilMemberDid: {}".format(keytool.create_address(self.cr_council_member_did)) + "\n\t" \
                   + "crCouncilMemberSign: {}".format(self.cr_council_member_sign.hex()) + "\n\t" \
                   + "hash: {}".format(self.hash.hex()) + "\n\t" \
                   + "}"
        elif self.proposal_type is self.CHANGE_SPONSOR_OWNER:
            return "CRCProposalChangeSponsor {" + "\n\t" \
                   + "proposalType: {}".format(self.proposal_type) + "\n\t" \
                   + "categoryData : {}".format(self.category_data) + "\n\t" \
                   + "sponsorPublicKey : {}".format(self.account.public_key()) + "\n\t" \
                   + "draftHash: {}".format(self.draft_hash.hex()) + "\n\t" \
                   + "targetProposalHash: {}".format(self.target_proposal_hash.hex()) + "\n\t" \
                   + "newRecipient: {}".format(keytool.create_address(self.new_recipient)) + "\n\t" \
                   + "newOwnerPublicKey: {}".format(self.new_owner_public_key.hex()) + "\n\t" \
                   + "sign: {}".format(self.sign.hex()) + "\n\t" \
                   + "crCouncilMemberDid: {}".format(keytool.create_address(self.cr_council_member_did)) + "\n\t" \
                   + "crCouncilMemberSign: {}".format(self.cr_council_member_sign.hex()) + "\n\t" \
                   + "hash: {}".format(self.hash.hex()) + "\n\t" \
                   + "}"
        elif self.proposal_type is self.CLOSE_PROPOSAL:
            return "CRCProposalCloseProposal {" + "\n\t" \
                   + "proposalType: {}".format(self.proposal_type) + "\n\t" \
                   + "categoryData : {}".format(self.category_data) + "\n\t" \
                   + "sponsorPublicKey : {}".format(self.account.public_key()) + "\n\t" \
                   + "draftHash: {}".format(self.draft_hash.hex()) + "\n\t" \
                   + "targetProposalHash: {}".format(self.target_proposal_hash.hex) + "\n\t" \
                   + "sign: {}".format(self.sign.hex()) + "\n\t" \
                   + "crCouncilMemberDid: {}".format(keytool.create_address(self.cr_council_member_did)) + "\n\t" \
                   + "crCouncilMemberSign: {}".format(self.cr_council_member_sign.hex()) + "\n\t" \
                   + "hash: {}".format(self.hash.hex()) + "\n\t" \
                   + "}"
        else:
            return "CRCProposal {" + "\n\t" \
                   + "proposalType: {}".format(self.proposal_type) + "\n\t" \
                   + "categoryData : {}".format(self.category_data) + "\n\t" \
                   + "sponsorPublicKey : {}".format(self.account.public_key()) + "\n\t" \
                   + "draftHash: {}".format(self.draft_hash.hex()) + "\n\t" \
                   + "budgets: {}".format(self.budget) + "\n\t" \
                   + "recipient: {}".format(keytool.create_address(self.recipient)) + "\n\t" \
                   + "sign: {}".format(self.sign.hex()) + "\n\t" \
                   + "crCouncilMemberDid: {}".format(keytool.create_address(self.cr_council_member_did)) + "\n\t" \
                   + "crCouncilMemberSign: {}".format(self.cr_council_member_sign.hex()) + "\n\t" \
                   + "hash: {}".format(self.hash.hex()) + "\n\t" \
                   + "}"

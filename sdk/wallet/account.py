#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/22 10:25 AM
# author: liteng

from sdk.wallet import keytool


class Account(object):

    def __init__(self, private_key_str=""):

        self._private_key = bytes.fromhex(private_key_str)
        self._public_key = None
        self._redeem_script = None
        self._program_hash = None
        self._address = None
        self._create_account()

    def _create_account(self):
        if len(self._private_key) == 0:
            ecc_pair = keytool.create_ecc_pair("P-256")
            self._private_key = ecc_pair.d.to_bytes()

        ecc_pair = keytool.get_ecc_by_private_key(self._private_key.hex())
        self._public_key = keytool.encode_point(ecc_pair.public_key(), True)
        self._redeem_script = keytool.create_redeem_script(self._public_key)
        self._program_hash = keytool.create_program_hash(self._redeem_script)
        self._address = keytool.create_address(self._program_hash)

    def ecc_pair(self):
        return keytool.get_ecc_by_private_key(self._private_key.hex())

    def ecc_public_key(self):
        return self.ecc_pair().public_key()

    def private_key(self):
        return self._private_key.hex()

    def public_key(self):
        return self._public_key.hex()

    def redeem_script(self):
        return self._redeem_script.hex()

    def program_hash(self):
        return self._program_hash.hex()

    def address(self):
        return self._address

    def deposit_address(self):
        return keytool.create_deposit_address(self._program_hash)

    def sign(self, data: bytes):
        return keytool.ecdsa_sign(self._private_key, data)

    def __repr__(self):
        return "Account: {\n\t" + \
                "private_key:   " + self.private_key() + "\n\t" + \
                "public key :   " + self.public_key() + "\n\t" + \
                "redeem script: " + self.redeem_script() + "\n\t" + \
                "program hash:  " + self.program_hash() + "\n\t" + \
                "address:       " + self.address() + "\n}"



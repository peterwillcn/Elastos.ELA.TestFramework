#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 22:50
# file: keystore.py

import base58
from configs import config
from utils import util
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Hash import RIPEMD160


class KeyStore(object):

    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.sign_script = None
        self.program_hash = None
        self.address = None
        self._create_keystore()

    def _create_keystore(self):

        ecc_key_pair = ECC.generate(curve=config.KEYSTORE_ECC_TYPE)
        self.private_key = ecc_key_pair.d.to_bytes()
        ecc_key_public = ecc_key_pair.public_key()
        self.public_key = util.encode_point(True, ecc_key_public)
        self.sign_script = self._publickey_to_sign_script()
        self.program_hash = self._script_to_program_hash()
        self.address = self._program_hash_to_address().decode()

    def _publickey_to_sign_script(self):
        return bytes([len(self.public_key)]) + self.public_key + bytes([config.TX_STANDARD])

    def _script_to_program_hash(self):
        temp = SHA256.new(self.sign_script)
        md = RIPEMD160.new(data=temp.digest())
        data = md.digest()
        sign_type = self.sign_script[len(self.sign_script) - 1]
        program_hash = None
        if sign_type == config.TX_STANDARD:
            program_hash = bytes([33]) + data
        if sign_type == config.TX_MULTI_SIG:
            program_hash = bytes([18]) + data
        return program_hash

    def _program_hash_to_address(self):

        data = self.program_hash
        double_value = SHA256.new(SHA256.new(data).digest()).digest()
        flag = double_value[0:4]
        data = data + flag
        encoded = base58.b58encode(data)
        return encoded

    def to_string(self):
        string = "private key: " + self.private_key.hex() + "\n" \
                + "public key: " + self.public_key.hex() + "\n" \
                + "sign script: " + self.sign_script.hex() + "\n" \
                + "program hash: " + self.program_hash.hex() + "\n" \
                + "address: " + self.address
        return string
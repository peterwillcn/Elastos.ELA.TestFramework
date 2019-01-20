#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 22:50
# file: wallet.py

import os
import json
import base58
from utils import util
from configs import constant
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
        self._save_to_file()

    def _create_keystore(self):

        ecc_key_pair = ECC.generate(curve=constant.KEYSTORE_ECC_TYPE)
        self.private_key = ecc_key_pair.d.to_bytes()
        ecc_key_public = ecc_key_pair.public_key()
        self.public_key = util.encode_point(True, ecc_key_public)
        self.sign_script = self._publickey_to_sign_script()
        self.program_hash = self._script_to_program_hash()
        self.address = self._program_hash_to_address().decode()

    def _publickey_to_sign_script(self):
        return bytes([len(self.public_key)]) + self.public_key + bytes([constant.TX_STANDARD])

    def _script_to_program_hash(self):
        temp = SHA256.new(self.sign_script)
        md = RIPEMD160.new(data=temp.digest())
        data = md.digest()
        sign_type = self.sign_script[len(self.sign_script) - 1]
        program_hash = None
        if sign_type == constant.TX_STANDARD:
            program_hash = bytes([33]) + data
        if sign_type == constant.TX_MULTI_SIG:
            program_hash = bytes([18]) + data
        return program_hash

    def _program_hash_to_address(self):

        data = self.program_hash
        double_value = SHA256.new(SHA256.new(data).digest()).digest()
        flag = double_value[0:4]
        data = data + flag
        encoded = base58.b58encode(data)
        return encoded

    def to_dict(self):
        data = {
            "private_key": self.private_key.hex(),
            "public_key": self.public_key.hex(),
            "sign_script": self.sign_script.hex(),
            "program_hash": self.program_hash.hex(),
            "address": self.address
        }
        return data

    def _save_to_file(self):
        path = constant.KEYSTORE_FILE_NAME
        if os.path.exists(path):
            with open(path, 'r') as f:
                load_dict = json.load(f)
                length = len(load_dict)
                load_dict['addr #' + str(length)] = self.to_dict()
            with open(path, 'w') as f:
                json.dump(load_dict, f, indent=4)
        else:
            with open(path, 'w') as f:
                json.dump({"addr #0": self.to_dict()}, f, indent=4)
#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 22:50
# file: wallet.py

from src.tools import util
from src.core.wallet import keytool


class KeyStore(object):

    def __init__(self, password: str, ecc_key=None):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.password = password
        self.private_key = None
        self.ecc_public_key = None
        self.public_key = None
        self.sign_script = None
        self.program_hash = None
        self.address = None
        self.create_keystore(ecc_key)
        self.keystore_dat = self.gen_keystore_dat(self.password)

    def create_keystore(self, ecc_key=None):
        if ecc_key is None:
            ecc_key_pair = keytool.create_ecc_pair("P-256")
        else:
            ecc_key_pair = ecc_key
        self.private_key = ecc_key_pair.d.to_bytes()

        self.ecc_public_key = ecc_key_pair.public_key()
        self.public_key = keytool.encode_point(True, self.ecc_public_key)
        self.sign_script = self._publickey_to_sign_script()
        self.program_hash = self._script_to_program_hash()
        self.address = self._program_hash_to_address()

    def _publickey_to_sign_script(self):
        return bytes([len(self.public_key)]) + self.public_key + bytes([0xac])

    def _script_to_program_hash(self):
        # temp = SHA256.new(self.sign_script)
        # md = RIPEMD160.new(data=temp.digest())
        # data = md.digest()
        temp = keytool.sha256_hash(self.sign_script, 1)
        data = keytool.ripemd160_hash(temp, 1)
        sign_type = self.sign_script[len(self.sign_script) - 1]
        program_hash = None
        if sign_type == 0xac:
            program_hash = bytes([33]) + data
        if sign_type == 0xae:
            program_hash = bytes([18]) + data
        return program_hash

    # def _program_hash_to_address(self):
    #     data = self.program_hash
    #     double_value = keytool.sha256_hash(data, 2)
    #     flag = double_value[0:4]
    #     data = data + flag
    #     encoded = base58.b58encode(data)
    #     return encoded

    def _program_hash_to_address(self):
        return keytool.program_hash_to_address(self.program_hash)

    def gen_keystore_dat(self, password: str):
        iv_bytes = keytool.create_urandom(16)
        master_key_bytes = keytool.create_urandom(32)
        password_double_hash = keytool.sha256_hash(str.encode(password), 2)
        password_thrice_hash = keytool.sha256_hash(str.encode(password), 3)

        master_key_encrypted_bytes = keytool.aes_encrypt(master_key_bytes, password_double_hash, iv_bytes)

        private_key_encrypted_bytes = keytool.encrypt_private_key(
            master_key_bytes,
            bytearray(self.private_key),
            self.ecc_public_key,
            iv_bytes
        )

        store = {
            "Version": "1.0.0",
            "PasswordHash": password_thrice_hash.hex(),
            "IV": iv_bytes.hex(),
            "MasterKey": master_key_encrypted_bytes.hex(),
            "Account": [
                {
                    "Address": self.address,
                    "ProgramHash": self.program_hash.hex(),
                    "RedeemScript": self.sign_script.hex(),
                    "PrivateKeyEncrypted": private_key_encrypted_bytes.hex(),
                    "Type": "main-account"
                }
            ]
        }
        return store

    def to_dict(self):
        data = {
            "private_key": self.private_key.hex(),
            "public_key": self.public_key.hex(),
            "sign_script": self.sign_script.hex(),
            "program_hash": self.program_hash.hex(),
            "address": self.address
        }
        return data


if __name__ == '__main__':

    private_key = "eb6a70ec334e4d64b1068e51af7ada8923303cc23e8bb77f49dc02a357400980"

    k = KeyStore("123", keytool.get_ecc_by_private_key(private_key))

    keytool.save_to_dat(k.keystore_dat, "aaa.dat")

    print("keystore: ", k.to_dict())
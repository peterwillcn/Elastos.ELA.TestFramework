#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/21 10:55 AM
# author: liteng

from src.core.wallet import keytool
from src.tools.log import Logger


class Account(object):

    def __init__(self, keystore_dat: dict, password: str):
        self.keystore_dat = keystore_dat
        self.password = password
        self.iv = bytes.fromhex(self.get_iv())
        self.encrypt_master_key = bytes.fromhex(self.get_encrypt_master_key())
        self.encrypt_private_key = bytes.fromhex(self.get_encrypt_private_key())
        self.mater_key = self.get_master_key()
        self.private_key = self.get_private_key()

    def get_iv(self):
        if "IV" not in self.keystore_dat.keys():
            Logger.error("keystore_dat dose not contain key IV")
            return None

        return self.keystore_dat["IV"]

    def get_encrypt_master_key(self):
        if "MasterKey" not in self.keystore_dat.keys():
            Logger.error("keystore_dat dose not contain key MasterKey")
            return None

        return self.keystore_dat["MasterKey"]

    def get_encrypt_private_key(self):
        if "Account" not in self.keystore_dat.keys():
            Logger.error("keystore_dat dose not contain key Account")
            return None

        at = self.keystore_dat["Account"][0]
        if "PrivateKeyEncrypted" not in at.keys():
            Logger.error("Account dose not contain key PrivateKeyEncrypted")
            return None

        return at["PrivateKeyEncrypted"]

    def get_master_key(self):
        password_twice_hash = keytool.sha256_hash(str.encode(self.password), 2)
        encrypt_master_key = self.get_encrypt_master_key()
        if encrypt_master_key is None:
            Logger.error("encrypt master key is None")
            return None

        master_key = keytool.aes_decrypt(bytes.fromhex(encrypt_master_key), password_twice_hash, self.iv)

        return master_key

    def get_private_key(self):
        encrypt_private_key = self.get_encrypt_private_key()
        if encrypt_private_key is None:
            Logger.error("encrypt private key is None")
            return None

        encrypt_private_key_bytes = bytes.fromhex(encrypt_private_key)
        if len(encrypt_private_key_bytes) != 96:
            Logger.error("encrypt private key length is not 96")
            return None

        private_key = keytool.aes_decrypt(encrypt_private_key_bytes, self.mater_key, self.iv)

        return private_key[64: 96]









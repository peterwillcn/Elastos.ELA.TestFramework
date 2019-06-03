#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/22 11:34 AM
# author: liteng

import os
import json

from src.core.wallet import keytool
from src.core.wallet.account import Account

from src.tools.log import Logger
from src.tools import util


class Keystore(object):

    MAIN_ACCOUNT = "main-account"
    SUB_ACCOUNT = "sub-account"

    def __init__(self, arg, password="123"):
        self._password = password
        self._valid = False
        self._password_double_hash = keytool.sha256_hash(str.encode(self._password), 2)
        self._password_thrice_hash = keytool.sha256_hash(str.encode(self._password), 3)
        self._accounts_data_list = list()
        self._sub_accounts_list = list()

        if isinstance(arg, Account):
            self._main_account = arg
            self._iv = keytool.create_urandom(16)
            self._master_key = keytool.create_urandom(32)
            self._master_key_encrypted = keytool.aes_encrypt(self._master_key, self._password_double_hash, self._iv)
            self._accounts_data_list.append(self._create_account_data(self._main_account, self.MAIN_ACCOUNT))

        elif isinstance(arg, str):
            self._store_dict = util.read_config_file(arg)
            if not self._check_password():
                return
            if "IV" not in self._store_dict.keys():
                return
            self._iv = bytes.fromhex(self._get_iv())
            self._master_key_encrypted = bytes.fromhex(self._get_master_key_encrypted())
            self._master_key = self._get_master_key()
            self._accounts_data_list = self._get_accounts_data()
            self._main_account = self._get_account(0)
            self._sub_accounts_list = self._get_sub_accounts()

        self._valid = True

    def _check_password(self):
        ret = keytool.sha256_hash(str.encode(self._password), 3).hex() == self._get_password_hash()
        if not ret:
            Logger.error("Invalid password!")

        return ret

    def _create_account_data(self, account: Account, account_type: str):
        private_key_encrypted = keytool.encrypt_private_key(
            self._master_key,
            bytes.fromhex(account.private_key()),
            account.ecc_public_key(),
            self._iv
        )

        account_data = dict()
        account_data["Address"] = account.address()
        account_data["ProgramHash"] = account.program_hash()
        account_data["RedeemScript"] = account.redeem_script()
        account_data["PrivateKeyEncrypted"] = private_key_encrypted.hex()
        account_data["Type"] = account_type

        return account_data

    def _get_iv(self):
        if "IV" not in self._store_dict.keys():
            Logger.error("keystore_dat dose not contain key IV")
            return None

        return self._store_dict["IV"]

    def _get_password_hash(self):
        if "PasswordHash" not in self._store_dict.keys():
            Logger.error("keystore_dat dose not contain key PasswordHash")
            return None

        return self._store_dict["PasswordHash"]

    def _get_master_key_encrypted(self):
        if "MasterKey" not in self._store_dict.keys():
            Logger.error("keystore_dat dose not contain key MasterKey")
            return None

        return self._store_dict["MasterKey"]

    def _get_master_key(self):
        password_twice_hash = keytool.sha256_hash(str.encode(self._password), 2)
        encrypt_master_key = self._get_master_key_encrypted()
        if encrypt_master_key is None:
            Logger.error("encrypt master key is None")
            return None

        master_key = keytool.aes_decrypt(bytes.fromhex(encrypt_master_key), password_twice_hash, self._iv)

        return master_key

    def _get_accounts_data(self, ):
        if "Account" not in self._store_dict.keys():
            Logger.error("keystore_dat dose not contain key Account")
            return None

        return self._store_dict["Account"]

    def _get_account(self, index):
        encrypt_private_key = self._accounts_data_list[index]["PrivateKeyEncrypted"]
        if encrypt_private_key is None:
            Logger.error("encrypt private key is None")
            return None

        encrypt_private_key_bytes = bytes.fromhex(encrypt_private_key)
        if len(encrypt_private_key_bytes) != 96:
            Logger.error("encrypt private key length is not 96")
            return None

        private_key = keytool.aes_decrypt(encrypt_private_key_bytes, self._master_key, self._iv)[64: 96]
        account = Account(private_key.hex())
        return account

    def _get_sub_accounts(self):
        subs = list()
        for i in range(1, len(self._accounts_data_list)):
            sub = self._get_account(i)
            subs.append(sub)

        return subs

    def iv(self):
        return self._iv.hex()

    def master_key(self):
        return self._master_key.hex()

    def add_sub_account(self, sub_account: Account):
        if not self._valid:
            Logger.error("Invalid keystore!")
            return
        self._sub_accounts_list.append(sub_account)
        sub_account_data = self._create_account_data(sub_account, self.SUB_ACCOUNT)
        self._accounts_data_list.append(sub_account_data)

    def main_account(self):
        if not self._valid:
            Logger.error("Invalid keystore!")
            return None
        return self._main_account

    def sub_accounts(self):
        if not self._valid:
            Logger.error("Invalid keystore!")
            return None
        return self._sub_accounts_list

    def password(self):
        if not self._valid:
            Logger.error("Invalid keystore!")
            return ""
        return self._password

    def export_private_key(self):
        if not self._valid:
            Logger.error("Invalid keystore!")
            return None
        return self.main_account().private_key()

    def key_store_dict(self):
        if not self._valid:
            Logger.error("Invalid keystore!")
            return None
        store_dict = {
            "Version": "1.0.0",
            "PasswordHash": self._password_thrice_hash.hex(),
            "IV": self._iv.hex(),
            "MasterKey": self._master_key_encrypted.hex(),
            "Account": self._accounts_data_list
        }

        return store_dict

    def save_to_file(self, dest_dir_path: str):
        if not self._valid:
            Logger.error("Invalid keystore!")
            return False
        if dest_dir_path is "":
            Logger.debug("Invalid parameter!")
            return False

        if not os.path.exists(dest_dir_path):
            os.makedirs(dest_dir_path)

        file_path = os.path.join(dest_dir_path, "keystore.dat")
        util.write_config_file(self.key_store_dict(), file_path)

        return True

    def __repr__(self):
        if not self._valid:
            Logger.error("Invalid keystore!")
            return ""
        return json.dumps(self.key_store_dict(), indent=4)


if __name__ == '__main__':
    a = Account()

    k = Keystore(a, "123")
    print(k)

    print(a)

    print("main private key: ", k.export_private_key())

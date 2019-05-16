#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:00 PM
# author: liteng

import os

from src.tools import util
from src.tools.log import Logger

from src.core.wallet import keytool
from src.core.wallet.keystore import KeyStore
from src.core.parameters.params import Parameter


class KeyStoreManager(object):

    def __init__(self, params: Parameter):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.params = params
        self.password = params.ela_params.password
        self.keystore_saved_dir = ""
        self.special_private_key = "7f24c750a43ff800e80edbe199a09847242b2a820f9cec29c32f540b85245afb"
        self.owner_key_stores = list()
        self.node_key_stores = list()
        self.special_key_stores = list()
        self.arbiter_stores = list()
        self.sub_key_stores = list()
        self.sub_key_stores2 = list()
        self.crc_public_keys = list()

        self.init_keystore_files()
        self.foundation_key_store = self.special_key_stores[0]
        self.tap_key_store = self.special_key_stores[4]

    def init_keystore_files(self):
        Logger.info("{} begin to generate the key stores".format(self.tag))

        self.keystore_saved_dir = os.path.join(self.params.root_path, "datas/keystores")
        if not os.path.exists(self.keystore_saved_dir):
            os.mkdir(self.keystore_saved_dir)
        else:
            os.system("rm -fr " + self.keystore_saved_dir + "/*")

        # generate special keystore such as foundation, miner and tap(水龙头地址)
        self.create_special_stores("main_foundation", True)
        self.create_special_stores("main_miner", False)
        self.create_special_stores("side_foundation", False)
        self.create_special_stores("side_miner", False)
        self.create_special_stores("main_tap", False)
        self.create_special_stores("side_tap", False)
        Logger.debug("{} generate special keystore on success!".format(self.tag))

        # generate general keystore such as owner and node
        self.create_general_stores("owner", self.owner_key_stores)
        self.create_general_stores("node", self.node_key_stores)
        self.gen_crc_public_keys()
        # generate original arbiters key stores
        if self.params.arbiter_params.enable:
            self.create_arbiter_stores()

        Logger.info("{} generate the key stores on success!".format(self.tag))

    def add_sub_account(self, main_dat: dict, sub_keystore: KeyStore):
        iv = main_dat['IV']
        encrypted_master_key = main_dat['MasterKey']

        password_double_hash = keytool.sha256_hash(str.encode(self.password), 2)
        master_key = keytool.aes_decrypt(bytes.fromhex(encrypted_master_key), password_double_hash, bytes.fromhex(iv))
        private_key_encrypted_bytes = keytool.encrypt_private_key(
            master_key,
            bytearray(sub_keystore.private_key),
            sub_keystore.ecc_public_key,
            bytes.fromhex(iv)
        )

        main_dat["Account"].append(
            {
                "Address": sub_keystore.address,
                "ProgramHash": sub_keystore.program_hash.hex(),
                "RedeemScript": sub_keystore.sign_script.hex(),
                "PrivateKeyEncrypted": private_key_encrypted_bytes.hex(),
                "Type": "sub-account"
            }
        )
        return main_dat

    def create_special_stores(self, category: str, first_time: bool):
        special_dat_dir = os.path.join(self.keystore_saved_dir, "special")
        if os.path.exists(special_dat_dir) and first_time:
            print("exists {}".format(special_dat_dir))
            # os.system("rm " + special_dat_dir + "/*.dat")
        elif not os.path.exists(special_dat_dir):
            os.makedirs(special_dat_dir)
        k = KeyStore(self.password)
        self.special_key_stores.append(k)
        keytool.save_to_json(k, category + ":", os.path.join(self.keystore_saved_dir, "special.json"), first_time)
        keytool.save_to_dat(k.keystore_dat, os.path.join(special_dat_dir, category + ".dat"))

    def create_general_stores(self, category: str, category_list: list):
        category_dat_dir = os.path.join(self.keystore_saved_dir, category + "_keystores")
        if os.path.exists(category_dat_dir):
            print("exists {}".format(category_dat_dir))
            # os.system("rm " + category_dat_dir + "/*.dat")
        else:
            os.makedirs(category_dat_dir)

        for i in range(self.params.ela_params.number + 1):
            if i == 0:
                first_time = True
            else:
                first_time = False

            if i == 5 and category == "owner":
                if self.special_private_key is None or self.special_private_key == "":
                    k = KeyStore(self.password)
                else:
                    k = KeyStore(self.password, ecc_key=keytool.get_ecc_by_private_key(self.special_private_key))
            else:
                k = KeyStore(self.password)
            category_list.append(k)
            keytool.save_to_json(
                k,
                category + " #" + str(i) + ":",
                os.path.join(self.keystore_saved_dir, category + "_keystore.json"),
                first_time
            )
            keytool.save_to_dat(
                k.keystore_dat,
                os.path.join(category_dat_dir, category + "_" + str(i) + ".dat")
            )

        Logger.debug("{} generate {} keystores on success!".format(self.tag, category))

    def create_arbiter_stores(self):
        arbiter_dat_dir = os.path.join(self.keystore_saved_dir, "arbiter_keystores")
        if os.path.exists(arbiter_dat_dir):
            # os.system("rm " + arbiter_dat_dir + "/*.dat")
            print("exists {} ".format(arbiter_dat_dir))
        else:
            os.makedirs(arbiter_dat_dir)

        # generate original arbiter keystore
        for i in range(5):
            if i == 0:
                first_time = True
            else:
                first_time = False

            k = KeyStore(self.password)
            self.arbiter_stores.append(k)

            sub_k = KeyStore(self.password)
            self.sub_key_stores.append(sub_k)

            sub_k2 = KeyStore(self.password)
            self.sub_key_stores2.append(sub_k2)

            keytool.save_to_json(
                k,
                "origin arbiter #" + str(i) + ": ",
                os.path.join(self.keystore_saved_dir, "arbiter_keystore.json"),
                first_time
            )
            keytool.save_to_json(
                sub_k,
                "sub account #" + str(i) + ":",
                os.path.join(self.keystore_saved_dir, "sub_keystore.json"),
                first_time
            )

            keytool.save_to_json(
                sub_k2,
                "sub2 account #" + str(i) + ":",
                os.path.join(self.keystore_saved_dir, "sub_keystore2.json"),
                first_time
            )

            keytool.save_to_dat(
                self.add_sub_account(self.add_sub_account(k.keystore_dat, sub_k), sub_k2),
                os.path.join(arbiter_dat_dir, "origin_arbiter_" + str(i) + ".dat")
            )

        # generate crc arbiter keystore
        for i in range(self.params.ela_params.crc_number + 1):
            if i == 0:
                continue
            k = self.node_key_stores[i]
            self.arbiter_stores.append(k)
            sub_k = KeyStore(self.password)
            self.sub_key_stores.append(sub_k)

            sub_k2 = KeyStore(self.password)
            self.sub_key_stores2.append(sub_k2)

            keytool.save_to_json(
                k,
                "crc arbiter #" + str(i) + ": ",
                os.path.join(self.keystore_saved_dir, "arbiter_keystore.json"),
                False
            )

            keytool.save_to_json(
                sub_k,
                "sub account #" + str(i + 5 - 1) + ":",
                os.path.join(self.keystore_saved_dir, "sub_keystore.json"),
                False
            )

            keytool.save_to_json(
                sub_k2,
                "sub2 account #" + str(i + 5 - 1) + ":",
                os.path.join(self.keystore_saved_dir, "sub_keystore2.json"),
                False
            )

            keytool.save_to_dat(
                self.add_sub_account(self.add_sub_account(k.keystore_dat, sub_k), sub_k2),
                os.path.join(arbiter_dat_dir, "crc_arbiter_" + str(i) + ".dat")
            )

        Logger.debug("{} generate arbiter keystores on success! ".format(self.tag))

    def gen_crc_public_keys(self):
        for i in range(1, self.params.ela_params.crc_number + 1):
            self.crc_public_keys.append(self.node_key_stores[i].public_key.hex())






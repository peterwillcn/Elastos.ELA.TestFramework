#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:00 PM
# author: liteng

import os

from src.middle.tools import util
from src.middle.tools.log import Logger

from src.bottom.wallet import keytool
from src.bottom.wallet.keystore import KeyStore
from src.bottom.parameters.params import Parameter


class KeyStoreManager(object):

    def __init__(self, params: Parameter):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.root_path = params.root_path
        self.num = params.ela_params.number
        self.password = params.ela_params.password
        self.keystore_saved_dir = ""
        self.owner_key_stores = list()
        self.node_key_stores = list()
        self.special_key_stores = list()
        self.original_arbiter_stores = list()
        self._save_keystore_files()

    def _save_keystore_files(self):
        Logger.info("{} begin generating the key stores".format(self.tag))

        self.keystore_saved_dir = os.path.join(self.root_path, "datas/keystores")
        if not os.path.exists(self.keystore_saved_dir):
            os.mkdir(self.keystore_saved_dir)

        # generate special keystore such as foundation, miner and tap(水龙头地址)
        self.create_general_stores()
        # generate original arbiters key stores
        self.create_original_stores()
        # generate general keystore such as owner and node
        self.create_special_stores()

    def create_a_keystore(self, prefix: str, dat_dir: str, json_name: str, dat_file_name: str, first_time: bool):
        dest_dir_path = os.path.join(self.keystore_saved_dir, dat_dir)
        if not os.path.exists(dest_dir_path):
            os.makedirs(dest_dir_path)
        elif first_time:
            os.system("rm " + dest_dir_path + "/*.dat")
        dest_file_path = os.path.join(self.keystore_saved_dir, json_name)

        k = KeyStore(self.password)

        keytool.save_to_json(k, prefix, dest_file_path, first_time)
        keytool.save_to_dat(k, os.path.join(dest_dir_path, dat_file_name))

        return k

    def create_special_stores(self):
        self.special_key_stores.append(
            self.create_a_keystore("Foundation: ", "special", "special.json", "foundation.dat", True)
        )
        self.special_key_stores.append(
            self.create_a_keystore("Miner:", "special", "special.json", "miner.dat", False)
        )
        self.special_key_stores.append(
            self.create_a_keystore("Tap:", "special", "special.json", "tap.dat", False)
        )
        Logger.debug("{} create {} special keystores on success!".format(
            self.tag, len(self.special_key_stores)))

    def create_original_stores(self):
        for i in range(5):
            if i == 0:
                first_time = True
            else:
                first_time = False
            self.original_arbiter_stores.append(
                self.create_a_keystore(
                    "Original Arbiter #" + str(i) + ":",
                    "original_arbiter_keystores",
                    "original_arbiter.json",
                    "original_arbiter_" + str(i) + ".dat",
                    first_time
                )
            )
        Logger.debug("{} create {} original keystores on success!".format(
            self.tag, len(self.original_arbiter_stores)))

    def create_general_stores(self):
        for i in range(self.num):
            if i == 0:
                first_time = True
            else:
                first_time = False

            self.owner_key_stores.append(
                self.create_a_keystore(
                    "Owner #" + str(i),
                    "owner_keystores",
                    "owner_keystore.json",
                    "owner_" + str(i) + ".dat",
                    first_time
                )
            )

            self.node_key_stores.append(
                self.create_a_keystore(
                    "Node #" + str(i),
                    "node_keystores",
                    "node_keystore.json",
                    "node_" + str(i) + ".dat",
                    first_time
                )
            )
        Logger.debug("{} generate {} keystore on success!".format(
            self.tag, len(self.node_key_stores)))



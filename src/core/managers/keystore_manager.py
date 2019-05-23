#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:00 PM
# author: liteng

import os
import time

from src.tools import util
from src.tools.log import Logger

from src.core.parameters.params import Parameter

from sdk.wallet.account import Account
from sdk.wallet.keystore import Keystore
from sdk.common import util


class KeyStoreManager(object):

    INDEX_FOUNDATION = 0
    INDEX_MAIN_MINER = 1
    INDEX_SIDE_MINER = 2
    INDEX_TAP = 3
    INDEX_CROSS_DID = 4
    INDEX_CROSS_TOKEN = 5
    INDEX_CROSS_NEO = 6
    INDEX_CROSS_ETH = 7
    INDEX_BACK_UP = 8

    def __init__(self, params: Parameter):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.params = params
        self.password = params.ela_params.password
        self.key_message_saved_dir = ""
        self.stables_path = ""

        self.special_accounts = list()
        self.owner_accounts = list()
        self.node_accounts = list()
        self.arbiter_accounts = list()
        self.origin_arbiter_accounts = list()
        self.sub1_accounts = list()
        self.sub2_accounts = list()
        self.sub3_accounts = list()
        self.category_dict = dict()

        self._init_category_dict()
        self._init_key_stores()

        self.foundation_account = self.special_accounts[self.INDEX_FOUNDATION]
        self.main_miner_account = self.special_accounts[self.INDEX_MAIN_MINER]
        self.side_miner_account = self.special_accounts[self.INDEX_SIDE_MINER]
        self.tap_account = self.special_accounts[self.INDEX_TAP]
        self.cross_did_account = self.special_accounts[self.INDEX_CROSS_DID]
        self.cross_token_account = self.special_accounts[self.INDEX_CROSS_TOKEN]
        self.cross_neo_account = self.special_accounts[self.INDEX_CROSS_NEO]
        self.cross_eth_account = self.special_accounts[self.INDEX_CROSS_ETH]

        # self._create_keystore_files()

    def _init_key_stores(self):
        self.stables_path = os.path.join(self.params.root_path, "datas/stables")
        if not os.path.exists(self.stables_path):
            Logger.error("{} target keystore path is not found, exit...".format(self.tag))
            time.sleep(1)
            exit(-1)

        self._read_key_stores("special", 13)
        self._read_key_stores("node", 37)
        self._read_key_stores("owner", 37)
        self._read_key_stores("arbiter", 13)
        self._read_key_stores("origin", 5)
        self._read_key_stores("sub1", 13)
        self._read_key_stores("sub2", 13)
        self._read_key_stores("sub3", 13)

    def _init_category_dict(self):
        self.category_dict["special"] = self.special_accounts
        self.category_dict["node"] = self.node_accounts
        self.category_dict["owner"] = self.owner_accounts
        self.category_dict["arbiter"] = self.arbiter_accounts
        self.category_dict["origin"] = self.origin_arbiter_accounts
        self.category_dict["sub1"] = self.sub1_accounts
        self.category_dict["sub2"] = self.sub2_accounts
        self.category_dict["sub3"] = self.sub3_accounts

    def _read_key_stores(self, category: str, num: int):
        dest_path = os.path.join(self.stables_path, category + ".json")
        if not os.path.exists(dest_path):
            Logger.error("{} read key stores failed, dest path {} is not found, exit...".format(self.tag, dest_path))
            time.sleep(1)
            exit(-1)

        content_dict = util.read_config_file(dest_path)

        for i in range(num):
            private_key_str = content_dict[category + "_" + str(i)]["private_key"]
            Logger.debug("{} {}_{} private key: {}".format(self.tag, category, i, private_key_str))
            a = Account(private_key_str)
            self.category_dict[category].append(a)

    def _create_keystore_files(self):
        Logger.info("{} begin to generate the key stores".format(self.tag))

        self.key_message_saved_dir = os.path.join(self.params.root_path, "datas/hello")
        if not os.path.exists(self.key_message_saved_dir):
            os.mkdir(self.key_message_saved_dir)
        else:
            os.system("rm -fr " + self.key_message_saved_dir + "/*")

        self._create_keystore("special", 10)
        self._create_keystore("owner", 10)
        self._create_keystore("node", 10)
        self._create_keystore("arbiter", 13)
        self._create_keystore("origin", 5)

        Logger.info("{} generate the key stores on success!".format(self.tag))

    def _create_keystore(self, category: str, num: int):
        keystore_saved_dir = os.path.join(self.key_message_saved_dir, category)
        if not os.path.exists(keystore_saved_dir):
            os.makedirs(keystore_saved_dir)

        for i in range(num):
            if i == 0:
                first_time = True
            else:
                first_time = False

            a = Account()
            k = Keystore(a, self.password)
            self.category_dict[category].append(a)

            if category == "arbiter":
                sub1 = Account()
                k.add_sub_account(sub1)
                self.sub1_accounts.append(sub1)
                util.save_to_json(
                    sub1,
                    "sub1_" + str(i),
                    os.path.join(self.key_message_saved_dir, "sub1.json"),
                    first_time
                )

                sub2 = Account()
                k.add_sub_account(sub2)
                self.sub2_accounts.append(sub2)
                util.save_to_json(
                    sub2,
                    "sub2_" + str(i),
                    os.path.join(self.key_message_saved_dir, "sub2.json"),
                    first_time
                )

                sub3 = Account()
                k.add_sub_account(sub3)
                self.sub3_accounts.append(sub3)
                util.save_to_json(
                    sub3,
                    "sub3_" + str(i),
                    os.path.join(self.key_message_saved_dir, "sub3.json"),
                    first_time
                )

            util.save_to_json(
                a,
                category + "_" + str(i),
                os.path.join(self.key_message_saved_dir, category + ".json"),
                first_time
            )
            util.save_to_dat(k.key_store_dict(), os.path.join(keystore_saved_dir, category + str(i) + ".dat"))

        Logger.debug("{} create {} keystores on success!".format(self.tag, category))






#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:00 PM
# author: liteng

import os

from src.tools import util
from src.tools.log import Logger

from src.core.parameters.params import Parameter

from sdk.wallet.account import Account
from sdk.wallet.keystore import Keystore
from sdk.common import util


class KeyStoreManager(object):

    def __init__(self, params: Parameter):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.params = params
        self.password = params.ela_params.password
        self.key_message_saved_dir = ""

        self.special_accounts = list()
        self.owner_accounts = list()
        self.node_accounts = list()
        self.arbiter_accounts = list()
        self.sub1_accounts = list()
        self.sub2_accounts = list()
        self.sub3_accounts = list()

        self._init_key_stores()
        # self._create_keystore_files()

    def _init_key_stores(self):
        pass

    def _create_keystore_files(self):
        Logger.info("{} begin to generate the key stores".format(self.tag))

        self.key_message_saved_dir = os.path.join(self.params.root_path, "datas/keystores")
        if not os.path.exists(self.key_message_saved_dir):
            os.mkdir(self.key_message_saved_dir)
        else:
            os.system("rm -fr " + self.key_message_saved_dir + "/*")

        self._create_keystore("special", 13)
        self._create_keystore("owner", 109)
        self._create_keystore("node", 109)
        self._create_keystore("arbiter", 13)

        Logger.info("{} generate the key stores on success!".format(self.tag))

    def _create_keystore(self, category: str, num: int):
        keystore_saved_dir = os.path.join(self.key_message_saved_dir, category)
        if not os.path.exists(keystore_saved_dir):
            os.makedirs(keystore_saved_dir)

        if category == "special":
            for i in range(num):
                if i == 0:
                    first_time = True
                else:
                    first_time = False
                a = Account()
                k = Keystore(a, self.password)
                self.special_accounts.append(a)

                util.save_to_json(
                    a,
                    category + " #" + str(i),
                    os.path.join(self.key_message_saved_dir, category + ".json"),
                    first_time
                )
                util.save_to_dat(k.key_store_dict(), os.path.join(keystore_saved_dir, category + str(i) + ".dat"))

        elif category == "owner":
            for i in range(num):
                if i == 0:
                    first_time = True
                else:
                    first_time = False
                a = Account()
                k = Keystore(a, self.password)
                self.owner_accounts.append(a)

                util.save_to_json(
                    a,
                    category + " #" + str(i),
                    os.path.join(self.key_message_saved_dir, category + ".json"),
                    first_time
                )
                util.save_to_dat(k.key_store_dict(), os.path.join(keystore_saved_dir, category + str(i) + ".dat"))

        elif category == "node":
            for i in range(num):
                if i == 0:
                    first_time = True
                else:
                    first_time = False
                a = Account()
                k = Keystore(a, self.password)
                self.node_accounts.append(a)

                util.save_to_json(
                    a,
                    category + " #" + str(i),
                    os.path.join(self.key_message_saved_dir, category + ".json"),
                    first_time
                )
                util.save_to_dat(k.key_store_dict(), os.path.join(keystore_saved_dir, category + str(i) + ".dat"))

        elif category == "arbiter":
            for i in range(num):
                if i == 0:
                    first_time = True
                else:
                    first_time = False

                a = self.node_accounts[i]
                k = Keystore(a, self.password)
                self.arbiter_accounts.append(a)

                sub1 = Account()
                k.add_sub_account(sub1)
                self.sub1_accounts.append(sub1)

                sub2 = Account()
                k.add_sub_account(sub2)
                self.sub2_accounts.append(sub2)

                sub3 = Account()
                k.add_sub_account(sub3)
                self.sub3_accounts.append(sub3)

                util.save_to_json(
                    a,
                    category + " #" + str(i),
                    os.path.join(self.key_message_saved_dir, category + ".json"),
                    first_time
                )
                util.save_to_dat(k.key_store_dict(), os.path.join(keystore_saved_dir, category + str(i) + ".dat"))

        Logger.debug("{} create {} keystores on success!".format(self.tag, category))






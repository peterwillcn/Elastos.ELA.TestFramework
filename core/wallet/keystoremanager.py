#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:00 PM
# author: liteng

import os
import json
import time
from logs.log import Logger
from configs import constant
from core.wallet.keystore import KeyStore


class KeyStoreManager(object):

    def __init__(self, count):
        self.tag = '[KeyStoreManager]'
        if count < 10:
            Logger.error('{} count should not be less than 10,' 
                         ' here count is {}'.format(self.tag, count))
            exit(0)
        self.count = count
        self.key_stores = []
        self._get_key_stores()

    def _get_key_stores(self):
        for i in range(self.count):
            k = KeyStore()
            self.key_stores.append(k)
            self._save_to_file(k)

    @staticmethod
    def _save_to_file(k):
        path = constant.KEYSTORE_FILE_PATH
        if os.path.exists(path):
            with open(path, 'r') as f:
                load_dict = json.load(f)
                length = len(load_dict)
                load_dict[constant.KEYSTORE_MANAGER_PREFIX + str(length)] = k.to_dict()
            with open(path, 'w') as f:
                json.dump(load_dict, f, indent=4)
        else:
            with open(path, 'w') as f:
                json.dump({constant.KEYSTORE_MANAGER_PREFIX + '0': k.to_dict()}, f, indent=4)



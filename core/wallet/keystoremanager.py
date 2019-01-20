#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:00 PM
# author: liteng

import os
import json
from configs import constant
from core.wallet.keystore import KeyStore


class KeyStoreManager(object):

    def __init__(self, count):
        self.count = count
        self.keystores = self._get_keystores()

    def _get_keystores(self):
        keystores = []
        for i in range(self.count):
            k = KeyStore()
            self._save_to_file(k)
            keystores.append(k)
        return keystores

    def _save_to_file(self, k):
        path = constant.KEYSTORE_FILE_NAME
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
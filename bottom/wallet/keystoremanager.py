#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:00 PM
# author: liteng

from bottom.wallet import keytool
from bottom.logs.log import Logger
from bottom.wallet.keystore import KeyStore


class KeyStoreManager(object):

    def __init__(self, password: str, count: int):
        self.tag = "[KeyStoreManager]"
        if count < 10:
            Logger.error("{} count should not be less than 10," 
                         " here count is {}".format(self.tag, count))
            exit(0)
        self.count = count
        self.password = password
        self.key_stores = []
        self._save_keystore_files()

    def _save_keystore_files(self):
        for i in range(self.count):
            k = KeyStore(self.password)
            self.key_stores.append(k)
            keytool.save_to_json(k)
            keytool.save_to_dat(k, i)
            print("generate keystore {} on success!".format(i))


if __name__ == "__main__":
    m = KeyStoreManager("123", 10)




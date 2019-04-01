#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:00 PM
# author: liteng

from middle.common.log import Logger

from bottom.wallet import keytool
from bottom.wallet.keystore import KeyStore


class KeyStoreManager(object):

    def __init__(self, num: int, password: str):
        self.tag = "[bottom.wallet.keystore_manager.KeyStoreManager]"
        self.num = num
        self.password = password
        self.key_stores = []
        self._save_keystore_files()

    def _save_keystore_files(self):
        Logger.info("{} begin generating the key stores".format(self.tag))
        for i in range(self.num):
            k = KeyStore(self.password)
            self.key_stores.append(k)
            if i == 0:
                keytool.save_to_json(k, True)
            else:
                keytool.save_to_json(k, False)
            keytool.save_to_dat(k, i)
            Logger.debug("{} generate keystore {} on success!".format(self.tag, i))


if __name__ == "__main__":
    m = KeyStoreManager(10, "123")




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
        self.general_key_stores = list()
        self.special_key_stores = list()
        self._save_keystore_files()

    def _save_keystore_files(self):
        Logger.info("{} begin generating the key stores".format(self.tag))

        # generate special keystore such as foundation, miner and tap(水龙头地址)
        for i in range(3):
            k = KeyStore(self.password)
            self.special_key_stores.append(k)
            if i == 0:
                keytool.save_to_json(k, "foundation: ", "datas/special.json", True)
                keytool.save_to_dat(k, i, "datas/special", "foundation.dat")
            elif i == 1:
                keytool.save_to_json(k, "miner: ", "datas/special.json", False)
                keytool.save_to_dat(k, i, "datas/special", "miner.dat")
            elif i == 2:
                keytool.save_to_json(k, "tap: ", "datas/special.json", False)
                keytool.save_to_dat(k, i, "datas/special", "tap.dat")

        # generate general keystore like crc, producers and others
        for i in range(self.num):
            k = KeyStore(self.password)
            self.general_key_stores.append(k)
            if i == 0:
                keytool.save_to_json(k, "Addr #" + str(i), "datas/general.json", True)
            else:
                keytool.save_to_json(k, "Addr #" + str(i), "datas/general.json", False)
            keytool.save_to_dat(k, i, "datas/general", "keystore_" + str(i) + ".dat")
            Logger.debug("{} generate keystore {} on success!".format(self.tag, i))


if __name__ == "__main__":
    m = KeyStoreManager(10, "123")




#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 18:00
# file: main.py

from core.wallet import keystoremanager

if __name__ == "__main__":

    manager = keystoremanager.KeyStoreManager(10)

    keystores = manager.keystores
    keystore = keystores[5]
    print(keystore.private_key.hex())
    print(keystore.public_key.hex())
    print(keystore.sign_script.hex())
    print(keystore.program_hash.hex())
    print(keystore.address)
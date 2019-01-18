#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 18:00
# file: main.py

import time
from service import jar

import base58

from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Hash import RIPEMD160

from logs.log import Logger
from keystore import keystore

if __name__ == "__main__":

    keystore = keystore.KeyStore()
    print("keystore information: \n", keystore.to_string())
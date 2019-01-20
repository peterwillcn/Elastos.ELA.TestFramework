#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 17:29
# file: config.py

JAR_NAME = 'Elastos.ELA.AutoTest.Java.jar'
JAR_HTTP_SERVICE = ' org.elastos.elaweb.HttpServer'

COLOR_END = '\033[0m'
COLOR_BLUE = '\033[0;34m'
COLOR_GREEN = '\033[1;32m'
COLOR_YELLOW = '\033[1;33m'
COLOR_RED = '\033[0;31m'

KEYSTORE_ECC_TYPE = 'P-256'
KEYSTORE_FILE_NAME = "./datas/keystore.json"

KEYSTORE_MANAGER_PREFIX = 'Addr #'

INFINITY_LEN = 1
FLAG_LEN = 1
X_OR_Y_VALUE_LEN = 32
COMPRESSED_LEN = 33
NON_COMPRESSED_LEN = 65
COMPEVEN_FLAG = 0x02
COMPODD_FLAG = 0x03
NON_COMPRESSED_FLAG = 0x04
P256_PARAMA = -3
EMPTY_BYTE = 0x00

TX_STANDARD = 0xac
TX_MULTI_SIG = 0xae

UINT168_SIZE = 21


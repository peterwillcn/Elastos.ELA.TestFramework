#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 17:29
# file: constant.py

import os
import time

HOME_DIR = os.environ['HOME']

JAR_NAME = 'Elastos.ELA.AutoTest.Java.jar'
JAR_HTTP_SERVICE = ' org.elastos.elaweb.HttpServer'

NODE_TYPE_MAIN = 'main_node'
NODE_TYPE_ARBITER = 'arbiter_node'
NODE_TYPE_DID = 'did_node'
NODE_TYPE_TOKEN = 'token_node'
NODE_TYPE_NEO = 'neo_node'

NODE_BINARY_MAIN = 'ela'
NODE_BINARY_ARBITER = 'arbiter'
NODE_BINARY_DID = 'did'
NODE_BINARY_TOKEN = 'token'
NODE_BINARY_NEO = 'sideNeo'

NODE_CONFIG = 'Configuration'
NODE_PORT = 'NodePort'
NODE_PORT_INFO = 'HttpInfoPort'
NODE_PORT_REST = 'HttpRestPort'
NODE_PORT_WS = 'HttpWsPort'
NODE_PORT_JSON = 'HttpJsonPort'
NODE_PORT_OPEN = 'NodeOpenPort'
NODE_PORT_BASE = 30000
NODE_PORT_DIFF = 1000
NODE_PORT_TYPE = 100

NODE_PATH_MAIN = os.path.join(HOME_DIR, 'dev/src/github.com/elastos/Elastos.ELA/ela')
NODE_PATH_ARBITER = os.path.join(HOME_DIR, 'dev/src/github.com/elastos/Elastos.ELA.Arbiter/arbiter')
NODE_PATH_DID = os.path.join(HOME_DIR, 'dev/src/github.com/elastos/Elastos.ELA.SideChain.ID/did')
NODE_PATH_TOKEN = os.path.join(HOME_DIR, 'dev/src/github.com/elastos/Elastos.ELA.SideChain.Token/token')
NODE_PATH_NEO = os.path.join(HOME_DIR, 'dev/src/github.com/elastos/Elastos.ELA.SideChain.NeoVM/sideNeo')
TEST_PARAENT_PATH = os.path.join(HOME_DIR, 'testing-work/standard-test')
CURRENT_DATE_TIME = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime())


COLOR_END = '\033[0m'
COLOR_BLUE = '\033[0;34m'
COLOR_GREEN = '\033[1;32m'
COLOR_YELLOW = '\033[1;33m'
COLOR_RED = '\033[0;31m'

KEYSTORE_ECC_TYPE = 'P-256'
KEYSTORE_FILE_NAME = "./datas/keystore.json"
KEYSTORE_MANAGER_PREFIX = 'Addr #'

POST_RESPONSE_ERROR = 'error'
POST_RESPONSE_RESULT = 'result'

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

LOCAL_HOST = '127.0.0.1'

METHOD_GET_CONNECTION_COUNT = 'getconnectioncount'
METHOD_DISCRETE_MINING = 'discretemining'



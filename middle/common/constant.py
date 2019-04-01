#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 17:29
# file: constant.py

import os
import time


JAR_NAME = "Elastos.ELA.AutoTest.Java.jar"
JAR_HTTP_SERVICE = " org.elastos.elaweb.HttpServer"

NODE_BINARY_MAIN = "ela"
NODE_BINARY_ARBITER = "arbiter"
NODE_BINARY_DID = "did"
NODE_BINARY_TOKEN = "token"
NODE_BINARY_NEO = "sideNeo"

CONFIG_TITLE = "Configuration"
CONFIG_SEED_LIST = "SeedList"
CONFIG_PORT_NODE = "NodePort"
CONFIG_PORT_INFO = "HttpInfoPort"
CONFIG_PORT_REST = "HttpRestPort"
CONFIG_PORT_WS = "HttpWsPort"
CONFIG_PORT_JSON = "HttpJsonPort"
CONFIG_PORT_OPEN = "NodeOpenPort"
CONFIG_FOUNDATION_ADDRESS = "FoundationAddress"
CONFIG_PAY_TO_MINER = "PayToAddr"
CONFIG_AUTO_MINING = "AutoMining"
CONFIG_INSTANT_BLOCK = "InstantBlock"
CONFIG_POW = "PowConfiguration"
CONFIG_ARBITER_ENABLE = "EnableArbiter"

CONFIG_ARBITER_CONFIGURATION = "ArbiterConfiguration"
CONFIG_PUBLIC_KEY = "PublicKey"
CONFIG_CRC_ARBITERS = "CRCArbiters"
CONFIG_NET_ADDRESS = "NetAddress"
CONFIG_NORMAL_ARBITERS_COUNT = "NormalArbitratorsCount"
CONFIG_CANDIDATES_COUNT = "CandidatesCount"
CONFIG_PRE_CONNECT_OFFSET = "PreConnectOffset"
CONFIG_CHECK_ADDRESS_HEIGHT = "CheckAddressHeight"
CONFIG_VOTE_START_HEIGHT = "VoteStartHeight"
CONFIG_ONLY_DPOS_HEIGHT = "CRCOnlyDPOSHeight"
CONFIG_PUBLIC_DPOS_HEIGHT = "PublicDPOSHeight"

CONFIG_RPC = "RpcConfiguration"
CONFIG_RPC_USER = "User"
CONFIG_RPC_PASS = "Pass"
CONFIG_RPC_WHITE_LIST = "WhiteIPList"

CONFIG_PORT_BASE = 30000
CONFIG_PORT_DIFF = 1000
CONFIG_PORT_TYPE = 100

COLOR_END = "\033[0m"
COLOR_BLUE = "\033[0;34m"
COLOR_GREEN = "\033[1;32m"
COLOR_YELLOW = "\033[1;33m"
COLOR_RED = "\033[0;31m"

PRODUCER_REGISTER = "Register Producer"
PRODUCER_UPDATE = "Update Producer"
PRODUCER_CANCEL = "Cancel producer"
PRODUCER_REDEEM = "Redeem Producer"

POST_RESPONSE_ERROR = "error"
POST_RESPONSE_RESULT = "result"

MAIN_CHAIN_FOUNDATION_ADDRESS = "MainChainFoundationAddress"
MAIN_CHAIN_DEFAULT_PORT = "MainChainDefaultPort"
SIDE_CHAIN_FOUNDATION_ADDRESS = "SideChainFoundationAddress"
MINER_ADDRESS = "MinerAddress"
SPV_SEED_LIST = "SpvSeedList"




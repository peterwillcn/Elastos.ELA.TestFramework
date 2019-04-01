#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 3:01 PM
# author: liteng

from middle.parameters.ela_params import ElaParams
from middle.parameters.arbiter_params import ArbiterParams
from middle.parameters.did_params import DidParams
from middle.parameters.token_params import TokenParams
from middle.parameters.neo_params import NeoParams

from middle.common.log import Logger


class Parameter(object):

    def __init__(self, config):
        self.tag = "[middle.parameters.params.Parameter]"
        self.top_config = config
        self.ela_params = ElaParams(config["ela"])
        self.arbiter_params = ArbiterParams(config["arbiter"])
        self.did_params = DidParams(config["did"])
        self.token_params = TokenParams(config["token"])
        self.neo_params = NeoParams(config["neo"])
        self.check_params()

    def check_params(self):
        if self.ela_params.number < self.ela_params.crc_number:
            Logger.error("{} Ela should have more nodes than crc, please check your config.json file...".format(self.tag))
            exit(-1)

    @staticmethod
    def default_ela_config():
        ela_config = {
            "Configuration": {
                "ActiveNet": "main",
                "Magic": 7630401,
                "Version": 23,
                "SeedList": [
                    "127.0.0.1:30338"
                ],
                "HttpInfoPort": 20333,
                "HttpInfoStart": True,
                "HttpRestPort": 20334,
                "HttpWsPort": 20335,
                "HttpJsonPort": 20336,
                "NodePort": 20338,
                "PrintLevel": 0,
                "MaxLogsSize": 0,
                "MaxPerLogSize": 0,
                "MinCrossChainTxFee": 10000,
                "FoundationAddress": "8VYXVxKKSAxkmRrfmGpQR2Kc66XhG6m3ta",
                "PowConfiguration": {
                    "PayToAddr": "8VYXVxKKSAxkmRrfmGpQR2Kc66XhG6m3ta",
                    "AutoMining": True,
                    "MinerInfo": "ELA",
                    "MinTxFee": 100,
                    "InstantBlock": False
                },
                "RpcConfiguration": {
                    "User": "ElaUser",
                    "Pass": "Ela123",
                    "WhiteIPList": [
                        "127.0.0.1"
                    ]
                },
                "EnableArbiter": False,
                "ArbiterConfiguration": {
                    "PublicKey": "030c756d9ac85337b3c9a4d94a70e2d3f99c6cbb6f78becbfc08baa3df830e5fb4",
                    "Magic": 7630403,
                    "NodePort": 30338,
                    "ProtocolVersion": 0,
                    "Services": 0,
                    "PrintLevel": 1,
                    "SignTolerance": 5,
                    "MaxLogsSize": 0,
                    "MaxPerLogSize": 0,
                    "OriginArbiters": [
                        "02f3876d0973210d5af7eb44cc11029eb63a102e424f0dc235c60adb80265e426e",
                        "03c96f2469b43dd8d0e6fa3041a6cee727e0a3a6658a9c28d91e547d11ba8014a1",
                        "036d25d54fb7a40bc7c3e836a26c9e30d5294bc46f6918ad61d0937960f13307bc",
                        "0248ddc9ac60f1e5b9e9a26719a8a20e1447e6f2bbb0d31597646f1feb9704f291",
                        "02e34e47a06955ef1ec0d325c9edada34a0df6e519530344cc85f5942d061223b3"
                    ],
                    "CRCArbiters": [
                        {
                            "PublicKey": "02eae9164bd143eb988fcd4b7a3c9c04a44eb9a009f73e7615e80a5e8ce1e748b8",
                            "NetAddress": "127.0.0.1:10078"
                        },
                        {
                            "PublicKey": "0294d85959f746b8e6e579458b41eea05afeae50f5a37a037de601673cb24133d9",
                            "NetAddress": "127.0.0.1:10178"
                        },
                        {
                            "PublicKey": "03b0a3a16edfba8d9c1fed9094431c9f24c78b8ceb04b4b6eeb7706f1686b83499",
                            "NetAddress": "127.0.0.1:10278"
                        },
                        {
                            "PublicKey": "0222461ae6c9671cad288f10469f9fd759912f257c64524367dc12c40c2bb4046d",
                            "NetAddress": "127.0.0.1:10378"
                        }
                    ],
                    "NormalArbitratorsCount": 24,
                    "CandidatesCount": 72,
                    "EmergencyInactivePenalty": 50000000000,
                    "MaxInactiveRounds": 1440,
                    "InactivePenalty": 10000000000,
                    "InactiveEliminateCount": 12,
                    "EnableEventRecord": False,
                    "PreConnectOffset": 360
                },
                "CheckAddressHeight": 88812,
                "VoteStartHeight": 88812,
                "CRCOnlyDPOSHeight": 1008812,
                "PublicDPOSHeight": 1108812
            }
        }
        return ela_config

    @staticmethod
    def default_arbiter_config():
        arbiter_config = {
            "Configuration": {
                "Magic": 7530402,
                "Version": 0,
                "SeedList": [
                    "127.0.0.1:10025",
                    "127.0.0.1:10125",
                    "127.0.0.1:10225",
                    "127.0.0.1:10325"
                ],
                "PrintLevel": 1,
                "SpvPrintLevel": 4,
                "HttpInfoPort": 10021,
                "HttpInfoStart": True,
                "HttpRestPort": 10022,
                "HttpWsPort": 10023,
                "NodePort": 10025,
                "HttpJsonPort": 10024,
                "NodeOpenPort": 10056,
                "OpenService": False,
                "MainNode": {
                    "Rpc": {
                        "IpAddress": "127.0.0.1",
                        "HttpJsonPort": 10014
                    },
                    "SpvSeedList": ["127.0.0.1:10016"],
                    "Magic": 7630401,
                    "MinOutbound": 1,
                    "MaxConnections": 3,
                    "FoundationAddress": "8VYXVxKKSAxkmRrfmGpQR2Kc66XhG6m3ta",
                    "DefaultPort": 10015
                },
                "SideNodeList": [
                    {"Rpc": {
                        "IpAddress": "127.0.0.1",
                        "HttpJsonPort": 10034
                    },
                        "ExchangeRate": 1.0,
                        "GenesisBlock": "56be936978c261b2e649d58dbfaf3f23d4a868274f5522cd2adb4308a955c4a3",
                        "KeystoreFile": "keystore1.dat",
                        "PayToAddr": "ERtJFJaEfmABKDy3Afbrpwb6nDrRUGkZ6k"
                    }
                ],
                "MinThreshold": 10000000,
                "DepositAmount": 10000000,
                "SyncInterval": 1000,
                "SideChainMonitorScanInterval": 1000,
                "ClearTransactionInterval": 60000,
                "MinReceivedUsedUtxoMsgNumber": 1,
                "MinOutbound": 3,
                "MaxConnections": 8,
                "SideAuxPowFee": 50000
            }
        }
        return arbiter_config

    @staticmethod
    def default_did_config():
        did_config = {
            "Configuration": {
                "Magic": 7630403,
                "SpvMagic": 7630401,
                "Version": 23,
                "SeedList": [
                    "127.0.0.1:10035",
                    "127.0.0.1:10135",
                    "127.0.0.1:10235",
                    "127.0.0.1:10335"
                ],
                "SpvSeedList": ["127.0.0.1:10015"],
                "MainChainFoundationAddress": "EM8DhdWEFmuLff9fH7fZssK7h5ayUzKcV7",
                "FoundationAddress": "8VYXVxKKSAxkmRrfmGpQR2Kc66XhG6m3ta",
                "SpvMinOutbound": 3,
                "SpvMaxConnections": 10,
                "SpvPrintLevel": 1,
                "ExchangeRate": 1.0,
                "MinCrossChainTxFee": 10000,
                "HttpInfoPort": 10031,
                "HttpInfoStart": True,
                "HttpRestPort": 10032,
                "HttpWsPort": 10033,
                "WsHeartbeatInterval": 60,
                "HttpJsonPort": 10034,
                "NoticeServerUrl": "",
                "OauthServerUrl": "",
                "NodePort": 10035,
                "NodeOpenPort": 10036,
                "OpenService": True,
                "PrintLevel": 1,
                "MaxLogsSize": 1000,
                "MaxPerLogSize": 0,
                "IsTLS": False,
                "CertPath": "./sampleDestroyAddr-cert.pem",
                "KeyPath": "./sample-cert-key.pem",
                "CAPath": "./sample-ca.pem",
                "MultiCoreNum": 4,
                "MaxTransactionInBlock": 10000,
                "MaxBlockSize": 8000000,
                "ConsensusType": "pow",
                "PowConfiguration": {
                    "PayToAddr": "EgB9HTpRxbboSTSLcT2SLcQPXqiJyEZfM7",
                    "AutoMining": False,
                    "MinerInfo": "ELA",
                    "MinTxFee": 100,
                    "InstantBlock": True
                }
            }
        }
        return did_config

    @staticmethod
    def default_token_config():
        token_config = {
            "Configuration": {
                "Magic": 7630404,
                "SpvMagic": 7630401,
                "Version": 23,
                "SeedList": [
                    "127.0.0.1:10045",
                    "127.0.0.1:10145",
                    "127.0.0.1:10245",
                    "127.0.0.1:10345"
                ],
                "SpvSeedList": [
                    "127.0.0.1:10015"
                ],
                "SpvMinOutbound": 3,
                "SpvMaxConnections": 10,
                "ExchangeRate": 1.0,
                "MinCrossChainTxFee": 10000,
                "HttpInfoPort": 10041,
                "HttpInfoStart": True,
                "HttpRestPort": 10042,
                "HttpWsPort": 10043,
                "WsHeartbeatInterval": 60,
                "HttpJsonPort": 10044,
                "NoticeServerUrl": "",
                "OauthServerUrl": "",
                "NodePort": 10045,
                "NodeOpenPort": 10046,
                "OpenService": True,
                "PrintLevel": 1,
                "MaxLogsSize": 0,
                "MaxPerLogSize": 0,
                "IsTLS": False,
                "CertPath": "./sample-cert.pem",
                "KeyPath": "./sample-cert-key.pem",
                "CAPath": "./sample-ca.pem",
                "MultiCoreNum": 4,
                "MaxTransactionInBlock": 10000,
                "MaxBlockSize": 8000000,
                "ConsensusType": "pow",
                "PrintSyncState": True,
                "MainChainDefaultPort": 10015,
                "MainChainFoundationAddress": "8ZNizBf4KhhPjeJRGpox6rPcHE5Np6tFx3",
                "FoundationAddress": "8NRxtbMKScEWzW8gmPDGUZ8LSzm688nkZZ",
                "PowConfiguration": {
                    "PayToAddr": "EPCQFq9buN6RGHdVDxZn7sEZxAnV6dQpcV",
                    "AutoMining": False,
                    "MinerInfo": "ELA",
                    "MinTxFee": 100,
                    "InstantBlock": True
                }
            }
        }
        return token_config

    @staticmethod
    def default_neo_config():
        neo_config = {
            "Configuration": {
                "Magic": 7630405,
                "SpvMagic": 7630401,
                "Version": 1,
                "SeedList": [
                    "127.0.0.1:10055",
                    "127.0.0.1:10155",
                    "127.0.0.1:10255",
                    "127.0.0.1:10355"
                ],
                "SpvSeedList": [
                ],
                "SpvMinOutbound": 3,
                "SpvMaxConnections": 10,
                "ExchangeRate": 1.0,
                "MinCrossChainTxFee": 10000,
                "HttpInfoPort": 10051,
                "HttpInfoStart": True,
                "HttpRestPort": 10052,
                "HttpWsPort": 10053,
                "WsHeartbeatInterval": 60,
                "HttpJsonPort": 10054,
                "NoticeServerUrl": "",
                "OauthServerUrl": "",
                "NodePort": 10055,
                "NodeOpenPort": 10056,
                "OpenService": True,
                "PrintLevel": 1,
                "MaxLogsSize": 0,
                "MaxPerLogSize": 0,
                "IsTLS": False,
                "CertPath": "./sample-cert.pem",
                "KeyPath": "./sample-cert-key.pem",
                "CAPath": "./sample-ca.pem",
                "MultiCoreNum": 4,
                "MaxTransactionInBlock": 10000,
                "MaxBlockSize": 8000000,
                "ConsensusType": "pow",
                "PrintSyncState": True,
                "DisableTxFilters": False,
                "MainChainDefaultPort": 10015,
                "MainChainFoundationAddress": "EM8DhdWEFmuLff9fH7fZssK7h5ayUzKcV7",
                "FoundationAddress": "EPwPux7M4YQZyhJbGsZzCUSdkEby3s8uYJ",
                "PowConfiguration": {
                    "PayToAddr": "EbnrcE57wWRrUA5NuUNg4uCksFk39hhoxR",
                    "AutoMining": False,
                    "MinerInfo": "ELA",
                    "MinTxFee": 100,
                    "InstantBlock": True
                }
            }
        }
        return neo_config


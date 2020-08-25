#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 3:01 PM
# author: liteng

from src.tools import util
from src.tools.log import Logger

from src.core.parameters.ela_params import ElaParams
from src.core.parameters.arbiter_params import ArbiterParams
from src.core.parameters.did_params import DidParams
from src.core.parameters.token_params import TokenParams
from src.core.parameters.neo_params import NeoParams


class Parameter(object):

    def __init__(self, config, root_path):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.top_config = config
        self.root_path = root_path
        self.ela_params = ElaParams(config["ela"])
        self.arbiter_params = ArbiterParams(config["arbiter"], self.ela_params)
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
                "ActiveNet": "regnet",
                "Magic": 2018201,
                "DisableDNS": True,
                "PermanentPeers": [
                    "127.0.0.1:10018",
                    "127.0.0.1:10118",
                    "127.0.0.1:10218",
                    "127.0.0.1:10318",
                    "127.0.0.1:10418",
                    "127.0.0.1:10518",
                    "127.0.0.1:10618",
                    "127.0.0.1:10718",
                    "127.0.0.1:10818",
                    "127.0.0.1:10918"
                ],
                "HttpInfoStart": True,
                "HttpInfoPort": 10113,
                "HttpRestStart": True,
                "HttpRestPort": 10114,
                "HttpWsStart": True,
                "HttpWsPort": 10115,
                "EnableRPC": True,
                "HttpJsonPort": 10116,
                "NodePort": 10118,
                "PrintLevel": 0,
                "MaxLogsSize": 0,
                "MaxPerLogSize": 0,
                "MinCrossChainTxFee": 10000,
                "PowConfiguration": {
                    "PayToAddr": "ELFguDWvxPgcUxWKueTSGpc1eeGEnqLCK1",
                    "AutoMining": False,
                    "MinerInfo": "ELA",
                    "MinTxFee": 100,
                    "InstantBlock": True
                },
                "RpcConfiguration": {
                    "User": "",
                    "Pass": "",
                    "WhiteIPList": [
                        "0.0.0.0"
                    ]
                },
                "DPoSConfiguration": {
                    "EnableArbiter": True,
                    "Magic": 2019000,
                    "IPAddress": "127.0.0.1",
                    "DPoSPort": 10119,
                    "PrintLevel": 0,
                    "SignTolerance": 5,
                    "MaxLogsSize": 0,
                    "MaxPerLogSize": 0,
                    "OriginArbiters": [
                        "038eba1db314e7569aafc62a3c0fd1de9fe6359f88962521768a37786fce62dd37",
                        "02fb5528297b3c43e015d7e20a62b2fc70592cb0b08dfdec7ff95bcd11ff5a5fe6",
                        "03a9d3bbed3db04a4a6c167514b6a4e187b3eaeb3b8d4edd9a618d27b9fe4a0179",
                        "03022428a02e52ef0dd6adc1c7d95ea9cd93854057e9dd6a48486dc536ece71603",
                        "0251fc966a08f0e097711f54fa22ef69c90510ea8e8cf4431e8167c221cf3c7b86"
                    ],
                    "CRCArbiters": [
                        "0342eeb0d664e2507d732382c66d0eedbd0a0f989179fd33d71679aa607d5d3b57",
                        "02cf7e80d1a1a76ab6259e0abdf2848c618655393f1fa3328901f80949ebed1476",
                        "02514cab9af25ee95e102b5c3a7c862b16f24b2de88d0110176e66ea379dfbc7a9",
                        "0322766f133141d2c9d82fb7e331ea6ec7c52e14de2c76bea0f59e479a1408fee3"
                    ],
                    "NormalArbitratorsCount": 8,
                    "CandidatesCount": 24,
                    "EmergencyInactivePenalty": 0,
                    "MaxInactiveRounds": 20,
                    "InactivePenalty": 0,
                    "PreConnectOffset": 5,
                    "PublicKey": "0342eeb0d664e2507d732382c66d0eedbd0a0f989179fd33d71679aa607d5d3b57"
                },
                "EnableUtxoDB": True,
                "CheckAddressHeight": 101,
                "VoteStartHeight": 100,
                "CRCOnlyDPOSHeight": 300,
                "PublicDPOSHeight": 308,
                "SeedList": [
                    "127.0.0.1:10018",
                    "127.0.0.1:10118",
                    "127.0.0.1:10218",
                    "127.0.0.1:10318",
                    "127.0.0.1:10418",
                    "127.0.0.1:10518",
                    "127.0.0.1:10618",
                    "127.0.0.1:10718",
                    "127.0.0.1:10818",
                    "127.0.0.1:10918"
                ],
                "MaxNodePerHost": 100,
                "CRConfiguration": {
                    "MemberCount": 4,
                    "VotingPeriod": 2000,
                    "DutyPeriod": 4000,
                    "DepositLockupBlocks": 2160,
                    "CRCAppropriatePercentage": 10,
                    "MaxCommitteeProposalCount": 128,
                    "MaxProposalTrackingCount": 128,
                    "ProposalCRVotingPeriod": 10,
                    "ProposalPublicVotingPeriod": 10,
                    "CRAgreementCount": 4,
                    "VoterRejectPercentage": 10,
                    "RegisterCRByDIDHeight": 300,
                    "CRAssetsAddress": "CRASSETSXXXXXXXXXXXXXXXXXXXX2qDX5J",
                    "CRExpensesAddress": "CREXPENSESXXXXXXXXXXXXXXXXXX4UdT6b",
                    "CRCAddress": "",
                    "CRVotingStartHeight": 300,
                    "CRCommitteeStartHeight": 350,
                    "SecretaryGeneral": "02A9D37E010950F810485512926BA13713BAF7F7675CC08DC4040E9802A84F410C",  # privateKey:E0076A271A137A2BD4429FA46E79BE3E10F2A730585F8AC2763D570B60469F11
                    "MaxCRAssetsAddressUTXOCount": 100,
                    "MinCRAssetsAddressUTXOCount": 50,
                    "CRAssetsRectifyTransactionHeight": 2000,
                    "CRCProposalWithdrawPayloadV1Height": 100,
                    "RectifyTxFee": 10000,
                    "RealWithdrawSingleFee": 10000,
                    "CRClaimDPOSNodeStartHeight": 385,
                    "CRClaimDPOSNodePeriod": 20
                },
                "CheckRewardHeight": 100,
                "FoundationAddress": "EgLe9ZAQyLmjxFZLp5em9VfqsYKvdhpGys",
                "RPCServiceLevel": "MiningPermitted",
                "NodeProfileStrategy": "Balanced",
                "MaxBlockSize": 8000000
            }
        }
        return ela_config

    @staticmethod
    def default_arbiter_config():
        arbiter_config = {
            "Configuration": {
                "ActiveNet": "regnet",
                "Magic": 2018203,
                "Version": 0,
                "NodePort": 10528,
                "PrintLevel": 0,
                "SpvPrintLevel": 0,
                "MaxLogsSize": 0,
                "MaxPerLogSize": 0,
                "HttpJsonPort": 10526,
                "MainNode": {
                    "Rpc": {
                        "IpAddress": "127.0.0.1",
                        "HttpJsonPort": 10516,
                        "User": "",
                        "Pass": "",
                        "WhiteIPList": [
                            "0.0.0.0"
                        ]
                    },
                    "SpvSeedList": [
                        "127.0.0.1:10518"
                    ],
                    "Magic": 2018201,
                    "MinOutbound": 1,
                    "MaxConnections": 3,
                    "FoundationAddress": "EgLe9ZAQyLmjxFZLp5em9VfqsYKvdhpGys",
                    "DefaultPort": 10518
                },
                "SideNodeList": [
                    {
                        "Rpc": {
                            "IpAddress": "127.0.0.1",
                            "HttpJsonPort": 10536,
                            "User": "",
                            "Pass": ""
                        },
                        "ExchangeRate": 1.0,
                        "GenesisBlock": "56be936978c261b2e649d58dbfaf3f23d4a868274f5522cd2adb4308a955c4a3",
                        "MiningAddr": "EM984iGC3w444ysVwUshekYzHRkKJry5ne",
                        "PayToAddr": "Eg4FRyiMa2xvjv2Kzd7V4jxRxWm1bv4JGY",
                        "PowChain": True
                    }
                ],
                "OriginCrossChainArbiters": [
                    "038eba1db314e7569aafc62a3c0fd1de9fe6359f88962521768a37786fce62dd37",
                    "02fb5528297b3c43e015d7e20a62b2fc70592cb0b08dfdec7ff95bcd11ff5a5fe6",
                    "03a9d3bbed3db04a4a6c167514b6a4e187b3eaeb3b8d4edd9a618d27b9fe4a0179",
                    "03022428a02e52ef0dd6adc1c7d95ea9cd93854057e9dd6a48486dc536ece71603",
                    "0251fc966a08f0e097711f54fa22ef69c90510ea8e8cf4431e8167c221cf3c7b86"
                ],
                "CRCCrossChainArbiters": [
                    "0342eeb0d664e2507d732382c66d0eedbd0a0f989179fd33d71679aa607d5d3b57",
                    "02cf7e80d1a1a76ab6259e0abdf2848c618655393f1fa3328901f80949ebed1476",
                    "02514cab9af25ee95e102b5c3a7c862b16f24b2de88d0110176e66ea379dfbc7a9",
                    "0322766f133141d2c9d82fb7e331ea6ec7c52e14de2c76bea0f59e479a1408fee3"
                ],
                "DPoSNetAddress": "127.0.0.1:10119",
                "CRCOnlyDPOSHeight": 300,
                "MinThreshold": 10000000,
                "DepositAmount": 10000000,
                "SyncInterval": 1000,
                "SideChainMonitorScanInterval": 1000,
                "ClearTransactionInterval": 60000,
                "MinOutbound": 3,
                "MaxConnections": 8,
                "SideAuxPowFee": 50000,
                "MaxTxsPerWithdrawTx": 1000,
                "RpcConfiguration": {
                    "User": "",
                    "Pass": "",
                    "WhiteIPList": [
                        "0.0.0.0"
                    ]
                }
            }
        }

        return arbiter_config

    @staticmethod
    def default_did_config():
        did_config = {
            "ActiveNet": "regnet",
            "Magic": 2018202,
            "NodePort": 10138,
            "DisableDNS": True,
            "PermanentPeers": [
                "127.0.0.1:10138",
                "127.0.0.1:10238",
                "127.0.0.1:10338",
                "127.0.0.1:10438",
                "127.0.0.1:10538"
            ],
            "SPVMagic": 2018201,
            "SPVDisableDNS": True,
            "SPVPermanentPeers": [
                "127.0.0.1:10018",
                "127.0.0.1:10118",
                "127.0.0.1:10218",
                "127.0.0.1:10318",
                "127.0.0.1:10418",
                "127.0.0.1:10518"
            ],
            "ExchangeRate": 1.0,
            "MinCrossChainTxFee": 10000,
            "EnableREST": True,
            "RESTPort": 10134,
            "EnableWS": True,
            "WSPort": 10135,
            "EnableRPC": True,
            "RPCPort": 10136,
            "RPCUser": "",
            "RPCPass": "",
            "RPCWhiteList": [
                "0.0.0.0"
            ],
            "Loglevel": 0,
            "PerLogFileSize": 20,
            "LogsFolderSize": 2048,
            "DisableTxFilters": False,
            "EnableMining": False,
            "InstantBlock": True,
            "PayToAddr": "Eg4FRyiMa2xvjv2Kzd7V4jxRxWm1bv4JGY",
            "MinerInfo": "ELA",
            "FoundationAddress": "EgLe9ZAQyLmjxFZLp5em9VfqsYKvdhpGys"
        }
        return did_config

    @staticmethod
    def default_token_config():
        token_config = {
            "ActiveNet": "regnet",
            "Magic": 2018202,
            "NodePort": 10138,
            "DisableDNS": True,
            "PermanentPeers": [
                "127.0.0.1:10138",
                "127.0.0.1:10238",
                "127.0.0.1:10338",
                "127.0.0.1:10438",
                "127.0.0.1:10538"
            ],
            "SPVMagic": 2018201,
            "SPVDisableDNS": True,
            "SPVPermanentPeers": [
                "127.0.0.1:10018",
                "127.0.0.1:10118",
                "127.0.0.1:10218",
                "127.0.0.1:10318",
                "127.0.0.1:10418",
                "127.0.0.1:10518"
            ],
            "ExchangeRate": 1.0,
            "MinCrossChainTxFee": 10000,
            "EnableREST": True,
            "RESTPort": 10134,
            "EnableWS": True,
            "WSPort": 10135,
            "EnableRPC": True,
            "RPCPort": 10136,
            "RPCUser": "",
            "RPCPass": "",
            "RPCWhiteList": [
                "0.0.0.0"
            ],
            "Loglevel": 0,
            "PerLogFileSize": 20,
            "LogsFolderSize": 2048,
            "DisableTxFilters": False,
            "EnableMining": False,
            "InstantBlock": True,
            "PayToAddr": "Eg4FRyiMa2xvjv2Kzd7V4jxRxWm1bv4JGY",
            "MinerInfo": "ELA",
            "FoundationAddress": "EgLe9ZAQyLmjxFZLp5em9VfqsYKvdhpGys"
        }

        return token_config

    @staticmethod
    def default_neo_config():
        neo_config = {
            "ActiveNet": "regnet",
            "Magic": 2018202,
            "NodePort": 10138,
            "DisableDNS": True,
            "PermanentPeers": [
                "127.0.0.1:10138",
                "127.0.0.1:10238",
                "127.0.0.1:10338",
                "127.0.0.1:10438",
                "127.0.0.1:10538"
            ],
            "SPVMagic": 2018201,
            "SPVDisableDNS": True,
            "SPVPermanentPeers": [
                "127.0.0.1:10018",
                "127.0.0.1:10118",
                "127.0.0.1:10218",
                "127.0.0.1:10318",
                "127.0.0.1:10418",
                "127.0.0.1:10518"
            ],
            "ExchangeRate": 1.0,
            "MinCrossChainTxFee": 10000,
            "EnableREST": True,
            "RESTPort": 10134,
            "EnableWS": True,
            "WSPort": 10135,
            "EnableRPC": True,
            "RPCPort": 10136,
            "RPCUser": "",
            "RPCPass": "",
            "RPCWhiteList": [
                "0.0.0.0"
            ],
            "Loglevel": 0,
            "PerLogFileSize": 20,
            "LogsFolderSize": 2048,
            "DisableTxFilters": False,
            "EnableMining": False,
            "InstantBlock": True,
            "PayToAddr": "Eg4FRyiMa2xvjv2Kzd7V4jxRxWm1bv4JGY",
            "MinerInfo": "ELA",
            "FoundationAddress": "EgLe9ZAQyLmjxFZLp5em9VfqsYKvdhpGys"
        }
        return neo_config

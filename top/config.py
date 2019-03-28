#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/20 3:25 PM
# author: liteng

ela = {
    "Configuration": {
        "Magic": 20181212,
        "Version": 23,
        "SeedList": [
            "172.31.32.193:25338",
            "172.31.43.101:25338",
            "172.31.45.130:25338",
            "172.31.40.70:25338",
            "172.31.32.224:25338",
            "172.31.38.65:25338",
            "172.31.38.89:25338"
        ],
        "HttpInfoPort": 25333,
        "HttpInfoStart": True,
        "HttpRestPort": 25334,
        "HttpWsPort": 25335,
        "WsHeartbeatInterval": 60,
        "HttpJsonPort": 25336,
        "NodePort": 25338,
        "NodeOpenPort": 25866,
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
        "MinCrossChainTxFee": 10000,
        "PowConfiguration": {
            "PayToAddr": "EWUSe87Qiekzpx7Xqf8RphdwNX5Z84iGEA",
            "AutoMining": False,
            "MinerInfo": "ELA",
            "MinTxFee": 100,
            "ActiveNet": "MainNet"
        },
        "FoundationAddress": "EVNLb3kJLxMePeBJ4nJowxhxSps8qSMZrH",
        "EnableArbiter": True,
        "ArbiterConfiguration": {
            "PublicKey": "024babfecea0300971a6f0ad13b27519faff0ef595faf9490dc1f5f4d6e6d7f3fb",
            "Magic": 20181210,
            "NodePort": 25339,
            "ProtocolVersion": 0,
            "Services": 0,
            "PrintLevel": 0,
            "SignTolerance": 5,
            "MaxLogsSize": 0,
            "MaxPerLogSize": 0,
            "MaxConnections": 100,
            "NormalArbitratorsCount": 8,
            "CandidatesCount": 24,
            "EmergencyTriggerTimeSpan": 3600,
            "EmergencyDuration": 604800,
            "OriginArbiters": [
                "0247984879d35fe662d6dddb4edf111c9f64fde18ccf8af0a51e4b278c3411a8f2",
                "032e583b6b578cccb9bbe4a53ab54a3e3e60156c01973b16af52b614813fca1bb2",
                "0223b8e8098dd694f4d20ea74800b1260a5a4a0afe7f6a0043c7e459c84ff80fba",
                "03982eaa9744a3777860013b6b988dc5250198cb81b3aea157f9b429206e3ae80f",
                "0328443c1e4bdb5b60ec1d017056f314ba31f8f9f43806128fac20499a9df27bc2"
            ],
            "CRCArbiters": [
                {
                    "PublicKey": "024babfecea0300971a6f0ad13b27519faff0ef595faf9490dc1f5f4d6e6d7f3fb",
                    "NetAddress": "172.31.32.193:25339"
                },
                {
                    "PublicKey": "0243ff13f1417c69686bfefc35227ad4f5f4ca03ccb3d3a635ae8ed67d57c20b97",
                    "NetAddress": "172.31.43.101:25339"
                },
                {
                    "PublicKey": "024ac1cdf73e3cbe88843b2d7279e6afdc26fc71d221f28cfbecbefb2a48d48304",
                    "NetAddress": "172.31.45.130:25339"
                },
                {
                    "PublicKey": "0274fe9f165574791f74d5c4358415596e408b704be9003f51a25e90fd527660b5",
                    "NetAddress": "172.31.40.70:25339"
                }
            ],
        },

        "RpcConfiguration": {
            "User": "",
            "Pass": "",
            "WhiteIpList": [
                "0.0.0.0"
            ]
        },

        "HeightVersions": [
            0,
            101,
            200,
            20000
        ]
    }
}

arbiter = {
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

did = {
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


token = {
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

neo = {
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
        "HttpInfoPort":  10051,
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
        "PrintLevel":  1,
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


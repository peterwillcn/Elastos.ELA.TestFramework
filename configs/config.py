#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/20 3:25 PM
# author: liteng

main_chain = {
  "Configuration":  {
      "Magic": 7530401,
      "Version": 23,
      "SeedList": [
            "127.0.0.1:10015",
            "127.0.0.1:10115",
            "127.0.0.1:10215",
            "127.0.0.1:10315",
      ],
      "HttpInfoPort": 10011,
      "HttpInfoStart": True,
      "HttpRestPort": 10012,
      "NodeOpenPort": 10016,
      "OpenService": True,
      "HttpWsPort": 10013,
      "WsHeartbeatInterval": 60,
      "HttpJsonPort": 10014,
      "NoticeServerUrl": "",
      "OauthServerUrl": "",
      "NodePort": 10015,
      "PrintLevel": 1,
      "IsTLS": False,
      "CertPath": "./sample-cert.pem",
      "KeyPath": "./sample-cert-key.pem",
      "CAPath": "./sample-ca.pem",
      "MultiCoreNum": 4,
      "MaxTransactionInBlock": 10000,
      "MaxBlockSize": 8000000,
      "FoundationAddress": "8VYXVxKKSAxkmRrfmGpQR2Kc66XhG6m3ta",
      "PowConfiguration": {
          "PayToAddr": "ESqZDVDeucDnq9d6Unvrd6rrwy7A8Ag6Bi",
          "MiningServerIP": "127.0.0.1",
          "MiningServerPort": 5555,
          "MiningSelfPort": 31339,
          "TestNet": True,
          "AutoMining": False,
          "MinerInfo": "ELA",
          "MinTxFee": 100,
          "ActiveNet": "RegNet"
      },
    "EnableArbiter": False,
      "Arbiters": [
        "03e333657c788a20577c0288559bd489ee65514748d18cb1dc7560ae4ce3d45613",
        "02dd22722c3b3a284929e4859b07e6a706595066ddd2a0b38e5837403718fb047c",
        "03e4473b918b499e4112d281d805fc8d8ae7ac0a71ff938cba78006bf12dd90a85",
        "03dd66833d28bac530ca80af0efbfc2ec43b4b87504a41ab4946702254e7f48961",
        "02c8a87c076112a1b344633184673cfb0bb6bce1aca28c78986a7b1047d257a448"
      ],
      "RpcConfiguration": {
        "User": "",
        "Pass": "",
        "WhiteIpList": [
            "0.0.0.0"
      ]
    }
  }
}


arbiter_chain = {
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

did_chain = {
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


token_chain = {
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

neo_chain = {
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


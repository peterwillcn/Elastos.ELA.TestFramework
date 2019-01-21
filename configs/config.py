#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/20 3:25 PM
# author: liteng

main_chain = {
  "Configuration":  {
      "Magic": 20190120,
      "Version": 23,
      "SeedList": [
            "127.0.0.1:30338",
            "127.0.0.1:31338",
            "127.0.0.1:32338",
            "127.0.0.1:33338",
      ],
      "HttpInfoPort": 31333,
      "HttpInfoStart": True,
      "HttpRestPort": 31334,
      "NodeOpenPort": 30866,
      "OpenService": True,
      "HttpWsPort": 31335,
      "WsHeartbeatInterval": 60,
      "HttpJsonPort": 31336,
      "NoticeServerUrl": "",
      "OauthServerUrl": "",
      "NodePort": 31338,
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
    "SeedList": ["127.0.0.1:10538",
                 "127.0.0.1:11538"],
    "NodePort": 30338,
    "PrintLevel": 1,
    "SpvPrintLevel": 4,
    "HttpJsonPort": 30336,
    "MainNode": {
      "Rpc": {
        "IpAddress": "127.0.0.1",
        "HttpJsonPort": 31336
      },
      "SpvSeedList": ["127.0.0.1:20866"],
      "Magic": 7630401,
      "MinOutbound": 1,
      "MaxConnections": 3,
      "FoundationAddress": "8VYXVxKKSAxkmRrfmGpQR2Kc66XhG6m3ta",
      "DefaultPort": 30866
    },
    "SideNodeList": [
        {"Rpc": {
          "IpAddress": "127.0.0.1",
          "HttpJsonPort": 33336
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
      "Magic": 7630404,
      "SpvMagic": 7630401,
      "Version": 23,
      "SeedList": [
            "127.0.0.1:30608",
            "127.0.0.1:31608",
            "127.0.0.1:32608",
            "127.0.0.1:33608"
        ],
      "SpvSeedList": ["127.0.0.1:30866"],
      "MainChainFoundationAddress": "EM8DhdWEFmuLff9fH7fZssK7h5ayUzKcV7",
      "FoundationAddress": "8VYXVxKKSAxkmRrfmGpQR2Kc66XhG6m3ta",
      "SpvMinOutbound": 3,
      "SpvMaxConnections": 10,
      "SpvPrintLevel": 1,
      "ExchangeRate": 1.0,
      "MinCrossChainTxFee": 10000,
      "HttpInfoPort": 33333,
      "HttpInfoStart": True,
      "HttpRestPort": 33334,
      "HttpWsPort": 33335,
      "WsHeartbeatInterval": 60,
      "HttpJsonPort": 33336,
      "NoticeServerUrl": "",
      "OauthServerUrl": "",
      "NodePort": 33338,
      "NodeOpenPort": 30607,
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
        "Magic": 7630402,
        "SpvMagic": 7630401,
        "Version": 23,
        "SeedList": [
          "127.0.0.1:10808",
          "127.0.0.1:11808",
          "127.0.0.1:12808",
          "127.0.0.1:13808"
        ],
        "SpvSeedList": [
          "127.0.0.1:20866"
        ],
        "SpvMinOutbound": 3,
        "SpvMaxConnections": 10,
        "ExchangeRate": 1.0,
        "MinCrossChainTxFee": 10000,
        "HttpInfoPort": 31603,
        "HttpInfoStart": True,
        "HttpRestPort": 31604,
        "HttpWsPort": 31605,
        "WsHeartbeatInterval": 60,
        "HttpJsonPort": 31606,
        "NoticeServerUrl": "",
        "OauthServerUrl": "",
        "NodePort": 31608,
        "NodeOpenPort": 31607,
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
        "MainChainDefaultPort": 30866,
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
        "Magic": 7630409,
        "SpvMagic": 7630401,
        "Version": 1,
        "SeedList": [
          "127.0.0.1:10908",
          "127.0.0.1:11908",
          "127.0.0.1:12908",
          "127.0.0.1:13908"
        ],
        "SpvSeedList": [
        ],
        "SpvMinOutbound": 3,
        "SpvMaxConnections": 10,
        "ExchangeRate": 1.0,
        "MinCrossChainTxFee": 10000,
        "HttpInfoPort":  30603,
        "HttpInfoStart": True,
        "HttpRestPort": 30604,
        "HttpWsPort": 30607,
        "WsHeartbeatInterval": 60,
        "HttpJsonPort": 30606,
        "NoticeServerUrl": "",
        "OauthServerUrl": "",
        "NodePort": 30808,
        "NodeOpenPort": 30807,
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
        "MainChainDefaultPort": 30866,
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


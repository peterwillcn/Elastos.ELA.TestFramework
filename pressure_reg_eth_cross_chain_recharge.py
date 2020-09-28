import time
import os
import os.path
import json

from src.control.tx import TxControl
from src.tools.log import Logger

# # withdraw from side chain
# config = {
#     "recharge": 0,
#     "rpc_port": 10216,
#     "host": "127.0.0.1",
#     "outputs_num": 10,
#     "inputs_num": 10,
#     "block_size": 1,
#     "pressure_private_key": "fcbcd369529e4229468ac4f78627467bbe2b6f1c6625b1d9f0f55bf11e638090",
#     # EM7U5Y8AJcv49pUPQ5jPpt93Nmcwh3ti4Y
#     "tap_private_key": "bd758440a858baaff56ec1783388bc44135ed44bb0e4f25ad6cf28be45896d74",
#     # EWRwrmBWpYFwnvAQffcP1vrPCS5sGTgWEB
#     "lock_address": "0000000000000000000000000000000000"
# }

keystoredir = "/root/node/eth_nodes/oracle/keystore"
# recharge to side chain
config = {
    "recharge": 1,
    "rpc_port": 10016,
    "host": "127.0.0.1",
    "outputs_num": 1,
    "inputs_num": 1,
    "block_size": 1,
    "pressure_private_key": "fcbcd369529e4229468ac4f78627467bbe2b6f1c6625b1d9f0f55bf11e638090",
    # EM7U5Y8AJcv49pUPQ5jPpt93Nmcwh3ti4Y
    "tap_private_key": "bd758440a858baaff56ec1783388bc44135ed44bb0e4f25ad6cf28be45896d74",
    # EWRwrmBWpYFwnvAQffcP1vrPCS5sGTgWEB
    "eth_tap_address": "0x53781e106a2e3378083bdcede1874e5c2a7225f8",
    "lock_address": "XaKGQrBSAUPF9pAZMz7Ek1S1SdRaw1NfKJ" # eth
    #"lock_address":"XKUh4GLhFJiqAMTF6HyWQrV9pK9HcGUdfJ" # did
}


def test_content():
    tx = TxControl(config)
    tx.get_current_height()
    tx.ready_for_pressure_outputs()
    tx.ready_for_pressure_cross_chain()

if __name__ == '__main__':
    Logger.warn("[main] begin testing")
    test_content()
    Logger.warn("[main] end testing")

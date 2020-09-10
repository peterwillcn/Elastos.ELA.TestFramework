import time

from src.control.tx import TxControl
from src.tools.log import Logger

config = {
    "rpc_port": 10116,
    "host": "127.0.0.1",
    "outputs_num": 10,
    "inputs_num": 10,
    "block_size": 1,
    "pressure_private_key": "fcbcd369529e4229468ac4f78627467bbe2b6f1c6625b1d9f0f55bf11e638090",
    # EM7U5Y8AJcv49pUPQ5jPpt93Nmcwh3ti4Y
    "tap_private_key": "bd758440a858baaff56ec1783388bc44135ed44bb0e4f25ad6cf28be45896d74",
    # EWRwrmBWpYFwnvAQffcP1vrPCS5sGTgWEB
    "lock_address": "XFNwHEkHvAvMK7b3BuF5dJUJ1ZvbpprQ14"
}


def test_content():
    # pressure test inputs more
    tx = TxControl(config)

    while True:
        tx.get_current_height()
        tx.ready_for_pressure_outputs()
        tx.ready_for_pressure_cross_chain()

        # producer vote
        # tx.ready_for_cross_chain()

        # cr vote
        # tx.ready_for_cr()

        # crc proposal


if __name__ == '__main__':
    Logger.warn("[main] begin testing")
    test_content()
    Logger.warn("[main] end testing")

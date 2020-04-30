import time

from src.control.tx import TxControl
from src.tools.log import Logger

config = {
    "rpc_port": 22336,
    "host": "23.22.178.172",
    "inputs_num": 6000,
    "block_size": 1,
    "pressure_private_key": "de2f13721b1351833cdc49846b2e3e7d1dfb36ad103abd0f26cc78b5242b5874",
    # EbHBvtcy1TxxU6jCxf7cAWdhrQz9GGQ1ca
    "tap_private_key": "5843b9068fa32999529da9a218837c07f6718a574698ab0008bda9cd0560073e"
    # ET7g8qUq4nehZhd6qSe4Q9WyeNZu5Havom
}


def test_content():
    # pressure test inputs more
    tx = TxControl(config)

    while True:
        tx.get_current_height()
        tx.ready_for_pressure_inputs()
        # tx.ready_for_pressure_big_block()

        # producer vote
        tx.ready_for_dpos()

        # cr vote
        tx.ready_for_cr()

        # crc proposal


if __name__ == '__main__':
    Logger.warn("[main] begin testing")
    test_content()
    Logger.warn("[main] end testing")

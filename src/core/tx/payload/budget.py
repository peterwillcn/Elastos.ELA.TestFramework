
import struct

from src.tools import serialize
from src.tools.log import Logger

from src.core.wallet.account import Account
from src.core.tx.payload.payload import Payload
from src.core.wallet import keytool


class Budget(object):
    IMPREST = 0x00
    NORMAL_PAYMENT = 0x01
    FINAL_PAYMENT = 0x02

    def __init__(self, budget_type: int, stage: int, amount: int):
        self.type = budget_type
        self.stage = stage
        self.amount = amount

    def serialize(self, version: int):
        r = b""
        r += struct.pack("<B", self.type)
        r += struct.pack("<B", self.stage)
        r += struct.pack("<q", self.amount)
        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def __repr__(self):
        return "Budget {" + "\n\t" \
               + "type: {}".format(self.type) + "\n\t" \
               + "stage : {}".format(self.stage) + "\n\t" \
               + "amount : {}".format(self.amount) + "\n\t" \
               + "}"

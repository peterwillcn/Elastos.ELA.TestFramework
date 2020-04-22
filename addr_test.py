
from decimal import Decimal
from src.core.services import rpc
from src.tools import util

config = {
    'path': './balance.csv',
    'rpc_port': 20336
}


def read_csv(path: str):
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    return lines


def test_addr():
    path = config['path']
    port = config['rpc_port']
    data: list = read_csv(path)
    for i in range(1, len(data)):
        print(data[i])
        s_data = data[i].split(',')
        addr = s_data[0]
        v1 = int(s_data[1])
        value = rpc.get_balance_by_address(addr, port)
        if v1 != int(Decimal(value) * util.TO_SELA):
            print("addr:{}, v1:{} != v2:{}".format(addr, v1, value))

    '''
     Comparison of Read csv File Address and Amount to Node Data Address Amount
    '''
if __name__ == '__main__':
    test_addr()

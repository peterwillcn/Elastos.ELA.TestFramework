import subprocess
import time
import requests

import config
from Utility import util
from Utility.node import JarServer
from requests.auth import HTTPDigestAuth


def utxo(vout, private_key, txid):
    return [{
        "txid": txid,
        "vout": vout,
        "privatekey": private_key
    }]


def output(address):
    return [{
        "address": address,
        "amount": "0.00000001"
    }]


def get_block_count(url):
    resp = util.post_request(url, "getblockcount")
    return resp["result"]


def list_unspent(url, addresses):
    resp = util.post_request(url, "listunspent", params={"addresses": addresses})
    if ('error' not in resp) or resp["error"] is None:
        return resp["result"]
    else:
        assert False, 'list_unspent: ' + resp["error"]


def create_transaction(utxos, outputs):
    url_ = 'http://127.0.0.1:8989'
    try:
        resp = requests.post(url_, json={"method": "genrawtx",
                                         "params": {"transaction": {"inputs": utxos, "outputs": outputs}}},
                             headers={"content-type": "application/json"},
                             auth=requests.auth.HTTPBasicAuth(config.auth_User, config.auth_Pass))
        # print("method", method, " params", params, " url", url)
        return resp.text
    except requests.exceptions.RequestException as e:
        print("Post Requiest Error:", e)
        return False


def get_txpool_size(url):
    result = util.post_request(url, "getrawmempool", params={})
    if result["error"] is None:
        tx_pool = result['result']
        return len(tx_pool)
    else:
        return False


def send_raw_transaction(url, data):
    resp = util.post_request(url, "sendrawtransaction", params={"data": data})
    if resp["error"] is None:
        return resp["result"]
    else:
        assert False, 'send_raw_transaction: ' + str(resp)


if __name__ == '__main__':
    subprocess.getoutput("killall java")

    url = 'http://127.0.0.1:22336'
    txid = '9061481933dabf697d0cb2a47934c88593583d666fa873bfe45e0dca45805df0'  # regtest
    vout_start = 2436
    vout_end = 24999

    private_key = ''
    address = ''

    next_height = 0
    step = 0
    util.formate_output(mode="BLUE", result="启动jar包，构造大交易", testname="", step=step)
    JarServer(jar_type='big_tx')

    while True:
        current_height = get_block_count(url)
        tx_size = get_txpool_size(url)

        print('next_height:{}\t current_height:{}\t tx_pool:{}'.format(next_height - 1, current_height - 1, tx_size))

        if next_height < current_height and tx_size < 1:
            if vout_start <= vout_end:
                for v in range(vout_start, vout_start + 2):
                    step += 1
                    util.formate_output(mode="BLUE", result="构造{}个交易".format(step), testname="", step=step)
                    addresses = list()
                    addresses.append(address)
                    data = create_transaction(utxo(v, private_key, txid), output(address))
                    util.formate_output(mode="BLUE", result="发送{}个交易".format(step), testname="", step=step)
                    print('txid:', send_raw_transaction(url, data.strip()))

                    util.formate_output(mode="BLUE", result="使用{}个vout".format(v), testname="", step=step)
                    vout_start += 1
            else:
                assert False, '余额不足'
        next_height = current_height
        time.sleep(10)

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/20 3:37 PM
# author: liteng

import os
import json
import time
import shutil

from configs import constant
from configs import config
from decimal import Decimal
from logs.log import Logger
from utils import switch
from utils import util
from core.deploy import node
from core.service import jar
from core.service import rpc
from core.wallet import keystoremanager


class Deploy(object):

    def __init__(self):
        self.main_nodes = []
        self.arbiter_nodes = []
        self.did_nodes = []
        self.token_nodes = []
        self.neo_nodes = []
        self.rpc = rpc.RPC()
        self.tag = '[Deploy] '
        self.fee = 10000
        self.jar_service = jar.JarService()
        self.switch_list = self._switch_list()
        self.switch_path = switch.switch_path()
        self.switch_config = switch.switch_config()
        self.key_manager = keystoremanager.KeyStoreManager(constant.KEYSTORE_MANAGER_INIT_COUNT)
        self.main_chain_foundation_address = self.key_manager.key_stores[0].address
        self.side_chain_foundation_address = self.key_manager.key_stores[1].address
        self.miner_address = self.key_manager.key_stores[2].address
        self.arbiter_public_keys = util.gen_arbiter_public_keys(self.key_manager.key_stores[3:8])

    def _switch_list(self):
        switcher = {
            constant.NODE_TYPE_MAIN: self.main_nodes,
            constant.NODE_TYPE_ARBITER: self.arbiter_nodes,
            constant.NODE_TYPE_DID: self.did_nodes,
            constant.NODE_TYPE_TOKEN: self.token_nodes,
            constant.NODE_TYPE_NEO: self.neo_nodes
        }
        return switcher

    def _switch_node(self, index, cmd_dir, _config, content):
        switcher = {
            constant.NODE_TYPE_MAIN: node.MainNode(index, cmd_dir, _config, content),
            constant.NODE_TYPE_ARBITER: node.ArbiterNode(index, cmd_dir, _config, content),
            constant.NODE_TYPE_DID: node.DidNode(index, cmd_dir, _config, content),
            constant.NODE_TYPE_TOKEN: node.TokenNode(index, cmd_dir, _config, content),
            constant.NODE_TYPE_NEO: node.NeoNode(index, cmd_dir, _config, content)
        }
        return switcher

    def deploy_node_environment(self, node_type: str, num: int):

        if num < 0:
            Logger.error('{} Invalid param num: {}'.format(self.tag, num))
            return False
        Logger.debug('{} deploy {} binary'.format(self.tag, node_type))
        src_path = os.path.join(self.switch_path[node_type])
        if not os.path.exists(src_path):
            Logger.error('{} path not found: '.format(src_path))
            return False
        _config = self.switch_config[node_type]

        content = {}
        content[constant.MAIN_CHAIN_FOUNDATION_ADDRESS] = self.main_chain_foundation_address
        content[constant.SIDE_CHAIN_FOUNDATION_ADDRESS] = self.side_chain_foundation_address
        content[constant.MINER_ADDRESS] = self.miner_address

        for i in range(num):
            dest_path = os.path.join(constant.TEST_PARAENT_PATH, node_type,
                                     constant.CURRENT_DATE_TIME, 'node' + str(i))
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            shutil.copy(src_path, dest_path + '/ela')

            config_path = os.path.join(dest_path, 'config.json')
            # config_path = dest_path + '/config.json'
            main_chain_default_port = util.reset_config_ports(i, constant.NODE_TYPE_MAIN, constant.CONFIG_PORT_OPEN)
            content[constant.MAIN_CHAIN_DEFAULT_PORT] = main_chain_default_port
            content[constant.SPV_SEED_LIST] = [constant.HOST_NAME + ':' + str(main_chain_default_port)]
            content[constant.CONFIG_ARBITERS] = self.arbiter_public_keys
            n = self._switch_node(i, dest_path, _config, content)[node_type]
            n.generate_config()
            with open(config_path, 'w') as f:
                json.dump(n.config, f, indent=4)
            self.switch_list[node_type].append(n)

        return True

    def start_nodes(self, node_type: str):
        length = len(self.switch_list[node_type])
        for i in range(length):
            self.switch_list[node_type][i].start()
            time.sleep(1)

    def stop_nodes(self, node_type: str):
        length = len(self.switch_list[node_type])
        for i in range(length):
            self.switch_list[node_type][i].stop()
        self.jar_service.stop()

    def wait_rpc_service(self, content=1,  timeout=60):

        stop_time = time.time() + timeout

        while time.time() <= stop_time:
            result = []
            for i in range(len(self.main_nodes)):
                count = self.rpc.get_connection_count()
                Logger.debug('{} connection count: {}'.format(self.tag, count))
                if count and count >= content:
                    result.append(True)
                else:
                    result.append(False)
                if result.count(True) == len(self.main_nodes):
                    Logger.debug('{} Nodes connect with each other, '
                                 'rpc service is successfully started.'.format(self.tag))
                    return True
                time.sleep(2)
        Logger.error('{} Node can not connect with each other, wait rpc service timed out!')
        return False

    def check_foundation_amount(self):
        balance = self.rpc.get_balance_by_address(self.main_nodes[0].main_chain_foundation_address)
        Logger.debug('{} foundation address balance: {}'.format(self.tag, balance))

    def mining_101_blocks(self):
        hash_list = self.rpc.discrete_mining(101)
        if len(hash_list) != 101:
            Logger.error("{} Discrete mining 101 blocks failed.".format(self.tag))
            return False
        Logger.debug('{} Discrete mining 101 blocks on success'.format(self.tag))
        Logger.debug('{} Discrete mining 101 blocks hashes: {}'.format(self.tag, hash_list))
        return True

    def get_utxos_amount(self, utxos, mode='ela'):
        amount = 0
        if not isinstance(utxos, list):
            utxos = [utxos]
        for utxo in utxos:
            amount += float(utxo['amount']) * 100000000
        return int(amount)

    def get_enough_value_for_amount(self, utxos, amount, fee, index=-1, quantity=0, utxo_value=0, mode='ela'):
        if utxo_value <= amount + fee and amount >= 0:
            index += 1
            utxo_value += self.get_utxos_amount(utxos[index], mode=mode)
            quantity += 1
            return self.get_enough_value_for_amount(utxos=utxos, utxo_value=utxo_value, amount=amount,
                                               fee=fee, index=index, quantity=quantity, mode=mode)
        elif utxo_value > amount + fee and amount < 0:  # 这个条件是为了构造amount为负数的异常测试， 保证input里有输入
            utxo_value += self.get_utxos_amount(utxos[0], mode=mode)
            quantity = 1
            return {'utxo_value': utxo_value, 'quantity': quantity}
        else:
            return {'utxo_value': utxo_value, 'quantity': quantity}

    def get_utxo_from_rpc(self, port: int, address, assetid=None, privateKey=''):
        utxos = []
        resp = self.rpc.list_unspent_utxos(addresses=address, assetid=assetid)
        print("resp **********", resp)
        for index in resp:
            utxos.append({'txid': index['txid'], 'index': index['vout'], 'amount': index['amount'],
                          'address': index['address'], 'privatekey': privateKey})
        return utxos

    def gen_input_for_transaction(self, utxos, mode="address"):
        input = []
        if not isinstance(utxos, list):
            utxos = [utxos]
        for utxo in utxos:
            if not utxo['amount'] == '0':
                input.append({"txid": utxo["txid"], "vout": utxo["index"], mode: utxo[mode]})
        return input

    def gen_transaction_outputs(self, addresses: list, amount: int, change_address: str, utxo_value: int, fee=100):
        print("type addresses: ", type(addresses))
        print('type amount: ', type(amount))
        print('type change_address: ', type(change_address))
        print('type utxos_value: ', type(utxo_value))
        print('type fee: ', type(fee))
        if utxo_value < ((amount + fee) * len(addresses) + 1):
            print("utxo is not enough!")
            return None
        else:
            change_value = utxo_value - (amount + fee) * len(addresses)
            change_value = str(Decimal(str(change_value)) / Decimal(100000000))
            amount = str(Decimal(str(amount)) / Decimal(100000000))
            output = []
            for addr in addresses:
                output.append({"address": addr, "amount": amount})
            if not float(change_value) == 0:
                output.append({"address": change_address, "amount": change_value})
            return output

    def generate_inputs(self, input_keystore, amount: int):
        utxos = self.get_utxo_from_rpc(
            port=self.main_nodes[0].rpc_port,
            address=input_keystore.address,
            privateKey=input_keystore.private_key.hex()
        )

        resp = self.get_enough_value_for_amount(utxos=utxos, amount=amount, fee=self.fee)
        utxos_value = resp['utxo_value']
        print('utxos_value: ', utxos_value)
        print('type utxos_value: ', type(utxos_value))
        utxos_quantitiy = resp['quantity']
        inputs = self.gen_input_for_transaction(utxos=utxos[0:utxos_quantitiy], mode='privatekey')
        print("inputs: ", inputs)
        return inputs, utxos_value

    def generate_outputs(self, output_addresses, change_address, utxos_value: int, amount: int):
        outputs = self.gen_transaction_outputs(
            addresses=output_addresses,
            amount=amount,
            change_address=change_address,
            utxo_value=utxos_value,
        )
        print('outputs: ', outputs)
        return outputs

    def ordinary_transaction(self, input_keystore, output_addresses, amount: int):
        inputs, utxos_value = self.generate_inputs(input_keystore, amount)
        outputs = self.generate_outputs(output_addresses, input_keystore.address, utxos_value, amount)
        content = self.jar_service.create_transaction(utxos=inputs, outputs=outputs)
        raw = content["rawtx"]
        txid = content["txhash"].lower()
        print("[Manager] raw data: ", raw)
        print("[Manager] txid: ", txid)
        resp = self.rpc.send_raw_transaction(data=raw)
        result = resp == txid
        if not result:
            print("[Manager] ordinary transaction result: ", result)
            return result

        print("ordinary transaction on success!")
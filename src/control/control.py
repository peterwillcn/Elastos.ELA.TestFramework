#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/7 7:05 PM
# author: liteng

import os
import math
import time

from src.core.services import rpc
from src.core.parameters.params import Parameter
from src.core.managers.env_manager import EnvManager
from src.core.managers.node_manager import NodeManager
from src.core.managers.keystore_manager import KeyStoreManager
from src.core.managers.tx_manager import TransactionManager
from src.core.managers.rpc_manager import RpcManager
from src.tools import util
from src.tools import constant
from src.tools.log import Logger


class Controller(object):

    PRODUCER_STATE_ACTIVE = "Active"
    PRODUCER_STATE_INACTIVE = "Inactive"

    def __init__(self, up_config: dict):
        self.tag = util.tag_from_path(__file__, Controller.__name__)

        # set config
        self.up_config = up_config
        self.root_path = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../../"))
        self.config = util.read_config_file(os.path.join(self.root_path, "config.json"))
        self.node_types = ["ela", "arbiter", "did", "token", "neo"]
        self.reset_config(up_config)

        self.params = Parameter(self.config, self.root_path)
        self.check_params()
        self.env_manager = EnvManager()
        self.keystore_manager = KeyStoreManager(self.params)

        self.node_manager = NodeManager(self.params, self.env_manager, self.keystore_manager)
        self.rpc_manager = RpcManager(self.node_manager)
        self.tx_manager = TransactionManager(self.node_manager)
        # init tap amount and register amount(unit: ELA)
        self.tap_amount = 20000000
        self.register_amount = 6000
        self.node_amount = 5000
        # necessary keystore
        self.foundation_keystore = self.keystore_manager.special_key_stores[0]
        self.tap_keystore = self.keystore_manager.special_key_stores[4]

        self.init_for_testing()
        self.later_nodes = self.node_manager.ela_nodes[(self.params.ela_params.number -
                                                              self.params.ela_params.later_start_number + 1):]

        self.dpos_votes_dict = dict()

    def init_for_testing(self):
        self.node_manager.deploy_nodes()
        Logger.info("{} deploying nodes on success!".format(self.tag))
        self.node_manager.start_nodes()
        Logger.info("{} starting nodes on success!".format(self.tag))
        self.rpc_manager.mining_blocks_ready(self.node_manager.main_foundation_address)
        Logger.info("{} mining 110 blocks on success!".format(self.tag))
        time.sleep(5)

        self.rpc_manager.init_pubkey_nodes()
        self.rpc_manager.init_normal_dpos_public_keys()

        ret = self.tx_manager.recharge_necessary_keystore(
            input_keystore=self.foundation_keystore,
            keystores=[self.tap_keystore],
            amount=self.tap_amount * constant.TO_SELA
        )

        self.check_result("recharge tap keystore", ret)

        Logger.info("{} recharge tap keystore {} ELAs on success!".format(self.tag, self.tap_amount * constant.TO_SELA))

        ret = self.tx_manager.recharge_necessary_keystore(
            input_keystore=self.tap_keystore,
            keystores=self.keystore_manager.owner_key_stores,
            amount=self.register_amount * constant.TO_SELA
        )

        self.check_result("recharge owner keystore", ret)

        ret = self.tx_manager.recharge_necessary_keystore(
            input_keystore=self.tap_keystore,
            keystores=self.keystore_manager.node_key_stores,
            amount=self.node_amount * constant.TO_SELA
        )

        self.check_result("recharge node keystore", ret)

        Logger.info("{} recharge producer on success!".format(self.tag))

        if self.params.arbiter_params.enable:
            ret = self.tx_manager.recharge_necessary_keystore(
                input_keystore=self.tap_keystore,
                keystores=self.keystore_manager.arbiter_stores,
                amount=3 * constant.TO_SELA
            )

            self.check_result("recharge arbiter keystore", ret)
            Logger.info("{} recharge each arbiter keystore {} ELAs on success!")

            ret = self.tx_manager.recharge_necessary_keystore(
                input_keystore=self.tap_keystore,
                keystores=self.keystore_manager.sub_key_stores,
                amount=3 * constant.TO_SELA
            )
            self.check_result("recharge sub keystore", ret)
            Logger.info("{} recharge each sub keystore {} ELAs on success!")

            ret = self.tx_manager.recharge_necessary_keystore(
                input_keystore=self.tap_keystore,
                keystores=self.keystore_manager.sub_key_stores2,
                amount=3 * constant.TO_SELA
            )
            self.check_result("recharge sub keystore2", ret)
            Logger.info("{} recharge each sub keystore2 {} ELAs on success!")

    def ready_for_dpos(self):
        ret = self.tx_manager.register_producers_candidates()
        self.check_result("register producers", ret)
        Logger.info("{} register producers on success!".format(self.tag))
        ret = self.tx_manager.vote_producers_candidates()
        self.check_result("vote producers", ret)
        Logger.info("{} vote producer on success!".format(self.tag))

        self.get_dpos_votes()

    def check_params(self):
        if self.params.ela_params.number < 3 * self.params.ela_params.crc_number + \
                self.params.ela_params.later_start_number:
            Logger.error("Ela node number should be >= 3 * crc number + later start number , " 
                         "please check your config in the beginning of your test case or config.json, exit...")
            time.sleep(1)
            exit(-1)

    def show_current_next_info(self):
        return self.rpc_manager.show_arbiter_info()

    def reset_config(self, up_config: dict):
        for key in up_config.keys():
            if key is "side":
                if not up_config[key]:
                    self.config["arbiter"]["enable"] = False
                    self.config["did"]["enable"] = False
                    self.config["token"]["enable"] = False
                    self.config["neo"]["enable"] = False
                continue

            if key in self.node_types:
                _config = self.up_config[key]
                for k in _config.keys():
                    self.config[key][k] = _config[k]

    def terminate_all_process(self):
        Logger.info("{} terminal all the process and exit...".format(self.tag))
        self.node_manager.stop_nodes()

    def start_later_nodes(self):
        for node in self.later_nodes:
            node.start()

    def check_result(self, case: str, result: bool):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if result:
            print(current_time + Logger.COLOR_GREEN + " [PASS!] " + Logger.COLOR_END + case + "\n")
        else:
            print(current_time + Logger.COLOR_RED + " [NOT PASS!] " + Logger.COLOR_END + case + "\n")
            self.terminate_all_process()
            exit(0)

    def check_nodes_height(self):
        return self.rpc_manager.check_nodes_height()

    def get_node_public_keys(self, start: int, end: int):
        public_key_list = list()
        for i in range(start, end):
            node = self.node_manager.ela_nodes[i]
            public_key_list.append(node.get_node_public_keys())
        return public_key_list

    def start_stop_nodes(self):
        for node in self.node_manager.ela_nodes:
            if not node.running:
                node.start()

    def get_total_tx_fee(self, transactions: list):
        Logger.debug("{} transactions length: {}".format(self.tag, len(transactions)))
        if len(transactions) == 0:
            return 0
        tx_fee = 0
        for tx in transactions:
            if tx.valid:
                tx_fee += tx.tx_fee

        return tx_fee

    @staticmethod
    def get_inflation_per_year():
        inflation_per_year = 3300 * 10000 * constant.TO_SELA * 4 / 100
        # Logger.debug("{} inflation per year: {}".format(self.tag, inflation_per_year))
        return inflation_per_year

    def get_reward_per_block(self):
        block_generate_interval = 2
        generated_blocks_per_year = 365 * 24 * 60 / block_generate_interval
        inflation_per_year = self.get_inflation_per_year()
        reward_per_block = inflation_per_year / generated_blocks_per_year
        # Logger.debug("{} per block reward: {}".format(self.tag, reward_per_block))
        return reward_per_block

    def check_dpos_income(self, real_income: dict, theory_income: dict):
        if real_income is None or real_income == {}:
            Logger.debug("{} Params real_income is None".format(self.tag))
            return False

        if theory_income is None or theory_income == {}:
            Logger.debug("{} Params theory_income is None".format(self.tag))
            return False

        real_income_keys = real_income.keys()
        theory_income_keys = theory_income.keys()

        if len(real_income_keys) != len(theory_income_keys):
            Logger.debug("{} real income keys is not equal theory income keys".format(self.tag))
            return False

        for key in real_income_keys:
            real = real_income[key]
            theory = theory_income[key]
            result = abs(real - theory) < 10
            if not result:
                return False

        return True

    def get_dpos_theory_income(self, block_num: int, tx_fee: int, dpos_votes: dict):
        Logger.debug("{} block num: {}".format(self.tag, block_num))
        Logger.debug("{} tx fee: {}".format(self.tag, tx_fee))
        dpos_origin_income = math.ceil(self.get_reward_per_block() * 35 / 100) * block_num + (tx_fee * 35 / 100)
        Logger.debug("{} dpos origin income: {}".format(self.tag, dpos_origin_income))
        total_block_confirm_reward = math.floor(dpos_origin_income * 25 / 100)
        total_top_producers_reward = math.floor(dpos_origin_income * 75 / 100)

        Logger.debug("{} income1: {}".format(self.tag, total_block_confirm_reward))
        Logger.debug("{} income2: {}".format(self.tag, total_top_producers_reward))

        current_arbiters = self.rpc_manager.get_arbiter_names("arbiters")
        if not current_arbiters:
            Logger.error("{} get current arbiters info error".format(self.tag))
            return None

        current_candidates = self.rpc_manager.get_arbiter_names("candidates")
        if not current_candidates:
            Logger.error("{} get current candidates info error".format(self.tag))
            return None

        individual_first_reward = math.floor(total_block_confirm_reward / len(current_arbiters))
        total_votes = dpos_votes["total"]
        Logger.debug("dpos total votes: {}".format(total_votes))
        individual_second_reward = math.floor(total_top_producers_reward / total_votes)
        Logger.debug("{} income1 each: {}".format(self.tag, individual_first_reward))
        Logger.debug("{} income2 each: {}".format(self.tag, individual_second_reward))

        theory_incomes = dict()

        # calculate current arbiter rewards
        theory_incomes["CRC-I"] = individual_first_reward * 4
        for node_name in current_arbiters:
            if node_name.startswith("CRC"):
                continue
            theory_incomes[node_name] = individual_first_reward + dpos_votes[node_name] * individual_second_reward

        # calculate current candidates rewards
        for node_name in current_candidates:
            if node_name.startswith("CRC"):
                continue
            theory_incomes[node_name] = dpos_votes[node_name] * individual_second_reward

        Logger.debug("{} theory income: {}".format(self.tag, sorted(theory_incomes.items())))
        return theory_incomes

    def get_dpos_real_income(self, height: int):
        response = rpc.get_block_by_height(height)
        if response is False or not isinstance(response, dict):
            Logger.error("{} rpc response invalid".format(self.tag))
            return None

        # Logger.debug("{} response: {}".format(self.tag, response))
        vout_list = response["tx"][0]["vout"]
        Logger.debug("{} vout list length: {}".format(self.tag, len(vout_list)))
        sum = 0.0
        income_dict = dict()
        for vout in vout_list:
            address = vout["address"]
            if address == self.node_manager.main_foundation_address or address == self.node_manager.main_miner_address:
                continue

            value = float(vout["value"])
            if isinstance(address, str) and address.startswith("8"):
                income_dict["CRC-I"] = value * constant.TO_SELA
            else:
                income_dict[self.node_manager.address_name_dict[address]] = value * constant.TO_SELA
            sum += value

        Logger.debug("{} income dict: {}".format(self.tag, sorted(income_dict.items())))
        Logger.debug("{} dpos votes: {}".format(self.tag, self.dpos_votes_dict))
        return income_dict

    def get_dpos_votes(self):
        list_producers = rpc.list_producers(0, 200)
        if list_producers is False:
            return 0

        total_votes = float(list_producers["totalvotes"])
        # candidates = rpc.get_arbiters_info()["candidates"]
        dpos_votes = dict()

        producers = list_producers["producers"]
        for producer in producers:
            node_pubkey = producer["nodepublickey"]
            dpos_votes[self.node_manager.node_pubkey_name_dict[node_pubkey]] = float(producer["votes"])

        # if after_h2_transactions is not None:
        #     for tx_income in after_h2_transactions:
        #         if tx_income.node_pubkey != "" and tx_income.node_pubkey in candidates:
        #             total_votes -= tx_income.votes
        #             node_name = self.node_manager.node_pubkey_name_dict[tx_income.node_pubkey]
        #             origin_votes = dpos_votes[node_name]
        #             origin_votes -= tx_income.votes
        #             dpos_votes[node_name] = origin_votes

        Logger.debug("{} total votes: {}".format(self.tag, total_votes))
        dpos_votes["total"] = total_votes
        self.dpos_votes_dict = dpos_votes
        return dpos_votes

    def has_dpos_reward(self, height: int):
        response = rpc.get_block_by_height(height)
        if response is False:
            Logger.error("{} rpc response invalid".format(self.tag))
            return False

        # Logger.debug("{} response: {}".format(self.tag, response))
        return len(response["tx"][0]["vout"]) > 2

    @staticmethod
    def get_current_height():
        return rpc.get_block_count() - 1

    @staticmethod
    def discrete_mining_blocks(num: int):
        rpc.discrete_mining(num)

    @staticmethod
    def get_height_times(height_times: dict, current_height: int):
        if current_height not in height_times.keys():
            height_times[current_height] = 1
        else:
            height_times[current_height] += 1
        return height_times[current_height]

    @staticmethod
    def get_producer_state(index: int):
        list_producers = rpc.list_producers(0, 100)
        producers = list_producers["producers"]
        return producers[index]["state"]

    @staticmethod
    def get_current_arbiter_public_keys():
        return rpc.get_arbiters_info()["arbiters"]

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
        self.root_path = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))
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

    def get_node_public_key(self, start: int, end: int):
        public_key_list = list()
        for i in range(start, end):
            node = self.node_manager.ela_nodes[i]
            public_key_list.append(node.get_node_public_key())
        return public_key_list

    def start_stop_nodes(self):
        for node in self.node_manager.ela_nodes:
            if not node.running:
                node.start()

    def get_inflation_per_year(self):
        inflation_per_year = 3300 * 10000 * constant.TO_SELA * 4 / 100
        Logger.debug("{} inflation per year: {}".format(self.tag, inflation_per_year))
        return inflation_per_year

    def get_reward_per_block(self):
        block_generate_interval = 2
        generated_blocks_per_year = 365 * 24 * 60 / block_generate_interval
        inflation_per_year = self.get_inflation_per_year()
        reward_per_block = inflation_per_year / generated_blocks_per_year
        Logger.debug("{} per block reward: {}".format(self.tag, reward_per_block))
        return reward_per_block

    def check_income_distribution(self):
        dpos_origin_income = math.ceil(self.get_reward_per_block() * 35 / 100)
        Logger.debug("{} dpos origin income: {}".format(self.tag, dpos_origin_income))
        income1 = math.floor(dpos_origin_income * 25 / 100)
        income2 = math.floor(dpos_origin_income * 75 / 100)

        Logger.debug("{} income1: {}".format(self.tag, income1))
        Logger.debug("{} income2: {}".format(self.tag, income2))

        income1_each = math.floor(income1 / 12)
        dpos_votes = self.get_dpos_votes()
        total_votes = int(dpos_votes["total"])
        income2_each = math.floor(income2 / total_votes)
        Logger.debug("{} income1 each: {}".format(self.tag, income1_each))
        Logger.debug("{} income2 each: {}".format(self.tag, income2_each))

        theory_incomes = dict()
        theory_incomes["CRC-I"] = income1_each * 4 * 12
        theory_incomes["PRO-005"] = income1_each + dpos_votes["PRO-005"] * income2_each * 12
        theory_incomes["PRO-006"] = income1_each + dpos_votes["PRO-006"] * income2_each * 12
        theory_incomes["PRO-007"] = income1_each + dpos_votes["PRO-007"] * income2_each * 12
        theory_incomes["PRO-008"] = income1_each + dpos_votes["PRO-008"] * income2_each * 12
        theory_incomes["PRO-009"] = income1_each + dpos_votes["PRO-009"] * income2_each * 12
        theory_incomes["PRO-010"] = income1_each + dpos_votes["PRO-010"] * income2_each * 12
        theory_incomes["PRO-011"] = income1_each + dpos_votes["PRO-011"] * income2_each * 12
        theory_incomes["PRO-012"] = income1_each + dpos_votes["PRO-012"] * income2_each * 12
        theory_incomes["PRO-013"] = dpos_votes["PRO-013"] * income2_each * 12
        theory_incomes["PRO-014"] = dpos_votes["PRO-014"] * income2_each * 12
        theory_incomes["PRO-015"] = dpos_votes["PRO-015"] * income2_each * 12
        theory_incomes["PRO-016"] = dpos_votes["PRO-016"] * income2_each * 12
        theory_incomes["PRO-017"] = dpos_votes["PRO-017"] * income2_each * 12
        theory_incomes["PRO-018"] = dpos_votes["PRO-018"] * income2_each * 12
        theory_incomes["PRO-019"] = dpos_votes["PRO-019"] * income2_each * 12
        theory_incomes["PRO-020"] = dpos_votes["PRO-020"] * income2_each * 12

        Logger.debug("{} theory income: {}".format(self.tag, theory_incomes))

    def get_dpos_income(self, height: int):
        response = rpc.get_block_by_height(height)
        if response is False or not isinstance(response, dict):
            Logger.error("{} rpc response invalid".format(self.tag))
            return False

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
                income_dict["CRC-I"] = value
            else:
                income_dict[self.node_manager.address_name_dict[address]] = value
            sum += value

        income_dict["total"] = sum

        Logger.debug("{} income dict: {}".format(self.tag, income_dict))
        Logger.debug("{} dpos votes: {}".format(self.tag, self.dpos_votes_dict))
        return income_dict

    def get_dpos_votes(self):
        list_producers = rpc.list_producers(0, 200)
        if list_producers is False:
            return 0

        total_votes = list_producers["totalvotes"]
        producers = list_producers["producers"]

        dpos_votes = dict()
        for producer in producers:
            owner_pubkey = producer["ownerpublickey"]
            dpos_votes[self.node_manager.owner_pubkey_name_dict[owner_pubkey]] = float(producer["votes"])

        dpos_votes["total"] = float(total_votes)
        self.dpos_votes_dict = dpos_votes
        return dpos_votes

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


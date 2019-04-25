#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 4:59 PM
# author: liteng

import os
import time
import shutil

from src.middle.tools import util
from src.middle.tools import constant
from src.middle.tools.log import Logger

from src.middle.managers.env_manager import EnvManager
from src.middle.managers.service_manager import ServiceManager
from src.middle.managers.keystore_manager import KeyStoreManager


from src.bottom.nodes.ela import ElaNode
from src.bottom.nodes.arbiter import ArbiterNode
from src.bottom.nodes.did import DidNode
from src.bottom.nodes.token import TokenNode
from src.bottom.nodes.neo import NeoNode
from src.bottom.parameters.params import Parameter


class NodeManager(object):

    def __init__(self, params: Parameter, env_manager: EnvManager, service_manager: ServiceManager, keystore_manager: KeyStoreManager):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.params = params
        self.env_manager = env_manager
        self.service_manager = service_manager
        self.keystore_manager = keystore_manager
        self.ela_nodes = []
        self.arbiter_nodes = []
        self.did_nodes = []
        self.token_nodes = []
        self.neo_nodes = []

        self.main_foundation_address = self.keystore_manager.special_key_stores[0].address
        self.side_foundation_address = self.keystore_manager.special_key_stores[1].address
        self.main_miner_address = self.keystore_manager.special_key_stores[2].address
        self.side_miner_address = self.keystore_manager.special_key_stores[3].address
        self.tap_address = self.keystore_manager.special_key_stores[4].address
        self.nodes_dict = {
            "ela": self.ela_nodes,
            "arbiter": self.arbiter_nodes,
            "did": self.did_nodes,
            "token": self.token_nodes,
            "neo": self.neo_nodes
        }

    def deploy_nodes(self):
        ret = False
        if self.params.ela_params.enable:
            ret = self._deploy_nodes("ela", self.params.ela_params.number)
        if self.params.did_params.enable:
            ret = self._deploy_nodes("did", self.params.did_params.number)
        if self.params.token_params.enable:
            ret = self._deploy_nodes("token", self.params.token_params.number)
        if self.params.neo_params.enable:
            ret = self._deploy_nodes("neo", self.params.neo_params.number)

        return ret

    def start_nodes(self):
        if self.params.ela_params.enable:
            for i in range(len(self.ela_nodes)):
                self.ela_nodes[i].start()
                time.sleep(0.5)
            self.service_manager.wait_rpc_ready(self.ela_nodes[0].rpc_port)

        if self.params.did_params.enable:
            for i in range(len(self.did_nodes)):
                self.did_nodes[i].start()
                time.sleep(0.5)
            self.service_manager.wait_rpc_ready(self.did_nodes[0].rpc_port)
            self.create_side_info("did")

        if self.params.token_params.enable:
            for i in range(len(self.token_nodes)):
                self.token_nodes[i].start()
                time.sleep(0.5)
            self.service_manager.wait_rpc_ready(self.token_nodes[0].rpc_port)
            self.create_side_info("token")

        if self.params.arbiter_params.enable:
            if self.params.arbiter_params.enable:
                self._deploy_nodes("arbiter", self.params.arbiter_params.number)
                time.sleep(2)
                self.start_arbiter_nodes()

    def start_arbiter_nodes(self):
        arbiter_node_number = len(self.arbiter_nodes)
        if arbiter_node_number <= 0:
            return False
        for i in range(arbiter_node_number):
            self.arbiter_nodes[i].start()

        return True

    def stop_nodes(self):
        if self.params.ela_params.enable:
            for i in range(len(self.ela_nodes)):
                self.ela_nodes[i].stop()
                time.sleep(0.5)

        if self.params.arbiter_params.enable:
            for i in range(len(self.arbiter_nodes)):
                self.arbiter_nodes[i].stop()
                time.sleep(0.5)

        if self.params.did_params.enable:
            for i in range(len(self.did_nodes)):
                self.did_nodes[i].stop()
                time.sleep(0.5)

        if self.params.token_params.enable:
            for i in range(len(self.token_nodes)):
                self.token_nodes[i].stop()
                time.sleep(0.5)

        if self.params.neo_params.enable:
            for i in range(len(self.token_nodes)):
                self.neo_nodes[i].stop()
                time.sleep(0.5)

    def _init_nodes(self, category: str, config, index: int, cwd_dir: str, ela_type="normal"):

        if category == "ela":
            node = ElaNode(index, config, self.params.ela_params, self.keystore_manager, cwd_dir, ela_type)
        elif category == "arbiter":
            node = ArbiterNode(index, config, self.params.arbiter_params, self.keystore_manager, cwd_dir)
        elif category == "did":
            node = DidNode(index, config, self.params.did_params, self.keystore_manager, cwd_dir)
        elif category == "token":
            node = TokenNode(index, config, self.params.token_params, self.keystore_manager, cwd_dir)
        elif category == "neo":
            node = NeoNode(index, config, self.params.neo_params, cwd_dir)
        else:
            node = None

        return node

    def _deploy_nodes(self, category: str, num: int):
        src_path = os.path.join(self.env_manager.elastos_path, self.env_manager.src_path_dict[category])
        if not os.path.exists(src_path):
            return False
        Logger.debug("{} src_path: {}".format(self.tag, src_path))
        config_path = os.path.join(src_path, "config.json.sample")
        if os.path.exists(config_path):
            Logger.debug("{} config.json will generate from the sample".format(self.tag))
            config_dict = util.read_config_file(config_path)
        else:
            Logger.debug("{} config.json will generate from the default".format(self.tag))
            config_dict = self.env_manager.config_dict[category]

        global ela_type

        for i in range(num+1):
            if category == "ela" and i == 0:
                dest_path = os.path.join(
                    self.env_manager.test_path, category + "_nodes",
                    self.env_manager.current_date_time,
                    "miner"
                )
                ela_type = ElaNode.TYPE_MINER
            elif category == "ela" and i <= self.params.ela_params.crc_number:
                dest_path = os.path.join(
                    self.env_manager.test_path, category + "_nodes",
                    self.env_manager.current_date_time,
                    "crc" + str(i)
                )

                ela_type = ElaNode.TYPE_CRC

            elif category == "ela" and i <= self.params.ela_params.crc_number * 3:
                dest_path = os.path.join(
                    self.env_manager.test_path, category + "_nodes",
                    self.env_manager.current_date_time,
                    "producer" + str(i)
                )
                ela_type = ElaNode.TYPE_PRODUCER
            else:
                if category is not "ela" and i == num:
                    break
                else:
                    ela_type = ElaNode.TYPE_CANDIDATE
                dest_path = os.path.join(
                    self.env_manager.test_path, category + "_nodes",
                    self.env_manager.current_date_time,
                    category + str(i)
                )
            Logger.debug("{} dest_path: {}".format(self.tag, dest_path))
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            shutil.copy(os.path.join(src_path, category), os.path.join(dest_path, category + str(i)))
            node = self._init_nodes(
                category,
                config_dict,
                i,
                dest_path,
                ela_type
            )
            node.reset_config()
            util.write_config_file(node.config, os.path.join(dest_path, "config.json"))
            self.nodes_dict[category].append(node)

            if category == "ela":
                shutil.copy(
                    os.path.join(self.params.root_path, "datas/keystores/owner_keystores", "owner_" + str(i) + ".dat"),
                    os.path.join(dest_path, "owner.dat")
                )

                shutil.copy(
                    os.path.join(self.params.root_path, "datas/keystores/node_keystores", "node_" + str(i) + ".dat"),
                    os.path.join(dest_path, "keystore.dat")
                )

            if i == 0 and category == "ela":
                shutil.copy(
                    os.path.join(self.params.root_path, "datas/keystores/special/main_foundation.dat"),
                    os.path.join(dest_path, "foundation.dat")
                )

                shutil.copy(
                    os.path.join(self.params.root_path, "datas/keystores/special/main_miner.dat"),
                    os.path.join(dest_path, "miner.dat")
                )

                # shutil.copy(
                #     os.path.join(self.params.root_path, "datas/keystores/special/main_tap.dat"),
                #     os.path.join(dest_path, "tap.dat")
                # )

            if category == "arbiter":
                if i <= 4:
                    shutil.copy(
                        os.path.join(
                            self.params.root_path,
                            "datas/keystores/arbiter_keystores/origin_arbiter_" + str(i) +".dat"),
                        os.path.join(dest_path, "keystore.dat")
                    )
                else:
                    shutil.copy(
                        os.path.join(
                            self.params.root_path,
                            "datas/keystores/arbiter_keystores/crc_arbiter_" + str(i - 5 + 1) + ".dat"),
                        os.path.join(dest_path, "keystore.dat")
                    )

        return True

    def create_side_info(self, node_type: str):
        self.params.arbiter_params.side_info[node_type] = dict()
        side_port = util.reset_port(0, node_type, "json_port")
        side_chain_genesis_hash = self.service_manager.rpc.get_block_hash_by_height(0, side_port)
        Logger.debug("{} {} genesis hash: {}".format(
            self.tag,
            node_type,
            self.params.arbiter_params.side_chain_genesis_hash
            )
        )

        recharge_address = self.service_manager.jar_service.gen_genesis_address(
            block_hash=side_chain_genesis_hash
        )
        self.params.arbiter_params.recharge_address = recharge_address
        self.params.arbiter_params.withdraw_address = "0000000000000000000000000000000000"
        self.params.arbiter_params.side_chain_genesis_hash = side_chain_genesis_hash

        Logger.info("{} recharge address: {}".format(self.tag, self.params.arbiter_params.recharge_address))
        Logger.info("{} withdraw address: {}".format(self.tag, self.params.arbiter_params.withdraw_address))

        self.params.arbiter_params.side_info[node_type][constant.SIDE_GENESIS_ADDRESS] = side_chain_genesis_hash
        self.params.arbiter_params.side_info[node_type][constant.SIDE_RECHARGE_ADDRESS] = recharge_address




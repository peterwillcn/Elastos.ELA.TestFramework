#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 11:32 AM
# author: liteng


import time

from src.tools.log import Logger
from src.tools import constant
from src.tools import util
from src.control.control import Controller

from src.core.tx.payload.function_code import FunctionCode
from src.core.tx.payload.neo_contract_deploy import NeoDeployContract
from src.core.tx.payload.neo_contract_invoke import NeoInvokeContract
from src.core.services import rpc


config = {
    "ela": {
        "number": 12,
        "crc_number": 4,
        "later_start_number": 0,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": True,
    "arbiter": {
        "enable": True,
        "number": 4,
        "pow_chain": True,
        "print_level": 0
    },
    "neo": {
        "enable": True,
        "number": 4,
        "instant_block": True
    },
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.ready_for_dpos()

    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]
    side_port = controller.node_manager.neo_nodes[0].rpc_port

    # side account config
    side_account1 = controller.keystore_manager.special_accounts[10]
    side_account2 = controller.keystore_manager.special_accounts[11]

    global test_case
    test_case = "test neo deploy contract"
    current_height = controller.get_current_height()

    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global before_h1
    before_h1 = True

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))

        if times >= 1000:
            result = False
            break

        if current_height > h2 + 2:

            test_case = "cross chain recharge neo side account1"
            Logger.info("### Testing {} ###".format(test_case))
            result = controller.tx_manager.cross_chain_transaction("neo", True, side_account1.address())
            controller.check_result(test_case, result)

            controller.discrete_mining_blocks(1)
            time.sleep(2)
            #
            # test_case = "cross chain recharge neo side account2"
            # Logger.info("### Testing {} ###".format(test_case))
            # result = controller.tx_manager.cross_chain_transaction("neo", True, side_account2.address())
            # controller.check_result(test_case, result)
            #
            # controller.discrete_mining_blocks(1)
            # time.sleep(2)

            before_deploy_balance = controller.get_address_balance(side_account2.address(), side_port)
            # code = "5bc56b6c766b00527ac46c766b51527ac4616168164e656f2e52756e74696d652e47657454726967676572609c6c766b52527ac46c766b52c3647501616c766b00c3066465706c6f79876c766b53527ac46c766b53c36414006161e001007d016c766b54527ac4626a016c766b00c3046e616d65876c766b55527ac46c766b55c36414006161e0010049026c766b54527ac4623f016c766b00c30673796d626f6c876c766b56527ac46c766b56c36414006161e0010095026c766b54527ac46212016c766b00c30b746f74616c537570706c79876c766b57527ac46c766b57c36414006161e0010007026c766b54527ac462e0006c766b00c3087472616e73666572876c766b58527ac46c766b58c3642b00616c766b51c300c36c766b51c351c36c766b51c352c3615272e00103b0026c766b54527ac4629a006c766b00c30962616c616e63654f66876c766b59527ac46c766b59c3641b00616c766b51c300c361e00101ff016c766b54527ac46263006c766b00c307646563696d616c876c766b5a527ac46c766b5ac36414006161e0010033026c766b54527ac462350004747275656c766b54527ac4622600186e6f74206170706c69636174696f6e20636f6e74726163746c766b54527ac46203006c766b54c3616c756655c56b616115215d4ab7ebc27ed8c9d7a5f7e33b08b8ca93af07a66168184e656f2e52756e74696d652e436865636b5769746e657373009c6c766b53527ac46c766b53c3640f0061006c766b54527ac4629e000700c06e31d910016c766b00527ac46168164e656f2e53746f726167652e476574436f6e74657874056173736574617ce001020c036c766b51527ac403c0c62d6c766b52527ac46c766b51c30b746f74616c537570706c796c766b52c3615272e000030603616c766b51c36115215d4ab7ebc27ed8c9d7a5f7e33b08b8ca93af07a66c766b00c3615272e00003340361516c766b54527ac46203006c766b54c3616c756651c56b61057a636f696e6c766b00527ac46203006c766b00c3616c756652c56b616168164e656f2e53746f726167652e476574436f6e74657874056173736574617ce0010256026c766b00527ac46c766b00c30b746f74616c537570706c79617ce0010211036c766b51527ac46203006c766b51c3616c756651c56b61017a6c766b00527ac46203006c766b00c3616c756653c56b6c766b00527ac4616168164e656f2e53746f726167652e476574436f6e74657874056173736574617ce00102da016c766b51527ac46c766b51c36c766b00c3617ce00102e7020400e1f505966c766b52527ac46203006c766b52c3616c756651c56b61586c766b00527ac46203006c766b00c3616c75665ac56b6c766b00527ac46c766b51527ac46c766b52527ac4616c766b52c3009f6c766b56527ac46c766b56c3640f0061006c766b57527ac4624d016c766b00c36168184e656f2e52756e74696d652e436865636b5769746e657373009c6c766b58527ac46c766b58c3640f0061006c766b57527ac46210010400e1f5056c766b52c3956a52527ac46168164e656f2e53746f726167652e476574436f6e74657874056173736574617ce00102e3006c766b53527ac46c766b53c36c766b00c3617ce00102f0016c766b54527ac46c766b54c36c766b52c39f6c766b59527ac46c766b59c3640f0061006c766b57527ac46295006c766b53c36c766b00c36c766b54c36c766b52c394615272e000030301616c766b53c36c766b51c3617ce0010294016c766b55527ac46c766b53c36c766b51c36c766b55c36c766b52c393615272e00003cd0061616c766b00c36c766b51c36c766b52c3615272087472616e7366657254c168124e656f2e52756e74696d652e4e6f7469667961516c766b57527ac46203006c766b57c3616c756652c56b6c766b00527ac46c766b51527ac46152c5766c766b00c3007cc4766c766b51c3517cc4616c756654c56b6c766b00527ac46c766b51527ac46c766b52527ac46c766b00c351c301007e6c766b51c37e6c766b53527ac46c766b00c300c36c766b53c36c766b52c3615272680f4e656f2e53746f726167652e507574616c756654c56b6c766b00527ac46c766b51527ac46c766b52527ac46c766b00c351c301007e6c766b51c37e6c766b53527ac46c766b00c300c36c766b53c36c766b52c3615272680f4e656f2e53746f726167652e507574616c756653c56b6c766b00527ac46c766b51527ac46c766b00c351c301007e6c766b51c37e6c766b52527ac46c766b00c300c36c766b52c3617c680f4e656f2e53746f726167652e476574616c756653c56b6c766b00527ac46c766b51527ac46c766b00c351c301007e6c766b51c37e6c766b52527ac46c766b00c300c36c766b52c3617c680f4e656f2e53746f726167652e476574616c7566ab"
            code = util.read_avm_file("./datas/code.avm")
            Logger.info("code: {}".format(code))
            function_code = FunctionCode(
                code=code,
                params_type=[FunctionCode.TYPE_STRING, FunctionCode.TYPE_ARRAY],
                return_type=FunctionCode.TYPE_OBJECT,
            )

            payload = NeoDeployContract(
                function_code=function_code,
                name="xiaobin",
                code_version="v0.0.1",
                author="xiaobin",
                email="xiaobin@163.com",
                description="simple neo contract",
                program_hash=bytes.fromhex(side_account1.program_hash()),
                gas=int(500 * constant.TO_SELA),
            )

            ret = controller.tx_manager.deploy_neo_contract(
                input_private_key=side_account1.private_key(),
                output_addresses=[side_account2.address()],
                payload=payload,
                amount=1 * constant.TO_SELA,
                rpc_port=side_port,
            )

            controller.check_result("deploy neo contract test", ret)
            controller.mining_side_blocks(side_port, 6)

            after_deploy_balance = controller.get_address_balance(side_account2.address(), side_port)

            Logger.info("before deploy contract side account2 balance: {}".format(before_deploy_balance))
            Logger.info("after deploy contract side account2 balance: {}".format(after_deploy_balance))

            controller.discrete_mining_blocks(1)
            time.sleep(1)
            controller.discrete_mining_blocks(1)
            time.sleep(1)

            Logger.debug("current height: {}".format(controller.get_current_height()))
            test_case = "invoke neo contract function deploy test"
            Logger.info("begin {}".format(test_case))

            contract_params = {FunctionCode.TYPE_STRING: "deploy"}

            invoke_payload = NeoInvokeContract(
                params=contract_params,
                program_hash=bytes.fromhex(side_account1.program_hash()),
                gas=0,
            )

            ret = controller.tx_manager.invoke_neo_contract(
                input_private_key=side_account1.private_key(),
                output_addresses=[side_account2.address()],
                payload=invoke_payload,
                amount=int(1 * constant.TO_SELA),
                rpc_port=side_port,
            )

            controller.check_result(test_case, ret)
            controller.mining_side_blocks(side_port, 6)
            balance3 = controller.get_address_balance(side_account2.address(), side_port)
            Logger.info("after invoke transaction, side account2 balance is {}".format(balance3))
            response = rpc.invoke_function(
                operation="balanceOf",
                param={"type": "Hash160", "value": "ab555802d53185891cc51bdac7bcc8e78c3053d7"},
                return_type="Integer",
                port=side_port,
            )

            Logger.info("after invoke deploy function, result: {}".format(response))
            result = int(response["result"]) == 3000000
            controller.check_result("invoke deploy balance test", result)

            test_case = "invoke neo contract function transfer test"
            transfer_account = controller.keystore_manager.sub1_accounts[0]
            contract_params2 = {FunctionCode.TYPE_STRING: "transfer", FunctionCode.TYPE_ARRAY: [{
                FunctionCode.TYPE_HASH160: "ab555802d53185891cc51bdac7bcc8e78c3053d7",
                FunctionCode.TYPE_HASH160_2: transfer_account.program_hash(),
                FunctionCode.TYPE_INTEGER: 1000000,
            }]}
            invoke_payload2 = NeoInvokeContract(
                params=contract_params2,
                program_hash=bytes.fromhex(side_account1.program_hash()),
                gas=0,
            )

            ret = controller.tx_manager.invoke_neo_contract(
                input_private_key=side_account1.private_key(),
                output_addresses=[side_account2.address()],
                payload=invoke_payload2,
                amount=int(1 * constant.TO_SELA),
                rpc_port=side_port,
            )

            controller.check_result(test_case, ret)
            controller.mining_side_blocks(side_port, 6)
            balance4 = controller.get_address_balance(side_account2.address(), side_port)
            Logger.info("after invoke transaction, side account2 balance is {}".format(balance4))

            result = rpc.invoke_function(
                operation="balanceOf",
                param={"type": "Hash160", "value": transfer_account.program_hash()},
                return_type="Integer",
            )

            Logger.info("after transfer contract, result: {}".format(result))

            transfer_account_balance = result["result"]
            result = int(transfer_account_balance) == 1000000
            controller.check_result("invoke transfer balance test", result)
            Logger.debug("Start later nodes and check all nodes height")
            controller.start_later_nodes()
            result = controller.check_nodes_height()
            controller.check_result("check all nodes height", result)
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.check_result(test_case, result)
    controller.terminate_all_process(result)


if __name__ == '__main__':

    times = config["times"]
    if times > 1:
        config["stop"] = True

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)


#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:40 AM
# author: liteng

from src.tools import util, constant


class ElaParams(object):

    def __init__(self, config: dict):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.magic = constant.CONFIG_MAGIC_ELA
        self.enable = config["enable"]
        self.arbiter_enable = config["arbiter_enable"]
        self.number = config["number"]
        self.password = config["password"]
        self.crc_number = config["crc_number"]
        self.active_net = config["active_net"]
        self.later_start_number = config["later_start_number"]
        self.disable_dns = config["disable_dns"]
        self.ip_address = config["ip_address"]
        self.print_level = config["print_level"]
        self.auto_mining = config["auto_mining"]
        self.instant_block = config["instant_block"]
        self.pre_connect_offset = config["pre_connect_offset"]
        self.check_address_height = config["check_address_height"]
        self.vote_start_height = config["vote_start_height"]
        self.crc_dpos_height = config["crc_dpos_height"]
        self.public_dpos_height = config["public_dpos_height"]
        self.max_inactivate_rounds = config["max_inactivate_rounds"]
        self.inactive_penalty = config["inactive_penalty"]
        self.emergency_inactive_penalty = config["emergency_inactive_penalty"]
        self.cr_check_reward_height = config["cr_check_reward_height"]
        self.cr_voting_start_height = config["cr_voting_start_height"]
        self.cr_committee_start_height = config["cr_committee_start_height"]
        self.member_count = config["member_count"]
        self.cr_voting_period = config["cr_voting_period"]
        self.cr_duty_period = config["cr_duty_period"]
        self.max_node_per_host = config["max_node_per_host"]
        self.voting_period = config["voting_period"]
        self.duty_period = config["duty_period"]
        self.deposit_lockup_blocks = config["deposit_lockup_blocks"]
        self.crc_appropriate_percentage = config["crc_appropriate_percentage"]
        self.max_committee_proposal_count = config["max_committee_proposal_count"]
        self.max_proposal_tracking_count = config["max_proposal_tracking_count"]
        self.proposal_cr_voting_period = config["proposal_cr_voting_period"]
        self.proposal_public_voting_period = config["proposal_public_voting_period"]
        self.cr_agreement_count = config["cr_agreement_count"]
        self.voter_reject_percentage = config["voter_reject_percentage"]
        self.register_cr_by_did_height = config["register_cr_by_did_height"]
        self.cr_claim_dpos_node_start_height = config["cr_claim_dpos_node_start_height"]

#!/usr/bin/env python3
from .constants import CAPTCHATools


def test_amihuman(eosio_testnet):
    account = eosio_testnet.new_account()

    ec, out = eosio_testnet.push_action(
        CAPTCHATools.contract_name,
        'amihuman',
        [account],
        f'{account}@active'
    )
    assert ec == 0
    for action_trace in out['processed']['action_traces']:
    	if 'console' in action_trace:
    		print(action_trace['console'])
    assert False
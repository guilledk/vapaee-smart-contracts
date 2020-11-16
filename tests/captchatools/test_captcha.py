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
    output = ''
    for action_trace in out['processed']['action_traces']:
    	if 'console' in action_trace:
    		output += action_trace['console']

    for y in range(CAPTCHATools.CHALLANGE_HEIGHT):
    	for x in range(CAPTCHATools.CHALLANGE_WIDTH):
    		print(output[(y * CAPTCHATools.CHALLANGE_WIDTH) + x], end='')
    	print()

    assert False
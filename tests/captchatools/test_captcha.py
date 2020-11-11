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
    assert False
#!/usr/bin/env python3
import secrets

from hashlib import sha256

from .constants import RNGProvider


def test_getnum(eosio_testnet):
    account = eosio_testnet.new_account()
    hasha = sha256(b'test').hexdigest()

    ec, out = eosio_testnet.push_action(
        RNGProvider.contract_name,
        'requestnum',
        [account, hasha],
        f'{account}@active'
    )
    assert ec == 0

    requests = eosio_testnet.get_table(
        RNGProvider.contract_name,
        RNGProvider.contract_name,
        'rngrequests'
    )

    row = next(
        (req for req in requests['rows'] if req['hash_a'] == hasha),
        None
    )

    assert row is not None

    hashb = secrets.token_hex(32)

    ec, out = eosio_testnet.push_action(
        RNGProvider.contract_name,
        'fillrequest',
        [hashb],
        f'{RNGProvider.contract_name}@active'
    )
    assert ec == 0

    requests = eosio_testnet.get_table(
        RNGProvider.contract_name,
        RNGProvider.contract_name,
        'rngrequests'
    )

    row = next(
        (req for req in requests['rows'] if req['hash_b'] == hashb),
        None
    )

    assert row is not None
    assert row['hash_a'] == hasha
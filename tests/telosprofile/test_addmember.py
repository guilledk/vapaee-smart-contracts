#!/usr/bin/env python3

from .constants import TelosProfile


def test_addmember(eosio_testnet):
    creat_account, creat_alias = TelosProfile.new_profile(eosio_testnet)
    user_account, user_alias = TelosProfile.new_profile(eosio_testnet)
    org_name = TelosProfile.add_organization(eosio_testnet, creat_account, creat_alias)

    TelosProfile.add_member(
        eosio_testnet,
        creat_account,
        creat_alias,
        org_name,
        user_alias
    )

    user_profile = TelosProfile.get_profile(eosio_testnet, user_alias)

    org = TelosProfile.get_organization(eosio_testnet, org_name) 

    members = eosio_testnet.get_table(
        TelosProfile.contract_name,
        str(org['id']),
        'members'
    )

    member = next((
        row for row in members['rows']
        if row['profile_id'] == user_profile['id']),
        None
    )

    assert member is not None


def test_addmember_profile_not_found_admin(eosio_testnet):
    ec, out = eosio_testnet.push_action(
        TelosProfile.contract_name,
        'addmember',
        ['not an alias', 'not an org', 'not an alias'],
        'eosio@active'
    )
    assert ec == 1
    assert 'profile not found (admin)' in out


def test_addmember_profile_not_found_user(eosio_testnet):
    creat_account, creat_alias = TelosProfile.new_profile(eosio_testnet)
    
    ec, out = eosio_testnet.push_action(
        TelosProfile.contract_name,
        'addmember',
        [creat_alias, 'not an org', 'not an alias'],
        'eosio@active'
    )
    assert ec == 1
    assert 'profile not found (user)' in out


def test_addmember_not_authorized_sig(eosio_testnet):
    creat_account, creat_alias = TelosProfile.new_profile(eosio_testnet)
    user_account, user_alias = TelosProfile.new_profile(eosio_testnet)
    
    ec, out = eosio_testnet.push_action(
        TelosProfile.contract_name,
        'addmember',
        [creat_alias, 'not an org', user_alias],
        'eosio@active'
    )
    assert ec == 1
    assert 'not authorized (sig)' in out


def test_addmember_organization_not_found(eosio_testnet):
    creat_account, creat_alias = TelosProfile.new_profile(eosio_testnet)
    user_account, user_alias = TelosProfile.new_profile(eosio_testnet)
    
    ec, out = eosio_testnet.push_action(
        TelosProfile.contract_name,
        'addmember',
        [creat_alias, 'not an org', user_alias],
        f'{creat_account}@active'
    )
    assert ec == 1
    assert 'organization not found' in out


def test_addmember_not_a_member_admin(eosio_testnet):
    creat_account, creat_alias = TelosProfile.new_profile(eosio_testnet)
    user_account, user_alias = TelosProfile.new_profile(eosio_testnet)
    org_name = TelosProfile.add_organization(eosio_testnet, creat_account, creat_alias)

    bad_account, bad_alias = TelosProfile.new_profile(eosio_testnet)

    ec, out = eosio_testnet.push_action(
        TelosProfile.contract_name,
        'addmember',
        [bad_alias, org_name, user_alias],
        f'{bad_account}@active'
    )
    assert ec == 1
    assert 'not a member (admin)' in out


def test_addmember_not_authorized_org(eosio_testnet):
    creat_account, creat_alias = TelosProfile.new_profile(eosio_testnet)
    user_account, user_alias = TelosProfile.new_profile(eosio_testnet)
    org_name = TelosProfile.add_organization(eosio_testnet, creat_account, creat_alias)

    TelosProfile.add_member(
        eosio_testnet,
        creat_account,
        creat_alias,
        org_name,
        user_alias
    )

    bad_account, bad_alias = TelosProfile.new_profile(eosio_testnet)

    ec, out = eosio_testnet.push_action(
        TelosProfile.contract_name,
        'addmember',
        [user_alias, org_name, bad_alias],
        f'{user_account}@active'
    )
    assert ec == 1
    assert 'not authorized (org)' in out


def test_addmember_already_a_member(eosio_testnet):
    creat_account, creat_alias = TelosProfile.new_profile(eosio_testnet)
    user_account, user_alias = TelosProfile.new_profile(eosio_testnet)
    org_name = TelosProfile.add_organization(eosio_testnet, creat_account, creat_alias)

    TelosProfile.add_member(
        eosio_testnet,
        creat_account,
        creat_alias,
        org_name,
        user_alias
    )

    ec, out = eosio_testnet.push_action(
        TelosProfile.contract_name,
        'addmember',
        [creat_alias, org_name, user_alias],
        f'{creat_account}@active'
    )
    assert ec == 1
    assert 'already a member' in out

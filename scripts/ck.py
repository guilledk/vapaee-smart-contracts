#!/usr/bin/env python3


"""
helpful script to check for action name repeats between contracts,
this is useful for fixing the dreadful error:

You successfully re-deployed the contract code, but when you broadcast one of 
the contracts methods to the blockchain you get below error message:

```
Error 3050004: eosio_assert_code assertion failure
Error Details:
assertion failure with error code: 8000000000000000000
```

Possible solution: If you are referencing a smart contract from another smart
contract and each of them have at least one action with the same name you will
experience the above error when sending to the blockchain one of those actions,
so what you have to do is to make sure the action names between those two
contracts are not common.

source: https://developers.eos.io/manuals/eosio.cdt/v1.7/troubleshooting/index
"""

import json

from pathlib import Path


abis = {}

for abi_path in Path('contracts').glob('**/*.abi'):
    with open(abi_path, 'r') as abi_file:
        abi = json.loads(abi_file.read())

        contract_name = abi_path.name
        abis[contract_name] = abi


for contract, abi in abis.items():
    print(f'{contract}:')

    print('\t[[eosio::action]]:')
    for action in [a['name'] for a in abi['actions']]:
        for sub_contract, sub_abi in abis.items():
            if sub_contract == contract:
                continue

            if action in [a['name'] for a in sub_abi['actions']]:
                print(f'\t\t - {action} in {sub_contract}')

    print('\t[[eosio::table]]:')
    for table in [t['name'] for t in abi['tables']]:
        for sub_contract, sub_abi in abis.items():
            if sub_contract == contract:
                continue

            if table in [t['name'] for t in sub_abi['tables']]:
                print(f'\t\t - {table} in {sub_contract}')




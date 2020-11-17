#pragma once
#include <vapaee/base/base.hpp>
#include <vapaee/rng/tables/rng.hpp>

namespace vapaee {
    namespace rng {
        namespace core {

            void action_requestnum(name user, uint64_t id, checksum256 hash) {
            	require_auth(user);

            	rngrequests requests(contract, contract.value);
            	requests.emplace(user, [&]( auto& row ) {
            		row.id = id;
            		row.hash_a = hash;
            	});
            }

            void action_fillrequest(uint64_t id, checksum256 hash) {
            	require_auth(contract);

            	rngrequests requests(contract, contract.value);
            	auto iter = requests.find(id);
            	check(iter != requests.end(), "request not found");
            	requests.modify(iter, contract, [&]( auto& row ) {
            		row.hash_b = hash;
            	});
            }

        };     
    };
};

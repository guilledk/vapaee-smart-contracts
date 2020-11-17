#pragma once
#include <vapaee/base/base.hpp>
#include <vapaee/rng/modules/core.hpp>

using namespace eosio;
using namespace std;

namespace vapaee {
    using namespace rng;

    CONTRACT rngprovider : public eosio::contract {

        public:
            rngprovider(name receiver, name code, datastream<const char*> ds) :
	            contract(receiver, code, ds),
	            request_index_obj(receiver, receiver.value)
	            { }

#include <vapaee/rng/tables/rng.hpp>

            request_index request_index_obj;

            uint64_t next_request_key() {
	            auto state = request_index_obj.get_or_create(get_self(), numericstate{0});
	            uint64_t counter = state.counter;
	            request_index_obj.set(numericstate{counter + 1}, get_self());
	            return counter;
	        }

	        ACTION requestnum(name user, checksum256 hash) {
	        	core::action_requestnum(user, next_request_key(), hash);
	        }

	        ACTION fillrequest(checksum256 hash) {
	        	core::action_fillrequest(request_index_obj.get().counter - 1, hash);
	        }

    };

}; // eosio namespace
#include <vapaee/base/base.hpp>

TABLE rngrequest {
	uint64_t id;
	checksum256 hash_a;
	checksum256 hash_b;

	uint64_t primary_key() const { return id; }
};

typedef eosio::multi_index<"rngrequests"_n, rngrequest> rngrequests;

typedef eosio::singleton<"lastrequest"_n, numericstate> request_index;
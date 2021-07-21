#include "./_aux.hpp"


// scope: owner
struct [[eosio::table]] deposits_table {
    asset amount;
    uint64_t primary_key() const { return amount.symbol.code().raw(); }
};

typedef eosio::multi_index< "deposits"_n, deposits_table > deposits;
        

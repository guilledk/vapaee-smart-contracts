#include "./_aux.hpp"


// scope: token_symbol
struct [[eosio::table]] tokenevents_table {
    name event;
    name receptor;
    uint64_t primary_key() const { return event.value; }
};

typedef eosio::multi_index< "tokenevents"_n, tokenevents_table > tokenevents;


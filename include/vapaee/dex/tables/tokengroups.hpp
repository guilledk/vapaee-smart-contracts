#include "./_aux.hpp"

        
// scope: contract
struct [[eosio::table]] tokengroups_table {
    uint64_t id;
    name admin;       // whoever register this group
    string title;
    string website;
    string brief;
    string banner;    // big wide image
    string thumbnail; // small image
    vector<symbol_code> currencies;
    uint64_t primary_key() const { return id; }
};

typedef eosio::multi_index< "tokengroups"_n, tokengroups_table> tokengroups;
        

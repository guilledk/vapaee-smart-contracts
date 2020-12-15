#pragma once
#include <vapaee/base/base.hpp>
#include <vapaee/tprofile/tables.hpp>

namespace vapaee {
    namespace tprofile {
        namespace prof {

            template <typename T>
            name signed_by_any_owner(T& prof_it) {
                print("pid:", prof_it->id, "\n");
                for(auto owner : prof_it->owners) {
                    if (has_auth(owner))
                        return owner;
                }
                return "null"_n;
            }

            auto get_profile(string alias) {
                 profiles prof_table(contract, contract.value);

                auto alias_index = prof_table.get_index<"alias"_n>();
                auto prof_it = alias_index.find(vapaee::utils::hash(alias));
                optional<decltype(prof_it)> option;
                if (prof_it != alias_index.end())
                    option = make_optional(prof_it);

                return option;
            }

            void action_add_profile(name owner, string alias) {
                require_auth(owner);

                check_empty(get_profile(alias), "identical profile exists");

                profiles prof_table(contract, contract.value);
                prof_table.emplace(owner, [&](auto& row) {
                    row.id = prof_table.available_primary_key();
                    row.owners.push_back(owner);
                    row.alias = alias;
                    row.points = 1;
                });
            }

            void action_chg_profile(string old_alias, string new_alias) {
                auto prof_it = check_value(get_profile(old_alias), "profile not found");

                name owner = signed_by_any_owner(prof_it);
                check(owner != "null"_n, "not authorized");

                check_empty(get_profile(new_alias), "identical profile exists");
  
                profiles prof_table(contract, contract.value);
                auto alias_index = prof_table.get_index<"alias"_n>();
                alias_index.modify(prof_it, owner, [&](auto& row) {
                    row.alias = new_alias;
                });
            }

            void action_update_points(string alias) {
                profiles prof_table(contract, contract.value);

                auto alias_index = prof_table.get_index<"alias"_n>();
                auto profile_iter = alias_index.find(vapaee::utils::hash(alias));
                check(profile_iter != alias_index.end(), "profile not found");

                /*
                    points calculation

                    platform_weighted_sum = [
                        total_platform_profile_score * platform_global_count
                        for platform in platforms
                    ]

                    points = 1 + floor(
                        (platform_weighted_sum) / total_platforms_global_count
                    )
                */

                // save user points in each platform to an array indexed by platform id
                platforms plat_table(contract, contract.value);

                uint64_t platform_count = plat_table.available_primary_key();
                uint64_t profile_totals[platform_count];

                links link_table(contract, profile_iter->id);
                for(auto link_iter : link_table)
                    profile_totals[link_iter.platform_id] = link_iter.points;

                // iterate over platforms and perform weighted sum, also save total link amount
                uint64_t platforms_total_count = 0;
                uint64_t weighted_sum = 0;

                for(auto plat_iter : plat_table) {
                    weighted_sum += profile_totals[plat_iter.id] * plat_iter.counter;
                    platforms_total_count += plat_iter.counter;
                }

                // finally update points
                // there shouldn't be any ram deltas
                alias_index.modify(profile_iter, contract, [&](auto& row) {
                    row.points = 1 + floor((float)(weighted_sum) / (float)(platforms_total_count));
                    row.kyclevel = floor(log2(row.points));
                });

            }

        };     
    };
};

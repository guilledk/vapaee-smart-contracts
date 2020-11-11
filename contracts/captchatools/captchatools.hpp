#pragma once
#include <vapaee/base/base.hpp>
#include <vapaee/captcha/modules/core.hpp>

using namespace eosio;
using namespace std;

namespace vapaee {
    using namespace captcha;

    CONTRACT captchatools : public eosio::contract {

        public:
            using contract::contract;

            ACTION amihuman(name user) {
                core::action_am_i_human(user);
            }

    };

}; // eosio namespace
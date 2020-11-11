#pragma once
#include <vapaee/base/base.hpp>
#include <vapaee/captcha/font_matrix.h>

namespace vapaee {
    namespace captcha {
        namespace core {

        	void action_am_i_human(name user) {
        		require_auth(user);

        		uint64_t seed = current_time_point().time_since_epoch().count() + user.value;

        		print(vapaee::utils::rand_range(seed, FONT_MATRIX_SIZE));
        	}

        };     
    };
};

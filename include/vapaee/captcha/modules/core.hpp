#pragma once
#include <vapaee/base/base.hpp>
#include <vapaee/captcha/font_matrix.h>
#include <vapaee/captcha/challenge.hpp>

namespace vapaee {
    namespace captcha {
        namespace core {

            void glyph_cpy(uint8_t char_id, std::string &target, uint8_t x, uint8_t y) {
                uint32_t chunk_index = font_jmp_table[char_id];
                uint32_t glyph_index = 0;
                while(font_matrix[chunk_index].amount != 0) {
                    for (int i = 0; i < font_matrix[chunk_index].amount; i++) {
                        uint32_t y_offset = glyph_index / GLYPH_TILE_SIZE;
                        uint32_t x_offset = glyph_index % GLYPH_TILE_SIZE;
                        if (font_matrix[chunk_index].value == 1)
                            target[((y + y_offset) * CHALLANGE_WIDTH) + x + x_offset] = '#';
                        glyph_index++;
                    }
                    chunk_index++;
                }
            }

        	void action_am_i_human(name user) {
        		require_auth(user);

                std::string render(CHALLANGE_WIDTH * CHALLANGE_HEIGHT, ' ');
                uint8_t current_x_pos = 0;
                uint8_t current_y_pos = (CHALLANGE_HEIGHT / 2) - (GLYPH_TILE_SIZE / 2);
                for (int i = 0; i < CHALLENGE_CHARS; i++) {
                    glyph_cpy(i + 1, render, current_x_pos, current_y_pos);
                    current_x_pos += GLYPH_TILE_SIZE + 1;
                }
                print(render);
        	}

        };     
    };
};

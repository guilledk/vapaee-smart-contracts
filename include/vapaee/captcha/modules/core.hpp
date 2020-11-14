#pragma once
#include <vapaee/base/base.hpp>
#include <vapaee/captcha/font_matrix.h>
#include <vapaee/captcha/challenge.hpp>

#define ASCII_ZERO 48

namespace vapaee {
    namespace captcha {
        namespace core {

            void glyph_cpy(uint8_t char_id, uint8_t* target, uint8_t x, uint8_t y) {
                uint8_t chunk_index = font_jmp_table[char_id];
                print("gcpy[", char_id, "]: ", x, ", ", y, "->", chunk_index, "\n");
                uint8_t glyph_index = 0;
                while(font_matrix[chunk_index].amount != 0) {
                    for (int i = 0; i < font_matrix[chunk_index].amount; i++) {
                        uint8_t y_offset = glyph_index / GLYPH_TILE_SIZE;
                        uint8_t x_offset = glyph_index % GLYPH_TILE_SIZE;
                        target[((y + y_offset) * CHALLANGE_HEIGHT) + x_offset + x] = font_matrix[chunk_index].value;
                        glyph_index++;
                    }
                    chunk_index++;
                }
            }

        	void action_am_i_human(name user) {
        		require_auth(user);

        		uint64_t seed = current_time_point().time_since_epoch().count() + user.value;

                uint8_t* challange = new uint8_t[CHALLANGE_WIDTH * CHALLANGE_HEIGHT];
                uint8_t current_x_pos = 0;
                uint8_t current_y_pos = (CHALLANGE_HEIGHT / 2) - (GLYPH_TILE_SIZE / 2);
                for (int i = 1; i < CHALLENGE_CHARS + 1; i++) {
                    glyph_cpy(i, challange, current_x_pos, current_y_pos);
                    current_x_pos += GLYPH_TILE_SIZE;
                }

                std::string render;
                for (int y = 0; y < CHALLANGE_HEIGHT; y++) {
                    for (int x = 0; x < CHALLANGE_WIDTH; x++) {
                        render += (char)(challange[(y * CHALLANGE_HEIGHT) + x] + ASCII_ZERO);
                    }
                    render += '\n';
                }
                print(render);
        	}

        };     
    };
};

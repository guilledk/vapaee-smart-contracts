#pragma once
#include <vapaee/base/base.hpp>
#include <vapaee/captcha/font_matrix.h>
#include <vapaee/captcha/challenge.hpp>

#define ASCII_ZERO 48

namespace vapaee {
    namespace captcha {
        namespace core {

            void glyph_cpy(glyph_chunk* chunks, uint8_t** target, uint8_t x, uint8_t y) {
                uint8_t chunk_index = 0;
                uint8_t glyph_index = 0;
                while((chunk_index < GLYPH_DATA_SIZE) && (chunks[chunk_index].value != GLYPH_STOP)) {
                    for (int i = 0; i < chunks[chunk_index].amount; i++) {
                        uint8_t y_offset = glyph_index / GLYPH_TILE_SIZE;
                        uint8_t x_offset = glyph_index - (y_offset * GLYPH_TILE_SIZE);
                        target[x + x_offset][y + y_offset] = chunks[chunk_index].value;
                        glyph_index++;
                    }
                    chunk_index++;
                }
            }

        	void action_am_i_human(name user) {
        		require_auth(user);

        		uint64_t seed = current_time_point().time_since_epoch().count() + user.value;

                uint8_t captcha[CHALLENGE_CHARS] = {
                    (uint8_t)vapaee::utils::rand_range(seed, FONT_MATRIX_SIZE),
                    (uint8_t)vapaee::utils::rand_range(seed, FONT_MATRIX_SIZE),
                    (uint8_t)vapaee::utils::rand_range(seed, FONT_MATRIX_SIZE),
                    (uint8_t)vapaee::utils::rand_range(seed, FONT_MATRIX_SIZE),
                    (uint8_t)vapaee::utils::rand_range(seed, FONT_MATRIX_SIZE)
                };

                uint8_t challange[CHALLANGE_WIDTH][CHALLANGE_HEIGHT] = {0};

                uint8_t current_x_pos = 0;
                uint8_t current_y_pos = (CHALLANGE_HEIGHT / 2) - (GLYPH_TILE_SIZE / 2);
                for (int i = 0; i < CHALLENGE_CHARS; i++) {
                    glyph_cpy(font_matrix[captcha[i]], (uint8_t**)challange, current_x_pos, current_y_pos);
                    current_x_pos += GLYPH_TILE_SIZE;
                }

                std::string render;
                for (int y = 0; y < CHALLANGE_WIDTH; y++) {
                    for (int x = 0; x < CHALLANGE_WIDTH; x++) {
                        render += (char)(challange[x][y] + ASCII_ZERO);
                    }
                    render += '\n';
                }
                print(render);
        	}

        };     
    };
};

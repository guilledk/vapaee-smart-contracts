#!/usr/bin/env python3
import argparse

from PIL import Image


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
	    "font_path", type=str,
	    help=f"bitmap font file path"
	    )
	parser.add_argument(
	    "tile_size", type=int,
	    help=f"font tile size in pixels"
	    )
	parser.add_argument(
	    "-o", "--output", type=str,
	    help=f"output header path"
	    )
	parser.add_argument(
	    "-t", "--tabs", action='store_true',
	    help=f"use tabs instead of spaces in the output header"
	    )
	args = parser.parse_args()

	font = Image.open(args.font_path)
	tile_size = args.tile_size
	pixels = font.load()

	total_width, total_height = font.size

	assert total_width % tile_size == 0
	assert total_height % tile_size == 0

	y_delta = int(total_height / tile_size)
	x_delta = int(total_width / tile_size)

	max_chunk = 4
	stop_char = 4

	glyphs = []

	def pixel_to_value(pixel):
		return 0 if pixel == (0, 0, 0) else 1

	# outer fors iterate through the glyphs
	for y in range(y_delta):
		for x in range(x_delta):
			glyph_data = []
			# inner fors iterate over local pixel data

			nonzero = False
			for local_y in range(tile_size):
				local_x = 0
				while not local_x == tile_size:
					cur_chunk = [
						pixel_to_value(pixels[
							(x * tile_size) + local_x,
							(y * tile_size) + local_y
						]),
						0
					]
					while (not local_x == tile_size) and (
						pixel_to_value(
							pixels[
								(x * tile_size) + local_x,
								(y * tile_size) + local_y
							]
						) == cur_chunk[0]):
						cur_chunk[1] += 1
						local_x += 1

					if cur_chunk[0] == 1:
						nonzero = True

					glyph_data.append(cur_chunk)

			if nonzero:
				assert len(glyph_data)
				glyphs.append(glyph_data)

	if args.output:
		out_path = args.output
	else:
		out_path = 'font_matrix.h'

	if args.tabs:
		tab = '\t'
	else:
		tab = '    '

	font_matrix_size = len(glyphs)
	glyph_data_size = tile_size * tile_size

	with open(out_path, 'w') as out_file:
		out_file.write('#ifndef _FONT_MATRIX_H_\n')
		out_file.write('#define _FONT_MATRIX_H_\n')
		out_file.write('\n')
		out_file.write(f'#define FONT_MATRIX_SIZE {font_matrix_size}\n')
		out_file.write(f'#define GLYPH_TILE_SIZE {tile_size}\n')
		out_file.write(f'#define GLYPH_MAX_CHUNK {max_chunk}\n')
		out_file.write('#define GLYPH_DATA_SIZE (GLYPH_MAX_CHUNK * GLYPH_TILE_SIZE)\n')
		out_file.write(f'#define GLYPH_STOP {stop_char}\n')
		out_file.write('\n')
		out_file.write('typedef struct {\n')
		out_file.write('    uint8_t value;\n')
		out_file.write('    uint8_t amount;\n')
		out_file.write('} glyph_chunk;\n')
		out_file.write('\n')
		out_file.write(
			'glyph_chunk font_matrix[FONT_MATRIX_SIZE][GLYPH_DATA_SIZE] = {\n'
		)

		for glyph_num, glyph_data in enumerate(glyphs):
			out_file.write(f'{tab}{{')

			i = 0
			while i < (tile_size * max_chunk):
				if i < len(glyph_data):
					out_file.write(f'{{{glyph_data[i][0]},{glyph_data[i][1]}}}')
				else:
					out_file.write(f'{{{stop_char},20}}')

				i += 1
				if i < (tile_size * max_chunk):
					out_file.write(',')

			out_file.write('}')
			if glyph_num < len(glyphs):
				out_file.write(',')
			
			out_file.write('\n')

		out_file.write('};\n')
		out_file.write('\n')
		out_file.write('#endif //_FONT_MATRIX_H_\n')
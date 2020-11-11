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

	glyphs = []

	# outer fors iterate through the glyphs
	for y in range(y_delta):
		for x in range(x_delta):
			glyph_data = []
			# inner fors iterate over local pixel data
			for local_y in range(tile_size):
				for local_x in range(tile_size):
					if pixels[
						(x * tile_size) + local_x,
						(y * tile_size) + local_y
					] == (255, 255, 255):
						glyph_data.append(1)
					else:
						glyph_data.append(0)

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
		out_file.write(f'#define GLYPH_DATA_SIZE {glyph_data_size}\n')
		out_file.write('\n')
		out_file.write(
			'uint8_t font_matrix[FONT_MATRIX_SIZE][GLYPH_DATA_SIZE] = {\n'
		)

		for glyph_num, glyph_data in enumerate(glyphs):
			out_file.write(f'{tab}{{')
			
			for i, val in enumerate(glyph_data):
				out_file.write(str(val))
				if i < len(glyph_data):
					out_file.write(',')

			out_file.write('}')
			if glyph_num < len(glyphs):
				out_file.write(',')
			
			out_file.write('\n')

		out_file.write('};\n')
		out_file.write('\n')
		out_file.write('#endif //_FONT_MATRIX_H_\n')
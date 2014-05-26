#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw
import argparse
import csv

Y_OFFSET = 104
P9_EVEN_OFFSET_X = 133
P9_ODD_OFFSET_X = 91

P8_EVEN_OFFSET_X = 365
P8_ODD_OFFSET_X = 326

ROW_ADVANCE = 12

DEFAULT_PINS = ((9, 1, "GND"), (9, 2, "GND"), (9, 43, "GND"), (9, 44, "GND"), (9, 45, "GND"), (9, 46, "GND"), (8, 1, "GND"), (8, 2, "GND"))

def draw_pin(image, font, header, pin, text):
	pin_draw = ImageDraw.Draw(image)
	x_offset = 0
	y_offset = Y_OFFSET
	text_width, text_height = pin_draw.textsize(text, font=font)
	if header == 8:
		if pin % 2 == 0:
			x_offset = P8_EVEN_OFFSET_X
		else:
			x_offset = P8_ODD_OFFSET_X-text_width
	elif header == 9:
		if pin % 2 == 0:
			x_offset = P9_EVEN_OFFSET_X
		else:
			x_offset = P9_ODD_OFFSET_X-text_width
	if pin % 2 == 0:
		pin_index = pin/2
	else:
		pin_index = (pin+1)/2
	pin_draw.text((x_offset, y_offset+(ROW_ADVANCE*(pin_index-1))), text, (127, 126, 124), font=font)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BBB Pinmap creator')
    parser.add_argument('-t', help="Specify template image to use", dest='template_image')
    parser.add_argument('-o', help="Specify output image", dest='output_image')
    parser.add_argument('-p', help="Specify pin file", dest='pin_file')

    args = parser.parse_args()

    font = ImageFont.truetype("DroidSans.ttf", 13)

    template_image = Image.open(args.template_image)
    for pin in DEFAULT_PINS:
    	draw_pin(template_image, font, pin[0], pin[1], pin[2])

    if args.pin_file:
	    with open(args.pin_file, 'rb') as pinfile:
	    	pinreader = csv.reader(pinfile)
	    	for row in pinreader:
	    		draw_pin(template_image, font, int(row[0]), int(row[1]), row[2])

    template_image.save(open(args.output_image, 'wb'), "PNG")
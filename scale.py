# import required module
from PIL import Image, ExifTags, ImageEnhance
import os
import sys
import argparse
import numpy as np
import cv2
from PIL.ExifTags import TAGS
from math import *

from PIL import Image
import numpy as np
from os import listdir

def laal(cropped_img_path, background_img_path, image_name):
	cropped_img = Image.open(cropped_img_path)
	background_img = Image.open(background_img_path)
	cropped_width = cropped_img.width
	cropped_height = cropped_img.height
	
	background_width = background_img.width
	background_height = background_img.height
	print(background_width)
	print(background_height)

	print(cropped_width)
	print(cropped_height)
	if cropped_width > (background_width/3) or cropped_height > (background_height/3):
		if cropped_width > (background_width/3):
			cropped_img.thumbnail((ceil(background_width/3) ,ceil(background_width/3)),Image.ANTIALIAS)
		else:
			cropped_img.thumbnail((ceil(background_height/3) ,ceil(background_height/3)),Image.ANTIALIAS)
		cropped_img.save(os.path.join(args.output_path, "adjusted/" + image_name))

def adjust_img(cropped_img, image_name):
	contrast = ImageEnhance.Contrast(cropped_img)
	contrast.enhance(1.5).save(os.path.join(args.output_path, "enhanced/" + image_name))
	cropped_img = Image.open(os.path.join(args.output_path, "enhanced/" + image_name))
	sharpness = ImageEnhance.Sharpness(cropped_img)
	sharpness.enhance(1.5).save(os.path.join(args.output_path, "enhanced/" + image_name))



def crop(png_image_name):
    pil_image = Image.open(png_image_name)
    np_array = np.array(pil_image)
    blank_px = [255, 255, 255, 0]
    mask = np_array != blank_px
    coords = np.argwhere(mask)
    x0, y0, z0 = coords.min(axis=0)
    x1, y1, z1 = coords.max(axis=0) + 1
    cropped_box = np_array[x0:x1, y0:y1, z0:z1]
    pil_image = Image.fromarray(cropped_box, 'RGBA')
    print(pil_image.width, pil_image.height)
    # pil_image.save(png_image_name)
    # print(png_image_name)

for f in listdir('.'):
    if f.endswith('.png'):
        crop(f)

parser = argparse.ArgumentParser()
parser.add_argument('--input-path', type=str, help='path of input images')
parser.add_argument('--background-path', type=str, help='path of background images')
parser.add_argument('--output-path', type=str, help='path of background images')
args = parser.parse_args()

# check input arguments
if not os.path.exists(args.input_path):
    print('Cannot find input path: {0}'.format(args.input_path))
    exit()
if not os.path.exists(args.background_path):
    print('Cannot find background path: {0}'.format(args.background_path))
    exit()
if not os.path.exists(args.output_path):
    print('Cannot find background path: {0}'.format(args.output_path))
    exit()
image_names = os.listdir(args.input_path)
for image_name in image_names:
	img = Image.open(os.path.join(args.input_path, image_name))
	img.getbbox()  # (64, 89, 278, 267)
	im2 = img.crop(img.getbbox())
	im2.save(os.path.join(args.output_path, "cropped/" +  image_name))
	laal(os.path.join(args.output_path, "cropped/" + image_name), os.path.join(args.background_path, image_name), image_name)
	augmented_img = adjust_img( Image.open(os.path.join(args.output_path, "adjusted/" + image_name)) , image_name)


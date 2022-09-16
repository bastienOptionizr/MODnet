import requests
import sys
import os, shutil
import argparse
from PIL import Image, ExifTags, ImageEnhance
import glob
from random import *
import math


parser = argparse.ArgumentParser()
parser.add_argument('--base-image', type=str, help='path of the base image')
parser.add_argument('--background-path', type=str, help='path of the background image')
parser.add_argument('--position-x', type=str, help='position x')
parser.add_argument('--position-y', type=str, help='position y')
parser.add_argument('--rotation', type=str, help='rotation in degree')
parser.add_argument('--max-size-width', type=str, help='max size width')
parser.add_argument('--max-size-height', type=str, help='max size height')
parser.add_argument('--image-name', type=str, help='name of the output image')
args = parser.parse_args()

# check input arguments
if not args.base_image:
    print('Cannot find image base path: {0}'.format(args.base_image))
    exit()
if not args.background_path:
    print('Cannot find background path: {0}'.format(args.background_path))
    exit()
if not args.position_x:
    print('Cannot find position x: {0}'.format(args.position_x))
    exit()
if not args.position_y:
    print('Cannot find posiiton y: {0}'.format(args.rotation_y))
    exit()
if not args.rotation:
    print('Cannot find rotation: {0}'.format(args.rotation))
    exit()
if not args.max_size_width:
    print('Cannot find rotation: {0}'.format(args.max_size_width))
    exit()
if not args.max_size_height:
    print('Cannot find rotation: {0}'.format(args.max_size_height))
    exit()

def adjust_image(cropped_img_path, max_size, image_name, rotation):

	adjusted_path = "adjusted_" + image_name.split(".")[0] + ".png"
	cropped_img = Image.open(cropped_img_path)
	cropped_width = cropped_img.width
	cropped_height = cropped_img.height
	maxwidth = int(max_size[0])
	maxheight = int(max_size[1])
	ratio = min(maxwidth/cropped_width, maxheight/cropped_height)
	img = cropped_img.resize((math.ceil(cropped_width * ratio),math.ceil(cropped_height * ratio)), Image.ANTIALIAS)
	img = img.rotate(int(rotation))
	img.save(adjusted_path);
	return adjusted_path


def download_img(url):
	response = requests.get(url)
	image_name =  "tmp/image_" + str(randint(1, 100)) + ".png"
	open(image_name, "wb").write(response.content);
	return image_name;

def fuse_background( foreground_img, background_img,img_name, position_x, position_y):
	
	background = Image.open(background_img)
	foreground = Image.open(foreground_img)

	background.paste(foreground, (int(position_x), int(position_y)), foreground)
	background.save("output/" + img_name);
	return img_name;

isExist = os.path.exists("tmp")


isExist = os.path.exists("tmp")


if not isExist:  
  os.makedirs("tmp")
else:
	shutil.rmtree("tmp")
	os.makedirs("tmp")

if args.image_name:
	name_foreground = args.image_name
else:
	name_foreground = os.path.basename(tmp_path_foreground)


tmp_path_foreground = download_img(args.base_image)
tmp_path_background = download_img(args.background_path)
name_background = os.path.basename(tmp_path_background)




tmp_adjusted_path = adjust_image(tmp_path_foreground, [args.max_size_width, args.max_size_height], name_foreground, args.rotation)

final_path = fuse_background(tmp_adjusted_path, tmp_path_background, name_foreground, args.position_x, args.position_y)
shutil.rmtree("tmp")
os.remove("adjusted_" + name_foreground)
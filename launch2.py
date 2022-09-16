import requests
import sys
import os, shutil
import argparse
from PIL import Image, ExifTags, ImageEnhance
import glob
from random import *


parser = argparse.ArgumentParser()
parser.add_argument('--base-image', type=str, help='path of the base image')
args = parser.parse_args()

print(args)
# check input arguments
if not args.base_image:
    print('Cannot find base image url: {0}'.format(args.base_image))
    exit()


def download_img(url):
	response = requests.get(url)
	image_name =  "tmp/image_" + str(randint(1, 100)) + ".png"
	open(image_name, "wb").write(response.content);
	return image_name;

def crop_image(path_img, image_name):
	cropped_path = "output/"+ image_name;
	img = Image.open(path_img)
	img.getbbox()  # (64, 89, 278, 267)
	im2 = img.crop(img.getbbox())
	im2.save(cropped_path)
	return cropped_path

def remove_background():
	os.system("python3 -m demo.image_matting.colab.inference         --input-path tmp --output-path output     --ckpt-path ./pretrained/modnet_photographic_portrait_matting.ckpt")


# Check whether the specified path exists or not
isExist = os.path.exists("tmp")


if not isExist:  
  os.makedirs("tmp")
else:
	shutil.rmtree("tmp")
	os.makedirs("tmp")

tmp_path = download_img(args.base_image)
image_name = os.path.basename(tmp_path)
print(image_name)
remove_background()
crop_image("output/" + image_name, image_name)
shutil.rmtree("tmp")

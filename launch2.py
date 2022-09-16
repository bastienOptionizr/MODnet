import requests
import sys
import os, shutil
import argparse
from PIL import Image, ExifTags, ImageEnhance
import glob
from random import *
import json


parser = argparse.ArgumentParser()
parser.add_argument('--base-image', type=str, help='path of the base image')
parser.add_argument('--image-name', type=str, help='name of the output image')
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

def crop_image_api(img_path, img_name):
	payload={'image_url': img_path + img_name }
	files=[
	  ('image_file',(img_name,open(img_path + img_name,'rb'),'image/jpeg'))
	]
	headers = {
	  'Rm-Token': '6319e05bd72005.17370944'
	}

	response = requests.request("POST", url, headers=headers, data=payload, files=files)
	text_response = '{"status":200,"preview_demo":"https://file.removal.ai/preview/577d1825-b02b-4f82-9c5d-d7b150bd592c_7.png","url":"https://file.removal.ai/original/577d1825-b02b-4f82-9c5d-d7b150bd592c_7_0B1ZNE.png","high_resolution":"https://file.removal.ai/original/577d1825-b02b-4f82-9c5d-d7b150bd592c_7_0B1ZNE.png","low_resolution":"https://file.removal.ai/low_resolution/577d1825-b02b-4f82-9c5d-d7b150bd592c_7.png","original_width":0,"original_height":0,"preview_width":0,"preview_height":0}'
	data = json.loads(response.text)
	#data = json.loads(text_response)
	cropped_img_url = data["url"]
	response = requests.get(cropped_img_url)
	open(os.path.join("output/" + image_name.split('.')[0] + '.png'), "wb").write(response.content)

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

if args.image_name:
	image_name = args.image_name
else:
	image_name = os.path.basename(tmp_path)

os.rename(tmp_path, "tmp/" + image_name)

remove_background()
crop_image("output/" + image_name, image_name)
#crop_image_api("output/" + image_name, image_name)
shutil.rmtree("tmp")

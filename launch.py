import requests
import sys
import os, shutil
import json
import argparse
from PIL import Image, ExifTags, ImageEnhance
from math import *




def download_img(url, img_id):
	response = requests.get(url)
	open("input/" + img_id + ".png", "wb").write(response.content);
	return os.path.join(args.input_path, img_id + ".png");

def crop_image(path_img, path_background, image_name):
	cropped_path = os.path.join(args.output_path, "cropped/" +  image_name + ".png") 
	img = Image.open(path_img)
	img.getbbox()  # (64, 89, 278, 267)
	im2 = img.crop(img.getbbox())
	im2.save(cropped_path)
	adjusted_path = adjust_image(cropped_path, os.path.join(args.background_path, path_background + ".png"), image_name)
	return adjusted_path

def adjust_image(cropped_img_path, background_img_path, image_name):

	adjusted_path = os.path.join(args.output_path, "adjusted/" + image_name + ".png")
	
	cropped_img = Image.open(cropped_img_path)
	background_img = Image.open(background_img_path)
	cropped_width = cropped_img.width
	cropped_height = cropped_img.height
	
	background_width = background_img.width
	background_height = background_img.height


	if cropped_width > (background_width/2) or cropped_height > (background_height/2):
		if cropped_width > (background_width/3):
			cropped_img.thumbnail((ceil(background_width/2) ,ceil(background_width/2)),Image.ANTIALIAS)
		else:
			cropped_img.thumbnail((ceil(background_height/2) ,ceil(background_height/2)),Image.ANTIALIAS)
		cropped_img.save(adjusted_path);

		return os.path.join(adjusted_path);
	else:
		return cropped_img_path; 

def enhance_img(cropped_img, image_name):
	enhance_path = os.path.join(args.output_path,  image_name + ".png")
	contrast = ImageEnhance.Contrast(cropped_img)
	contrast.enhance(1.5).save(enhance_path)
	cropped_img = Image.open(enhance_path)
	sharpness = ImageEnhance.Sharpness(cropped_img)
	sharpness.enhance(1.5).save(enhance_path)
	
	return enhance_path;


def fuse_background( foreground_img, background_img,img_name):
	
	background = Image.open(background_img)
	foreground = Image.open(foreground_img)

	background.paste(foreground, (512 - foreground.width, 512 - foreground.height), foreground)
	background.save(os.path.join(args.output_path, img_name  + ".png"));
	# enhance_path = enhance_img(os.path.join(args.output_path, img_name  + ".png"), img_name + ".png")
	return os.path.join(args.output_path, img_name  + ".png");

def treat_image(img_config):
	# crop image and adjust it to background
	path_tmp_cropped_img = crop_image(img_config["output_path"], img_config["background"], img_config["id"])
	path_pasted_background_img = fuse_background(path_tmp_cropped_img, os.path.join(args.background_path, img_config["background"] + ".png"), img_config["id"])
	# print(img_config["final_img_description"])
	# print("cd ../stable-diffusion ; python3 /home/optionizr/stable-diffusion/scripts/img2img.py --prompt '" + img_config["final_img_description"] + "' --init-img /home/optionizr/MODnet/" + path_pasted_background_img + " --strength 0.4 --outdir /home/optionizr/outputs --skip_grid")
	os.system("cd ../stable-diffusion ; python3 /home/optionizr/stable-diffusion/scripts/img2img.py --prompt '" + img_config["final_img_description"] + "' --init-img /home/optionizr/MODnet/" + path_pasted_background_img + " --strength 0.4 --outdir /home/optionizr/outputs --skip_grid")
	remove_tmp_files(img_config);

# def compute_imgs():
# 	os.system("python3 ../stable-diffusion/scripts/img2img.py --prompt '" + background_description"' --plms")
# 	# python3 scripts/img2img.py --prompt "by dali" --init-img /home/optionizr/image/$i.png --strength 0.4

# def paste_background(background_img, input_img):
# 	os.system("python3 -m paste_background.py   --input-path output         --output-path output --background-path background")

def remove_background():
	os.system("python3 -m demo.image_matting.colab.inference         --input-path input --output-path output     --ckpt-path ./pretrained/modnet_photographic_portrait_matting.ckpt")

def remove_tmp_files(img_config):
	if os.path.exists(os.path.join(args.output_path, "cropped/" + img_config["id"] + ".png")):
	  os.remove(os.path.join(args.output_path, "cropped/" + img_config["id"] + ".png"))
	if os.path.exists(os.path.join(args.output_path, "adjusted/" + img_config["id"] + ".png")):
	  os.remove(os.path.join(args.output_path, "adjusted/" + img_config["id"] + ".png"))
	if os.path.exists(os.path.join(args.input_path, img_config["id"] + ".png")):
	  os.remove(os.path.join(args.input_path, img_config["id"] + ".png"))


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

list_img = []

input_path = args.input_path
cropped_path = os.path.join(args.output_path, "cropped")
adjusted_path = os.path.join(args.output_path, "adjusted")
enhanced_path = os.path.join(args.output_path, "enhanced")

# Check whether the specified path exists or not
isExist = os.path.exists(input_path)

if not isExist:  
  os.makedirs(input_path)

isExist = os.path.exists(cropped_path)

if not isExist:  
  os.makedirs(cropped_path)


# Check whether the specified path exists or not
isExist = os.path.exists(adjusted_path)

if not isExist:  
  os.makedirs(adjusted_path)

# Check whether the specified path exists or not
isExist = os.path.exists(enhanced_path)

if not isExist:  
  os.makedirs(enhanced_path)

with open('todo.txt') as f:
    lines = [line for line in f]
    for line in lines:
    	line_tab=line.split(" | ")
    	if len(line_tab) > 5:
	    	img_id=line_tab[0]
	    	img_url=line_tab[1]
	    	background_img=line_tab[2]
	    	email=line_tab[3]
	    	final_img_description=line_tab[4]
	    	crop_module = line_tab[5]

	    	img_config = {
	    		"id": 					img_id,
	    		"url": 					img_url,
	    		"background": 			background_img,
	    		"email": 					email,
	    		"final_img_description": 	final_img_description,
	    		"crop": 					crop_module
	    	};


	    	if os.path.exists(os.path.join(args.background_path, img_config["background"] + ".png")):
	    		img_config["path"] = download_img(img_config["url"], img_config["id"])
	    		list_img.append(img_config)

remove_background()
for img in list_img:
	img["output_path"] = os.path.join(args.output_path, img["id"] + ".png")
	treat_image(img)
	    	# if "api" in crop_module:
	    		# os.system('python3 crop_background_api.py input/ ' + img_name + ' output/')
	    	# else:
	    		# os.system('python3 -m demo.image_matting.colab.inference   --input-path input   --output-path output     --ckpt-path ./pretrained/modnet_photographic_portrait_matting.ckpt --img-path ' + img_name)
	    	
	    	# treat_image(img_config)
	
	# create_script(lines)
	# paste_background()

import requests
import sys
import os, shutil
import json


def create_script(lines):
	with open(os.path.join("/home/optionizr/", "launch_script.sh"), "w") as f:
		f.write("#!/bin/bash")
		f.write("cd ../stable-diffusion")
		f.write("conda activate ldm")
		# END=5
		# for ((i=1;i<=END;i++)); do
		#     echo $i
		# done
    	line_tab=line.split("|")
  #   	if len(line_tab) > 3:
	 #    	img_name=line_tab[0]
	 #    	background_description=line_tab[1]
	 #    	final_img_description=line_tab[2]
	 #    	crop_module = line_tab[3]
		# f.write('	python3 scripts/img2img.py --prompt "' + final_img_description + '" --init-img /home/optionizr/image/$i.png --strength 0.4')



def compute_imgs():
	os.system("python3 ../stable-diffusion/scripts/img2img.py --prompt '" + background_description"' --plms")
	# python3 scripts/img2img.py --prompt "by dali" --init-img /home/optionizr/image/$i.png --strength 0.4

def paste_background(background_img, input_img):
	os.system("python3 -m paste_background.py   --input-path demo/image_matting/colab/output         --output-path demo/image_matting/colab/output --background-path background")

def clear_env():
	clear_dir('demo/colab/output')
	clear_dir('final_output')

def clear_dir():
	folder = 'demo/colab/output'
	for filename in os.listdir(folder):
	    file_path = os.path.join(folder, filename)
	    try:
	        if os.path.isfile(file_path) or os.path.islink(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path):
	            shutil.rmtree(file_path)
	    except Exception as e:
	        print('Failed to delete %s. Reason: %s' % (file_path, e))

clear_env()

with open('todo.txt') as f:
    lines = [line for line in f]
    for line in Lines:
    	line_tab=line.split("|")
    	if len(line_tab) > 3:
	    	img_name=line_tab[0]
	    	background_description=line_tab[1]
	    	final_img_description=line_tab[2]
	    	crop_module = line_tab[3]

	    	if "api" in crop_module:
	    		os.system('python3 crop_background_api.py demo/image_matting/colab/input/ ' + img_name + ' demo/image_matting/colab/output/')
	    	else:
	    		os.system('python3 -m demo.image_matting.colab.inference   --input-path demo/image_matting/colab/input   --output-path demo/image_matting/colab/output     --ckpt-path ./pretrained/modnet_photographic_portrait_matting.ckpt --img-path ' + img_name)
	
	# create_script(lines)
	paste_background()

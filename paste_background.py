from PIL import Image
import os
import sys
import argparse
import numpy as np
def fuse_background(background_img, foreground_img, img_name):
	
	background = Image.open(background_img)
	foreground = Image.open(foreground_img)

	background.paste(foreground, (0, 0), foreground)
	background.show()
	background.save(os.path.join(args.output_path, img_name.split('.')[0]) + ".png")

parser = argparse.ArgumentParser()
parser.add_argument('--input-path', type=str, help='path of input images')
parser.add_argument('--output-path', type=str, help='path of output images')
parser.add_argument('--background-path', type=str, help='path of pre-trained MODNet')
args = parser.parse_args()

# check input arguments
if not os.path.exists(args.input_path):
    print('Cannot find input path: {0}'.format(args.input_path))
    exit()
if not os.path.exists(args.output_path):
    print('Cannot find output path: {0}'.format(args.output_path))
    exit()
if not os.path.exists(args.background_path):
    print('Cannot find ckpt path: {0}'.format(args.ckpt_path))
    exit()
image_names = os.listdir(args.input_path)
for image_name in image_names:
	print(image_name)
	print(args.background_path)
	if os.path.exists(os.path.join(args.background_path, image_name)):
		fuse_background(os.path.join(args.background_path, image_name) , os.path.join(args.input_path, image_name), image_name )
	else:
		print("error background is absent")
		with open("logs", "a") as file_object:
		    # Append 'hello' at the end of file
		    file_object.write("[background_missing]" + image_name)



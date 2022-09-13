# import required module
from PIL import Image, ExifTags
import os
import sys
import argparse
import numpy as np
import cv2
from PIL.ExifTags import TAGS


from PIL import Image
import numpy as np
from os import listdir

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
args = parser.parse_args()

# check input arguments
if not os.path.exists(args.input_path):
    print('Cannot find input path: {0}'.format(args.input_path))
    exit()
image_names = os.listdir(args.input_path)
for image_name in image_names:
	# crop(os.path.join(args.input_path, image_name))
	img = Image.open(os.path.join(args.input_path, image_name))
	# im = Image.open("test.bmp")
	print(img.size)  # (364, 471)
	img.getbbox()  # (64, 89, 278, 267)
	im2 = img.crop(img.getbbox())
	print(im2.size)  # (214, 178)
	im2.save(os.path.join(args.input_path, "crop_" + image_name))
	# get image
	# exifdata = img.getexif()
	# print(exifdata)
	# iterating over all EXIF data fields
	# for tag_id in exifdata:
	#     # get the tag name, instead of human unreadable tag id
	#     tag = TAGS.get(tag_id, tag_id)
	#     data = exifdata.get(tag_id)
	#     # decode bytes 
	#     if isinstance(data, bytes):
	#         data = data.decode()
	#     print(f"{tag:25}: {data}")
	# img = img.resize((512,512), resample=Image.LANCZOS)
	# img.save(os.path.join(args.input_path, image_name))
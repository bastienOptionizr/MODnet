import os
import sys
import argparse
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

from src.models.modnet import MODNet


if __name__ == '__main__':
    # define cmd arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-path', type=str, help='path of output images')
    parser.add_argument('--img-path', type=str, help='path of the image')
    parser.add_argument('--ckpt-path', type=str, help='path of pre-trained MODNet')
    args = parser.parse_args()

    # check input arguments
    if not os.path.exists(args.output_path):
        print('Cannot find output path: {0}'.format(args.output_path))
        exit()
    if not os.path.exists(args.img_path):
        print('Cannot find img path: {0}'.format(args.img_path))
        exit()
    if not os.path.exists(args.ckpt_path):
        print('Cannot find ckpt path: {0}'.format(args.ckpt_path))
        exit()

    # define hyper-parameters
    ref_size = 512

    # define image to tensor transform
    im_transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ]
    )

    # create MODNet and load the pre-trained ckpt
    modnet = MODNet(backbone_pretrained=False)
    modnet = nn.DataParallel(modnet)

    if torch.cuda.is_available():
        modnet = modnet.cuda()
        weights = torch.load(args.ckpt_path)
    else:
        weights = torch.load(args.ckpt_path, map_location=torch.device('cpu'))
    modnet.load_state_dict(weights)
    modnet.eval()

    # inference images
    im_name = args.img_path
    print('Process image: {0}'.format(im_name))

    # read image
    im = Image.open(im_name)

    # unify image channels to 3
    im = np.asarray(im)
    if len(im.shape) == 2:
        im = im[:, :, None]
    if im.shape[2] == 1:
        im = np.repeat(im, 3, axis=2)
    elif im.shape[2] == 4:
        im = im[:, :, 0:3]

    # convert image to PyTorch tensor
    im = Image.fromarray(im)
    im = im_transform(im)

    # add mini-batch dim
    im = im[None, :, :, :]

    # resize image for input
    im_b, im_c, im_h, im_w = im.shape
    if max(im_h, im_w) < ref_size or min(im_h, im_w) > ref_size:
        if im_w >= im_h:
            im_rh = ref_size
            im_rw = int(im_w / im_h * ref_size)
        elif im_w < im_h:
            im_rw = ref_size
            im_rh = int(im_h / im_w * ref_size)
    else:
        im_rh = im_h
        im_rw = im_w
    
    im_rw = im_rw - im_rw % 32
    im_rh = im_rh - im_rh % 32
    im = F.interpolate(im, size=(im_rh, im_rw), mode='area')

    # inference
    _, _, matte = modnet(im.cuda() if torch.cuda.is_available() else im, True)

    # resize and save matte
    matte = F.interpolate(matte, size=(im_h, im_w), mode='area')
    matte = matte[0][0].data.cpu().numpy()
    matte_name = args.output_path
    Image.fromarray(((matte * 255).astype('uint8')), mode='L').save(args.output_path)
    import numpy as np
    from PIL import Image

    import numpy as np
    import matplotlib.pyplot as plt
    import glob
    from PIL import Image

    def transparent(myimage, image_name):
        img = Image.open(myimage)
        img = img.convert("RGBA")

        pixdata = img.load()

        width, height = img.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (255, 255, 255, 0)

        img.save(args.output_path, "PNG")
    
    # def color_to_alpha_mask(im, alpha_color):
    #     mask = (im[..., :3] == alpha_color).all(axis=2)
    #     alpha = np.where(mask, 0, 255)
    #     ny, nx, _ = im.shape
    #     im_rgba = np.zeros((ny, nx, 4), dtype=im.dtype)
    #     im_rgba[..., :3] = im
    #     im_rgba[..., -1] = alpha
    #     return im_rgba

    def combined_display(image, matte):
      # calculate display resolution
      w, h = image.width, image.height
      rw, rh = 800, int(h * 800 / (3 * w))
      
      # obtain predicted foreground
      image = np.asarray(image)
      if len(image.shape) == 2:
        image = image[:, :, None]
      if image.shape[2] == 1:
        image = np.repeat(image, 3, axis=2)
      elif image.shape[2] == 4:
        image = image[:, :, 0:3]
      matte = np.repeat(np.asarray(matte)[:, :, None], 3, axis=2) / 255
      foreground = image * matte + np.full(image.shape, 255) * (1 - matte)
      
      combined2 = Image.fromarray(np.uint8(foreground))
      #combined2.show()
      return combined2

    # visualize all images
    image_name = args.img_path
    matte_name = args.output_path
    print(matte_name)
    image = Image.open(image_name)
    matte = Image.open(os.path.join(args.output_path, matte_name))
    image = combined_display(image, matte)
    image.save(args.output_path)
    transparent(args.output_path, image_name.replace("input/").split('.')[0] + ".png")
      # target_color = (0, 0, 0)
      # im = plt.imread(os.path.join(args.output_path, "combined_"+ image_name.split('.')[0] + '.png'))
      # im_rgba = color_to_alpha_mask(im, target_color)
      # im_rgba = Image.fromarray(np.uint8(im_rgba))
      # im_rgba.save(os.path.join(args.output_path, "transparent_"+ image_name.split('.')[0] + '.png'));

#!/usr/bin/python3

"""
This script renames all image files within a given folder.
"""
import os
import glob
import argparse
import exifread
import PIL
from PIL import Image
from pathlib import Path

# setup from args
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, default='fotos',
    help='path to folder containing the original images. Default: ./fotos')
# parser.add_argument('output', type=str, default='fotos_renamed',
#     help='path to folder where the renamed images are stored. Not existing folder will be created. Default: ./fotos_renamed')
# parser.add_argument('nocopy', type=bool, default=False,
#     help='[WIP] only move/rename files without copy them to a new folder.')
# parser.add_argument('recursive', type=bool, default=False,
#     help='[WIP] check subfolders of the source recursively. Default: False')
# parser.add_argument('extension', type=str, default=None,
#     help='[WIP] only select images with this extension. (Casesensitiv). Default: None')
# parser.add_argument('web', type=bool, default=False,
#     help='crop images to fit in 1000x1000px and reduce jpg quality to 90%')
args = parser.parse_args()

# process images
# if args.extension is not None:
#     files = glob.iglob(args['from'])  # fix error
# else:

# files = sorted(os.listdir(args.input))
# for file in files:
#     with open(os.path.join(args.output, file), 'rb') as rf:
#         tags = exifread.process_file(rf)
#         print('file')

# print(list(glob.iglob(args.input + '*.jpg', recursive=True)))
filelist = []
for pat in ['*.jpg', '*.JPG', '*.jpeg', '*.JPEG']:
    filelist += list(glob.iglob(args.input+'/'+pat, recursive=True))
if not os.path.isdir(os.path.join(args.input, 'compressed')):
        os.makedirs(os.path.join(args.input, 'compressed'))
for filename in filelist:
    print(filename)
    root_dir = args.input
    p = Path(filename)
    img = p.relative_to(root_dir)
    new_name = os.path.join(root_dir, 'compressed', str(img))
    print(new_name)
    im = Image.open(filename)
    exif = im.info['exif']
    im.thumbnail([1600, 1600], PIL.Image.ANTIALIAS)
    im.save(new_name, 'JPEG', quality=90, exif=exif)
    #im = im.resize([1600, 1600], PIL.Image.ANTIALIAS)

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
import exifread
import os
import datetime as dt
from shutil import copyfile
from uuid import uuid4

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
#     help='crop images to fit in 1000x1000px and reduce jpg quality to 90%')
args = parser.parse_args()


def get_exif_date(image):
    """ reads the exif tags of an image file and returns datetime or None
    """
    tags = exifread.process_file(image)
    datetime = dt.datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
    new_name = datetime.strftime('%Y%m%d_%H%M%S')+'.jpg'
    return datetime, new_name, tags





if not os.path.isdir(os.path.join(args.input, 'renamed')):
    os.makedirs(os.path.join(args.input, 'renamed'))
if not os.path.isdir(os.path.join(args.input, 'rename_fails')):
    os.makedirs(os.path.join(args.input, 'rename_fails'))


jpg = list(glob.iglob(args.input + '*.jpg', recursive=True))
jpg_up = list(glob.iglob(args.input + '*.JPG', recursive=True))
jpeg = list(glob.iglob(args.input + '*.jpeg', recursive=True))
jpeg_up = list(glob.iglob(args.input + '*.JPEG', recursive=True))
all_matches = jpg + jpg_up + jpeg + jpeg_up
for filename in sorted(all_matches):
    try:
        root_dir = args.input
        p = Path(filename)
        img = p.relative_to(root_dir)
        with open(p, 'rb') as ri:
            date, fname, tags = get_exif_date(ri)
        new_path = (root_dir + 'renamed/' + str(img))
        target_folder = os.path.split(new_path)[0]
        new_fpath = os.path.join(target_folder, fname)
        i = 0
        while os.path.isfile(new_fpath):
            i += 1
            print(f'file exists already: increasing number: {i}')
            f_base, f_ext = os.path.splitext(fname)
            fname_i = f'{f_base}_{i}{f_ext}'
            new_fpath = os.path.join(target_folder, fname_i)
        print(new_fpath)

    except Exception as e:
        new_fpath = os.path.join(args.input, 'rename_fails', str(img))
        print(e)
    copyfile(p, new_fpath)
    #im = im.resize([1600, 1600], PIL.Image.ANTIALIAS)

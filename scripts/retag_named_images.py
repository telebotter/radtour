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
from PIL import ExifTags
from pathlib import Path
import exifread
import os
import datetime as dt
from shutil import copyfile

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


def set_exif_date(image, name):
    """ reads the exif tags of an image file and returns datetime or None
    """
    tags = exifread.process_file(image)
    datetime = dt.datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
    new_name = datetime.strftime('%Y%m%d_%H%M%S')+'.jpg'
    return datetime, new_name, tags



if not os.path.isdir(os.path.join(args.input, 'tagged')):
    os.makedirs(os.path.join(args.input, 'tagged'))

jpg = list(glob.iglob(args.input + '*.jpg', recursive=True))
jpg_up = list(glob.iglob(args.input + '*.JPG', recursive=True))
jpeg = list(glob.iglob(args.input + '*.jpeg', recursive=True))
jpeg_up = list(glob.iglob(args.input + '*.JPEG', recursive=True))
all_matches = jpg + jpg_up + jpeg + jpeg_up
for filename in all_matches:
    try:
        root_dir = args.input
        p = Path(filename)
        img = p.relative_to(root_dir)
        # im = Image.open(p)
        exif_format = '%Y:%m:%d %H:%M:%S'
        file_format = 'IMG_%Y%m%d_%H%M%S'
        fname = os.path.split(str(img))[1]
        fname_cut = fname[:19]
        fdate = dt.datetime.strptime(fname_cut, file_format)
        new_fpath = (root_dir + 'tagged/' + str(img))
        copyfile(p, new_fpath)
        # print(fname_cut)
        # print(fdate)
        # if 'exif' in im.info:
        #     exif = im.info['exif']
        # else:
        #     print('no exif data in image')
        #     exif = {}
        # for k,v in exif.items():
        #     print(f'{ExifTags.TAGS.get(k, k)}: {v}')

        # try pyexiv2
        import pyexiv2
        #from pyexiv2 import metadata as md
        metadata = pyexiv2.ImageMetadata(new_fpath)
        metadata.read()
        #metadata['Exif.DateTimeOriginal'] = fdate
        metadata['Exif.Image.DateTime'] = fdate
        metadata['Exif.Image.DateTimeOriginal'] = fdate
        #metadata['Exif.Photo.DateTime'] = fdate
        metadata['Exif.Photo.DateTimeOriginal'] = fdate
        metadata['Exif.Photo.UserComment'] = 'Set some DateTime from file name'
        metadata.write()
        print(metadata.exif_keys)

        #exif['EXIF DateTimeOriginal'] = fdate.strftime(exif_format)
        #im.save(new_fpath, 'JPEG', exif=exif)
        #print('saved')
    except Exception as e:
        if not os.path.isdir(os.path.join(args.input, 'tag_fails')):
            os.makedirs(os.path.join(args.input, 'tag_fails'))
        new_fpath = os.path.join(args.input, 'tag_fails', str(img))
        print('Error: ')
        raise e
    #im = im.resize([1600, 1600], PIL.Image.ANTIALIAS)

import exifread
import os
import datetime as dt


def get_exif_date(image):
    """ reads the exif tags of an image file and returns datetime or None
    """
    tags = exifread.process_file(image)
    datetime = dt.datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
    new_name = datetime.strftime('%Y%m%d_%H%M%S')+'.jpg'
    return datetime, new_name, tags

import exifread
import os
import datetime as dt
from shutil import copyfile


from django.core.management.base import BaseCommand, CommandError
from main.models import Tour
from bilder.models import Bild


class Command(BaseCommand):
    help = 'pass touralias and img folder'

    def add_arguments(self, parser):
        parser.add_argument('tour', type=str)
        parser.add_argument('folder', type=str)


    def handle(self, *args, **options):
        fpath = options['folder']
        tname = options['tour']
        target = '/home/django/tour/media/bilder/{}/'.format(tname)
        tour = Tour.objects.get(alias=tname)
        self.stdout.write('found tour: {}'.format(tour.name))
        files = os.listdir(fpath)
        for imgfile in sorted(files):  
            with open(os.path.join(fpath, imgfile), 'rb') as rf:
                try:
                    tags = exifread.process_file(rf)
                    print('tags parsed')
                    datetime = dt.datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
                    new_name = datetime.strftime('%Y-%m-%d_%H-%M-%S')+'.jpg'
                   
                except Exception as e:
                    print(e)
                    print('error reading file: ')
                    print(imgfile)
                    continue
            new_fpath = os.path.join(target,new_name)
            if os.path.exists(new_fpath):
                print('error file exist already')
                if filecmp.cmp(new_fpath, os.path.join(fpath, imgfile)):
                    print('file stats are same.. skipping')
                    continue
                else:
                    print('file stats differ... renaming')
                    cnt = 1
                    new_fname = datetime.strftime('%Y-%m-%d_%H-%M-%S') + '_'
                    while os.path.exists(os.path.join(target, new_fname+cnt+'.jpg'):
                            print('renaming again: '+str(cnt)
                            cnt = cnt+1

            if not os.path.exists(target):
                os.makedirs(target)
            print('saving file to: {}'.format(new_fpath))
            copyfile(os.path.join(fpath, imgfile), new_fpath) 

            # create image object to store tags and stuff
            fpath_rel = os.path.relpath(new_fpath, '/home/django/tour/media/')
            #existing_objects = Bild.objects.filter(bild=fpath_rel, tour=tour)
            bild = Bild.objects.create(bild=fpath_rel, tour=tour)
            
                #pass
            #tags = exifread.process_file(os.path.join(fpath, imgfile))
        #self.stdout.write(gj.dumps(mls))
        #tour.track = mls
        #tour.save()


        #folder_in
        #f = open(path_name, 'rb')
        #tags = exifread.process_file(f)

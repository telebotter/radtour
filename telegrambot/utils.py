import datetime as dt
import logging
import os
logger = logging.getLogger('django')

def csv2gpx(csvfile, bot, update):
    logger.info('function called')
    logger.info(update.callback_query.chat_instance)
    csvpath = os.path.join('/home/django/tour/media/telegram', csvfile)
    fname, ext = os.path.splitext(csvfile)
    gpxfile = os.path.join('/home/django/tour/media/telegram', fname+'.gpx')
    gpx = '<?xml version="1.0" encoding="UTF-8"?>\n'
    gpx += '''<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" creator="Oregon 400t" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">
<metadata>
<link href="http://www.garmin.com">
  <text>Garmin International</text>
</link>
<time>2009-10-17T22:58:43Z</time>
</metadata>'''
    gpx += '<trk><name>'
    gpx += fname +"</name>\n<trkseg>\n"
    with open(csvpath, 'r') as rf:
        header = True
        for line in rf:
            if header:
                header = False
                continue
            arr = line.split(',')
            #for
            csvdt = arr[3]+'-'+arr[4]
            timeobj = dt.datetime.strptime(csvdt, '%Y/%m/%d-%H:%M:%S')
            time = timeobj.strftime('%Y-%m-%dT%H:%M:%SZ')
            gpx += '<trkpt lat="{}" lon="{}"><ele>{}</ele><time>{}</time></trkpt>\n'.format(arr[0], arr[1], arr[2], time)
    gpx += '</trkseg></trk></gpx>'
    with open(gpxfile, 'w') as wf:
        wf.write(gpx)
    chat_id = update.callback_query.message.chat.id
    bot.send_document(chat_id, open(gpxfile, 'rb'))
    return gpxfile

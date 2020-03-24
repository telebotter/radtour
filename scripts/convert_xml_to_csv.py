import xml.etree.ElementTree as et
import pandas as pd
import os
import datetime as dt
import io

tour = 'portugal'
#start = dt.date(2012, 9, 1)
in_folder = f'/home/buki/cloud/fremd/touren/{tour}/tracks/gpx/'
out_folder = f'/home/buki/cloud/fremd/touren/{tour}/tracks/csv/'


def datefromfname(f, start):
    days = int(f[:2])-1
    dat = start + dt.timedelta(days=days)
    if '_' in f:
        t = int(f.split('_')[1][:2])
        tim = dt.time(t, 0)
    else:
        tim = dt.time(0, 0)
    dati = dt.datetime.combine(dat, tim)
    return dati





for f in sorted(os.listdir(in_folder)):
    print(f)
    if True:
        fi = open(os.path.join(in_folder, f), 'r')
        lines = fi.readlines()
        lines[1] = '<gpx>\n'
        #lines[2:7] = ''
        fi.close()
        fo = open(os.path.join(in_folder, f), 'w')
        fo.writelines(lines)
        fo.close()
    with open(os.path.join(in_folder, f), 'r') as xf:
        xtree = et.parse(xf)
    xroot = xtree.getroot() # <gpx>
    lat, lon, alt, time, date, speed = [], [], [], [], [], []
    first_time = False
    print(xroot.attrib)
    for trkpt in xroot.iter('trkpt'):
        lat.append(trkpt.attrib['lat'])
        lon.append(trkpt.attrib['lon'])
        try:
            alt.append(trkpt.find('ele').text)
        except:
            alt.append(0)
        try:
            dtstr = trkpt.find('time').text
            datetime = dt.datetime.strptime(dtstr, "%Y-%m-%dT%H:%M:%SZ")
        except:
            if not first_time:
                datetime = dt.datetime.strptime('2000-01-01T00:00:00Z', "%Y-%m-%dT%H:%M:%SZ")
            else:
                datetime = first_time
            # get dt from fname in days
            # datetime = datefromfname(f, start)
        if not first_time:
            first_time = datetime
        date.append(datetime.date())
        time.append(datetime.time())
        try:
            speed.append(trkpt.find('extensions').find('speed').text)
        except:
            speed.append(-1)

    data = {
        'Latitude': lat,
        'Longitude': lon,
        'Time': time,
        'Alt': alt,
        'Date': date,
        'Speed': speed}
    df = pd.DataFrame.from_dict(data)
    if len(lat) == 0:
        print(' - empty')
        continue
    fout = first_time.strftime('%Y%m%d_%H%M%S.csv')
    df.to_csv(os.path.join(out_folder, fout), sep=',')

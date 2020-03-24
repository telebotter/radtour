import pandas as pd
import json
import datetime as dt
import os

tour = 'schweden'
start = dt.date(2015, 8, 26)
in_folder = f'/home/buki/cloud/fremd/touren/{tour}/tracks/json/'
out_folder = f'/home/buki/cloud/fremd/touren/{tour}/tracks/csv/'

with open(os.path.join(in_folder, 'schweden.json'), 'r') as f:
    data = json.load(f)
for ft in data['features']:
    if ft['geometry']['type'] == 'LineString':
        print('match')
        break
points = ft['geometry']['coordinates'] # eins
lat, lon, alt, time, date, speed = [], [], [], [], [], []
for p in points:
    lon.append(p[0])
    lat.append(p[1])
    alt.append(0)
    time.append('00:00:00')
    date.append('2016-07-30')
    speed.append(-1)
data = {
    'Latitude': lat,
    'Longitude': lon,
    'Time': time,
    'Alt': alt,
    'Date': date,
    'Speed': speed}
df = pd.DataFrame.from_dict(data)
df.to_csv(os.path.join(out_folder, '20160730_000000.csv'), sep=',')

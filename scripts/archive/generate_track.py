import os
import pandas as pd
import geojson as gj
import datetime as dt

tour = 'alpen2'
csv_folder = f'/home/buki/cloud/touren/{tour}/tracks/logs/'
out_folder = os.path.join(csv_folder, '..')
csv_out = os.path.join(out_folder, f'{tour}.csv')
json_out = os.path.join(out_folder, f'{tour}.json')

# merge csv files
files = os.listdir(csv_folder)
contents = []
for f in files:
    print(f)
    df = pd.read_csv(os.path.join(csv_folder, f))
    #print(df)
    contents.append(df)
data = pd.concat(contents, ignore_index=True)
data.to_csv(csv_out, index=False)


# get points
data['day'] = pd.to_datetime(data['Date'])
#data.sort_values('Time', inplace=True)
points = data.groupby('day').agg('last')
points.to_csv(os.path.join(out_folder, f'{tour}_points.csv'), index=False)


# create geojson
wps = []
for index, row in points.iterrows():
    point = gj.Point((row['Longitude'], row['Latitude']))
    props = {'date': row['Date'], 'time': row['Time']}
    feature = gj.Feature(geometry=point, properties=props)
    wps.append(feature)
waypoints = gj.FeatureCollection(wps)
with open(os.path.join(out_folder, f'{tour}_points.json'), 'w') as wf:
    gj.dump(waypoints, wf)

grouped = data.groupby('day')
ft_list = []
for name, group in grouped:
    mls = gj.MultiLineString([
        [(row[1]['Longitude'], row[1]['Latitude']) for row in group.iterrows()]
    ])
    ft = gj.Feature(geometry=mls, properties={'date': name.strftime('%Y-%m-%d')})
    ft_list.append(ft)
daytracks = gj.FeatureCollection(ft_list)

with open(os.path.join(out_folder, f'{tour}_tracks.json'), 'w') as wf:
    gj.dump(daytracks, wf)

compl = wps.copy()
compl.extend(ft_list)
complete = gj.FeatureCollection(compl)
with open(json_out, 'w') as wf:
    gj.dump(complete, wf)

# one mls for tour model
multilinestring = gj.MultiLineString([
    [
        (row['Longitude'], row['Latitude']) for _, row in group.iterrows()
    ] for _, group in grouped
])

with open(os.path.join(out_folder, 'multilinestring.json'), 'w') as wf:
    gj.dump(multilinestring, wf)

import argparse
import os
import pandas as pd

# PROBLEM: SMOOSHES EVERYTHING WITH VALUE >= 3 DIGITS: lon=-125 --> lon=-12.5

parser = argparse.ArgumentParser()

parser.add_argument('JSON_In', help='The timestamped CSV location file')
parser.add_argument('Timestamp', help='mmddyyyy')

args = parser.parse_args()

dfile = open(args.JSON_In, 'r')
d = dfile.readlines()

lat = d[2::5]
lon = d[3::5]
time = d[4::5]
for i in range(len(lat)):
	lat[i] = float(lat[i][18:26])*10**-6
	lon[i] = float(lon[i][19:29])*10**-7
	time[i] = float(time[i][20:33])*10**-3

df = pd.DataFrame()
df['time'] = time
df['lat'] = lat
df['lon'] = lon
print(df)

directory = '{}/FilteredLocationsChunked_{}'.format(args.Timestamp, args.Timestamp)
if not os.path.exists(directory):
    os.makedirs(directory)

df.to_csv('{}FilteredLocationsFull_{}.csv'.format(args.Timestamp,args.Timestamp))
df[::len(df)//5000].to_csv('{}FilteredLocations5k_{}.csv'.format(args.Timestamp,args.Timestamp))
df[::len(df)//15000].to_csv('{}FilteredLocations15k_{}.csv'.format(args.Timestamp,args.Timestamp))
for i in range(32):
	df[i*len(df)//32:(i+1)*len(df)//32].to_csv('{}/FilteredLocationsChunked_{}/FilteredLocation{}of32_{}.csv'.format(args.Timestamp,args.Timestamp, (i+1), args.Timestamp))
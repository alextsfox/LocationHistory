import argparse
import os
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument('JSON_In', help='The filtered .json file')
parser.add_argument('CSV_Out_Dir', help='CSV out filename')

args = parser.parse_args()

dfile = open(args.JSON_In, 'r')
d = dfile.readlines()

lat = d[2::5]
lon = d[3::5]
t = d[4::5]

def getVal(data):
	for i in range(len(data)):

		val = ''
		number = False

		j = 0
		while True:

			if data[i][j] == ',':

				data[i] = float(val) * 10**-7
				break
			
			while not number:

				j += 1
				if data[i][j] == ':':

					j += 1
					number = True

			val += data[i][j]
			j += 1

getVal(lat)
getVal(lon)
for i in range(len(t)):
	t[i] = float(t[i][20:33]) * 10**-3

df = pd.DataFrame()
df['time'] = t
df['lat'] = lat
df['lon'] = lon
df['colorbar'] = [(1000*i)//len(t) for i in range(len(t))]
print(df)

df.to_csv('{}/FilteredLocationsFull.csv'.format(args.CSV_Out_Dir))
df[::len(df)//5000].to_csv('{}/FilteredLocations05k.csv'.format(args.CSV_Out_Dir))
df[::len(df)//15000].to_csv('{}/FilteredLocations15k.csv'.format(args.CSV_Out_Dir))


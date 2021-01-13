import os
import sys
import argparse
from time import time
import pandas as pd


parser = argparse.ArgumentParser()

parser.add_argument('jsonIn', help='The filtered .json file')
parser.add_argument('date', help='File date')

args = parser.parse_args()

dfile = open(args.jsonIn, 'r')
d = dfile.readlines()

# columns containing relevant data if the data formatting is screwed up after 
# this, you may need to open the filtered .json files yourself and find 
# the correct columns to use
lat = d[2::7]
lon = d[3::7]
t = d[4::7]
alt = d[5::7]
acc = d[6::7]

# converts JSON data into organized lists.
def getVal(data): # very fragile, do not mess with this
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
for i in range(len(alt)):
	if alt[i][16:-2] != 'null':
		alt[i] = float(alt[i][16:-2])
	else:
		alt[i] = -9999
for i in range(len(acc)):
	acc[i] = float(acc[i][16:])

# creating dataframe
df = pd.DataFrame()
df['time'] = t
df['lat'] = lat
df['lon'] = lon
df['alt'] = alt
df['acc'] = acc

print(df)

csvOut = 'csv-files/FilteredLocations_' + args.date

df.to_csv('{csvOut}_Full.csv'.format(csvOut=csvOut))

# optional. Just outputs a smaller dataset.
df[::len(df)//5000].to_csv('{csvOut}_005k.csv'.format(csvOut=csvOut))
df[::len(df)//15000].to_csv('{csvOut}_015k.csv'.format(csvOut=csvOut))
df[::len(df)//100000].to_csv('{csvOut}_100k.csv'.format(csvOut=csvOut))

print(df)
print('Successfully saved .csv files to {}'.format('/'.join(csvOut.split('/')[:-1])))
import os
import sys
import argparse
from time import time
import pandas as pd
import numpy as np


parser = argparse.ArgumentParser()

parser.add_argument('jsonIn', help='The filtered .json file')

args = parser.parse_args()

dfile = open(args.jsonIn, 'r')
d = dfile.readlines()

lat = d[2::5]
lon = d[3::5]
t = d[4::5]

# converts JSON data into organized lists.
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

# creating dataframe
df = pd.DataFrame()
df['time'] = t
df['lat'] = lat
df['lon'] = lon
df['colorbar'] = [(1000*i)//len(t) for i in range(len(t))]

csvOut = '/'.join(args.jsonIn.split('/')[:-1]) + '/FilteredLocations'

df.to_csv('{csvOut}_Full.csv'.format(csvOut=csvOut))
df[::len(df)//5000].to_csv('{csvOut}_005k.csv'.format(csvOut=csvOut))
df[::len(df)//15000].to_csv('{csvOut}_015k.csv'.format(csvOut=csvOut))
df[::len(df)//100000].to_csv('{csvOut}_100k.csv'.format(csvOut=csvOut))

print(df)
print('Successfully saved .csv files to {}'.format('/'.join(csvOut.slice('/')[:-1])))
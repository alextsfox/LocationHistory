import os
import sys
import argparse
from time import time
import pandas as pd
import numpy as np


parser = argparse.ArgumentParser()

parser.add_argument('jsonIn', help='The filtered .json file')
parser.add_argument('-s', '--slice', type=int, nargs=2, help='<start timestamp> <end timestamp> in seconds. Use this option if you only want to convert use a subset of the data.')

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


if args.slice is not None: # user specified a custom slice

	if args.slice[0] > 2*time() and args.slice[1] > 2*time():
		print('You entered a timeslice in the future. Aborting.')
		sys.exit()

	print('Creating custom files...')

	timeIndexA = 1
	timeIndexB = 1
	timestampA = args.slice[0]# - np.min(df.time)
	timestampB = args.slice[1]# - np.min(df.time)

	while df.iloc[timeIndexA]['time'] > timestampA:
		timeIndexA += len(df['time']//10000)
		if timeIndexA >= len(df['time']-1):
			timeIndexA = len(df['time']-2)
			break
	#print('timestampA', timestampA, 'timeIndexA', timeIndexA)

	while df.iloc[timeIndexB]['time'] > timestampB:
		timeIndexB += len(df['time']//10000)
		if timeIndexB >= len(df['time']-1):
			timeIndexB = len(df['time']-1)
			break

	#print('timestampB', timestampB, 'timeIndexB', timeIndexB)

	# print(timeIndexA)
	# print(timeIndexB)

	df = df[timeIndexA:timeIndexB]

	df.to_csv('{csvOut}_{start}-{end}_Full.csv'.format(start=args.slice[0], end=args.slice[1], csvOut=csvOut))
	df[::len(df)//5000].to_csv('{csvOut}_{start}-{end}_005k.csv'.format(start=args.slice[0], end=args.slice[1], csvOut=csvOut))
	df[::len(df)//15000].to_csv('{csvOut}_{start}-{end}_015k.csv'.format(start=args.slice[0], end=args.slice[1], csvOut=csvOut))
	df[::len(df)//100000].to_csv('{csvOut}_{start}-{end}_100k.csv'.format(start=args.slice[0], end=args.slice[1], csvOut=csvOut))

else:
	df.to_csv('{csvOut}_Full.csv'.format(csvOut=csvOut))
	df[::len(df)//5000].to_csv('{csvOut}_005k.csv'.format(csvOut=csvOut))
	df[::len(df)//15000].to_csv('{csvOut}_015k.csv'.format(csvOut=csvOut))
	df[::len(df)//100000].to_csv('{csvOut}_100k.csv'.format(csvOut=csvOut))

print(df)
print('Successfully saved .csv files to {}'.format('/'.join(csvOut.slice('/')[:-1])))

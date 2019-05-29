#takes a csv file as input, outputs a movie.
# this script is likely extremeluy volatile, and very innefficient. Only use on the output up csvParser.py or Location_History_TakeoutJSON_to_CSV.sh

import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import argparse
from datetime import datetime
import sys
import matplotlib as mpl
import time

print('saving preview image...')

def trim_to_box(arr, U,Le, Lo,R):
	UL = (U,Le)
	LR = (Lo,R)

	latList = np.copy(arr[:,2])
	latList[latList>UL[0]] = np.nan
	latList[latList<LR[0]] = np.nan
	
	lonList = np.copy(arr[:,3])
	lonList[lonList<UL[1]] = np.nan
	lonList[lonList>LR[1]] = np.nan

	dateList = np.copy(arr[:,1])
	if args.dates is not None:
		capDates = [int(date) for date in args.dates]
		stamp1 = time.mktime((capDates[0],capDates[1],capDates[2],0,0,0,0,0,0))
		stamp2 = time.mktime((capDates[3],capDates[4],capDates[5],0,0,0,0,0,0))
		dateList[dateList<stamp1] = np.nan
		dateList[dateList>stamp2] = np.nan

	newArr = np.hstack((
						arr[:,0][:,np.newaxis],
						dateList[:,np.newaxis],
						latList[:,np.newaxis],
						lonList[:,np.newaxis]))

	# remove nans
	newArr = newArr[~np.isnan(newArr).any(axis=1)]

	return newArr

# get csv file
def main():

	# load file in ascending time order, load (n x 1) arrays of lat, lon, and colorbar
	locHistRaw = np.loadtxt(args.csvIn, delimiter = ',', skiprows=1)[::-1]

	locHist = trim_to_box(locHistRaw, *args.trim)

	# incredibly messy way of getting an understandable timeline for the colorbar
	dateData = locHist[:,1]
	yyyymmdd = datetime.utcfromtimestamp(dateData[0]).strftime('%Y%m%d')
	decimalyearstart = float(yyyymmdd[:4] + '.' + str(int(int(yyyymmdd[4:6])/1.2)))
	colorData = ((dateData-dateData[0]))/3.1536E7 + decimalyearstart
	#print(colorData)
	# locHist = trim_to_box(locHist, *args.trim)

	lat = locHist[:,2]
	lon = locHist[:,3]

	ratio = (args.trim[3]-args.trim[1])/(args.trim[0]-args.trim[2])
	width=100
	fig = plt.figure(figsize=(width,width/ratio), dpi=100)
	scat = plt.scatter(lon,lat, c=colorData, s=1, cmap='viridis_r')

	#CONUS, visuals
	#configure figure style, restrict to box
	plt.xlim(args.trim[1], args.trim[3])
	plt.ylim(args.trim[2], args.trim[0])
	#plt.clim(colorData[0], colorData[-1])
	#plt.colorbar()
	plt.axis('off')


	plt.savefig(args.pngOut)
	print('preview image successfully saved')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('csvIn', help='location history CSV file')
	parser.add_argument('pngOut', help='out file path')

	parser.add_argument('-d', '--dates', nargs=6, help='span of dates to plot.  Usage: <yyyy1> <mm1> <dd1> <yyyy2> <mm2> <dd2>')

	requiredNamed = parser.add_argument_group('required named arguments')
	requiredNamed.add_argument('-t', '--trim', nargs=4, required=True, type=float, help='Trim the output to a box with corners <north border> <west border> <south border> <east border>')

	args = parser.parse_args()

	main()
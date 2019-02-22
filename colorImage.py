#takes a csv file as input, outputs a movie.
# this script is likely extremeluy volatile, and very innefficient. Only use on the output up csvParser.py or Location_History_TakeoutJSON_to_CSV.sh

import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import argparse
from datetime import datetime
import sys
import matplotlib as mpl

# def trim_to_box(arr, U,Le,Lo,R):
# 	UL = (U,Le)
# 	LR = (Lo,R)

# 	print(UL, LR)
# 	latList = np.copy(arr[:,2])
# 	print(latList)
# 	latList[latList>UL[0]] = np.nan
# 	latList[latList<LR[0]] = np.nan

# 	lonList = np.copy(arr[:,3])
# 	lonList[lonList<UL[1]] = np.nan
# 	lonList[lonList>LR[1]] = np.nan

# 	newArr = np.hstack((
# 						arr[:,0][:,np.newaxis],
# 						arr[:,1][:,np.newaxis],
# 						latList[:,np.newaxis],
# 						lonList[:,np.newaxis]
# 						))

# 	# remove nans
# 	newArr = newArr[~np.isnan(newArr).any(axis=1)]

# 	return newArr

print('saving preview image...')

# get csv file
parser = argparse.ArgumentParser()
parser.add_argument('csvIn', help='location history CSV file')
parser.add_argument('pngOut', help='out file path')

requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-t', '--trim', nargs=4, required=True, type=float, help='Trim the output to a box with corners <north border> <west border> <south border> <east border>')

args = parser.parse_args()

# load file in ascending time order, load (n x 1) arrays of lat, lon, and colorbar
locHist = np.loadtxt(args.csvIn, delimiter = ',', skiprows=1)[::-1]

# incredibly messy way of getting an understandable timeline for the colorbar
dateData = locHist[:,1]
yyyymmdd = datetime.utcfromtimestamp(dateData[0]).strftime('%Y%m%d')
decimalyearstart = float(yyyymmdd[:4] + '.' + str(int(int(yyyymmdd[4:6])/1.2)))
colorData = ((dateData-dateData[0]))/3.1536E7 + decimalyearstart

# locHist = trim_to_box(locHist, *args.trim)

lat = locHist[:,2]
lon = locHist[:,3]

ratio = (args.trim[3]-args.trim[1])/(args.trim[0]-args.trim[2])
width=60
fig = plt.figure(figsize=(width,width/ratio))
scat = plt.scatter(lon,lat, c=colorData, s=1, cmap='viridis_r')

#CONUS, visuals
#configure figure style, restrict to box
plt.xlim(args.trim[1], args.trim[3])
plt.ylim(args.trim[2], args.trim[0])
# plt.xlim(-125,-65)
# plt.ylim(25,50)
plt.clim(colorData[0], colorData[-1])
mpl.rcParams.update({'font.size': 42})
plt.colorbar()

plt.axis('off')

plt.savefig(args.pngOut)
print('preview image successfully saved')
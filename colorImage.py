#takes a csv file as input, outputs a movie.
# this script is likely extremeluy volatile, and very innefficient. Only use on the output up csvParser.py or Location_History_TakeoutJSON_to_CSV.sh

import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import argparse
from datetime import datetime
import sys

print('saving preview image...')
# get csv file
parser = argparse.ArgumentParser()
parser.add_argument('fileIn', help='location history CSV file')
parser.add_argument('fileOut', help='out file path')
args = parser.parse_args()

# load file in ascending time order, load (n x 1) arrays of lat, lon, and colorbar
locHist = np.loadtxt(args.fileIn, delimiter = ',', skiprows=1)[::-1]

# incredibly messy way of getting an understandable timeline for the colorbar
dateData = locHist[:,1]
yyyymmdd = datetime.utcfromtimestamp(dateData[0]).strftime('%Y%m%d')
decimalyearstart = float(yyyymmdd[:4] + '.' + str(int(int(yyyymmdd[4:6])/1.2)))
colorData = ((dateData-dateData[0]))/3.1536E7 + decimalyearstart

lat = locHist[:,2]
lon = locHist[:,3]

# creating figure object
fig = plt.figure(figsize=(120,80))

# for some reason, when we give it an empty array, it spazzes out, so we give it empty slices.
scat = plt.scatter(lon,lat, c=colorData, s=.4, cmap='viridis_r')

#colorbar and axis limits

#CONUS
plt.xlim(-125,-65)
plt.ylim(25,50)

#Northeast corridor
# plt.xlim(-82.,-73.9)
# plt.ylim(38.,40.83)

plt.clim(colorData[0], colorData[-1])
plt.axis('off')

plt.savefig(args.fileOut)
print('preview image successfully saved')
#takes a csv file as input, outputs a movie.
# this script is likely extremeluy volatile, and very innefficient. Only use on the output up csvParser.py or Location_History_TakeoutJSON_to_CSV.sh

import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import argparse
from datetime import datetime
import sys
from time import time as MEASURETIME

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
fig = plt.figure(figsize=(30,20))

# for some reason, when we give it an empty array, it spazzes out, so we give it empty slices.
scat = plt.scatter(lon[:1],lat[:1], c=colorData[:1], s=2, cmap='viridis_r')

#colorbar and axis limits

#CONUS
plt.xlim(-125,-65)
plt.ylim(25,50)
plt.clim(colorData[0], colorData[-1])
plt.axis('off')

#print('Ideal Timestep: ', (colorData[-1] - colorData[0])/3600)
#The number of points per frame by timestamp so that in the end we have a ~120 second movie

# a pretty progress bar
def update_progress(progress):
    barLength = 63 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\r[{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress*100,2), status)
    sys.stdout.write(text)
    sys.stdout.flush()

# time to advance each frame for timewise normalization
def getPtsThisFrame(i):
	
	timestep = (colorData[-1] - colorData[0])/10800
	
	# count datapoints ahead until we see that the number of points we've advanced through exceeds the timestep 
	indexStep = 0#i
	while timestep > 0:
		timestep -= (colorData[i + indexStep+1] - colorData[i + indexStep])
		indexStep += 1
	#print(i,len(colorData), 'IndexStep',indexStep, 'TrueTimeStep', colorData[i+indexStep]-colorData[i], 'TimeStepRemainder',timestep)

	nextIndex = i+indexStep
	# return the proper number of frames to advance to
	return nextIndex

k=0
l = 0
# calculate the number of frames we'll need
def mockAnimate(i, X=lon, Y=lat, T=colorData):
	global k
	global l
	
	try:
		global k
		nextIndex = getPtsThisFrame(k)
		k = nextIndex
		l += 1
		# set_offsets needs an nx2 array, so we use hstack to rotate and stack our arrays.
	
	# sneaky when we've run out the end of our data, trigger the save and exit condition.
	except IndexError as err:
		return l	

# initial frame function is an empty colorbar and empty point array
def init():

	scat.set_offsets([])
	scat.set_array([])

	return scat,

j=0
for m in range(len(colorData)):
	if mockAnimate(m) is not None:
		numFrames = mockAnimate(m)

# actual animation function
def animate(i, X=lon, Y=lat, T=colorData):

	
	try:
		global j

		# find what the next frame's index is
		nextIndex = getPtsThisFrame(j)
		j = nextIndex

		# set_offsets needs an nx2 array, so we use hstack to rotate and stack our arrays.
		XY = np.hstack((X[:nextIndex,np.newaxis], Y[:nextIndex, np.newaxis]))
		scat.set_offsets(XY)

		# who knows why we need this np.ravel thing? I don't.
		scat.set_array(np.ravel(T[:nextIndex]))

		# our progress bar
		update_progress(i/numFrames)
	
	# gets rid of issues with running off the end of our dataset
	except IndexError as err:
		pass

	return scat,

# frame speed, ms
interval = 0
print('starting animation...')
animation = anim.FuncAnimation(fig, animate, init_func=init,frames=numFrames, interval=interval, blit=True)#True)
print('animating...')
t2 = MEASURETIME()
animation.save(args.fileOut, fps=500, extra_args=['-vcodec', 'libx264'])
t1 = MEASURETIME()
t0 = (t2-t1)/3600
print('It took {} hours to make the movie.'.format(t0))
print('successfully saved as', args.fileOut)


#takes a csv file as input, outputs a movie.

import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import argparse
from datetime import datetime

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
fig = plt.figure(figsize=(20,10))

# for some reason, when we give it an empty array, it spazzes out, so we give it empty slices.
scat = plt.scatter(lon[:1],lat[:1], c=colorData[:1], s=0.4)

#colorbar and axis limits
plt.xlim(-100,-65)
plt.ylim(35,45)
plt.clim(colorData[0], colorData[-1])
plt.axis('off')

#print('Ideal Timestep: ', (colorData[-1] - colorData[0])/3600)
#The number of points per frame by timestamp so that in the end we have a 60 second movie
def getPtsThisFrame(i):

	# time to advance this frame
	timestep = (colorData[-1] - colorData[0])/3600


	# count frames ahead until we see that the timestep is below the threshold
	indexStep = 0#i
	while timestep > 0:
		try:
			timestep -= (colorData[i + indexStep+1] - colorData[i + indexStep])
			indexStep += 1
		except IndexError as err:
			break

	#print(i,len(colorData), 'IndexStep',indexStep, 'TrueTimeStep', colorData[i+indexStep]-colorData[i], 'TimeStepRemainder',timestep)

	nextIndex = i+indexStep
	# return the proper number of frames to advance to
	return nextIndex

# initial frame function is an empty colorbar and empty point array
def init():

	scat.set_offsets([])
	scat.set_array([])

	return scat,

# animation function progressively adds points by plotting slices [:i] iteratively.
def animate(i, X=lon, Y=lat, T=colorData):

	nextIndex = getPtsThisFrame(i)

	# set_offsets needs an nx2 array, so we use hstack to rotate and stack our arrays.
	XY = np.hstack((X[:nextIndex,np.newaxis], Y[:nextIndex, np.newaxis]))
	scat.set_offsets(XY)
	# who knows why we need this?
	scat.set_array(np.ravel(T[:nextIndex]))

	return scat,

# frame speed, ms
interval = 0
numFrames = len(colorData)

print('starting animation...')
animation = anim.FuncAnimation(fig, animate, init_func=init,frames=numFrames, interval=interval, blit=True)#True)
print('saving...')
animation.save(args.fileOut, fps=500, extra_args=['-vcodec', 'libx264'])
print('saved')
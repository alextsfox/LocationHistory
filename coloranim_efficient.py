# takes a csv file given by csvParser.py, makes a movie of it (or rather, series of movies)

import matplotlib.pyplot as plt
import matplotlib.animation as animate
import numpy as np
import argparse
from datetime import datetime
import sys

# take a unix timestamp in seconds, convert to a decimal of a year
def get_decimal_year(timestamp):
	# timestamp: unix timestamp, int

	yyyymmdd = datetime.utcfromtimestamp(timestamp).strftime('%Y%m%d')
	decimalYear = float(yyyymmdd[:4] + '.' + str(int(int(yyyymmdd[4:6])/1.2)))

	return decimalYear

# a nice looking progress bar
def update_progress(progress):
	# progress: float or int

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

# this function performs normalizes the frame length by timestamp
# otherwise, each frame would span an arbitrary amount of time.
def get_next_index(i, timestep):
	# i is an iterable integer
	# needs to output an index value to jump to
	
	# adjust the number datapoints to advance incrementally until the desired timestep is reached
	di = 0
	while timestep > 0:
		timestep -= (colorData[i+di + 1] - colorData[i+di])
		indexStep += 1

	nextIndex = i+indexStep
	# return the proper number of frames to advance to
	return nextIndex

# creates an array of the data point indexes to stop each frame at
def get_frame_list(dataArray, timestep):
	# data is an nxn array
	# timestep is a float

	# create a list of indexes to slice frames at
	indexList = []
	nextIndex = 0
	while nextIndex < len(data):
		indexList.append(nextIndex)
		nextIndex = get_next_index(nextIndex, timestep)

	# initialize and fill out an n x m x 3 array where each entry contains data for a frame
	frames = []
		for i in indexList[:-1]:
		frames.append(dataArray[i]:dataArray[i+1])

	# frames[i] give all the data points needed to create a frame
	return frames

def init():
	scat.set_offsets([])
	scat.set_array([])

	return scat,

def animate(i, dataArray):

	scat.set_offsets(dataArray[:i,:2:-1])
	scat.set_array(np.ravel(dataArray[:i,2]))
	# scat.set_array(dataArray[:i,2])
	update_progress(i/numFrames)

	return scat,

def main():
	# load file in ascending time order, load (n x 1) arrays of lat, lon, and colorbar
	locHist = np.loadtxt(args.fileIn, delimiter = ',', skiprows=1)[::-1]
	lat = locHist[:,2]
	lon = locHist[:,3]
	start_date = get_decimal_year(dateData[0])
	colorData = ((dateData-dateData[0]))/3.1536E7 + start_date

	# organize data into an nx3 array, where each row is timestamped
	dataArray = np.hstack(
		lat[:,np.newaxis],
		lon[:,np.newaxis],
		colorData[:,np.newaxis]
		)
						  			
	# figure framework, starting with an empty plot
	fig = plt.figure(figsize=(30,20))
	scat = plt.scatter(
		dataArray[:1,1],
		dataArray[:1,0], 
		c=dataArray[:1,2], 
		s=2, 
		cmap='viridis_r')

	#configure figure style, restrict to CONUS
	plt.xlim(-125,-65)
	plt.ylim(25,50)
	plt.clim(colorData[0], colorData[-1])
	plt.axis('off')

	# approx. 1 frame per day
	timestep = 1/365.25
	# each element of frames is the datapoints to make up a given frame
	frames = get_frame_list(dataArray, timestep)
	numFrames = len(frames)

	# create animation
	anim = animate.FuncAnimation(
		fig, 
		animate, 
		fargs=(dataArray),
		init_func=init,
		frames=numFrames,
		interval=0,
		blit=True)

	plt.show()
	#anim.save(args.fileOut, fps=30, extra_args=['-vcodec', 'libx264'])
	print('succesfully saved as', args.fileOut)

if __name__ == '__main__':
	
	# get csv file and outpath
	parser = argparse.ArgumentParser()
	parser.add_argument('fileIn', help='location history CSV file')
	parser.add_argument('fileOut', help='out file path')
	args = parser.parse_args()



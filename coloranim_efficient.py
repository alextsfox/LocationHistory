#  takes a csv file given by csvParser.py, makes a movie of it (or rather, series of movies)
import numpy as np
import argparse
from datetime import datetime
import sys

# a nice looking progress bar
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

# trims data to exclude everything outside of a given box
def trim_to_box(arr, U,Le, Lo,R):
	UL = (U,Le)
	LR = (Lo,R)

	latList = np.copy(arr[:,0])
	latList[latList>UL[0]] = np.nan
	latList[latList<LR[0]] = np.nan

	lonList = np.copy(arr[:,1])
	lonList[lonList<UL[1]] = np.nan
	lonList[lonList>LR[1]] = np.nan

	newArr = np.hstack((
						latList[:,np.newaxis],
						lonList[:,np.newaxis],
						arr[:,2][:,np.newaxis],
						arr[:,3][:,np.newaxis]))

	# remove nans
	newArr = newArr[~np.isnan(newArr).any(axis=1)]

	return newArr
						
# take a unix timestamp in seconds, convert to a decimal of a year
def get_decimal_year(timestamp):
	# timestamp: unix timestamp, int

	yyyymmdd = datetime.utcfromtimestamp(timestamp).strftime('%Y%m%d')
	decimalYear = float(yyyymmdd[:4] + '.' + str(int(int(yyyymmdd[4:6])/1.2)))

	return decimalYear

# this function performs normalizes the frame length by timestamp
# otherwise, each frame would span an arbitrary amount of time.
def get_next_index(i, timestep, colorData):
	# i is an iterable integer
	# needs to output an index value to jump to
	
	# adjust the number datapoints to advance incrementally until the desired timestep is reached
	di = 0
	while timestep > 0:
		timestep -= (colorData[i+di + 1] - colorData[i+di])
		di += 1

	nextIndex = i + di
	# return the proper number of frames to advance to
	return nextIndex

# creates an array of the movie frames.
# You may notice that this file has the name "efficient" in the title. Please note that "efficient" is used as purely a relative term here.
# Don't judge me.
def get_frame_list(dataArray, timestep, colorData):
	# data is an nxn array
	# timestep is a float

	# create a list of indexes to slice frames at
	indexList = []
	nextIndex = 0
	while nextIndex < len(dataArray) - 1:
		indexList.append(nextIndex)
		try:
			nextIndex = get_next_index(nextIndex, timestep, colorData)
		except IndexError as err:
			break

	# initialize and fill out an n x m x 3 array where each entry contains data for a frame
	frames = np.empty( (len(indexList)-1, len(dataArray), len(dataArray[0])) )
	frames[:] = -9999
	
	frames = np.delete(frames, np.s_[-2:], axis=1)
	
	print('Creating movie frames...')
	for i in range(len(indexList) - 1):
		frames[i,:indexList[i+1]] = dataArray[:indexList[i+1]]

	

	# frames[i] give all the data points needed to create a frame
	return frames, indexList

# sets the 30 most recent frames to black and large, all others to grey
def set_grey_frames(frames, indexList):
	# n x m x 3 array of frames

	newFrames = np.copy(frames)
	newFrames[:,:,2:] = [1.,9.]

	# 30 most recent frames set to black and large, all others are a slightly dim grey
	for i in range(12,len(newFrames)-1):

		# number of points added since last 20 frames.
		fiveFramesAgo = indexList[i-12]
		# in the current frame, set all "stale" points to be small and grey
		newFrames[i,:fiveFramesAgo,2:] = [0.6,2.]

	newFrames[-1,:,2:] = [0.6,2.]

	return newFrames

if __name__ == '__main__':
	
	# get csv file and outpath
	parser = argparse.ArgumentParser()
	parser.add_argument('fileIn', help='location history CSV file')

	requiredNamed = parser.add_argument_group('required named arguments')
	requiredNamed.add_argument('-t', '--trim', nargs=4, required=True, type=float, help='Trim the output to a box with corners <north border> <west border> <south border> <east border>')
	
	args = parser.parse_args()

	# load file in ascending time order, load (n x 1) arrays of lat, lon, and colorbar
	locHist = np.loadtxt(args.fileIn, delimiter = ',', skiprows=1)[::-1]
	dateData = locHist[:,1]
	lat = locHist[:,2]
	lon = locHist[:,3]
	start_date = get_decimal_year(dateData[0])
	colorData = ((dateData-dateData[0]))/3.1536E7 + start_date

	# organize data into an nx3 array, where each row is timestamped
	# fourth column is the size column
	dataArray = np.hstack((
			lat[:,np.newaxis],
			lon[:,np.newaxis],
			colorData[:,np.newaxis],
			2*np.ones_like(colorData[:,np.newaxis])
		))

	dataArray = trim_to_box(dataArray, *args.trim)

	# approx. 3 frame per day
	timestep = 1/(3*365.25)
	# each element of frames is the datapoints to make up a given frame
	frames, indexList = get_frame_list(dataArray, timestep, colorData)
	frames = set_grey_frames(frames, indexList)
	
	np.save('frames', frames)
	np.save('indexList', indexList)
	print('created frames.npy and indexList.npy')



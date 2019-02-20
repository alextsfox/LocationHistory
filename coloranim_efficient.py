#  takes a csv file given by csvParser.py, makes a movie of it (or rather, series of movies)
import matplotlib.pyplot as plt
import matplotlib.animation as make_animate
import numpy as np
import argparse
from datetime import datetime
import sys
from time import time as get_time

# take a unix timestamp in seconds, convert to a decimal of a year
def get_decimal_year(timestamp):
	# timestamp: unix timestamp, int

	yyyymmdd = datetime.utcfromtimestamp(timestamp).strftime('%Y%m%d')
	decimalYear = float(yyyymmdd[:4] + '.' + str(int(int(yyyymmdd[4:6])/1.2)))

	return decimalYear

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

# creates an array of the data point indexes to stop each frame at
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
	frames = []
	for i in range(len(indexList) - 1):
		frames.append(dataArray[:indexList[i+1]])

	# frames[i] give all the data points needed to create a frame
	return frames

# initialize an empty plot
def init():
	scat.set_offsets([])
	scat.set_array([])
	scat.set_sizes([])

	return scat,

# animation function called by FuncAnimation
def animate(i, frames,t):
	# iterable i
	# n x m x 3 array frames
	# float t

	scat.set_offsets(frames[i][:,1::-1])
	scat.set_array(np.ravel(frames[i][:,2]))
	scat.set_sizes(np.ravel(frames[i][:,3]))
	# scat.set_array(dataArray[:i,2])
	#update_progress(i/numFrames)
	t.append(get_time())
	# print(frames[:i,:].shape)

	return scat,

# sets the 30 most recent frames to black and large, all others to grey
def set_grey_frames(frames):
	# n x m x 3 array of frames

	newFrames = frames.copy()

	for i in range(30):
		# print('<30, changing')
		newFrames[i][:,2] = 1
		newFrames[i][:,3] = 100
		# print(newFrames[i][:,2:])
			
	#print(newFrames[2])

	# 30 most recent frames set to black and large, all others are a slightly dim grey
	for i in range(30,len(newFrames)):
		newFrames[i][:,2] = 0.3
		newFrames[i][:,3] = 2

		# if i<50:
		# 	print('step1, everything should be .3,2\n', newFrames[i][:,2:])

		frameIndexSpan = len(newFrames[i]) - len(newFrames[i-30])

		newFrames[i][-frameIndexSpan:,2] = 1
		newFrames[i][-frameIndexSpan:,3] = 100

		# if i<50:
		# 	print('step2, the tail of newFrames should be 1, 100\n', newFrames[i][:,2:])

		newFrames[i][:-frameIndexSpan,2] = 0.3
		newFrames[i][:-frameIndexSpan,3] = 2

		# if i<50:
		# 	print('step3, everything from the start to -frameIndexSpan should be .3,2\n', newFrames[i][:,2:])

		if i<50:
			print('in loop\n',newFrames[i][:,2:])

	for i in range(50):
		print('out of loop\n',newFrames[i])

	return newFrames

if __name__ == '__main__':
	
	# get csv file and outpath
	parser = argparse.ArgumentParser()
	parser.add_argument('fileIn', help='location history CSV file')
	parser.add_argument('fileOut', help='out file path')
	args = parser.parse_args()

	# load file in ascending time order, load (n x 1) arrays of lat, lon, and colorbar
	locHist = np.loadtxt(args.fileIn, delimiter = ',', skiprows=1)[::-10]
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
						  			
	# figure framework, starting with an empty plot
	fig = plt.figure(figsize=(30,20))
	scat = plt.scatter(
		dataArray[:1,1],
		dataArray[:1,0], 
		c=dataArray[:1,2], 
		s=dataArray[:1,3], 
		cmap='Greys')
	
	#configure figure style, restrict to CONUS
	plt.xlim(-125,-65)
	plt.ylim(30,50)
	plt.clim(colorData[0], colorData[-1])
	plt.axis('off')

	# approx. 1 frame per day
	timestep = 1/(3*365.25)
	# each element of frames is the datapoints to make up a given frame
	frames = get_frame_list(dataArray, timestep, colorData)
	frames = set_grey_frames(frames)
	plt.clim(0,1)
	numFrames = len(frames)

	# for i in range(100):
	# 	print(frames[i])

	# for i in range(len(frames)):
	# 	print(i,'\n', frames[i])

	# create animation
	t=[] #for tracking render time

	anim = make_animate.FuncAnimation(
		fig, 
		animate, 
		fargs=(frames,t),
		init_func=init,
		frames=numFrames,
		interval=0,
		blit=True)



	# plt.show()
	anim.save(args.fileOut, fps=30, extra_args=['-vcodec', 'libx264'])
	print('\nsuccesfully saved as', args.fileOut)

	t_diff=[]
	for i in range(1,len(t)):
		t_diff.append(t[i]-t[i-1])

	t_diff_smooth = []
	for i in range(len(t_diff) - 21):
		t_diff_smooth.append(np.mean(t_diff[i:i+20]))

	fig2, ax1 = plt.subplots()
	ax1.plot(range(len(t)), t, 'b-')
	ax1.set_xlabel('number of frames')
	# Make the y-axis label, ticks and tick labels match the line color.
	ax1.set_ylabel('total time', color='b')
	ax1.tick_params('y', colors='b')

	ax2 = ax1.twinx()
	ax2.plot(range(len(t_diff_smooth)),t_diff_smooth, 'r-')
	ax2.set_ylabel('time per frame', color='r')
	ax2.tick_params('y', colors='r')
	fig2.tight_layout()
	plt.show()



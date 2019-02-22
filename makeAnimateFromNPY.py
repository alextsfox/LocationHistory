import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse
import sys
import os
from time import time as get_time

# displays analytics at the end
def t_diff(t):

	# frame render time array
	t_diff=[]
	for i in range(1,len(t)):
		t_diff.append(t[i]-t[i-1])

	# low-pass filter
	t_diff_smooth = []
	for i in range(len(t_diff) - 21):
		t_diff_smooth.append(np.mean(t_diff[i:i+20]))

	fig2, ax1 = plt.subplots()
	ax1.plot(range(len(t)), t, 'b-')
	ax1.set_xlabel('number of frames')
	
	ax1.set_ylabel('total render time', color='b')
	ax1.tick_params('y', colors='b')

	ax2 = ax1.twinx()
	ax2.plot(range(len(t_diff_smooth)),t_diff_smooth, 'r-')
	ax2.set_ylabel('render time per frame', color='r')
	ax2.tick_params('y', colors='r')

	plt.title('Animation analytics')
	fig2.tight_layout()
	
	return fig2

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

# initialize an empty plot
def init():
	scat.set_offsets([])
	scat.set_array([])
	scat.set_sizes([])

	return scat,

# animation function called by FuncAnimation
def animate(i, frames,t, indexList):
	# iterable i
	# n x m x 3 array frames
	# float t

	# what's with this weird indexing [1::-1]? X = lat, Y = lon, and the file is organized by [lat,lon] = [y,x], so we index backwards.
	scat.set_offsets(frames[i,:indexList[i],1::-1])
	scat.set_array(np.ravel(frames[i,:indexList[i],2]))
	scat.set_sizes(np.ravel(frames[i,:indexList[i],3]))

	# progress bar and analytics
	update_progress(i/numFrames)
	t.append(get_time())

	return scat,

if __name__=='__main__':

	# get csv file and outpath
	parser = argparse.ArgumentParser()
	parser.add_argument('fileOut', help='out file path')
	parser.add_argument('-v', '--verbose', help='advanced analytics at the end', action='store_true')

	requiredNamed = parser.add_argument_group('required named arguments')
	requiredNamed.add_argument('-t', '--trim', nargs=4, required=True, type=float, help='Trim the output to a box with corners <north border> <west border> <south border> <east border>')

	args = parser.parse_args()

	t1 = [] # for tracking render time

	# frames + information on how long each frame is
	frames = np.load('frames.npy')
	indexList = np.load('indexList.npy')
	os.remove('frames.npy')
	os.remove('indexList.npy')

	print('frames.npy and indexList.npy successfully loaded and deleted.')

	numFrames = len(frames)
	timestep = 1/(3*365.25)

	# figure framework, starting with an empty plot
	ratio = (args.trim[3]-args.trim[1])/(args.trim[0]-args.trim[2])
	width = 30
	fig = plt.figure(figsize=(width,width/ratio), dpi=100)
	scat = plt.scatter(
		frames[:1,1],
		frames[:1,0], 
		c=frames[:1,2], 
		s=frames[:1,3], 
		cmap='Greys')

	#configure figure style, restrict to box
	# maxLat, minLat = np.max(frames[-1,:,0][frames[-1,:,0]!= -9999]), np.min(frames[-1,:,0][frames[-1,:,0]!= -9999])
	# maxLon, minLon = np.max(frames[-1,:,1][frames[-1,:,1]!= -9999]), np.min(frames[-1,:,1][frames[-1,:,1]!= -9999])
	plt.xlim(args.trim[1], args.trim[3])
	plt.ylim(args.trim[2], args.trim[0])
	plt.axis('off')
	plt.clim(0,1)

	print('Saving animation...')
	anim = animation.FuncAnimation(
			fig, 
			animate, 
			fargs=(frames,t1,indexList),
			init_func=init,
			frames=numFrames, 
			interval=1, 
			blit=True)

	anim.save(args.fileOut, fps=24, extra_args=['-vcodec', 'libx264'])
	print('\nsuccesfully saved as', args.fileOut)



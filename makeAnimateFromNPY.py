import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse
import sys
import os
from time import time as get_time


def t_diff(t):
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
	#print(frames.shape)
	scat.set_offsets(frames[i,:indexList[i],:2])
	scat.set_array(np.ravel(frames[i,:indexList[i],2]))
	scat.set_sizes(np.ravel(frames[i,:indexList[i],3]))
	update_progress(i/numFrames)
	t.append(get_time())


	return scat,

if __name__=='__main__':

	# get csv file and outpath
	parser = argparse.ArgumentParser()
	parser.add_argument('fileIn', help='movie frames CSV file')
	parser.add_argument('fileOut', help='out file path')
	args = parser.parse_args()

	t = [] # for tracking render time

	# frames + information on how long each frame is
	frames = np.load(args.fileIn)
	os.remove(args.fileIn)
	print(args.fileIn, 'successfully loaded and deleted.')
	numFrames = len(frames)
	timestep = 1/(3*365.25)

	#print(frames[:10])
	
	indexList = []
	for frame in frames:
		indexList.append(len(frame))

	# figure framework, starting with an empty plot
	fig = plt.figure(figsize=(30,20))
	scat = plt.scatter(
		frames[:1,1],
		frames[:1,0], 
		c=frames[:1,2], 
		s=frames[:1,3], 
		cmap='Greys')

	#configure figure style, restrict to CONUS
	plt.xlim(-125,-65)
	plt.ylim(30,50)
	plt.axis('off')
	plt.clim(0,1)

	anim = animation.FuncAnimation(
			fig, 
			animate, 
			fargs=(frames,t,indexList),
			init_func=init,
			frames=numFrames, 
			interval=1, 
			blit=True)

	anim.save(args.fileOut, fps=30, extra_args=['-vcodec', 'libx264'])
	print('\nsuccesfully saved as', args.fileOut)

	tplot = t_diff(t)
	plt.show(tplot)



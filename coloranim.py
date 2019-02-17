import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import argparse

# get csv file
parser = argparse.ArgumentParser()
parser.add_argument('fileIn', help='location history CSV file')
args = parser.parse_args()

# load file in ascending time order, load (n x 1) arrays of lat, lon, and colorbar
locHist = np.loadtxt(args.fileIn, delimiter = ',', skiprows=1)[::-1]
colorData = locHist[:,0]
lat = locHist[:,2]
lon = locHist[:,3]

numFrames = len(colorData)

# creating figure object
fig = plt.figure()

# for some reason, when we give it an empty array, it spazzes out, so we give it empty slices.
scat = plt.scatter(lon[:1],lat[:1], c=colorData[:1], s=10, cmap='viridis')

# initial frame function is an empty colorbar and empty point array
def init():

	scat.set_offsets([])
	scat.set_array([])

	return scat,

# animation function progressively adds points by plotting slices [:i] iteratively.
def animate(i, X=lon, Y=lat, T=colorData):

	# set_offsets needs an nx2 array, so we use hstack to rotate and stack our arrays.
	XY = np.hstack((X[:i,np.newaxis], Y[:i, np.newaxis]))
	scat.set_offsets(XY)
	# who knows why we need this?
	scat.set_array(np.ravel(T[:i]))

	return scat,

# frame speed, ms
interval = 0

#print(interval)
plt.xlim(-100,-65)
plt.ylim(35,45)
print('starting animation')
animation = anim.FuncAnimation(fig, animate, init_func=init,frames=numFrames, interval=interval, blit=True,)
print('saving...')
animation.save('animtest.mp4', fps=500, extra_args=['-vcodec', 'libx264'])
print('saved')
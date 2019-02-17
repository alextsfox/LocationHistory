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
colorData = np.array([(x, 0, 1-x) for x in locHist[:,0]])
lat = locHist[:,2]
lon = locHist[:,3]

numFrames = len(colorData)

# creating figure object
fig = plt.figure()
scat = plt.scatter([],[], s=10)#, c=[], cmap='viridis')

# initial frame function is an empty colorbar and empty point array
def init():

	scat.set_offsets([])
	#scat.set_array([])

	return scat,

# animation function progressively adds points by plotting slices [:i] iteratively.
def animate(i, X=lon, Y=lat, T=colorData):

	# set_offsets needs an nx2 array, so we use hstack to rotate and stack our arrays.
	#print(len(X))
	XY = np.hstack((X[:i,np.newaxis], Y[:i, np.newaxis]))
	print(XY)
	print(XY.shape)
	scat.set_offsets(XY)
	#scat.set_array(T)

	return scat,

# frame speed, ms
interval = 10

#print(interval)
plt.xlim(-100,-65)
plt.ylim(35,45)
animation = anim.FuncAnimation(fig, animate, init_func=init,frames=numFrames, interval=interval, blit=True,)

plt.show()



# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.animation as animation

# def main():
#     numframes = 100
#     numpoints = 10
#     color_data = np.random.random((numframes, numpoints))
#     x, y, c = np.random.random((3, numpoints))

#     fig = plt.figure()
#     scat = plt.scatter(x, y, c=c, s=100)

#     ani = animation.FuncAnimation(fig, update_plot, frames=xrange(numframes),
#                                   fargs=(color_data, scat))
#     plt.show()

# def update_plot(i, data, scat):
#     scat.set_array(data[i])
#     return scat,

# main()
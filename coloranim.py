import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('fileIn', help='location history CSV file')
args = parser.parse_args()

locHist = np.loadtxt(args.fileIn, delimiter = ',', skiprows=1)
colorData = locHist[:,0::-1]
lat, lon = locHist[:,2::-1], locHist[:,3::-1]

numFrames = len(colorData)

fig = plt.figure()
# ax = plt.axes(xlim=(-100.,-68.), ylim=(35.,50.))
# line, = ax.plot([],[], linestyle='None', marker='o', markersize=2, c=colorData[0])
scat = plt.scatter([],[], s=2 , c=[(0,0,0)])

def init():

	scat.set_array([],[],[])

	return scat,

def animate(i, X, Y, T):

	X = X[:i]
	Y = Y[:i]
	T = T[:i]
	scat.set_array(T)
	scat.set_offsets(X,Y)

	return scat,

interval = 20/numFrames

print(interval)
animation = anim.FuncAnimation(fig, animate, 
							   init_func=init, frames=numFrames, interval=interval, blit=True,
							   fargs=(lon, lat, colorData))
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
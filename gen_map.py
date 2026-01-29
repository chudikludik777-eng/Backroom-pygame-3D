import numpy as np
from numba import njit

@njit
def main(size):
	map = np.random.choice(np.array([True,False]), (size, size))
	map[0,:], map[size-1,:], map[:,0], map[:,size-1] = (True, True, True, True)
	
	xpos, ypos, rot = 1.5, 1.5, np.pi/4 # start position
	x, y = int(xpos), int(ypos)
	map[x][y] = 0
	
	# random walk through maze until other side is reached, clearing walls as necessary and
	# placing exit on other side
	count = 0
	while True:
		xtest, ytest = (x, y)
		if np.random.choice(np.array([True, False])):
			xtest += np.random.choice(np.array([-1, 1]))
		else:
			ytest += np.random.choice(np.array([-1, 1]))
		if (xtest > 0) and (xtest < size-1) and (ytest > 0) and (ytest < size-1):
			if map[xtest][ytest] == 0 or count > 5:
				count = 0
				x, y = (xtest, ytest)
				map[x][y] = 0
				if x == size-2:
					xexit, yexit = (x, y)
					break
			else:
				count += 1
	return xpos, ypos, rot, map, xexit, yexit
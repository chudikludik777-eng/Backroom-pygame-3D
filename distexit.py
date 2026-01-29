import numpy as np
from numba import njit

@njit
def main(xpos, ypos, xexit, yexit):
	# determine distance to exit using pythagorean theorum
	xexit -= 0.5
	yexit -= 0.5

	xdist = abs(xpos-xexit)
	ydist = abs(ypos-yexit)

	distexit = np.sqrt((xdist**2)+(ydist**2))

	return distexit
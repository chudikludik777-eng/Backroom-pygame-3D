import numpy as np
from numba import njit

@njit
def main(xpos, ypos, xexit, yexit):
	# determine angle to exit using trigonometry
	xpos -= 0.5
	ypos -= 0.5
	
	xdelta = xexit - xpos
	ydelta = yexit - ypos
	
	if xdelta > 0 and ydelta >= 0:
		quadrant = 1
	elif xdelta <= 0 and ydelta > 0:
		quadrant = 2
		xdelta = -xdelta
	elif xdelta < 0 and ydelta <= 0:
		quadrant = 3
		xdelta = -xdelta
		ydelta = -ydelta
	else:
		quadrant = 4
		ydelta = -ydelta
	
	if not xdelta:
		if ydelta >= 0:
			exitangle = np.pi/2
		else:
			exitangle = 3*np.pi/2
	else:
		exitangle = (np.arctan(ydelta/xdelta))
		
	if quadrant == 2:
		exitangle = np.pi - exitangle
	elif quadrant == 3:
		exitangle = np.pi + exitangle
	elif quadrant == 4:
		exitangle = 2*np.pi - exitangle
	
	return exitangle
	
if __name__ == "__main__":
	print(360*main(1, 1, 2*np.pi, 2, 3)/(2*np.pi))
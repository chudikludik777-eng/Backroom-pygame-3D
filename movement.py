import pygame as pg
import numpy as np

def main(xpos, ypos, rot, keys, tdelta, map, xrender, yrender):
	
	xspeed = 0.002 # horizontal speed
	yspeed = 0.003 # forward and backward speed
	tspeed = 0.003 # turning speed
	pwidth = 0.2 # player size
	
	x, y = xpos, ypos
	
	# strafing
	if keys[ord('a')]:
		x, y = x + np.sin(rot)*xspeed*tdelta, y - np.cos(rot)*xspeed*tdelta
	if keys[ord('d')]:
		x, y = x - np.sin(rot)*xspeed*tdelta, y + np.cos(rot)*xspeed*tdelta
	
	# turning
	if keys[pg.K_LEFT]:
		rot -= tspeed*tdelta
	if keys[pg.K_RIGHT]:
		rot += tspeed*tdelta
	
	# forward and backward
	if keys[pg.K_UP] or keys[ord('w')]:
		x, y = x + np.cos(rot)*yspeed*tdelta, y + np.sin(rot)*yspeed*tdelta
	if keys[pg.K_DOWN] or keys[ord('s')]:
		x, y = x - np.cos(rot)*yspeed*tdelta, y - np.sin(rot)*yspeed*tdelta
	
	# collision detection
	if not(map[int(x-pwidth)][int(y)] or map[int(x+pwidth)][int(y)] or
			map[int(x)][int(y-pwidth)] or map[int(x)][int(y+pwidth)]):
		xpos, ypos = x, y
	elif not(map[int(xpos-pwidth)][int(y)] or map[int(xpos+pwidth)][int(y)] or
			map[int(xpos)][int(y-pwidth)] or map[int(xpos)][int(y+pwidth)]):
		ypos = y
	elif not(map[int(x-pwidth)][int(ypos)] or map[int(x+pwidth)][int(ypos)] or
			map[int(x)][int(ypos-pwidth)] or map[int(x)][int(ypos+pwidth)]):
		xpos = x
	
	return xpos, ypos, rot
import numpy as np
from numba import njit

@njit
def main(frame, xrender, yrender, fov, rot, xpos, ypos, map, size, xexit, yexit, ceiling, floor,
		wall):
	ambient = 0.5
	
	rbuffer = np.full((xrender, yrender), False)
	
	frame, rbuffer, zbuffer = render_walls(frame, xrender, yrender, fov, rot, xpos, ypos,
			rbuffer, map, size, wall, ambient)
			
	frame, rbuffer, zbuffer = render_exit(frame, xrender, yrender, fov, rot, xpos, ypos,
			rbuffer, zbuffer, xexit, yexit, size)
	
	frame = render_surface(frame, xrender, yrender, fov, rot, xpos, ypos, rbuffer, size,
			floor, ambient, 'floor')
	
	frame = render_surface(frame, xrender, yrender, fov, rot, xpos, ypos, rbuffer, size,
			ceiling, ambient, 'ceiling')
	
	return frame
@njit
def render_walls(frame, xrender, yrender, fov, rot, xpos, ypos, rbuffer, map, size, wall,
		ambient):
	horizon = int(yrender/2)
	colwidth = fov/xrender # angular width of columns
	zbuffer = np.zeros(xrender)
	
	for i in range(xrender):
		rot_i = rot + np.deg2rad((i*colwidth) - (fov/2))
		sin_rot_i = np.sin(rot_i)
		cos_rot_i = np.cos(rot_i)
		anti_fisheye = np.cos(np.deg2rad((i*colwidth) - (fov/2)))
		
		# raycasting
		x, y = xpos, ypos
		while not map[int(x)%int(size-1)][int(y)%(size-1)]:
			x += 0.01*cos_rot_i
			y += 0.01*sin_rot_i
		raydist = abs((x - xpos)/cos_rot_i)
		zbuffer[i] = raydist # one dimensional zbuffer for rendering exit
		wallheight = int(horizon/(raydist*anti_fisheye + 0.01)) # half-height of wall on screen
		
		# shade value for darkening farther away columns
		shade = ambient + (1-ambient)*(wallheight/horizon)
		if shade > 1:
			shade = 1
		
		# get texture coordinates
		if x%1 < 0.01 or x%1 > 0.99:
			xwall = int(y*3%1*32)
		else:
			xwall = int(x*3%1*32)
		ywall = np.linspace(0, 3, wallheight*2)*32%32
		
		# render walls onto frame
		for k in range(wallheight*2):
			if horizon-wallheight+k>=0 and horizon-wallheight+k<yrender:
				frame[i][horizon-wallheight+k] = wall[xwall][int(ywall[k])]*shade
				rbuffer[i][horizon-wallheight+k] = True
	return frame, rbuffer, zbuffer
@njit
def render_surface(frame, xrender, yrender, fov, rot, xpos, ypos, rbuffer, size, texture,
		ambient, surf):
	horizon = int(yrender/2)
	colwidth = fov/xrender # angular width of columns
	
	if surf == 'floor':
		start = 0
		end = horizon
	elif surf == 'ceiling':
		start = horizon+1
		end = yrender
	
	for j in range(start, end):
		if surf == 'floor':
			shade = ambient + (1-ambient)*(1-(j/horizon))
		elif surf == 'ceiling':
			shade = ambient + (1-ambient)*(1-horizon/(j+1))
		if shade > 1:
			shade = 1
		elif shade < 0:
			shade = 0
		
		for i in range(xrender):
			if not rbuffer[i][yrender-j-1]:
				rot_i = rot + np.deg2rad((i*colwidth) - (fov/2))
				sin_rot_i = np.sin(rot_i)
				cos_rot_i = np.cos(rot_i)
				anti_fisheye = np.cos(np.deg2rad((i*colwidth) - (fov/2)))
				n = (horizon/(horizon-j))/anti_fisheye
				
				if surf == 'floor':
					x, y = (xpos + cos_rot_i*n), (ypos + sin_rot_i*n)
				elif surf == 'ceiling':
					x, y = (size-xpos) + cos_rot_i*n, (size-ypos) + sin_rot_i*n
				
				xsurf, ysurf = int(x*2%1*64), int(y*2%1*64)
				
				frame[i][yrender-j-1] = shade*(texture[xsurf][ysurf])
	return frame
@njit
def render_exit(frame, xrender, yrender, fov, rot, xpos, ypos, rbuffer, zbuffer, xexit, yexit,
		size):
	horizon = int(yrender/2)
	colwidth = fov/xrender # angular width of columns
	
	for i in range(xrender):
		rot_i = rot + np.deg2rad((i*colwidth) - (fov/2)) # angle of column i
		sin_rot_i = np.sin(rot_i)
		cos_rot_i = np.cos(rot_i)
		anti_fisheye = np.cos(np.deg2rad((i*colwidth) - (fov/2))) # correct for fisheye effect
		
		# raycasting
		x, y = xpos, ypos
		found_exit = False
		while (abs((x - xpos)/cos_rot_i) < zbuffer[i]) and not found_exit:
			x += 0.01*cos_rot_i
			y += 0.01*sin_rot_i
			if int(x) == xexit and int(y) == yexit:
				found_exit = True
		raydist = (abs((x - xpos)/cos_rot_i))
		exitheight = int((horizon/(raydist*anti_fisheye + 0.01))/1)
		
		# rendering exit to frame
		if found_exit:
			for k in range(exitheight*2):
				if (horizon-exitheight+k>=0 and horizon-exitheight+k<yrender
						and (i+(horizon-exitheight+k))%4==0):
					frame[i][horizon-exitheight+k] = (0,0,128)
					rbuffer[i][horizon-exitheight+k] = True
	return frame, rbuffer, zbuffer
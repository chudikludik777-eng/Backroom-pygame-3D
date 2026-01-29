import pygame as pg
import numpy as np
from gen_map import main as gen_map
from render_2 import main as render
from movement import main as movement
from distexit import main as distexit
from angleexit import main as angleexit

def main():
	pg.init()

	yrender = 180
	xrender = int(yrender*16/9)

	screen = pg.display.set_mode(
		size = (xrender, yrender),
		flags = pg.SCALED|pg.FULLSCREEN,
		depth = 32,
		vsync = 0
	)

	clock = pg.time.Clock()
	pg.event.set_allowed([pg.QUIT, pg.KEYDOWN])
	font = pg.font.Font(None, 16)
	fov = 60
	size = 25 # map size
	xpos, ypos, rot, map, xexit, yexit = gen_map(size) # generate map

	# initialize textures
	ceiling = pg.surfarray.array3d(pg.image.load('ceiling.png').convert())
	floor = pg.surfarray.array3d(pg.image.load('floor.png').convert())
	wall = pg.surfarray.array3d(pg.image.load('wall.png').convert())
	frame = np.full((xrender, yrender, 3), (255,0,0))

	# initialize sound
	exitsound = pg.mixer.Sound('pulse sound.wav')
	channel = pg.mixer.find_channel()

	running = True
	while running:
		if int(xpos) == xexit and int(ypos) == yexit:
			print("Congrats, you escaped the maze!")
			running = False
		for event in pg.event.get():
			if (event.type == pg.QUIT) or ((event.type == pg.KEYDOWN)
					and (event.key == pg.K_ESCAPE)):
				running = False

		# functionality abandoned for now, used for offsetting horizon
		"""
		counter += clock.get_time()
		hoffset = 10000#(np.cos(counter/100)/(yrender))*500000
		print(hoffset)
		"""
		# frame = np.full((xrender, yrender, 3), (255,0,0)) # clear frame to red for debugging purposes
		frame = render(frame, xrender, yrender, fov, rot, xpos, ypos, map, size, xexit, yexit, ceiling, floor, wall)

		# initialize surfaces
		surf = pg.surfarray.make_surface(frame)
		surf = pg.transform.scale(surf, (xrender, yrender))

		fps = int(clock.get_fps())
		pg.display.set_caption(f"Backrooms FPS: {str(fps)}")

		text_surface = font.render(str(fps), False, (0,255,255))
		# display to screen
		screen.blit(surf, (0,0))
		screen.blit(text_surface, (0,0))
		pg.display.update()

		dist = np.log(distexit(xpos, ypos, xexit, yexit)) # distance to center of exit
		if dist < 1:
			dist = 1
		angle = angleexit(xpos, ypos, xexit, yexit)-rot # angle to center of exit

		# volume of left and right speakers
		leftvolume = (1/dist)*((np.sin((np.pi-2.5)-angle)+1)/2)
		if leftvolume < 0:
			leftvolume = 0
		rightvolume = (1/dist)*((np.sin(2.5-angle)+1)/2)
		if rightvolume < 0:
			rightvolume = 0

		channel.set_volume(leftvolume, rightvolume)
		if not pg.mixer.get_busy():
			channel.play(exitsound)

		xpos, ypos, rot = movement(xpos, ypos, rot, pg.key.get_pressed(), clock.tick(), map, xrender, yrender)


if __name__ == '__main__':
	main()
	pg.quit()
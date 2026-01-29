import pygame as pg

def main():
	pg.init()
	pg.mixer.init()
	sndtest = pg.mixer.Sound("buzz.wav")
	sndtest.play()
	while True:
		pass

if __name__ == "__main__":
	main()
	pg.quit()
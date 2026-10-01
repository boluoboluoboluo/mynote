import pygame
import sys
import os

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, "data")

# object: game window
class Game:
	def __init__(self,width=800,height=300):
		self.screen = pygame.display.set_mode((width,height))
		self.running = True
		self.FPS = 60
		self.background = (0,0,0)


	def clear(self):
		self.screen.fill(self.background)

	def render(self,image,rect):
		self.screen.blit(image,rect)

	def punch_check(self,fist,chimp):
		if (fist.rect.x+fist.center_offset[0] > chimp.rect.left and 
				fist.rect.x+fist.center_offset[0] < chimp.rect.right and 
				fist.rect.y+fist.center_offset[1] > chimp.rect.top and 
				fist.rect.y+fist.center_offset[1] < chimp.rect.bottom):
			chimp.punched()
		else:
			fist.punch()

# entity: chimp
class Chimp:
	def __init__(self):
		self.image = pygame.image.load(os.path.join(DATA_DIR,"chimp.webp"))
		self.image_bak = self.image
		self.rect = self.image.get_rect()
		self.sound = pygame.mixer.Sound(os.path.join(DATA_DIR,"chimp.wav"))
		self.speed = 200 	# pixel/s
		self.angle = 0 		# tilt angle

	# auto move when game start
	def move(self,dt,limit_rect):
		if self.rect.left < limit_rect.left or self.rect.right > limit_rect.right:
			self.speed = -self.speed
		self.rect.x += self.speed * dt

	# been punched by fist
	def punched(self):
		self.angle += 12
		self.image = pygame.transform.rotate(self.image_bak,self.angle)	# rotate angle:12
		self.rect = self.image.get_rect(center=self.rect.center)
		self.sound.play()	# yell



# entity: fist
class Fist:
	def __init__(self):
		self.image = pygame.image.load(os.path.join(DATA_DIR,"fist.webp"))
		self.rect = self.image.get_rect()
		self.sound = pygame.mixer.Sound(os.path.join(DATA_DIR,"fist.wav"))
		self.center_offset = (25,25)


	def follow_mouse(self):
		mouse_x,mouse_y = pygame.mouse.get_pos()
		self.rect.x = mouse_x - self.center_offset[0]
		self.rect.y = mouse_y - self.center_offset[1]

	def punch(self):
		self.sound.play()	# punch


def main():
	pygame.init()
	clock = pygame.time.Clock()
	game = Game()
	chimp = Chimp()
	fist = Fist()

	while game.running:
		for evt in pygame.event.get():
			if evt.type == pygame.QUIT:
				game.running = False
			if evt.type == pygame.MOUSEBUTTONDOWN:
				game.punch_check(fist,chimp)

		dt = clock.tick(game.FPS) / 1000 	
		chimp.move(dt,game.screen.get_rect())
		fist.follow_mouse()

		game.clear()
		game.render(chimp.image,chimp.rect)
		game.render(fist.image,fist.rect)
		pygame.display.flip()

if __name__ == "__main__":
	main()
	pygame.quit()
	sys.exit()
	
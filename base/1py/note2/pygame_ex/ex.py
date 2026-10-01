import pygame
import sys


class Config:
	WIDTH = 800
	HEIGHT = 600
	FPS = 60
	BACKGROUND = (0,0,0)


class Ball(pygame.sprite.Sprite):
	def __init__(self,screen):
		super().__init__()
		self.image = pygame.Surface((50,50))
		self.image.fill((255,0,0))
		self.area = screen.get_rect()
		self.rect = self.image.get_rect(center=self.area.center)
		self.speed = 100 	# pixel/s


	def update(self,dt):
		


class GameEngine:
	def __init__(self):
		self.screen = pygame.display.set_mode((Config.WIDTH,Config.HEIGHT))
		self.running = True
		self.all_sprites = pygame.sprite.Group()
		self.clock = pygame.time.Clock()
		

	def run(self):
		while self.running:
			dt = self.clock.tick(Config.FPS) / 1000.0 		# s

			self._handle_events()

			# keys = pygame.key.get_pressed()
			# if keys[pygame.K_LEFT] or keys[pygame.K_a]:

			self._update(dt)

			self._draw()
			
		pygame.quit()
		sys.exit()


	def _handle_events(self):
		for evt in pygame.event.get():
			if evt.type == pygame.QUIT:
				self.running = False
		

	def _update(self,dt):
		self.all_sprites.update(dt)
		pass

	def _draw(self):
		self.screen.fill(Config.BACKGROUND)
		self.all_sprites.draw(self.screen)
		pygame.display.flip()
		

if __name__ == "__main__":
	pygame.init()
	game = GameEngine()
	ball = Ball(game.screen)
	game.all_sprites.add(ball)
	game.run()
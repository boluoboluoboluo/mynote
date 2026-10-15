import pygame #type:ignore
from config import Config
import random
from particle import Particle
import util

# 障碍 wh : (20,10) or (10,20) or (20,20)
class Obstacle(pygame.sprite.Sprite):
	def __init__(self,wh,bc,born_pos,level,name="obstacle"):
		super().__init__()
		self.name = name
		self.type = Config.OBSTACLE
		self._layer = Config.OBSTACLE
		self.image = pygame.Surface(wh)
		self.image.fill(bc)
		self.rect = self.image.get_rect()
		self.rect.topleft = born_pos
		self.level = level
		self.is_invincible = False
	@classmethod
	def create(cls,od):
		born_pos = (Config.OBSTACLE_WH[0] * od[0],Config.OBSTACLE_WH[1] * od[1])
		bc = Config.NORMAL_OBSTACLE_BC if od[2] == Config.NORMAL_OBSTACLE else Config.HARD_OBSTACLE_BC
		return cls(wh=Config.OBSTACLE_WH,bc=bc,born_pos=born_pos,level=od[2])
	
	def create_explosion(self,pos, count=40):
		"""在指定位置生成指定颜色和数量的粒子"""
		for _ in range(count):
			color = (random.randint(50,230),random.randint(50,230),random.randint(50,230))
			particle = Particle(pos[0], pos[1], color)
			util.add_particle(particle)








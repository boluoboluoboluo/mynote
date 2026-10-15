
import pygame	# type:ignore
import random
from config import Config

# --- 1. 定义粒子类 ---
class Particle(pygame.sprite.Sprite):
	def __init__(self, x, y, color):
		super().__init__()
		self._layer = Config.PARTICLE
		# 随机粒子的尺寸（2到6像素之间）
		self.size = random.randint(2, 6)
		self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
		self.color = color
		self.image.fill(self.color)
		self.rect = self.image.get_rect(center=(x, y))
		
		# 随机爆炸速度（向四周飞散）
		self.vx = random.uniform(-5, 5)
		self.vy = random.uniform(-7, 2)  # 给一个向上的初速度，更像炸开
		
		# 物理参数
		self.gravity = 0.2  # 重力模拟
		self.alpha = 255    # 初始透明度
		self.fade_speed = random.randint(4, 8)  # 随机消失速度

	def update(self,dt,screen_rect,keys):
		# 1. 位置更新（物理运动）
		self.vy += self.gravity
		self.rect.x += self.vx
		self.rect.y += self.vy
		# print(self.rect)
		
		# 2. 渐隐效果（减少透明度）
		self.alpha -= self.fade_speed
		if self.alpha <= 0:
			self.kill()  # 透明度小于0时，从所有精灵组中移除该粒子
		else:
			# 更新 Surface 的透明度
			self.image.set_alpha(self.alpha)

	
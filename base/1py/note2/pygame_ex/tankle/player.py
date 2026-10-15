
import pygame #type:ignore
from config import Config
import util

class Player(pygame.sprite.Sprite):
	def __init__(self,wh,bc,born_pos,speed=100,name=""):
		super().__init__()
		self.name = name
		self.type = Config.PLAYER
		self._layer = Config.PLAYER
		self.image = pygame.Surface(wh)
		# self.transparent_image = pygame.Surface(wh, pygame.SRCALPHA)	# 透明
		self.image.fill(bc)
		self.rect = self.image.get_rect()
		self.rect.topleft = born_pos
		self.speed = speed
		self.direction = pygame.Vector2(1,0)
		self.change_direction = False
		self.pos = pygame.Vector2(self.rect.x,self.rect.y)
		self.born_time = pygame.time.get_ticks()
		self.is_invincible = True  # 无敌
	@classmethod
	def born(cls):
		return cls(wh=Config.PLAYER_WH,bc=Config.PLAYER_BC,speed=Config.PLAYER_SPEED,born_pos=Config.PLAYER_BORN_POS,name=Config.PLAYER_ONE)

	# 检查无敌状态
	def check_invincible(self):
		if self.is_invincible:
			cur_time = pygame.time.get_ticks()
			if cur_time - self.born_time > Config.INVINCIBLE_INTERVAL:
				self.is_invincible = False
				self.image.set_alpha(None)
			else:
				if (cur_time // Config.BLINK_INTERVAL) % 2 == 0:
					self.image.set_alpha(0)	# 设置透明
				else:
					self.image.set_alpha(None)	# 恢复显示

	def update(self,dt,screen_rect,keys):
		self.check_invincible()

		# 按键事件
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.direction.x = -1
			self.direction.y = 0
			self.pos += self.direction * self.speed * dt 	# 更新 pos坐标
		elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.direction.x = 1
			self.direction.y = 0
			self.pos += self.direction * self.speed * dt
		elif keys[pygame.K_UP] or keys[pygame.K_w]:
			self.direction.x = 0
			self.direction.y = -1
			self.pos += self.direction * self.speed * dt
		elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.direction.x = 0
			self.direction.y = 1
			self.pos += self.direction * self.speed * dt

		min_x, max_x = 0, screen_rect.width - self.rect.width
		min_y, max_y = 0, screen_rect.height - self.rect.height
		self.pos.x = max(min_x,min(self.pos.x,max_x))
		self.pos.y = max(min_y,min(self.pos.y,max_y))

		old_row,old_col = self.rect.y//Config.scale,self.rect.x//Config.scale
		# print("==================",old_row,old_col)
		# 更新坐标
		self.rect.topleft = (int(self.pos.x), int(self.pos.y))
		row,col = self.rect.y//Config.scale,self.rect.x//Config.scale
		if row != old_row or col != old_col:
			Config.sheet_groups[old_row][old_col].remove(self)
			# 添加到网格
			util.add_to_sheets(self)

	def rand_direction(self):	# 为维持碰撞代码,而兼容的方法 (或者说自动模式?)
		pass

	def shoot(self):
		# print(len(Bullet.pool))
		bullet = util.get_bullet()
		bullet.owner = self.type
		bullet.direction.x = self.direction.x
		bullet.direction.y = self.direction.y
		bullet.rect.center = self.rect.center
		bullet.pos.x = bullet.rect.x
		bullet.pos.y = bullet.rect.y

		util.add_bullet(bullet)



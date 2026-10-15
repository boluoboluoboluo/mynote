
import pygame #type:ignore
import random
from config import Config
import util
from particle2 import Particle

class Enemy(pygame.sprite.Sprite):
	def __init__(self,wh,bc,born_pos,speed=50,name=""):
		super().__init__()
		self.name = name
		self.type = Config.ENEMY
		self._layer = Config.ENEMY
		self.image = pygame.Surface(wh)
		self.image.fill(bc)
		self.rect = self.image.get_rect()
		self.rect.topleft = born_pos
		self.speed = speed
		self.pos = pygame.Vector2(self.rect.x,self.rect.y)
		self.direction = pygame.Vector2(0,0)
		self.change_direction = False
		self.born_time = pygame.time.get_ticks()
		self.is_invincible = True
		self.rand_direction()	# 随机方向

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
		
		# 上一帧的诉求,通知要换方向(发生碰撞等)
		if self.change_direction:
			self.rand_direction()
			self.change_direction = False
		# 判断是否射击 大概 3秒(180帧) 射击 1次
		if random.random() < 0.0055:	# 1/180
			self.shoot()
		# pos坐标更新
		self.pos += self.direction * self.speed * dt

		min_x, max_x = 0, screen_rect.width - self.rect.width
		min_y, max_y = 0, screen_rect.height - self.rect.height
		# 边界检测
		if self.pos.x < min_x or self.pos.x > max_x or self.pos.y < min_y or self.pos.y > max_y:
			self.rand_direction()
		self.pos.x = max(min_x,min(self.pos.x,max_x))
		self.pos.y = max(min_y,min(self.pos.y,max_y))

		old_row,old_col = self.rect.y//Config.scale,self.rect.x//Config.scale
		# 更新坐标
		self.rect.topleft = (int(self.pos.x), int(self.pos.y))
		row,col = self.rect.y//Config.scale,self.rect.x//Config.scale
		if row != old_row or col != old_col:
			Config.sheet_groups[old_row][old_col].remove(self)
			# 添加到网格
			util.add_to_sheets(self)

	# 随便改变方向
	def rand_direction(self):
		choices = ((1,0),(-1,0),(0,1),(0,-1))	# 右,左,下,上
		rt = random.choice(choices)
		self.direction.x = rt[0]
		self.direction.y = rt[1]

	# 发射子弹
	def shoot(self):
		bullet = util.get_bullet()
		bullet.owner = self.type
		bullet.direction.x = self.direction.x
		bullet.direction.y = self.direction.y
		bullet.rect.center = self.rect.center
		bullet.pos.x = bullet.rect.x
		bullet.pos.y = bullet.rect.y

		util.add_bullet(bullet)

	# 生成实例
	@classmethod
	def born(cls):
		# 出生点坐标:
		locates = list(Config.ENEMY_BORN_POS)
		random.shuffle(locates)	# 打乱顺序 ,随机出生点出生
		for x in locates:
			rect = pygame.Rect(x[0], x[1], Config.ENEMY_WH[0], Config.ENEMY_WH[1])
			# 矩形区域的网格
			sheet_group = Config.sheet_groups[rect.y//Config.scale][rect.x//Config.scale]
			# 检测碰撞
			is_clear = not any(rect.colliderect(sprite.rect) for sprite in sheet_group)
			if is_clear:
				obj = cls(wh=Config.ENEMY_WH,bc=Config.ENEMY_BC,born_pos=(rect.x,rect.y),name="enemy")
				util.add_enemy(obj)
				return True
		return False
	
	# --- 2. 触发爆炸的函数 ---
	def create_explosion(self,pos, count=40):
		color = (230,0,0)
		"""在指定位置生成指定颜色和数量的粒子"""
		for _ in range(count):
			
			particle = Particle(pos[0], pos[1], color)
			util.add_particle(particle)



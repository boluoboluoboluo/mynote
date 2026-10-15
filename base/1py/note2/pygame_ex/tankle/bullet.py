
import pygame #type:ignore
import util
from config import Config

class Bullet(pygame.sprite.Sprite):
	def __init__(self,wh,bc,name="bullet"):
		super().__init__()
		self.name = name
		self.type = Config.BULLET
		self._layer = Config.BULLET
		self.image = pygame.Surface(wh)
		self.image.fill(bc)
		self.rect = self.image.get_rect()
		self.speed = Config.BULLET_SPEED
		self.direction = pygame.Vector2(0,0)
		self.owner = None
		self.pos = pygame.Vector2(0,0)
		self.is_invincible = False

	def update(self,dt,screen_rect,keys):
		# pos坐标更新
		self.pos += self.direction * self.speed * dt

		min_x, max_x = 0, screen_rect.width - self.rect.width
		min_y, max_y = 0, screen_rect.height - self.rect.height
		# 边界检测
		if self.pos.x < min_x or self.pos.x > max_x or self.pos.y < min_y or self.pos.y > max_y:
			self.kill()
			util.recycle_bullet(self)	# 子弹回收
			return
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






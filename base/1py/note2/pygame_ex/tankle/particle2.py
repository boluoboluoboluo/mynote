import pygame # type:ignore
import random
from config import Config

class Particle(pygame.sprite.Sprite):
	def __init__(self, x, y, color):
		super().__init__()
		self._layer = Config.PARTICLE
		# 1. 随机决定基础尺寸（大碎片和小碎片）
		# 80% 是小碎片(3~6像素)，20% 是大碎片(8~14像素)
		if random.random() < 0.2:
			self.size_w = random.randint(8, 14)
			self.size_h = random.randint(8, 14)
		else:
			self.size_w = random.randint(3, 6)
			self.size_h = random.randint(3, 6)
			
		# 创建一个支持透明度的画布，画布大小取宽高的最大值以容纳旋转/多边形
		max_dim = max(self.size_w, self.size_h) * 2
		self.image = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)
		self.color = color
		
		# 2. 随机选择一种形状进行绘制
		shape_type = random.choice(["rect", "ellipse", "triangle", "polygon"])
		center_pt = max_dim // 2
		
		if shape_type == "rect":
			# 矩形/长方形
			rect_path = pygame.Rect(center_pt - self.size_w//2, center_pt - self.size_h//2, self.size_w, self.size_h)
			pygame.draw.rect(self.image, self.color, rect_path)
			
		elif shape_type == "ellipse":
			# 椭圆/圆形
			rect_path = pygame.Rect(center_pt - self.size_w//2, center_pt - self.size_h//2, self.size_w, self.size_h)
			pygame.draw.ellipse(self.image, self.color, rect_path)
			
		elif shape_type == "triangle":
			# 三角形（随机三个顶点）
			w, h = self.size_w, self.size_h
			pts = [
				(center_pt, center_pt - h//2), 
				(center_pt - w//2, center_pt + h//2), 
				(center_pt + w//2, center_pt + h//2)
			]
			pygame.draw.polygon(self.image, self.color, pts)
			
		elif shape_type == "polygon":
			# 不规则四边形/多边形（给矩形四个角加随机偏移）
			w, h = self.size_w, self.size_h
			offset = 3
			pts = [
				(center_pt - w//2 + random.randint(-offset, offset), center_pt - h//2 + random.randint(-offset, offset)),
				(center_pt + w//2 + random.randint(-offset, offset), center_pt - h//2 + random.randint(-offset, offset)),
				(center_pt + w//2 + random.randint(-offset, offset), center_pt + h//2 + random.randint(-offset, offset)),
				(center_pt - w//2 + random.randint(-offset, offset), center_pt + h//2 + random.randint(-offset, offset))
			]
			pygame.draw.polygon(self.image, self.color, pts)

		self.rect = self.image.get_rect(center=(x, y))
		
		# 3. 物理与动画参数
		self.vx = random.uniform(-3, 3)
		self.vy = random.uniform(-5, 2)  
		self.gravity = 0.1
		self.alpha = 255    
		self.fade_speed = random.randint(7, 13)  
		
		# 4. 旋转参数（让不规则形状转起来才逼真！）
		self.orig_image = self.image.copy() # 保留原图用于旋转，避免图片变模糊
		self.angle = 0
		self.rot_speed = random.uniform(-10, 10) # 随机旋转速度和方向

	def update(self,dt,screen_rect,keys):
		# 位置更新
		self.vy += self.gravity
		self.rect.x += self.vx
		self.rect.y += self.vy
		
		# 自转更新
		self.angle += self.rot_speed
		
		# 渐隐更新
		self.alpha -= self.fade_speed
		if self.alpha <= 0:
			self.kill()
		else:
			# 同时应用旋转和透明度
			rotated_image = pygame.transform.rotate(self.orig_image, self.angle)
			rotated_image.set_alpha(self.alpha)
			
			# 保持旋转时的中心点不变
			old_center = self.rect.center
			self.image = rotated_image
			self.rect = self.image.get_rect(center=old_center)
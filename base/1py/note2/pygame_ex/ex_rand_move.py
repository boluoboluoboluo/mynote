import pygame
import sys
import random

class Config:
	WIDTH = 800
	HEIGHT = 600
	FPS = 60
	BACKGROUND = (0,0,0)


class Ball(pygame.sprite.Sprite):
	def __init__(self,screen,radius,pos,color,speed):
		super().__init__()
		self.image = pygame.Surface((radius*2,radius*2),pygame.SRCALPHA)	# pygame.SRCALPHA : 背景透明
		self.area = screen.get_rect()
		self.rect = self.image.get_rect(center=pos)
		self.pos = pos
		pygame.draw.circle(self.image,color,(radius,radius),radius)
		self.speed = speed 	# 像素/s


	def update(self,dt,screen_rect):
		self.pos += self.speed * dt
		self.rect.center = self.pos
		# 左右边缘碰撞检测
		if self.rect.left < screen_rect.left or self.rect.right > screen_rect.right:
			self.speed.x *= -1
			# 防止边缘卡死
			if self.rect.left < screen_rect.left:
				self.rect.left = screen_rect.left
			if self.rect.right > screen_rect.right:
				self.rect.right = screen_rect.right
		# 上下边缘碰撞检测
		if self.rect.top < screen_rect.top or self.rect.bottom > screen_rect.bottom:
			self.speed.y *= -1
			# 防止边缘卡死
			if self.rect.top < screen_rect.top:
				self.rect.top = screen_rect.top
			if self.rect.bottom > screen_rect.bottom:
				self.rect.bottom = screen_rect.bottom


class GameEngine:
	def __init__(self):
		self.screen = pygame.display.set_mode((Config.WIDTH,Config.HEIGHT), pygame.RESIZABLE)	#  pygame.RESIZABLE:窗口自适应
		self.running = True
		self.all_sprites = pygame.sprite.Group()
		self.clock = pygame.time.Clock()


	def run(self):
		while self.running:
			dt = self.clock.tick(Config.FPS) / 1000.0 		# s
			dt = min(dt, 0.05) 		# 防止因拖动窗口等导致卡顿 dt变长,导致下一帧画面异常
			self._handle_events()

			self._update(dt)

			self._draw()
			
		pygame.quit()
		sys.exit()


	def _handle_events(self):
		for evt in pygame.event.get():
			if evt.type == pygame.QUIT:
				self.running = False
			# 捕捉窗口移动/改变大小等系统事件
			elif evt.type in (pygame.WINDOWMOVED, pygame.WINDOWEXPOSED):
				# 当窗口被移动或重新暴露时，强制重新绘制一次画面
				self._draw()
			# 监听窗口大小改变事件
			elif evt.type == pygame.VIDEORESIZE:
				WIDTH, HEIGHT = evt.w, evt.h
				# 重新设置屏幕大小（如果不写这行，画面会直接黑掉或拉伸变形）
				self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
		

	def _update(self,dt):
		self.all_sprites.update(dt,self.screen.get_rect())
		sprites = self.all_sprites.sprites()
		for i in range(len(sprites)):
			for j in range(i+1,len(sprites)):
				ball1 = sprites[i]
				ball2 = sprites[j]
				# 碰撞检测
				if pygame.sprite.collide_circle(ball1, ball2):
					pos_diff = ball1.pos - ball2.pos 	# ball2圆心指向ball1圆心的向量,法线方向向量
					if pos_diff.length() == 0: 
						pos_diff = pygame.Vector2(1, 0) # 防止重合时除以 0
					normal = pos_diff.normalize() 		# 变成单位长度为1的向量(法线向量)
					tangent = pygame.Vector2(-normal.y, normal.x)	# 顺时针旋转90°(电脑屏幕y轴是向下的),表示两个圆球切线的向量(切线向量)
					# 防粘连修复,碰撞检测时,2个圆的位置已经重叠一部分了,需要分开一点,防止下一帧又检测出碰撞,卡死
					overlap = (ball1.radius + ball2.radius) - pos_diff.length()
					ball1.pos += normal * (overlap / 2)
					ball2.pos -= normal * (overlap / 2)
					# ---
					# 点积（dot）的作用：算出 speed 在 (normal/tangent => 法线/切线) 方向上的速度分量(有符号)
					v1n = ball1.speed.dot(normal)
					v1t = ball1.speed.dot(tangent)
					v2n = ball2.speed.dot(normal)
					v2t = ball2.speed.dot(tangent)
					# ---
					# 改变法线速度，保持切线速度
					v1n_new, v2n_new = v2n, v1n 	# 这里的逻辑:法线速度直接对调
					# ---
					# 情况 B：如果小球质量不同（比如大球撞小球），用下面这两行替换上面那行】
					# m1, m2 = ball1.mass, ball2.mass
					# v1n_new = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
					# v2n_new = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)
					# ---
					# 将新的法线速度和未变的切线速度，重新拼回 X/Y 轴速度
					# 新的速度 = 新的法线速度标量 * 法线方向向量 + 切线速度标量 * 切线方向向量
					ball1.speed = normal * v1n_new + tangent * v1t
					ball2.speed = normal * v2n_new + tangent * v2t


	def _draw(self):
		self.screen.fill(Config.BACKGROUND)
		self.all_sprites.draw(self.screen)
		pygame.display.flip()
		

if __name__ == "__main__":
	game = GameEngine()
	for i in range(10):		# create 10 balls
		# 随机半径
		radius = random.randint(10,20)
		# 随机圆心坐标
		pos = (random.randint(radius,Config.WIDTH-radius),random.randint(radius,Config.HEIGHT-radius))
		# 随机颜色
		color = (random.randint(10,255),random.randint(10,255),random.randint(10,255))
		# 随机速度向量
		speed_x = random.choice([random.randint(100,200),random.randint(-200,-100)])
		speed_y = random.choice([random.randint(100,200),random.randint(-200,-100)])
		speed = pygame.Vector2(speed_x,speed_y)
		# ---
		ball = Ball(game.screen,radius,pos,color,speed)
		game.all_sprites.add(ball)
	game.run()
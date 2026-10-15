
import pygame #type:ignore
from config import Config
from enemy import Enemy
from player import Player
from obstacle import Obstacle
from bullet import Bullet
import util
import math
import color_effect

class Engine:
	def __init__(self):
		self.screen = pygame.display.set_mode((Config.WIDTH,Config.HEIGHT))
		pygame.display.set_caption("fight test")
		self.running = True
		self.clock = pygame.time.Clock()
		# 自定义事件ID, enemy 出生事件
		self.SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
		# 定时器,2000毫秒(2秒)触发一次
		pygame.time.set_timer(self.SPAWN_ENEMY_EVENT, 2000)
		self.background_surf = color_effect.create_gradient_surface(Config.WIDTH,Config.HEIGHT)
		# 
		self.prepare()

	@classmethod
	def prepare(cls):
		# 网格初始化
		row,col = Config.HEIGHT // Config.scale,Config.WIDTH // Config.scale
		# 2维元组
		Config.sheet_groups = tuple(
			tuple(pygame.sprite.Group() for _ in range(col))
			for _ in range(row)
		)
		Config.map_num = len(Config.MAP)-1	# 地图数量
		
	def destroy_data(self):
		for obj in Config.render_group:
			obj.kill()
		Config.bullet_pool = []
		
	def init_data(self):
		Config.borned_enemy_amount = 0
		Config.game_state = 1
		Config.borned_enemy_amount = 0
		Config.enemy_speed = 0
		Config.enemy_amount = 0
		Config.switch_timer = 0
		# player 实例
		player = Player.born()
		util.add_player(player)
		# 子弹池 初始化
		for _ in range(100):
			Config.bullet_pool.append(Bullet(wh=Config.BULLET_WH,bc=Config.BULLET_BC,name="bullet"))

	def load_map_data(self):
		self.destroy_data()
		self.init_data()
		# 地图 
		map = Config.MAP[Config.cur_map]
		Config.enemy_amount = map['enemy_amount']
		Config.enemy_speed = map['enemy_speed']
		# 障碍
		for od in map['obstacle_data']:
			o = Obstacle.create(od)
			util.add_obstacle(o)

	# 检查关卡
	def check_level(self):
		if len(Config.player_group) == 0:
			Config.game_state = Config.GAME_OVER	# 结束
			return
		if len(Config.enemy_group) == 0 and Config.borned_enemy_amount == Config.enemy_amount:
			if Config.cur_map ==  Config.map_num:
				Config.game_state = Config.GAME_OVER	# 结束
			else:
				Config.game_state = Config.GAME_SWITCH
				Config.switch_timer = pygame.time.get_ticks()	# 内置当前毫秒时间戳	

	# 屏幕提示
	def draw_text(self,msg):
		font = pygame.font.SysFont("arial", 40)
		text = font.render(msg, True, (200,200,200),(0,0,180))
		rect = text.get_rect(center=(Config.WIDTH//2, Config.HEIGHT//2))
		self.screen.blit(text, rect)
		
	def draw_dynamic_text(self,msg):
		tip_image = pygame.Surface((300,70),pygame.SRCALPHA)
		tip_image.fill((0,0,180))
		font = pygame.font.SysFont("SimHei", 36) # 使用系统黑体
		text = font.render(msg, True, (200,200,200))
		text_rect = text.get_rect(center=(300//2, 70//2))
		tip_image.blit(text, text_rect)

		current_time = pygame.time.get_ticks()
		# 透明度按 正弦函数变动,
		alpha_scale = (math.sin(current_time * 0.003) + 1) / 2	# 调整到区间 (0,1),  0.003表示变化快慢
		dynamic_alpha = int(50 + alpha_scale * (230 - 50))		# 限制透明度范围
		tip_image.set_alpha(dynamic_alpha)

		rect = tip_image.get_rect(center=(Config.WIDTH//2, Config.HEIGHT//2))
		pygame.draw.rect(self.screen,Config.BACKGROUND,rect)
		self.screen.blit(tip_image,rect)

	def run(self):
		while self.running:
			dt = self.clock.tick(Config.FPS)/1000
			self._hand_evt()
			match Config.game_state:
				case Config.GAME_RUNNING:
					self.check_level()
					#
					keys = pygame.key.get_pressed()
					self._update(dt,keys)
					self._render()
				case Config.GAME_PAUSE:
					self.draw_text("pause")
					pygame.display.flip()
				case Config.GAME_SWITCH:
					cur_time = pygame.time.get_ticks()
					if cur_time - Config.switch_timer > Config.SWITCH_TIME_INTERVAL:
						Config.cur_map += 1
						self.load_map_data()
						Config.game_state = Config.GAME_RUNNING
					#
					self.draw_dynamic_text("next level...")
					pygame.display.flip()
				case Config.GAME_OVER:
					self.draw_text("game over...")
					pygame.display.flip()
			
	def _hand_evt(self):
		for evt in pygame.event.get():
			match evt.type:
				case pygame.QUIT:
					self.running = False
				case pygame.MOUSEBUTTONDOWN:
					# event.button 可以判断点的是哪个键：1=左键，2=中键(滚轮)，3=右键，4=滚轮上滚，5=滚轮下滚
					if evt.button == 1:
						for p in Config.player_group:
							if p.name == Config.PLAYER_ONE:
								p.shoot()
				case pygame.KEYDOWN:
					if evt.key == pygame.K_ESCAPE or evt.key == pygame.K_p:
						if Config.game_state == Config.GAME_RUNNING:
							Config.game_state = Config.GAME_PAUSE
						elif Config.game_state == Config.GAME_PAUSE:
							Config.game_state = Config.GAME_RUNNING
				case self.SPAWN_ENEMY_EVENT:	# 自定义事件
					if Config.game_state == Config.GAME_RUNNING and Config.borned_enemy_amount < Config.enemy_amount and len(Config.enemy_group) < 10:
						if Enemy.born():
							Config.borned_enemy_amount += 1

	def _update(self,dt,keys):
		# 更新坐标
		Config.update_group.update(dt,self.screen.get_rect(),keys)
		# 遍历所有精灵,进行碰撞检测
		for obj in Config.collide_group:
			# 保存当前 obj 下标
			row,col = (obj.rect.y//Config.scale),(obj.rect.x//Config.scale)
			# 碰撞检测处理
			self.handle_collide(obj)
			# 新下标
			new_row,new_col = (obj.rect.y//Config.scale),(obj.rect.x//Config.scale)
			if row != new_row or col != new_col:
				# 从旧格子移除
				Config.sheet_groups[row][col].remove(obj)
				# 新格子添加
				Config.sheet_groups[new_row][new_col].add(obj)

	def _render(self):
		# self.screen.fill(Config.BACKGROUND)
		self.screen.blit(self.background_surf, (0, 0))
		Config.render_group.draw(self.screen)
		pygame.display.flip()

	# 物体 obj 与周围8个格子的物体进行 碰撞检测
	def handle_collide(self,obj):
		# obj 格子下标
		row,col = (obj.rect.y//Config.scale),(obj.rect.x//Config.scale)
		min_row,max_row = max(0,row-1),min(row+1,Config.HEIGHT//Config.scale-1)
		min_col,max_col = max(0,col-1),min(col+1,Config.WIDTH//Config.scale-1)
		# 遍历周围8个格子
		for i in range(min_row,max_row+1):
			for j in range(min_col,max_col+1):
				# 与网格中 group 进行碰撞检测, 返回碰撞检测列表
				collides =  pygame.sprite.spritecollide(obj,Config.sheet_groups[i][j],False)
				if len(collides) > 0:
					for obj2 in collides:
						if obj == obj2:		# 排除自身
							continue
						util.handle_collide(obj,obj2)

	



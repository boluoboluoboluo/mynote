
from config import Config
import pygame	#type:ignore

def test():
    pass

# 将精灵添加对应的网格
def add_to_sheets(obj):
	# 网格索引
	row,col = obj.rect.y//Config.scale,obj.rect.x//Config.scale
	# 添加到对应网格
	Config.sheet_groups[row][col].add(obj)
# 添加玩家
def add_player(obj):
	Config.render_group.add(obj)
	Config.collide_group.add(obj)
	Config.player_group.add(obj)
	Config.update_group.add(obj)
# 添加敌方
def add_enemy(obj):
	Config.render_group.add(obj)
	Config.collide_group.add(obj)
	Config.enemy_group.add(obj)
	Config.update_group.add(obj)
# 添加子弹
def add_bullet(obj):
	Config.render_group.add(obj)
	Config.collide_group.add(obj)
	Config.update_group.add(obj)
# 添加障碍
def add_obstacle(obj):
	Config.render_group.add(obj)
	add_to_sheets(obj)
# 特效粒子
def add_particle(obj):
	Config.render_group.add(obj)
	Config.update_group.add(obj)
# 获取子弹
def get_bullet():
	return Config.bullet_pool.pop()
# 回收子弹
def recycle_bullet(bullet):
	 Config.bullet_pool.insert(0,bullet)
# 检查 obj 是否 和周围 8 个格子发生碰撞
def check_collide(obj):
	# obj 格子下标
	row,col = (obj.rect.y//Config.scale),(obj.rect.x//Config.scale)
	min_row,max_row = max(0,row-1),min(row+1,Config.HEIGHT//Config.scale-1)
	min_col,max_col = max(0,col-1),min(col+1,Config.WIDTH//Config.scale-1)
	# 遍历周围8个格子
	for i in range(min_row,max_row+1):
		for j in range(min_col,max_col+1):
			# 与网格中 group 进行碰撞检测, 返回碰撞检测列表
			collites =  pygame.sprite.spritecollide(obj,Config.sheet_groups[i][j],False)
			if len(collites) > 0:
				for obj2 in collites:
					if obj != obj2:
						return True
	return False
# 碰撞处理
def handle_collide(obj,obj2):
    # 如果是子弹
	if obj.type == Config.BULLET:
		if obj.owner == obj2.type:
			return
		if obj.type == obj2.type:
			return 
		if obj2.is_invincible:
			return
		if obj2.type == Config.OBSTACLE and obj2.level == Config.HARD_OBSTACLE:
			obj.kill()
			recycle_bullet(obj)
			return 
		obj.kill()
		obj2.create_explosion(obj2.rect.center)	# 死亡的特效
		obj2.kill()
		recycle_bullet(obj)
	elif obj2.type == Config.BULLET:
		if obj2.owner == obj.type:
			return
		if obj2.type == obj.type:
			return 
		if obj.is_invincible:
			return
		if obj.type == Config.OBSTACLE and obj.level == Config.HARD_OBSTACLE:
			obj2.kill()
			recycle_bullet(obj2)
			return 
		obj.create_explosion(obj.rect.center)	# 死亡的特效
		obj.kill()
		obj2.kill()
		recycle_bullet(obj2)
	else:	# 坦克
		# 重叠区域
		overlap_x = min(obj.rect.right, obj2.rect.right) - max(obj.rect.left, obj2.rect.left)
		overlap_y = min(obj.rect.bottom, obj2.rect.bottom) - max(obj.rect.top, obj2.rect.top)
		if overlap_x < overlap_y:	# x轴重叠部分小
			# obj 方向为 右,且 obj 在 obj2 的左边
			if obj.direction.x > 0 and obj.rect.x < obj2.rect.x:
				# obj 右侧与 obj2 左侧贴合
				obj.rect.right = max(obj.rect.width,obj2.rect.left)
			elif obj.direction.x < 0 and obj.rect.x > obj2.rect.x:
				obj.rect.left = min(Config.WIDTH-obj.rect.width,obj2.rect.right)
			obj.pos.x = obj.rect.x
			# 做标记,下一帧要换方向
			obj.change_direction = True
		else:
			if obj.direction.y > 0 and obj.rect.y < obj2.rect.y:	
				obj.rect.bottom = max(obj.rect.height,obj2.rect.top)
			elif obj.direction.y < 0 and obj.rect.y > obj2.rect.y:
				obj.rect.top = min(Config.HEIGHT-obj.rect.height,obj2.rect.bottom)
			obj.pos.y = obj.rect.y
			# 做标记,下一帧要换方向
			obj.change_direction = True



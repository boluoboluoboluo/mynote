import pygame #type:ignore
import sys
from engine import Engine

if __name__ == "__main__":
	pygame.init()
	engine = Engine()
	engine.load_map_data()
	# 运行
	engine.run()
	pygame.quit()
	sys.exit()


```py

import pygame
import pygame.camera
from pygame.locals import *
import sys
import time

pygame.init()
pygame.camera.init()

# cam = pygame.camera.Camera("/dev/video0",(640,480))

camlist = pygame.camera.list_cameras()
print(f"检测到摄像头设备: {camlist}")
if not camlist:
	print("can not find camera..")
	sys.exit()

cam = pygame.camera.Camera(camlist[0], (640, 480))
cam.start()		#注意,系统设置检查摄像头访问权限
time.sleep(1)	#摄像头启动需要时间
image = cam.get_image()
cam.stop()

rect = image.get_rect()
rect.center = (800 // 2, 600 // 2)

screen  = pygame.display.set_mode((800,600))
runing = True
clock = pygame.time.Clock() # 核心：Pygame 时钟

while runing:
	clock.tick(60)	#控制帧率

	for event in pygame.event.get():	#处理信号
		if event.type == pygame.QUIT:
			runing = False

	screen.blit(image, rect)
	pygame.display.flip()

pygame.quit()
sys.exit()
```


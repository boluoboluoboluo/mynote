

| 特性          | Pygame                       | Tkinter                                | PySide / PyQt (Qt 框架)                      |
| ------------- | ---------------------------- | -------------------------------------- | -------------------------------------------- |
| **核心定位**  | **2D 游戏与多媒体开发**      | **系统自带的简易轻量 UI**              | **工业级/商业级桌面软件开发**                |
| **渲染引擎**  | SDL（直通显卡，高频刷新）    | Tcl/Tk（纯 CPU 渲染，低频）            | Qt 引擎（支持 GPU 加速，极其强大）           |
| **UI 丰富度** | **无**（全部需要手写）       | **基础**（有按钮、文本框、标签）       | **极度丰富**（支持图表、网页嵌入、高级动画） |
| **界面美化**  | 靠自己画纯像素图片           | 非常简陋，有世纪初的老旧感             | 极强，支持 **CSS 样式表**，可做出极美界面    |
| **安装体积**  | 较小（几 MB）                | **内置**（无需安装，有 Python 就能跑） | **极大**（几十到几百 MB，打包后体积大）      |
| **适用场景**  | 魂斗罗、飞机大战、音乐播放器 | 写个简易刷票脚本、小工具的皮肤         | 工业控制软件、复杂的 3D 渲染器客户端         |



| 概念         | 游戏帧率（FPS）                          | 屏幕刷新率（Hz）                               |
| ------------ | ---------------------------------------- | ---------------------------------------------- |
| **底层本质** | **`while` 循环每秒执行的次数**。         | **物理屏幕每秒重绘画面的次数**。               |
| **决定因素** | 由显卡（GPU）和处理器（CPU）的性能决定。 | 由显示器硬件面板的物理规格决定。               |
| **工作内容** | 游戏算完一帧，就把画面“画”到显存里。     | 屏幕定期去显存里“拿”画面，展示给眼睛。         |
| **数值变化** | 动态变化（场景复杂时变低，简单时变高）。 | 物理固定（如 60Hz、144Hz，除非开启变频技术）。 |



```sh
#安装
pip install pygame		# 不兼容python 3.14版本,无法安装
pip install pygame-ce	# 替代者(社区版),api 同 pygame
#离线文档查看
python -m pygame.docs
```



```sh
#常用模块
pygame.display：控制窗口和屏幕显示
pygame.Surface：图像和画布对象（所有能画的东西都是 Surface）
pygame.event：管理从操作系统传来的键盘、鼠标、窗口事件
pygame.draw：在画布上绘制几何图形（线、矩形、圆等）
pygame.image 与 pygame.mixer：加载图片和播放声音
```

示例:

```py
import pygame
import sys

# 1. 优雅的配置管理
class Config:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    BACKGROUND_COLOR = (30, 30, 30)  # 深灰色 RGB

# 2. 优雅的实体（Entity）封装
class Player(pygame.sprite.Sprite): # 继承 Pygame 精灵类
    def __init__(self):
        super().__init__()
        # 创建一个 50x50 的正方形 Surface 作为玩家外观
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 128) ) # 绿色
        
        # rect 控制物体的位置与碰撞箱
        self.rect = self.image.get_rect()
        self.rect.center = (Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2)
        
        # 内部使用浮点数存储精确位置，防止像素取整导致运动卡顿
        self.pos_x = float(self.rect.x)
        self.speed = 300.0 # 每秒移动 300 像素

    def update(self, dt, keys):
        """优雅的物理更新：完全基于输入状态和 dt"""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos_x -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos_x += self.speed * dt

        # 将浮点数位置同步回整数的屏幕像素位置
        self.rect.x = int(self.pos_x)

# 3. 游戏主引擎类
class GameEngine:
    def __init__(self):
        pygame.init() # 初始化 Pygame 所有底层硬件模块
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("优雅的 Pygame 物理同步架构")
        
        self.clock = pygame.time.Clock() # 核心：Pygame 时钟
        self.is_running = True
        
        # 初始化游戏对象
        self.player = Player()

    def run(self):
        """核心游戏循环"""
        while self.is_running:
            # 第一步：计算两帧之间的真实时间差（单位：秒）
            # tick(60) 会限制最高帧率为 60，并返回自上一帧过去的时间（毫秒）
            dt = self.clock.tick(Config.FPS) / 1000.0

            # 第二步：处理“单次触发”事件（如点击右上角关闭、单次按键弹出菜单）
            self._handle_events()

            # 第三步：获取当前键盘所有按键的按压状态（适合处理长按持续移动）
            keys = pygame.key.get_pressed()

            # 第四步：物理状态更新（传入 dt 确保任何帧率下速度一致）
            self._update(dt, keys)

            # 第五步：渲染画面
            self._draw()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self, dt, keys):
        self.player.update(dt, keys)

    def _draw(self):
        self.screen.fill(Config.BACKGROUND_COLOR) # 擦除上一帧画面（清屏）
        
        # 将玩家的 image 绘制到屏幕对应的 rect 位置上
        self.screen.blit(self.player.image, self.player.rect)
        
        pygame.display.flip() # 核心：交换双缓冲区，将画好的画面推送到显示器

if __name__ == "__main__":
    game = GameEngine()
    game.run()

```


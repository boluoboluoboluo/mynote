package main

import "vendor:raylib"

SCREEN_TITLE :: "odin游戏"
SCREEN_WIDTH :: 800
SCREEN_HEIGHT :: 600
FPS :: 60

FONT_SIZE :: 16
FONT_PATH :: "C:\\Windows\\Fonts\\simhei.ttf"

CHARSET_WORDS :: "你好,游戏世界!使用方向键控制移动开始"
TIP_WORDS :: "游戏开始"
TIP_POS :: raylib.Vector2{10, 10}

PLAYER_INIT_POS :: raylib.Vector2{400, 300}
PLAYER_INIT_SPEED :: 300.0
PLAYER_RADIUS :: 20.0
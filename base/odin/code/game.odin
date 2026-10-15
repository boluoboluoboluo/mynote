package main

import "core:fmt"
import "vendor:raylib"
import "core:strings"

SCREEN_WIDTH :: 800
SCREEN_HEIGHT :: 600

FONT_SIZE :: 16
FONT_PATH :: "C:\\Windows\\Fonts\\simhei.ttf"

CHARSET_WORDS :: "你好,游戏世界!使用方向键控制移动开始"
TIP_WORDS :: "游戏开始"
TIP_POS :: raylib.Vector2{10, 10}

Game_Resource :: struct{
	font: raylib.Font,
	tip_pos: raylib.Vector2,	// 提示文字的坐标
	tip_words: cstring,		// 提示文字
}

load_game_resource :: proc() -> (resource: Game_Resource){	// 返回值一般用值类型
	// 所需要用到的全部字符(包括中英文,标点符号)
	c_strs := strings.clone_to_cstring(CHARSET_WORDS)	//转换成c风格字符串
	defer delete(c_strs)
	codepoint_count: i32
	// LoadCodepoints 会分析字符串，提取出里面用到的所有唯一字符
	codepoints := raylib.LoadCodepoints(c_strs, &codepoint_count)
	defer raylib.UnloadCodepoints(codepoints)
	// 传入码点数组和数量，告诉 Raylib 只生成这些中文字符的字形
	resource.font = raylib.LoadFontEx(FONT_PATH, FONT_SIZE, codepoints, codepoint_count)

	resource.tip_pos = TIP_POS
	resource.tip_words = cstring(TIP_WORDS)

	return resource

}

unload_game_resource :: proc(resource: ^Game_Resource){		// 结构体参数一般用指针
	raylib.UnloadFont(resource.font)
}

main :: proc(){
	
	// 核心：在初始化窗口前设置日志阈值
    // 只有 WARNING、ERROR 和 FATAL 级别的日志才会被打印
    raylib.SetTraceLogLevel(.WARNING) 

	// 窗口
	raylib.InitWindow(SCREEN_WIDTH,SCREEN_HEIGHT,"my odin game")
	defer raylib.CloseWindow()	// 程序退出关闭
	raylib.SetExitKey(.KEY_NULL)	// 设置 按esc 不关闭窗口

	
	game_s := load_game_resource()
	defer unload_game_resource(&game_s)


	// player
	player_pos := raylib.Vector2{400,300}
	player_speed :f32 = 300.0
	player_radius :f32 = 20.0

	raylib.SetTargetFPS(60)		// 设置帧率

	// 游戏循环
	for !raylib.WindowShouldClose(){
		// 控制帧率间隔
		dt := raylib.GetFrameTime()

		if raylib.IsKeyDown(.W) || raylib.IsKeyDown(.UP) do player_pos.y -= player_speed * dt
		if raylib.IsKeyDown(.S) || raylib.IsKeyDown(.DOWN) do player_pos.y += player_speed * dt
		if raylib.IsKeyDown(.A) || raylib.IsKeyDown(.LEFT) do player_pos.x -= player_speed * dt
		if raylib.IsKeyDown(.D) || raylib.IsKeyDown(.RIGHT) do player_pos.x += player_speed * dt

		// 渲染
		raylib.BeginDrawing()	// 开始渲染

		raylib.ClearBackground(raylib.RAYWHITE)

		// draw player
		raylib.DrawCircleV(player_pos,player_radius,raylib.LIME)


		raylib.DrawTextEx(game_s.font, game_s.tip_words, game_s.tip_pos, f32(FONT_SIZE), 2, raylib.DARKGRAY)

		raylib.EndDrawing() 	// 结束渲染

		// 帧结束,在此处统一释放临时内存
        free_all(context.temp_allocator) 

	}

}
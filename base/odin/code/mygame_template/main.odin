package main

import "vendor:raylib"
import "core:fmt"

main :: proc(){
	
    // 只有 WARNING、ERROR 和 FATAL 级别的日志才会被打印
    raylib.SetTraceLogLevel(.WARNING) 	// 这行代码要在初始化窗口之前
	// 窗口
	raylib.InitWindow(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
	raylib.SetExitKey(.KEY_NULL)		// 设置 按esc 不关闭窗口
	raylib.SetTargetFPS(FPS)			// 设置帧率
	defer raylib.CloseWindow()			// 程序退出关闭
	
	game_info: Game_Info
	game_init(&game_info)
	defer game_shutdown(&game_info)

	// 游戏循环
	for !raylib.WindowShouldClose(){
		// 控制帧率间隔
		dt := raylib.GetFrameTime()
		
		game_update(&game_info,dt)	// 更新
		game_draw(&game_info)		// 渲染

		// 帧结束,在此处统一释放临时内存
        free_all(context.temp_allocator) 
	}
}
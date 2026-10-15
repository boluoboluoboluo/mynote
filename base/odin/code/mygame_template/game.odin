package main

import "vendor:raylib"

Game_Info :: struct{
	res: Resource,
	tip_pos: raylib.Vector2,	// 提示文字坐标
	tip_words: cstring,			// 提示文字
	player: Player,
}

game_init :: proc(game_info: ^Game_Info){
	game_info.res = resource_load()	//加载资源
	game_info.tip_pos = TIP_POS
	game_info.tip_words = cstring(TIP_WORDS)

	player_init(&game_info.player)
}

game_update :: proc(game_info:^Game_Info,dt:f32){

	player_update(&game_info.player,dt)
}

game_draw :: proc(game_info:^Game_Info){
		raylib.BeginDrawing()	// 开始渲染
		raylib.ClearBackground(raylib.RAYWHITE)
		// draw player
		player_draw(&game_info.player)
		// draw tips
		raylib.DrawTextEx(game_info.res.font, game_info.tip_words, game_info.tip_pos, f32(FONT_SIZE), 2, raylib.DARKGRAY)

		raylib.EndDrawing() 	// 结束渲染
}

game_shutdown :: proc(game_info:^Game_Info){
	resource_unload(&game_info.res)
}
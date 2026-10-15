package main

import "vendor:raylib"

Player :: struct{
	pos: raylib.Vector2,
	speed: f32,
	radius: f32,
}

player_init :: proc(player:^Player){
	player.pos = PLAYER_INIT_POS
	player.speed = PLAYER_INIT_SPEED
	player.radius = PLAYER_RADIUS
}

player_update :: proc(player:^Player,dt:f32){

	if raylib.IsKeyDown(.W) || raylib.IsKeyDown(.UP) do player.pos.y -= player.speed * dt
	if raylib.IsKeyDown(.S) || raylib.IsKeyDown(.DOWN) do player.pos.y += player.speed * dt
	if raylib.IsKeyDown(.A) || raylib.IsKeyDown(.LEFT) do player.pos.x -= player.speed * dt
	if raylib.IsKeyDown(.D) || raylib.IsKeyDown(.RIGHT) do player.pos.x += player.speed * dt
}

player_draw :: proc(player:^Player){
	raylib.DrawCircleV(player.pos,player.radius,raylib.LIME)
}
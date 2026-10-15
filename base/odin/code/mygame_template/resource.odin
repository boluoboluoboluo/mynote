package main

import "vendor:raylib"
import "core:strings"

Resource :: struct{
	font: raylib.Font,
}

resource_load :: proc() -> (res: Resource){	// 返回值一般用值类型
	// 所需要用到的全部字符(包括中英文,标点符号)
	c_strs := strings.clone_to_cstring(CHARSET_WORDS)	//转换成c风格字符串
	defer delete(c_strs)
	codepoint_count: i32
	// LoadCodepoints 会分析字符串，提取出里面用到的所有唯一字符
	codepoints := raylib.LoadCodepoints(c_strs, &codepoint_count)
	defer raylib.UnloadCodepoints(codepoints)
	// 传入码点数组和数量，告诉 Raylib 只生成这些中文字符的字形
	res.font = raylib.LoadFontEx(FONT_PATH, FONT_SIZE, codepoints, codepoint_count)

	return res
}

resource_unload :: proc(res: ^Resource){		// 结构体参数一般用指针
	raylib.UnloadFont(res.font)
}
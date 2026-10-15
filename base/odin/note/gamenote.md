### 项目组织

```go
// 由于odin 语言同文件夹下文件天然互通,不需要显示引入
// 导致不知道哪个方法或者变量来自哪个文件

// 定义规范
 -- 文件里的结构体和方法名前缀和文件名相同
```

```go
// 项目结构参考

my_game/
├── build.bat / build.sh       # 构建脚本
├── assets/                    # 资源目录（图片、声音、配置等）
└── src/                       # 源代码根目录
    ├── main.odin              # 游戏入口，负责初始化和主循环
    │
    ├── core/                  # 核心基础模块（不依赖具体游戏逻辑）
    │   ├── package.odin       # (可选) 显式导出定义
    │   ├── window.odin        # 窗口与输入管理
    │   ├── renderer.odin      # 渲染封装
    │   └── audio.odin         # 音频封装
    │
    ├── game/                  # 游戏具体的业务逻辑（核心扩展区）
    │   ├── types.odin         # 游戏内全局共享的数据结构、枚举
    │   ├── state.odin         # 游戏状态机（主菜单、游戏中、暂停等）
    │   ├── player.odin        # 玩家逻辑
    │   ├── enemy.odin         # 敌人逻辑（可再分子目录）
    │   └── world.odin         # 地图、关卡与碰撞系统
    │
    └── utils/                 # 工具库
        ├── math.odin          # 数学计算辅助
        └── common.odin        # 通用宏或辅助函数

```



### 代码解析

```go
// import "vendor:raylib"
 -- 这行代码告诉 Odin 编译器去链接 Raylib 的二进制库（如 .dll、.so 或 .a 文件）
 -- Odin 的 vendor 库为你做好了 C 语言函数指针的映射。在程序启动时，操作系统会把 Raylib 的机器码加载到内存中，让你的 Odin 程序可以直接调用它们

// raylib.InitWindow(...)	
 -- 创建系统窗口：
 	在 Windows 上它调用了 CreateWindowExW()，在 Linux 上调用了 XCreateWindow() 或 Wayland API。
	操作系统为此窗口分配内存、注册句柄、并将其加入桌面的窗口管理器中
 -- 初始化图形上下文:
	Raylib 会通过 GLFW 库向显卡驱动申请一个 OpenGL 渲染上下文
	此时，显卡驱动会为你的窗口分配前缓冲区 和后缓冲区，专门用来存放画面像素

// defer raylib.CloseWindow()
 -- Odin 的 defer 会在函数退出时执行。它在底层执行了彻底的垃圾回收
	销毁刚才创建的 OpenGL 图形上下文、通知操作系统关闭窗口并释放窗口句柄、解绑输入设备（键盘鼠标），防止程序退出后造成内存泄漏或句柄残留。

// raylib.SetTargetFPS(60)
 -- 它在底层启动了一个高精度的定时器（Timer）。
	Raylib 记录下每帧的目标时间（1000 ÷ 60 ≈ 16.67 毫秒）。
	在后面的主循环中，如果一帧处理得太快（如只用 2毫秒），Raylib会调用操作系统的休眠函数
	让 CPU 核心主动挂起剩下的 14.67 毫秒，从而防止 CPU 跑满到 100% 并导致电脑发热。

// for !raylib.WindowShouldClose() {}
 -- 这是一个操作系统消息泵（Message Pump / Event Loop）。每执行1次循环，Raylib 底层就会向操作系统查询：
	-- 用户刚才点红叉了吗？按 Esc 了吗？把窗口拖走了吗？
	-- 如果用户点了红叉，操作系统会发送一个 WM_CLOSE 信号，Raylib 捕获后把内部的一个布尔值设为 true，循环就会终止。
	-- 同时，这个函数内部也会顺便刷新键盘和鼠标的状态（供 IsKeyDown 使用）。

// raylib.BeginDrawing()
 -- 清空画布: 通知显卡把后缓冲区（Back Buffer）里的旧像素全部擦除（通常擦成你指定的颜色，如白色）
 -- 状态机切换: OpenGL 是一个巨大的状态机，这一步会告诉显卡：
	我要开始往后缓冲区输入 2D 几何图形的顶点数据了，请准备好着色器（Shader）

// raylib.DrawCircleV(...)
 -- 数学离散化（CPU 端）:
	-- Raylib 在 CPU 里把这个圆拆分成几十个很小的三角形扇（Triangle Fan）。利用三角函数(sin / cos) 计算出这几十个三角形顶点的 X 和 Y 坐标
 -- 数据传输（Gpu 交互）:
	-- Raylib 把这些顶点坐标和颜色数据（RGBA 值）打包，通过 PCIe 总线发送给显卡的显存（VRAM）
 -- 光栅化与着色（GPU 端）:
	-- 显卡接收到顶点后，运行内置的着色器程序，把这些三角形变成一个个像素点，并把颜色写入后缓冲区对应的像素网格里。此时你在屏幕上还看不到它
	-- 执行到 raylib.EndDrawing() 时，Raylib 才会调用 SwapBuffers()，把画好的后缓冲区与屏幕正在显示的前缓冲区进行对调	
```

### 问题

```go
// 数据类型为什么要 f32 ,可不可以 payer_radius : f8,它们一起运算会怎样?
 -- 因为在现代计算机 CPU 和 GPU 的标准中，根本没有 f8（8位浮点数）这种数据类型
 -- 最基础、最通用的类型就是 f32（单精度浮点数，4字节） 和 f64
 -- 显卡的硬件架构是全为了 f32 优化的。显卡里有成千上万个 32 位浮点运算单元，用 f32 计算速度最快

 -- 强类型语言,不同类型的数据是绝对不能直接一起运算的, 编译器会报错
	speed: f32 = 300.0
	bonus: i32 = 10 
	// 必须把 bonus 转换成 f32 才能运算
	total_speed := speed + f32(bonus) 

// 用的浮点数小球坐标,画的时候是怎么转换成整数对应到屏幕位置的像素格子呢?
 -- 显卡的光栅化 :
	把浮点数坐标提交给显卡, 它会根据这个浮点数坐标，计算出这个圆在屏幕上覆盖了哪些像素格子
 -- 像素四舍五入与抗锯齿 :
	如果开启抗锯齿 -> 坐标在一个像素的中间（例如 0.5 处）时，显卡不会生硬地把它变黑或变白，而是会计算一个“覆盖率”
	如果关闭抗锯齿 -> 显卡会直接对坐标进行四舍五入或向下取整

// 为什么运行的时候内存,占了70多M? 我用pygame写一个简单的窗口程序才占10多M呢?
 -- Pygame 的欺骗性 :
	Pygame 底层基于 SDL1.2/2.0。当你看到 Pygame 只占 10M 内存时，那只是 Python 解释器和部分 CPU 数据的内存
	Pygame 默认使用的是 CPU 软件渲染
	它把很多图形窗口的缓冲工作交给了操作系统去打理。操作系统帮你占用的那部分显存和内存，并没有计入 Pygame 的进程里
 -- Raylib 的现代架构（显存与驱动预留）:
	Raylib 启动时，直接向显卡驱动申请了一个现代 OpenGL 渲染上下文
	为了保证游戏高效率、不卡顿，显卡驱动（比如 NVIDIA 或 AMD 驱动）会在你的游戏进程里预先开辟、隐藏分配一块缓冲区
	用来存放诸如顶点缓冲区、着色器程序以及随时准备提交给显卡的帧缓冲。这 70M 里，有 50M 以上其实是显卡驱动和 OpenGL 上下文的预开销
 -- 增长曲线不同: 
	Raylib 的 70M 是“起步价”。你的游戏里多放 10 个小人，内存可能还是 70M，几乎不涨
	Pygame 随着图片变多、游戏逻辑变复杂，Python 解释器的垃圾回收负担变重，内存会飙升得非常快
```

```go
// raylib 和 SDL 的区别是什么
 -- 见下表
```

| 特性           | **SDL (Simple DirectMedia Layer)**                           | **Raylib**                                                   |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **定位**       | **底层包装库 (Wrapper)**                                     | **上层游戏框架 (Framework)**                                 |
| **它负责什么** | 它只负责最脏最累的活：怎么帮你在不同系统上建个窗口、怎么获取键盘鼠标、怎么播放声音。它**默认不帮你画任何高级图形**。 | 它不仅帮你建窗口，还内置了一整套**图形渲染引擎、数学库、文字渲染器、甚至是 3D 渲染和简单的物理碰撞**。 |
| **画一个圆**   | 在 SDL 里，你得自己写算法去计算圆的像素点（或者调用第三方扩展库）。 | 直接调用 `DrawCircle`，一行代码搞定。                        |
| **3D 游戏**    | SDL 自身完全不支持 3D，你必须自己手写 OpenGL/Vulkan 代码配合 SDL。 | 内置 3D 渲染，可以直接加载 `.obj` 3D 模型和光源。            |
| **使用体验**   | 像是一个**毛坯房**，地基和框架很好，但家具（绘图函数）得你自己搬进去。 | 像是一个**精装房**，家具家电一应俱全，带上行李（代码逻辑）就能直接住。 |

**总结**：游戏开发者一般不直接用纯 SDL 码游戏，而是用 SDL 制作自己的引擎。而 **Raylib 就是一个别人用 C 语言和 OpenGL 帮你写好的、极度轻量且好用的现成 2D/3D 游戏引擎**，非常适合个人创作者。

### 程序问题

```go
// 关于局部变量和临时内存
 -- 局部变量,方法结束后,自动释放内存
 -- 临时内存,不会主动释放
	它会等到程序在某处执行 free_all(context.temp_allocator) 后,进行释放
	// 示例,分配到临时内存
	c_chinese_str := strings.clone_to_cstring(chinese_str, context.temp_allocator)
```



```go
// DrawText 显示的 中文乱码
 -- 默认使用的是 Raylib 自带的内置字体。这个内置字体只包含了基础的英文 ASCII 字符，根本没有中文字形
 -- Raylib 的 LoadFont 默认只加载 95 个 ASCII 码（英文和常用符号）
 -- 解决方案 :
	// 你需要加载一个支持中文的系统字体文件（如 .ttf 或 .otf），并在渲染时指定它。
	// 注意 .ttc 不支持,会导致乱码

	// 定义你想在游戏里显示的汉字字符串
	chinese_str := "你好，Odin 游戏世界！使用方向键控制移动"
	// 将 string 转换为 cstring（并在当前作用域结束时自动释放内存）
	c_chinese_str := strings.clone_to_cstring(chinese_str,)
	defer delete(c_chinese_str)
	// 获取字符串中所有字符的 Codepoints（码点个数）
    codepoint_count: i32
	// LoadCodepoints 会分析字符串，提取出里面用到的所有唯一字符
    codepoints := raylib.LoadCodepoints(c_chinese_str, &codepoint_count)
	defer raylib.UnloadCodepoints(codepoints) // 记得释放码点内存
	font_size: i32 = 32
	font := raylib.LoadFontEx("C:\\Windows\\Fonts\\simhei.ttf", font_size, codepoints, codepoint_count) 	
	defer raylib.UnloadFont(font) 	// 记得退出时释放字体

---------------------------
// 函数 raylib.DrawText
 -- 只支持英文和数字
	raylib.DrawText(text: cstring, posX: i32, posY: i32, fontSize: i32, color: raylib.Color)
	raylib.DrawText("Hello World! Score: 100", 20, 20, 20, raylib.RED)	// 示例
// 函数 raylib.DrawTextEx
 -- 支持中文/高清字体
 -- 它允许你传入通过 LoadFont 或 LoadFontEx 加载的自定义字体（如 .ttf, .otf）
	raylib.DrawTextEx(
        font:      raylib.Font,    // 1. 你加载的自定义字体对象
        text:      cstring,        // 2. 转换后的 cstring 文本
        position:  raylib.Vector2, // 3. 坐标结构体 {x, y}，必须是 f32 类型
        fontSize:  f32,            // 4. 字体大小，注意是 f32 类型
        spacing:   f32,            // 5. 字间距（通常设为 1.0 或 2.0，设为 0 会挤在一起）
        tint:      raylib.Color,   // 6. 字体颜色
    )
	raylib.DrawTextEx(font, c_chinese_str, tip_pos, f32(font_size), 2, raylib.DARKGRAY)	// 示例
---------------------------
// 函数 raylib.LoadFont
 -- 内部默认只会加载基础的 95 个 ASCII 字符,不支持中文
	raylib.LoadFont(fileName: cstring) -> raylib.Font
	font := raylib.LoadFont("my_cool_english_font.ttf")		// 示例

// 函数 raylib.LoadFontEx
 -- 精准控制要加载的字体大小以及需要加载哪些字符（码点/Codepoints）
	中文字符有成千上万个，如果把整张字库全加载进显存，游戏会瞬间卡死或崩溃。LoadFontEx 允许你传入一个「码点数组」（即你指定要用的汉字集合），告诉 Raylib：“我只用这几个汉字，你帮我把这几个汉字的图案生成好就行了。” 这样既能显示中文，又极大地节省了显存。
	raylib.LoadFontEx(
    fileName:       cstring, // 1. 字体文件路径（如 "simhei.ttf"）
    fontSize:       i32,     // 2. 预设的字体大小（如 32）。建议游戏中用多大，这里就填多大，这样字体的清晰度最高
    codepoints:     ^i32,    // 3. 指向码点数组的指针（告诉 Raylib 哪些汉字需要被加载）
    codepointCount: i32,     // 4. 码点数组里的字符总数量
) -> raylib.Font

```

```go
// c风格字符串cstring,odin原生字符串 区别是什么,一般它们分别用于哪些场景,怎么转换
 -- 区别,见下表
 -- 转换: 
	因为 cstring 必须以 \x00 结尾，所以转换通常伴随着内存分配（把原来的字串复制一份，并在末尾补上 \x00）

// string转 cstring:
	方式一:
	使用临时分配器（context.temp_allocator），它在一帧结束或特定时候统一释放，效率极高
	import "core:strings"
    odin_str := "你好 Raylib"
    // 转换并放入临时内存
    c_str := strings.clone_to_cstring(odin_str, context.temp_allocator) 
	
	方式二:
	使用默认分配器。因为是手动申请的，必须手动 delete，否则会内存泄漏。
    import "core:strings"
    odin_str := "游戏标题"
    c_str := strings.clone_to_cstring(odin_str) // 转换为cstring,默认分配堆内存
    defer delete(c_str) // 确保在作用域结束时释放

	方式三:
	字符串是写死在代码里的英文字面量，可以在末尾加 \x00，然后通过 cstring(...) 强转（这种方式不需要分配新内存）。
	c_str := cstring("Hello World\x00") // 安全，无需释放

//  从 cstring 转换为 string（较少用）
	当你从 Raylib 或其他 C 库获取到一个文本（比如玩家输入的文本或系统路径），需要拿到 Odin 内部处理时使用
	import "core:strings"
    // 假设这是从某个 C 库函数获取到的 cstring
    c_str: cstring = get_some_c_p_string() 
    // 转换方法：Odin 会自动计算长度并包装成原生 string 结构
    odin_str := string(c_str) 

	//注：这样转换出来的 odin_str 只是共享了 cstring 的指针。如果那个 cstring 随后被 C 库释放了，这个 odin_str 就会失效。如果需要长期持有，应该使用 strings.clone(string(c_str)) 复制一份。
```

| 特性         | Odin 原生字符串 (`string`)                                   | C 风格字符串 (`cstring`)                                     |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **底层结构** | **包含两个部分**：一个指向数据的指针，一个记录长度的整数（`len`）。 | **只有一个指针**：直接指向字符数据的内存地址。               |
| **结束标志** | **不依赖**任何特殊字符，长度由 `len` 决定。可以包含零值字节 `\x00`。 | **必须以空字符 `\x00` (Null-terminator) 结尾**。             |
| **安全性**   | **高**。因为知道明确长度，不会发生由于找不到结尾导致的内存越界。 | **低**。如果内存末尾漏掉了 `\x00`，读取时会一直向后蔓延，导致乱码或程序崩溃。 |
| **性能**     | 获取长度（`len(str)`）是 O(1) 复杂度（瞬间完成）。           | 获取长度必须遍历整个字符串直到发现 `\x00`，是 O(N) 复杂度。  |
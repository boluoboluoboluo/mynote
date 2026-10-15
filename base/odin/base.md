

```go
// 多行注释
使用 /* 开头，并用 */ 结尾



// 变量连接,输出

//导入文件 库文件?

// 运算符

//关系运算

```

```go
// 变量类型

a := 11
fmt.printf("%T\n", a)	// 打印变量类型

a := "ddd"
tid := typeid_of(type_of(a)) 
fmt.println("类型是:",tid)	// string
```

```go
// print

fmt.print("hello")				//打印
fmt.println("hello")			//打印,自动换行 \n
fmt.printf("%s","heelo")		//格式占位符 打印

a := fmt.tprint("ddd")			//临时分配内存
a := fmt.tprintf("dd%s","kk")	//临时分配内存,占位符形式

a := fmt.aprint("ddd")			//动态分配内存,需手动释放
a := fmt.aprintf("dd%s","kk")	//动态分配内存,占位符形式,需手动释放

fmt.fprint(w, ...)				// 把内容写入实现了 io.Writer 的接口 w
fmt.fprintln(w, ...)			// 写入内容并在末尾加换行
fmt.fprintf(w, format, ...)		// 使用占位符格式化写入

// 固定大小的内存（比如一个字节数组），想往里面格式化写数据，不产生任何新的内存分配
fmt.bprintf(buf, format, ...)	//将格式化后的字符串安全地写入 []u8 缓存区中。

fmt.eprintf("error")	// 向标准错误流打印
```



```go
// 0 false nil 区别:

// 0 
数值类型(如 int, f32, u8 等)
0 根据你声明的数值类型，占用 1, 2, 4 或 8 个字节

// false
布尔类型(bool)
false 在内存中通常占用 1 个字节（值为 0x00）

// nil
指针/零值字面量(untyped nil) 用于表示指针、切片、动态数组、映射（map）或过程（proc）的'空'或'未初始化'状态
nil 赋值给指针时，在内存中占用 4 或 8 个字节（取决于 32 位还是 64 位系统），其地址为 0x0
-----------------------------

// 编译期 严格的类型安全（没有隐式转换）

if true{fmt.print("hello")}		// 正确
if 1{fmt.print("hello")}		// 报错
if nil{fmt.print("hello")}		// 报错
if 0==false{}	//报错
if 0==nil{}		//报错
if false==nil{}	//报错


// 对于普通的 0、false 和 nil，底层没有任何类型标识符，纯靠编译器在编译时看管。
// 只有当你使用 any 类型或者进行运行时反射（Reflection）时，Odin 才会暴露出 typeid（类型标识符）

```

```go
// any 类型
 -- any 类型是 Odin 提供的特殊机制，用于在运行时代表任何类型。
 -- 只有当你把一个变量赋值给 any 时，编译器才会生成一个包含'类型标识符'的结构体：

// 显式使用 any 类型
val: any = i32(0) 

// any 的底层真实定义 (固定 16 字节 的结构体)
any :: struct {
    data: rawptr,      // 指向真实数据的指针 (8 字节)
    id:   typeid,      // 类型标识符！(Type ID，占用 8 字节)
}

```

```go
// 关于宏
// 宏（Macro） 的核心本质就是“代码的自动代换”
// 编译阶段起作用

// odin 内置编译指令 来替代宏

// 编译期条件判断 (#if)
#if ODIN_OS == .Windows {
    // 只有在 Windows 下编译时，这段代码才会被纳入
}

```

```go
// 关于 变量内存释放
在 Odin 语言中，函数内部的数据是否需要手动释放，取决于它在内存中存储的位置：是在栈（Stack）上，还是在堆（Heap）上。
普通变量都在栈上，不需要手动释放；只有通过'分配器（Allocator）'显式在堆上申请的动态数据，才需要手动释放

// 栈内存
 -- 基础类型普通变量
	如 a := 123, b := false, c := 3.14
 -- 固定大小的数组
	arr: [5]int			// 占用固定大小的连续栈内存
 -- 普通结构体实例
	p := Player{hp = 100}
 -- 临时字符串的指针和长度
	如 s := "hello") 	//本身存储在只读数据区
-------------------------------
// 堆内存 / 动态内存
 -- 使用 make 创建的动态数组，其底层内存是动态分配的
	arr := make([dynamic]int)
	defer delete(arr) 	// 必须释放，否则底层分配的内存会泄漏

 -- 映射 (Maps)
	哈希表在底层涉及复杂的动态内存桶结构
	scores := make(map[string]int)
	defer delete(scores) // 必须释放

 -- 显式分配的指针 (Allocated Pointers)
	通过分配器为某个结构体或变量单独申请了堆内存
	p_ptr := new(Player)	// 堆上为 Player 结构体申请内存，返回指针
	defer free(p_ptr) 		// 指针使用 free 释放，或者 delete(p_ptr^)

 -- 堆分配的字符串
	字符串进行克隆复制
	s := strings.clone("copy me")
	defer delete(s) 		// 必须释放



```



#### common

##### 输入

```go
package main

import "core:fmt"
import "core:os"

main :: proc() {
    fmt.print("请输入您的名字: ")
    
    // 准备一个缓冲区用于接收输入的文本
    buf: [128]byte
    
    // 从标准输入 (stdin) 读取一行
    n, err := os.read(os.stdin, buf[:])
    if err != nil {
        return
    }
    
    // 将读取到的字节切片转换为字符串（去掉尾部的换行符）
    input_text := string(buf[:n-1]) 
    
    fmt.printf("你好，%s!\n", input_text)
    
    // 仅仅想实现“按回车键继续...”的效果：
    fmt.print("按回车键退出程序...")
    os.read(os.stdin, buf[:1]) 
}

```

##### 睡眠

```go
package main

import "core:fmt"
import "core:time" // 1. 导入时间包

main :: proc() {
    fmt.println("开始倒计时...")
    
    // 睡眠 2 秒钟
    time.sleep(2 * time.Second) // 1.3.2
    fmt.println("过去了 2 秒")
    
    // 睡眠 500 毫秒
    time.sleep(500 * time.Millisecond) // 1.3.3
    fmt.println("又过去了 500 毫秒")
}
```

##### 随机数

```go
package main

import "core:fmt"
import "core:math/rand" // 导入随机数包

main :: proc() {
    // 1. 生成一个指定范围内的整数 [lo, hi) —— 包含下界，不包含上界
    // 比如生成一个 1 到 100 之间的随机数（包含 1，不包含 101）
    secret_num := rand.int32_range(1, 101) // 1.2.2
    fmt.println("1-100随机数:", secret_num)
    
    // 2. 生成一个 0.0 到 1.0 之间的随机浮点数
    float_num := rand.float32()
    fmt.println("随机浮点数:", float_num)
    
    // 3. 顺便生成一个布尔值（正反面）
    coin_flip := rand.bool()
    fmt.println("硬币正反:", coin_flip)
}

```



```go


```

#### 关键字

```go
// 声明与定义： package, import, proc, struct, union, enum, bit_field, bit_set, map, matrix
// 控制流： if, else, for, in, switch, case, break, continue, fallthrough, defer, return
// 特殊控制： when（编译期 if 语句）、where（泛型约束）
// 内置常量： true, false, nil
// 类型与转换： distinct, transmute, cast, typeid
// 其它/上下文： context, asm, inline, no_inline
```



#### 变量和声明

```go
// 变量声明（推导类型）
// Odin 采用类型后置的声明方式。

x := 42 	// 平台默认的 int 类型
y : f32 = 3.14

// 显式变量声明（未初始化，使用默认零值值）
z: i32 

// 常量声明（使用 ::）
PI :: 3.14159265

整数： i8, i16, i32, i64, i128 和无符号 u8 到 u128。还有 int 和 uint（取决于架构）。
浮点数： f16, f32, f64。
布尔： bool
字符串： string（只读的字节切片）和 cstring（兼容 C 语言的零结尾字符串）

// ------------------------
// 变量转换
// 没有隐式的类型转换（除了无损的字面量赋值）。你需要显式地进行类型转换

// 方式一 cast(目标类型) 表达式
a: i32 = 42
// 将 i32 转换为 f32 浮点数
b := cast(f32)a 

price: f64 = 19.99
// 将浮点数截断转换为整数
int_price := cast(int)price // 结果为 19

// 方式二 transmute(目标类型) 表达式
// 目标类型和原始类型占用的内存大小必须完全一致
// 把 4 个字节的浮点数，直接当做 4 个字节的无符号整数来读其位模式
f_val: f32 = 1.0
u_val := transmute(u32)f_val 
// ------------------------
// 编译期类型判断 (when + typeid_of)
// 用于泛型或编译期分支，不产生运行时开销。
print_val :: proc(val: $T) {
    // when 是编译期的 if
    when T == int {
        fmt.println("这是一个整数:", val)
    } when T == string {
        fmt.println("这是一个字符串:", val)
    }
}
// 运行时类型判断 (Any 类型 + switch type)：
// Odin 拥有内置的 any 类型（包含数据指针和 typeid）。你可以使用 switch in 来像动态语言一样判断和解包类型：
print_any :: proc(val: any) {
    switch v in val {
    case int:    fmt.println("运行时 int:", v)
    case string: fmt.println("运行时 string:", v)
    case:        fmt.println("其它未知类型")
    }
}
// ------------------------
```

#### 数字运算

```go
import "core:math"

a := 10
b := 3

sum := a + b   // 13
diff := a - b  // 7
prod := a * b  // 30
div := a / b   // 3 (整数除法直接截断)
mod := a % b   // 1 (取模/求余)

// 位运算
bits := 1 << 3 // 8 (左移，相当于 2 的 3 次方)
and_res := 5 & 3 // 1 (按位与)


x := -4.5
v1 := math.abs(x)    // 4.5 (绝对值)
v2 := math.floor(x)  // -5.0 (向下取整)
v3 := math.ceil(x)   // -4.0 (向上取整)
v4 := math.sqrt(16.0) // 4.0 (平方根)

// 幂运算
pow_res := math.pow(2.0, 3.0) // 8.0 (2 的 3 次方)

// 三角函数（传入弧度）
sin_val := math.sin(math.PI / 2) // 1.0


```

#### 字符串操作

`string` 本质上是一个**只读的字节切片**（结构体包含一个数据指针和一个长度）。要对字符串进行查找、分割、拼接等操作，需要导入 **`core:strings`** 包

```go
import "core:fmt"
import "core:strings"

main :: proc() {
    str := "Hello, Odin Language!"

    // 1. 获取长度 (直接使用内置的 len)
    length := len(str) // 21 (字节数)

    // 2. 检查包含与前后缀
    has_odin := strings.contains(str, "Odin") // true
    is_hello := strings.has_prefix(str, "Hello") // true

    // 3. 查找子串位置
    idx := strings.index(str, "Odin") // 7 (未找到返回 -1)

    // 4. 字符串裁剪 (去空格或指定字符)
    dirty_str := "   hello   "
    clean_str := strings.trim_space(dirty_str) // "hello"

    // 5. 字符串拼接 (使用 Builder，高效且避免内存碎片)
    sb: strings.Builder
    strings.builder_init(&sb)
    defer strings.builder_destroy(&sb)
    
    strings.write_string(&sb, "Game ")
    strings.write_string(&sb, "Engine")
    result := strings.to_string(sb) // "Game Engine"
    
    // 6. 分割字符串
    csv := "apple,banana,orange"
    fields, _ := strings.split(csv, ",") // 返回一个切片 []string
    defer delete(fields) // 注意：split 分配了切片内存，需要手动释放
}

```

#### 时间操作

```go
import "core:fmt"
import "core:time"

main :: proc() {
    // 1. 获取当前时间点
    start_time := time.now()

    // 2. 模拟耗时操作 (例如让程序睡眠 100 毫秒)
    time.sleep(100 * time.Millisecond)

    // 3. 计算时间差 (两个 Time 相减，得到一个 Duration)
    end_time := time.now()
    elapsed := time.diff(start_time, end_time)

    // 4. 将时长转换为所需的单位
    ms := time.duration_milliseconds(elapsed)
    fmt.printf("操作耗时: %f 毫秒\n", ms)

    // 5. 时间点的加减
    // 在当前时间的基础上增加 1 小时
    future_time := time.time_add(start_time, 1 * time.Hour)
    
    // 6. 格式化输出可读时间
    // Odin 支持通过指定格式将时间打印或转换为字符串
    fmt.println("当前高精度纳秒时间戳:", start_time._nsec)
}

```



#### 条件分支

```go
// 条件分支
// Odin 的控制流不需要圆括号，但大括号是强求的

score := 85
if score >= 90 {
    fmt.println("优秀")
} else if score >= 60 {
    fmt.println("及格")
} else {
    fmt.println("不及格")
}
```

#### for循环

```go
// for循环
// Odin 只有 for 一种循环关键字，但功能极其丰富

// 经典范围循环 (0 到 9)
for i in 0..<10 {
    fmt.println(i)
}

// 遍历数组/切片
items := [3]string{"苹果", "香蕉", "橙子"}
for item, index in items {
    fmt.printf("%d: %s\n", index, item)
}

// 类似 while 的循环
cond := true
for cond {
    // 执行代码
    cond = false
}
```

#### 结构体

```go
// 结构体
// 复合类型

Vector3 :: struct {
    x: f32,
    y: f32,
    z: f32,
}

// 实例化
v := Vector3{1.0, 2.0, 3.0}
v2 := Vector3{x = 5.0} // 指定字段初始化
```

#### 数组和切片

```go
// 数组和切片
// 固定数组： 长度是类型的一部分：[4]int
// 切片： 动态视窗：[]int
// 动态数组： 类似 C++ std::vector：[dynamic]int

arr: [3]int = {1, 2, 3}
slice: []int = arr[0..2] // 切片截取
dyn_arr: [dynamic]int
defer delete(dyn_arr) // 延迟释放内存
append(&dyn_arr, 10)
append(&dyn_arr, 20)
```

#### 函数和过程

```go
// 函数和过程
// 在 Odin 中，函数被称为 Procedure（过程），使用 proc 关键字声明。支持多返回值和命名返回值。

// 基础函数
add :: proc(a, b: int) -> int {
    return a + b
}

// 多返回值与延迟执行 (defer)
divide :: proc(a, b: f32) -> (f32, bool) {
    if b == 0 {
        return 0, false
    }
    return a / b, true
}
```

#### defer关键字

```go
// defer 关键字
// defer 用于延迟语句的执行到当前作用域结束时，非常适合用于资源和内存清理

file_open()
defer file_close() // 确保即使后面发生错误，文件也会被关闭
// 执行读取操作...
------------
// 编译期语法糖
 -- 当编译器检测到控制流即将离开当前作用域（例如遇到 return、循环中的 break/continue，或者自然执行到大括号 } 结尾）时，它会自动在这些退出点之前，以“后进先出”（LIFO）的顺序注入 defer 后面的代码
------------
// 作用域:
 -- defer 不仅仅针对整个函数。如果 defer 写在 if 块、for 循环或显式的 {} 代码块内部，它会在离开该代码块时立即执行，而不是等待整个函数结束
------------
// 求值时机 (Evaluation): 
-- defer 后面表达式中的参数变量会立即求值并捕获，但表达式的函数调用本身会延迟执行
x := 10
defer fmt.println(x) // 此时 x 的值 (10) 已经被捕获
x = 20
// 函数退出时，打印的是 10，而不是 20
------------

```

#### 内存管理 Allocator

```go
// 显式内存管理与 Allocator 接口
// Odin 不支持垃圾回收（GC），但它把分配器（Allocator）作为一等公民。你可以非常轻松地为特定代码块指定自定义分配器（如 Arena 分配器），这在游戏开发中极具威力。
// make 和 delete 它们成对出现，专门用来管理动态数据结构的生命周期

import "core:mem"

main :: proc() {
    // 使用 Arena 分配器进行高效的临时内存分配
    arena: mem.Arena
    mem.arena_init(&arena, make([]u8, 1024))
    defer delete(arena.backing)
    
    // 将当前上下文的分配器临时替换为 arena 分配器
    context.allocator = mem.arena_allocator(&arena)
    
    // 这里的分配都发生在 arena 中，无需手动逐个 free
    data := make([]int, 10) 
}
```

#### 上下文Contetxt

```go
// 上下文系统 (Context)
// Odin 拥有一个隐式的 context 变量，它在函数调用间传递。它包含了当前的分配器、日志记录器和线程信息，这允许你在不改变函数签名的情况下，改变深层第三方库的内存分配行为。
```


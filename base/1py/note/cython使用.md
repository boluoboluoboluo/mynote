#### 说明

```sh
# 说明
-- 它是 python 的第三方库
-- 它是 Python 的超集（Python + C 类型的结合体）。它既能看懂几乎所有的 Python 代码，又允许你在代码里直接写 C 语言的数据类型和函数
-- 后缀: .pyx

# 功能
1.让 Python 代码获得 C 语言的速度
2.当作胶水，无缝连接 C/C++ 的现成库

# 原理
.pyx文件 
-> cython编译器翻译成c源码
	-- 自动生成 .c 文件
-> 调用 GCC/MSVC 编译器,把c源码编译成二进制机器码
	-- 扩展模块 .so (Linux) 或 .pyd (Windows)
-> python 文件可以正常 import 使用

# 安装 
1. c++编译环境 (msvc)
	-- windows: 安装 Visual Studio Build Tools	  # 或只安装轻量的 gcc 编译器: (MinGW-w64)
	-- linux: sudo apt install build-essential		# ubuntu/debian,检查安装: gcc --version

2. python 环境
3. pip install cython

```

```py
# 示例: test.pyx
# 这是一个标准的 Cython 代码 (.pyx 文件)

# 1. 它可以写纯 Python
def normal_func():
    print("Hello from Cython")

# 2. 关键：它可以用 cdef 定义纯 C 类型的变量和函数
def fast_sum(int limit):
    cdef int i
    cdef int result = 0
    for i in range(limit):
        result += i
    return result
```



#### 示例

1. 编写 Cython 核心文件

   在你的项目文件夹下，新建一个文件，命名为 **`example.pyx`**（注意后缀是 `.pyx`），写入以下带有 C 类型的代码

   ```py
   # example.pyx
   def test_speed(int N):
       cdef int i
       cdef double result = 0.0
       for i in range(N):
           result += i * 0.5
       return result
   
   ```

2. 编写编译脚本

   在同一个文件夹下，新建一个普通的 Python 文件，命名为 **`setup.py`**，用来告诉系统如何编译：

   ```py
   # setup.py
   from setuptools import setup
   from Cython.Build import cythonize
   
   setup(
       ext_modules = cythonize("example.pyx")
   )
   
   ```

3. 执行编译命令

   打开终端，切换到你存放这两个文件的目录，运行以下编译命令：

   ```sh
   # 编译:
   python setup.py build_ext --inplace		# 建议在 linux 下编译
   
   # 说明:
   build_ext 	#代表构建扩展模块
   --inplace 	#代表把编译好的二进制文件直接放在当前文件夹下。
   
   # 编译后出现的文件:
   example.c	#这是 Cython 自动帮你生成的、长达几千行的 C 语言源码文件
   example.cp3x-xxxx.pyd (Windows) 或 .so (Mac/Linux)	#这是最终编译好的二进制动态链接库。
   ```

4. 在普通 Python 中调用

   现在，新建一个普通的 **`main.py`** 文件，就可以直接像导入普通模块一样调用这个百倍速的二进制文件了：

   ```py
   # main.py
   import time
   import example  # 导入刚刚编译好的模块
   
   N = 50000000  # 5000万次循环
   
   start = time.time()
   res = example.test_speed(N)
   end = time.time()
   
   print(f"计算结果: {res}")
   print(f"Cython 耗时: {end - start:.6f} 秒")
   
   ```

5. 运行

   ```sh
   # 在终端直接运行：
   python main.py
   ```

   
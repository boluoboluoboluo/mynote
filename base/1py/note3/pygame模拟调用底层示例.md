#### 问题

```sh
# 我的问题:
沿用pygame调用底层接口的逻辑,从头手动搭建并实现这个流程,完成最简单的功能:
最简单的python代码,直接调用window的绘制窗体api

编译dll
编写base.pyd
打包
发布
python导入包,调用

这个过程怎么实现

# 问题概述:
用 Windows 系统自带的 Win32 API 来实现一个最简单的功能：在 Python 中导入你写的包，调用一个方法，直接在桌面上弹出一个 Windows 原生空白窗体。
```

#### 解析

##### 一. 编写与编译底层 DLL

（模拟 SDL 库）

首先，我们用 C 语言写一个底层核心库，模拟 SDL 的角色。它负责直接和 Windows 操作系统打交道。

**编写 C 语言源码 `mylib.c`**

这个文件负责向 Windows 申请创建窗口。

```c
#include <windows.h>

HWND hwnd = NULL; // 全局变量，记录窗口“快捷方式”

// 1. init 时调用的函数：只负责把窗口在桌面上“画出来”就完事
__declspec(dllexport) void __stdcall CreateWindowOnly() {
    HINSTANCE hInstance = GetModuleHandle(NULL);
    WNDCLASS wc = {0};
    wc.lpfnWndProc = DefWindowProc; // 简化的默认处理
    wc.hInstance = hInstance;
    wc.lpszClassName = "PygameCloneClass";
    RegisterClass(&wc);

    // 画出窗口
    hwnd = CreateWindowEx(0, "PygameCloneClass", "Non-Blocking Window",
                          WS_OVERLAPPEDWINDOW | WS_VISIBLE,
                          CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
                          NULL, NULL, hInstance, NULL);
    // 注意：这里没有 while 循环！函数到这里就结束了！
}

// 2. 后续提供给 pygame.event.get() 调用的函数：只看一眼消息队列
__declspec(dllexport) int __stdcall PollEvent() {
    MSG msg;
    // PeekMessage 是非阻塞的：如果有消息就处理并返回 1，没消息立刻返回 0
    if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
        return 1; 
    }
    return 0; // 没消息，立刻放行
}


```

**编译生成 `mylib.dll`**

打开 Windows 的 Developer Command Prompt（或配置了 GCC/MinGW 的终端），运行编译命令，把它变成二进制动态链接库：

```sh
gcc -shared -o mylib.dll mylib.c -luser32 -lgdi32

```

此时，你得到了 `mylib.dll`（相当于 Pygame 目录下的 `SDL2.dll`）。

##### 二.编写与编译 Python C 扩展 `base.pyd`

（模拟 Pygame 核心）

 **编写 C 语言扩展源码 `base.c`**

我们需要用到 Python 官方提供的 C-API（`Python.h`）。

```c
#include <Python.h>
#include <windows.h>

// 声明底层 dll 里的两个核心函数指针类型
typedef void (__stdcall *Create_Func)();
typedef int (__stdcall *Poll_Func)();

// 全局句柄，用来记录已经加载的 DLL
HMODULE hDll = NULL;
Poll_Func PollEvent = NULL;

// 1. 对应 my_game_engine.init()
static PyObject* py_init_and_show(PyObject* self, PyObject* args) {
    if (!hDll) {
        hDll = LoadLibrary("mylib.dll");
        if (!hDll) {
            PyErr_SetString(PyExc_FileNotFoundError, "Cannot find mylib.dll!");
            return NULL;
        }
    }
    
    Create_Func CreateWindowOnly = (Create_Func)GetProcAddress(hDll, "CreateWindowOnly");
    PollEvent = (Poll_Func)GetProcAddress(hDll, "PollEvent"); // 顺便把轮询函数的地址也存下来

    CreateWindowOnly(); // 此时调用的是非阻塞、画完就完事的函数

    return Py_BuildValue("(ii)", 1, 0); // 瞬间返回给 Python
}

// 2.  新增：对应 my_game_engine.poll_event() 的 C 胶水函数
static PyObject* py_poll_event(PyObject* self, PyObject* args) {
    if (!PollEvent) {
        // 如果还没调用 init，直接返回 False 
        Py_RETURN_FALSE; 
    }

    // 调用 mylib.dll 里的非阻塞看消息函数
    int has_msg = PollEvent(); 

    // 把 C 语言的 1 或 0，转换成 Python 的 True 或 False 返回
    if (has_msg) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

// 3. 核心：在方法映射表里，把这两个函数都登记上去！
static PyMethodDef MyMethods[] = {
    {"init_and_show", py_init_and_show, METH_VARARGS, "Init and show window without blocking."},
    {"poll_event", py_poll_event, METH_VARARGS, "Look at the OS message queue once."}, // 👈 挂载成功
    {NULL, NULL, 0, NULL} 
};

static struct PyModuleDef basemodule = {
    PyModuleDef_HEAD_INIT, "base", NULL, -1, MyMethods
};

PyMODINIT_FUNC PyInit_base(void) {
    return PyModuleCreate(&basemodule);
}

```

**编译生成 `base.pyd`**

利用 Python 的编译路径和库，将其编译为 Python 专属的二进制扩展（注意更换为你电脑上的 Python 路径）：

```sh
gcc -shared -o base.pyd base.c -I"C:\Python311\include" -L"C:\Python311\libs" -lpython311

```

##### 三.打包与发布

（组织 site-packages 目录结构）

我们在本地手动模拟 `pip install` 后的成果，在电脑的任意干净目录下，手动建立一个名为 **`my_game_engine`** 的文件夹，作为我们的包。

按照 Pygame 的规范组织目录：

```
my_game_engine/                  # 对应 site-packages 下的 pygame 目录
├── __init__.py                  # 包的 Python 门面入口
├── base.pyd                     # 刚刚编译的 Python-C 胶水层
└── mylib.dll                    # 刚刚编译的底层 Win32 驱动对接库

```

**编写 `__init__.py`：**

```py
# my_game_engine/__init__.py
from .base import init_and_show, poll_event

def init():
    return init_and_show()

# 把 C 层的非阻塞轮询函数，完美映射给最外层
def event_poll():
    return poll_event()


```

##### 四.Python 导入包并调用

现在，在 `my_game_engine` 文件夹的**同级目录**下，创建一个普通的 Python 脚本 `main.py`。

```py
import my_game_engine
import time

print("正在非阻塞拉起窗口...")
status = my_game_engine.init()
print(f"底层初始化结果: {status} (瞧！这一行秒印出来了！)")

running = True
frame_count = 0

# 真正的非阻塞游戏主循环
while running:
    # 对应 pygame.event.get() 的底层工作原理：
    # 只要系统队列里还有残余的鼠标、键盘消息，就用 while 循环一口气把它抽干、处理完
    while my_game_engine.poll_event():
        # 如果底层检测到用户点了关闭，或者别的事件（这里可以扩充逻辑）
        # 暂时这里只是为了维持窗口清醒（DefWindowProc 默认在后台处理）
        pass

    # 模拟游戏在疯狂干别的事（比如渲染、移动角色）
    frame_count += 1
    if frame_count % 100000 == 0:
        print(f"游戏正常运行中，当前主线程循环跑了 {frame_count} 次")
        
    # 稍微睡一下防止 CPU 飙到 100%
    time.sleep(0.01)


```

##### 五.运行 `python main.py`
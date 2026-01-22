objdump 是 Linux 下 GNU Binutils 套件中的一个非常强大的工具，主要用于显示和分析目标文件（object file）、可执行文件、静态/动态库的各种内部信息。

最常见的用途就是反汇编（disassemble）二进制文件。

```sh
# 语法
objdump [选项] 文件名

#示例:反汇编static文件的.text 部分(section),内容输出到
objdump -Dj .text static > static.xxx.xx.txt	static.xxx.xx.txt
```

#### 最常用的 10 个选项

| 选项         | 缩写/等价           | 主要作用                                 | 典型使用场景                           | 示例命令                    |
| ------------ | ------------------- | ---------------------------------------- | -------------------------------------- | --------------------------- |
| `-d`         | `--disassemble`     | 只反汇编**可执行的 section**（最常用）   | 查看函数/代码逻辑                      | `objdump -d a.out`          |
| `-D`         | `--disassemble-all` | 反汇编**所有 section**（包含数据段）     | 完整查看整个文件内容                   | `objdump -D a.out`          |
| `-S`         | `--source`          | 反汇编时**尽量显示源代码**（需 -g 编译） | 源码级调试/理解编译结果                | `objdump -S -C a.out`       |
| `-C`         | `--demangle`        | 解码 C++ 符号名（非常重要！）            | 看可读的函数名                         | `objdump -C -d libxxx.so`   |
| `-h`         | `--section-headers` | 显示所有 section 的头部信息              | 查看 .text/.data/.bss 大小、地址、权限 | `objdump -h a.out`          |
| `-f`         | `--file-headers`    | 显示文件整体头部（ELF header）           | 快速看架构、入口点、类型               | `objdump -f a.out`          |
| `-x`         | `--all-headers`     | 显示**所有头部信息**（超级全）           | 想一次性看完所有元信息                 | `objdump -x a.out`          |
| `-t`         | `--syms`            | 显示符号表（类似简化版 nm）              | 查看有哪些函数、全局变量               | `objdump -t a.out`          |
| `-T`         | `--dynamic-syms`    | 显示**动态符号表**（.dynsym）            | 检查动态库导出的符号                   | `objdump -T libxxx.so`      |
| `-j section` | `--section=section` | 只显示/反汇编某个特定 section            | 只看 .text 或 .plt                     | `objdump -d -j .text a.out` |

#### 实用的 8 个组合示例

```sh
# 1. 最常用：反汇编 + 美化 C++ 符号 + 带源代码（推荐！）
g++ -g -O0 main.cpp -o main
objdump -S -C -d main | less

# 2. 只看某个函数的反汇编（非常实用）
objdump -C -d main | grep -A 30 "<main>:"     # 从 main 开始看 30 行

# 3. 查看 ELF 文件基本信息（架构、入口点等）
objdump -f main

# 4. 查看所有段的虚拟地址、大小、权限（排查段地址问题很常用）
objdump -h main

# 5. 查看动态库导出的所有符号（比 nm -D 更详细）
objdump -T -C libmylib.so | grep "func"

# 6. 完整反汇编整个文件（包含数据段，适合逆向）
objdump -D -C -M intel main > main.intel.asm   # intel 语法更习惯

# 7. 只看 .plt（动态链接跳转表）
objdump -d -j .plt main

# 8. 同时看重定位信息（逆向/漏洞分析常用）
objdump -dr main   # -d + -r
```


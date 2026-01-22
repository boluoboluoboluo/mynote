**strings** 是 Linux 下 GNU Binutils 套件中最简单却非常实用的工具之一。

它的核心功能：**从二进制文件（可执行文件、库、固件、dump文件、图片、压缩包等）中提取可打印的字符串序列**。

默认规则：

- 至少连续 **4 个** 可打印字符（ASCII 32~126）
- 以不可打印字符（通常是 null 字节 \0 或换行）结束
- 只扫描 ELF 文件中已初始化且可加载的 section（.text/.rodata/.data 等）

```sh
# 语法
strings [选项] 文件名...

#示例:从二进制文件提取可打印的字符串
strings -a -t x filename > filename.txt		
```

#### 最常用的 10 个用法

| 选项 / 写法                       | 作用                                   | 典型场景                                 | 示例命令                      |
| --------------------------------- | -------------------------------------- | ---------------------------------------- | ----------------------------- |
| 无选项                            | 默认提取 ≥4 字符的字符串               | 快速看二进制里有什么人类可读文本         | `strings a.out`               |
| `-n 6` / `-6`                     | 最小字符串长度改为 6（过滤掉太多短串） | 减少噪音，看更长的有意义字符串           | `strings -n 8 /bin/ls`        |
| `-a` / `--all`                    | 扫描**整个文件**（不区分 section）     | 固件、dump、图片、压缩包、data 文件      | `strings -a firmware.bin`     |
| `-f` / `--print-file-name`        | 每行字符串前打印文件名                 | 处理多个文件时区分来源                   | `strings -f *.so`             |
| `-t x` / `-tx`                    | 显示**十六进制偏移**（最常用）         | 知道字符串在文件中的大概位置             | `strings -t x libcrypto.so`   |
| `-t d` / `-td`                    | 显示**十进制偏移**                     | 与 gdb / hex 编辑器对齐                  | `strings -t d program`        |
| `-t o` / `-to`                    | 显示**八进制偏移**                     | 某些老工具/脚本需要                      | `strings -to core.dump`       |
| `-e l` / `-el`                    | 提取 little-endian 16-bit 宽字符       | Windows Unicode 字符串、UTF-16LE         | `strings -el some_dll.dll`    |
| `-e b` / `-eb`                    | 提取 big-endian 16-bit 宽字符          | 某些嵌入式/网络协议字符串                | `strings -eb firmware_be.bin` |
| `-w` / `--include-all-whitespace` | 把空白也算可打印字符（空格、tab等）    | 提取包含很多空格的字符串（如格式化消息） | `strings -w config_blob.bin`  |

#### 实用的 10 个组合示例

```sh
# 1. 最常用：快速看可执行文件里有什么（函数名、错误消息、路径等）
strings /bin/ls | less

# 2. 带偏移 + 文件名 + 最小长度（逆向/取证/恶意软件分析标配）
strings -a -f -n 6 -t x suspicious.exe > strings.txt

# 3. 只看包含特定关键词的字符串（找 URL、密钥、命令行参数等）
strings -a program.bin | grep -i "http\|key\|pass\|token\|api"

# 4. 查看动态库里硬编码的域名/IP/密钥（安全审计常用）
strings -n 10 lib*.so | grep "\."

# 5. 提取固件/ROM 中的字符串（嵌入式/IoT 逆向）
strings -a -n 5 -t x router_firmware.bin | less

# 6. 从 core dump / 内存 dump 找泄露的敏感信息
strings -a -n 8 core.12345 | grep -i "password\|token\|cookie"

# 7. 看压缩包/图片里是否藏了字符串（隐写分析入门）
strings -a secret.jpg | grep flag

# 8. 结合 grep 找特定格式（如版本号）
strings a.out | grep -E "[0-9]+\.[0-9]+\.[0-9]+"

# 9. 提取 UTF-16LE 字符串（常见于 Windows PE/一些协议）
strings -el windows_program.exe | grep -i error

# 10. 多文件批量 + 排序去重（快速看一堆 so 里重复的字符串）
strings -f *.so | sort | uniq -c | sort -nr | head -30
```




**YARA** 是一个非常强大且广泛使用的**开源工具和规则语言**，主要用于**恶意软件研究、检测和分类**。

YARA 就是恶意软件分析师的“指纹识别系统”，你定义什么样的“指纹”（规则），它就能帮你在海量二进制/文件中快速找出匹配的东西。

官网：https://virustotal.github.io/yara/

它的全称常被戏称为 **"YARA: Another Recursive Acronym"** 或 **"Yet Another Ridiculous Acronym"**（有点自嘲的递归缩写梗）。

### 核心一句话定义

YARA 是一个**模式匹配瑞士军刀**，允许安全研究人员通过编写**规则**（rules）来描述恶意软件家族（或任何你想匹配的文件模式），基于**文本字符串、正则表达式、二进制字节序列**等特征进行精确匹配。

### 它最常被用来做什么？

- 识别和分类已知恶意软件家族（Ransomware、Trojan、Backdoor、Infostealer 等）
- 检测变种（即使恶意软件作者改了部分代码或字符串，只要核心特征还在就能命中）
- 威胁狩猎（Threat Hunting）：在海量文件中快速找 IOC（Indicators of Compromise）
- 检测打包器（packer）、webshell、Cobalt Strike beacon、特定工具（如 Mimikatz、PowerShell Empire 等）
- 文件类型/格式指纹识别（比如判断是否是伪装成正常文件的恶意文档）
- 内存 dump 扫描、进程内存扫描、固件分析等

### 为什么它这么受欢迎？

- 开源免费（GitHub: VirusTotal/yara）
- 规则语言**灵活强大**：支持通配符、正则、十六进制、跳转、文件大小、PE/ELF 结构解析、熵计算、数学运算等
- 速度快：编译后扫描非常高效
- 几乎所有主流安全厂商和平台都支持：VirusTotal、FireEye、Kaspersky、CrowdStrike、Elastic、Wazuh、Loki、YARA-python 等
- 社区规则丰富：[https://github.com/Yara-Rules/rules](https://github.com/Yara-Rules/rules?referrer=grok.com) 有几千条现成规则

### 一个最经典的简单规则示例

```yara
rule SilentBanker
{
    meta:
        description = "Detects the infamous Silent Banker trojan"
        author      = "Example"
        date        = "2025"

    strings:
        $s1 = "bankofamerica" nocase
        $s2 = "silent_banker.exe" ascii
        $code = { 68 ?? ?? ?? ?? FF 15 ?? ?? ?? ?? }  // call [some API]

    condition:
        uint16(0) == 0x5A4D and          // MZ header (PE file)
        filesize < 500KB and
        any of them
}
```

这条规则的意思是： 如果文件是 PE 可执行文件、大小小于 500KB，并且包含上面任意一个字符串或字节模式，就判定为 SilentBanker 家族。

### 常用命令行用法（快速上手）

```sh
#安装命令:(如系统没有)
sudo apt install yara

# 扫描单个文件
yara rule.yar suspicious.exe

# 扫描目录（递归）
yara -r rules/ malware_samples/

# 只显示命中规则名（不显示细节）
yara -s rule.yar file.exe

# 扫描进程内存（Linux 示例）
yara -p <pid> rule.yar
```


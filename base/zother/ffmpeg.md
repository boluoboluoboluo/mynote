#### 安装

> ffmpeg的官方网站是：[http://ffmpeg.org/](https://link.zhihu.com/?target=http%3A//ffmpeg.org/)
>
> 版本：ffmpeg-7.0.2-essentials_build.7z	（自行根据实际情况选择系统及版本，我这里是windows11）

1. 解压到安装目录
2. bin目录添加到环境变量



#### 合并视频

示例视频`1.mp4`,`2.mp4`,`3.mp4`

```sh
# 命令
# -f concat 表示使用合并视频的功能。
# -i input.txt 指定一个包含视频文件列表的文本文件（input.txt）。
# output.mp4 是合并后的输出文件。
ffmpeg -f concat -i input.txt -c copy output.mp4
```

input.txt内容：

```
file '1.mp4'
file '2.mp4'
file '3.mp4'
```



#### 合并音频和视频

示例音频`audio.m4s`，视频为`video.m4s`

```sh
#cmd到音视频目录，执行合并命令：
ffmpeg -i "audio.m4s" -i "video.m4s" -c copy "output.mp4"

```

#### 剪辑视频

```sh
#参数说明：
‌输入文件‌：使用-i参数指定输入文件。
‌起始时间‌：使用-ss参数指定起始时间，例如-ss 00:00:10表示从第10秒开始裁剪。
‌持续时间‌：使用-t参数指定裁剪持续时间，例如-t 10表示裁剪10秒。或者使用-to参数指定结束时间，例如-to 00:00:20表示截取到第20秒结束。
‌复制编码‌：使用-c copy参数表示直接复制流，不进行重新编码。
‌输出文件‌：指定输出文件的名称和路径。

#剪辑视频第10秒开始往后10秒
ffmpeg -i input.mp4 -ss 00:00:10 -t 10 -c copy output.mp4
#剪辑视频第10秒到第20秒
ffmpeg -i input.mp4 -ss 00:00:10 -to 00:00:20 -c copy output.mp4
#剪辑视频第10秒到视频末尾
ffmpeg -i input.mp4 -ss 00:00:10 -codec copy output.mp4
```

#### 视频压缩

比特率直接影响画质和文件大小。降低比特率可显著压缩体积，但需平衡画质。

- **推荐设置**：
  - **H.264编码**：尝试将比特率设置为2-5 Mbps（1080p）或1-2 Mbps（720p）。
  - **H.265（HEVC）编码**：相同画质下比特率可比H.264低30-50%。

```sh
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -c:a aac -b:a 128k output.mp4
```

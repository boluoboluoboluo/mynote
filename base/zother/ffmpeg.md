#### 安装

> ffmpeg的官方网站是：[http://ffmpeg.org/](https://link.zhihu.com/?target=http%3A//ffmpeg.org/)
>
> 版本：ffmpeg-7.0.2-essentials_build.7z	（自行根据实际情况选择系统及版本，我这里是windows11）

1. 解压到安装目录
2. bin目录添加到环境变量



#### 合并视频

```sh
# 合并多个视频（用 | 分隔）
ffmpeg -i "concat:video1.ts|video2.ts|video3.ts" -c copy output.mp4		#注意是ts后缀
```

**方式二:**

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



##### 合并视频出现时长卡帧的问题解决

```sh
#问题描述: ffmpeg截取的视频再拼接时,可能会出现,时长不对,卡顿的问题
#解决:
#先将视频转换成ts格式,再拼接,就不会出问题
ffmpeg -i 1.mp4 -c copy 1.ts
ffmpeg -i 2.mp4 -c copy 2.ts
#再拼接 1.ts 和 2.ts即可

============
#说明:
ffmpeg -i 1.mp4 -c:v copy 1.ts		#表示视频流复制,但音频会重新编码
ffmpeg -i 1.mp4 -c copy 1.ts		#表示都不重新编码
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

========
#剪辑的视频开头卡顿解决方案:
#原因：直接从非关键帧（I帧）截取会导致播放器需要等待下一个关键帧才能解码。
#解决方案：
将 -ss（定位开始时间）参数放在 输入文件之前，FFmpeg会定位到最近的关键帧开始截取：
ffmpeg -ss [开始时间] -i [输入文件] -t [持续时间] -c copy [输出文件]

========
```

##### 关键帧剪辑

```sh
#如果当前想要截取的位置不是关键帧,会导致多截或少截的问题
#此时应该插入关键帧,方法如下:
#假如想要在视频第5秒位置截取,但第5秒不是关键帧,先插入关键帧:
	#说明:截取前15秒的视频,重新编码,并在5秒的位置插入一个关键帧
	ffmpeg -ss 00:00:00 -i input.mp4  -t 15 -c:v libx264 -force_key_frames 5 -c:a copy part1.mp4
	#剩下部分视频直接截取:
	ffmpeg -ss 00:00:15 -i input.mp4  -c copy part2.mp4
	#然后将格式转为ts,方便合并:
	ffmpeg -i part1.mp4 -c copy part1.ts
	ffmpeg -i part2.mp4 -c copy part2.ts
	#合并视频:
	ffmpeg -i "concat:part1.ts|part2.ts" -c copy output.mp4
	#最后对有关键帧的视频进行截取
	ffmpeg -ss 00:00:05 -i output.mp4  -c copy output2.mp4		#现在可以在第5秒截取了
```





#### 视频压缩

比特率直接影响画质和文件大小。降低比特率可显著压缩体积，但需平衡画质。

- **推荐设置**：
  - **H.264编码**：尝试将比特率设置为2-5 Mbps（1080p）或1-2 Mbps（720p）。
  - **H.265（HEVC）编码**：相同画质下比特率可比H.264低30-50%。

```sh
-b:v: 设置目标视频比特率 (如 1M, 1500k)。
-b:a: 设置目标音频比特率 (如 128k, 192k, 256k)。

ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -c:a aac -b:a 128k output.mp4

ffmpeg -i input.mov -c:v libx264 -c:a aac -b:a 192k output.mp4		//通用

# gpu加速,NVIDIA NVENC (H.264)
ffmpeg -i input.mp4 -c:v h264_nvenc -c:a copy output.mp4

ffmpeg -i input.mkv -c:v libx265 -c:a aac -b:a 192k output.mp4		//高效,需设备播放

# gpu加速,NVIDIA NVENC (H.265)
ffmpeg -i input.mp4 -c:v hevc_nvenc -c:a copy output.mp4
```

#### 视频字幕合并

```
ffmpeg -i input.mp4 -vf "subtitles=input.srt" output.mp4
```

#### 视频旋转

```sh
#命令
ffmpeg -i in.mov -vf "transpose=1" out.mov

#transpose为不同值时所代表的不同意义:
	0: 逆时针和垂直翻转90度(默认)
	1: 顺时针旋转90度
	2: 逆时针方向90度
	3: 顺时针和垂直翻转90度
	
#旋转180°
ffmpeg -i input.mp4 -vf "transpose=2,transpose=2" out.mp4
```

#### 视频转码并保存字幕

```sh
ffmpeg -i input.mkv -c:v copy -c:a copy -c:s mov_text output.mp4	#携带的软字幕在某些播放器可能无法播放,如微信

#将字幕烧录
ffmpeg -i input.mkv -vf "subtitles=input.mkv:stream_index=0" -c:a copy output.mp4

#外部字幕烧录
ffmpeg -i input.mkv -vf "subtitles=subtitles.srt" -c:a copy output.mp4
```

#### 保留特定音轨

```sh
# 只保留第1条和第3条音轨
ffmpeg -i input.mp4 -map 0:v -map 0:a:0 -map 0:a:2 -c copy output.mp4
```


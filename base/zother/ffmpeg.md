#### 安装

> ffmpeg的官方网站是：[http://ffmpeg.org/](https://link.zhihu.com/?target=http%3A//ffmpeg.org/)
>
> 版本：ffmpeg-7.0.2-essentials_build.7z	（自行根据实际情况选择系统及版本，我这里是windows11）

1. 解压到安装目录
2. bin目录添加到环境变量



#### 查看视频信息

```sh
#查看
ffmpeg -i input.mp4

#-show_format：显示容器格式、时长、文件大小、比特率等。
#-show_streams：显示每个流（视频、音频、字幕）的详细信息（编码类型、分辨率、帧率、采样率等）。
ffprobe -v error -show_format -show_streams input.mp4
```

#### 格式转换

```sh
#示例
ffmpeg -i a.wmv out.mp4		#wmv格式转mp4
```

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

#### 视频编码和压缩

```sh
===========#相关编码参数
-b:v: 设置目标视频比特率 (如 1M, 1500k)。	#2-5 Mbps（1080p）或1-2 Mbps（720p）。
-b:a: 设置目标音频比特率 (如 128k, 192k, 256k)。

#分辨率 -vf "scale=1024:-2" => 宽度指定1024,高度自动调节,且保持为偶数

##CRF范围：0（无损）到51（最差质量），常用值18-28 参考:
crf 18：近乎无损，文件较大
crf 23-25：高质量，肉眼难辨
crf 26-28：良好质量，推荐值
crf 30-32：可接受质量，文件小
crf 35+：低质量，仅用于预览
#注意: -b:v 和 -crf 不能同时使用

#preset预设
ultrafast：最快，文件最大
medium：默认，平衡选择
slow/slower：更慢，更小文件
veryslow：最慢，最小文件

==========#h264编码
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -c:a aac -b:a 128k output.mp4	#视频和音频编码
# gpu加速,NVIDIA NVENC (H.264)
ffmpeg -i input.mp4 -c:v h264_nvenc -c:a copy output.mp4

==========#h265编码 相同画质下比特率可比H.264低30-50%。
ffmpeg -i input.mkv -c:v libx265 -c:a aac -b:a 192k output.mp4		
# gpu加速,NVIDIA NVENC (H.265)
ffmpeg -i input.mp4 -c:v hevc_nvenc -c:a copy output.mp4
#
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -c:a aac -b:a 128k out.mp4		#平衡质量和大小
#
#指定码率 -b:v 
ffmpeg -i input.mp4 -c:v libx265 -b:v 500k -c:a aac -b:a 64k out.mp4
# 更激进：目标码率300kbps
ffmpeg -i input.mp4 -c:v libx265 -b:v 300k -c:a aac -b:a 48k out.mp4

#本人常用:
ffmpeg -i a.mp4 -c:v libx265 -b:v 500k -vf "scale=1024:-2" -c:a aac -b:a 50k out.mp4

#保持画质常用:
ffmpeg -i a.mp4 -c:v libx264 -crf 18 -vf "scale=1280:-2" -c:a aac -b:a 64k out.mp4
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

# 保持原编码格式导出音轨
# -vn 不处理视频
# -acodec copy 使用原音频编码器,不重新编码
ffmpeg -i input.mp4 -vn -acodec copy output.m4a

# 只提取第一条音频流导出 保持原编码格式
ffmpeg -i input.mp4 -map 0:a:0 -acodec copy output.m4a

# 提取特定时间段的音频
ffmpeg -i input.mp4 -ss 00:01:30 -t 00:00:60 -vn -acodec copy output.m4a

# 导出视频只保留第1条和第3条音轨
ffmpeg -i input.mp4 -map 0:v -map 0:a:0 -map 0:a:2 -c copy output.mp4

#编码音轨再提取	(如果原视频不能直接提取的话)
ffmpeg -i input.mp4 -vn -acodec aac -b:a 128k output.m4a
```

#### 问题记录

##### 合并视频卡顿

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

##### 截取的位置出现偏差

```sh
#描述: 如果当前想要截取的位置不是关键帧,会导致多截或少截的问题
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
	ffmpeg -ss 00:00:05 -i output.mp4  -c:v copy -c:a copy output2.mp4		#现在可以在第5秒截取了
```

##### 部分截取到ts容器问题

```sh
#说明:
#MP4和TS容器格式的时间戳处理机制不同：
#MP4容器要求时间戳从0开始，会自动重置时间戳
#TS容器保留原始时间戳，导致被剪切的音频部分也被包含进去
ffmpeg ss 10 -i input.mp4 -c copy output.mp4	#推荐
ffmpeg ss 10 -i input.mp4 -c copy output.ts		#不推荐

#解决:
1.先剪辑成mp4
2.将mp4转换成ts
3.再将ts合并成新的mp4
	ffmpeg -i "concat:video1.ts|video2.ts|video3.ts" -c copy output.mp4		#注意是ts后缀

```

##### 截取视频尾部位置不准确问题

```sh
#问题描述: 使用 -to 参数指定结束位置可能出现并没有从endtime位置截取的情况
ffmpeg -ss starttime -i input.mp4 -to endtime -c copy output.mp4
#优先使用 -t 参数,指定截取时长
ffmpeg -ss starttime -i input.mp4 -t timestamp -c copy output.mp4
```

##### 音频声道问题报错

```sh
#问题描述:视频编码时报错 => Unsupported channel layout "6 channels"
#说明:输入的音频有6声道
#解决:推荐将音频转换为立体声音,使用 -ac 2 参数
ffmpeg -i a.mp4 -c:v libx265 -b:v 2M -vf "scale=1280:-2" -c:a aac -b:a 64k -ac 2 out.mp4	#示例
```


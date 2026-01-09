
import os
import subprocess

###
#将当前目录的mp4文件的音轨提取出来

def test():
	files = os.listdir()
	for f in files:
		if os.path.isfile(f):
			name,extension = os.path.splitext(f)
			if extension.lower() == ".mp4":
				#导出音轨 命令:ffmpeg -i input.mp4 -vn -acodec copy output.m4a
				command = f'ffmpeg -i "{f}" -vn -acodec copy "{name}.m4a"'
				subprocess.run(command)
try:
	test()
	print("operation done...")
except Exception as e:
	print(e)


# input("input andy char to exit...")
#### gif缩小

> 需先安装`pillow`

```sh
#安装pillow包
pip install pillow
```

代码如下：

```py
from PIL import ImageSequence
import imageio

#压缩
def resize_gif(input_file, output_file, size):
	with Image.open(input_file) as im:
		frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
 
	# 设置新尺寸
	new_size = size

	# 缩小GIF中的每一帧
	resized_frames = [frame.resize(new_size, Image.NEAREST) for frame in frames]
	
	# 创建新的GIF
	resized_frames[0].save(output_file, 'gif',save_all=True, loop=0,append_images=resized_frames[1:])
 
#调整尺寸，缩小的最小尺寸，end_size
def prepare(srcfile):
	simg = Image.open(srcfile)
	w,h = simg.size
	end_size = 50
	dst = {}
	if w <= end_size or h <=end_size:
		dst['w'] = w
		dst['h'] = h
		return dst
	if w >= h:
		dst['h'] = end_size
		ratio = round(h/end_size,2)
		dst['w'] = round(w/ratio)
		return dst
	else:
		dst['w'] = end_size
		ratio = round(w/end_size,2)
		dst['h'] = round(h/ratio)
		return dst


#input目录下有1.gif,2.gif  ... 10.gif
#有output目录用于生成压缩后的gif
for i in range(10):
	srcfile = "input/" + str(i+1) + ".gif"
	print(srcfile)
	dst = prepare(srcfile)
	outfile = "output/" + str(i+1) + ".gif"
	# 使用函数缩小GIF
	resize_gif(srcfile, outfile, (dst['w'], dst['h']))
```


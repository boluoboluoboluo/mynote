
import random
import string
from captcha.image import ImageCaptcha

##说明：需要安装captcha 
#pip install captcha

#生成验证码
def gen_captcha():

	strs = string.digits+string.ascii_letters
	randstr = random.sample(strs,4)	#随机字符，固定数量

	imagecode=''.join(randstr)		#拼接字符串

	#这是ImageCaptcha自带的初始化内容width=160, height=60, fonts=None, font_sizes=None，可以自己设置
	captcha = ImageCaptcha(width=350,height=100)
	image = captcha.generate(imagecode)

	captcha_data = {"image":image,"code":imagecode}

	return captcha_data

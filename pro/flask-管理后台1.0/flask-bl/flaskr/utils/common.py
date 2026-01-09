
import json
import random,string
import re
from captcha.image import ImageCaptcha
from flask import render_template


#需安装； pip install captcha
#生成验证码
def bl_gen_captcha():

	strs = string.digits+string.ascii_letters
	randstr = random.sample(strs,4)	#随机字符，固定数量

	imagecode=''.join(randstr)		#拼接字符串

	#这是ImageCaptcha自带的初始化内容width=160, height=60, fonts=None, font_sizes=None，可以自己设置
	captcha = ImageCaptcha(width=350,height=100)
	image = captcha.generate(imagecode)

	captcha_data = {"image":image,"code":imagecode}

	return captcha_data

#list返回，一般用于常见的ajax返回
#code：通常-1为异常，1为正常（其他可根据实际情况自己配置逻辑）
#data：需要传递或处理的数据
#msg：通知信息
def bl_msg(code,data,msg):
	re_data = {"code":code,"data":data,"msg":msg}
	return re_data

#邮箱格式检查
def bl_check_email(email):
	return re.match(r'([a-zA-Z0-9_.+-]+@[a-pr-zA-PRZ0-9-]+\.[a-zA-Z0-9-.]+)',email)

#错误页面
#err_msg:报错信息
#http_code:http状态码，默认400(客户端请求出错)
def bl_err_page(err_msg,http_code=400):
	return render_template('huicommon/error.html',err_msg=err_msg),http_code

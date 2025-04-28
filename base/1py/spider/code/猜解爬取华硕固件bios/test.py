import time
import requests

###
#用途，猜解下载链接
###

#华硕bios固件下载链接示例 model为型号
# https://dlsvr04.asus.com.cn/pub/ASUS/GamingNB/Image/BIOS/107356/FX507ZCAS315.zip?model=FX507ZC
# https://dlsvr04.asus.com.cn/pub/ASUS/GamingNB/Image/BIOS/113143/FX507ZCAS316.zip?model=FX507ZC
# https://dlsvr04.asus.com.cn/pub/ASUS/GamingNB/Image/BIOS/107356/ASUS_FX507ZC_315_BIOS_Update.exe?model=FX507ZC


# 华硕biso固件下载链接，中间的106853是个错误数据，这个数据未知
# url = "https://dlsvr04.asus.com.cn/pub/ASUS/GamingNB/Image/BIOS/106853/FX507ZCAS314.zip?model=FX507ZC"

url_pre = "https://dlsvr04.asus.com.cn/pub/ASUS/GamingNB/Image/BIOS/"
url_mid = ""
url_sfx = "/FX507ZCAS314.zip?model=FX507ZC"


class D:
	param = [1,0,0,0,0,0]

	@staticmethod
	def sparam():		#生成字符串
		return ''.join(map(str,D.param))
		# return str(param)

	@staticmethod
	def clear_next_all(i):		#param数组i的值若改变，则数组下标i后面的内容重置
		if i+1 > len(D.param):
			return
		for x in range(i,len(D.param)):
			D.param[x] = 0

	@staticmethod
	def check(i):		#边界检查
		if i+1 > len(D.param):
			return 0
		if D.param[i] == 9:
			return 0
		return 1

	@staticmethod
	def create_str(i,j):	#递归生成数据
		if j:
			D.do_action()		#对生成的数据执行动作

		if D.check(i+1):
			D.create_str(i+1,0)

		D.param[i] += 1
		D.clear_next_all(i+1)

		if D.param[i] <= 9:
			D.create_str(i,1)

	@staticmethod
	def do_action():		#执行动作，这里生成链接，发送请求
		url_mid = D.sparam()
		url = url_pre + url_mid + url_sfx
		
		r = requests.get(url)
		print(url_mid + ":" + str(r.status_code))
		if str(r.status_code) == "200":
			
			print(url)
			exit(0)

		time.sleep(0.03)	#每3毫秒执行一次


#执行方法
# D.create_str(0,1)



	
	



# r = requests.get(url)

# print(r.status_code)

# f = open("x.zip","wb")
# f.write(r.content)


# f.close()
# print("done...")


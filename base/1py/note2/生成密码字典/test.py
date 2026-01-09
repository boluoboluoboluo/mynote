
#生成100~999的所有数字，可增加位数
#可拓展，例如生成a000000~z999999,等，需调整代码
class D:
	param = [1,0,0]		#初始数据

	#转字符串
	@staticmethod
	def sparam():
		return ''.join(map(str,D.param))
		# return str(param)

	#用于重置数组下标i后面的的数据
	@staticmethod
	def clear_next_all(i):
		if i+1 > len(D.param):
			return
		for x in range(i,len(D.param)):
			D.param[x] = 0

	#判断边界
	@staticmethod
	def check(i):
		if i+1 > len(D.param):
			return 0
		if D.param[i] == 9:
			return 0
		return 1



	# i：当前数组下标
	# j：标识，用于递归i+1数组下标出现重复生成的问题，初始值固定传1就行
	@staticmethod	#递归生成数字
	def create_str(i,j):
		if j:
			print(D.sparam())

		if D.check(i+1):
			D.create_str(i+1,0)

		D.param[i] += 1
		D.clear_next_all(i+1)

		if D.param[i] <= 9:
			D.create_str(i,1)


D.create_str(0,1)	#


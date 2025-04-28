### 查看内存

* 使用跨平台模块`psutil`查看内存资源，需先安装模块：

```sh
pip install psutil	#如报错，请先使用管理员模式升级pip
```

* 代码

```py
import os
import psutil
import gc

#查看内存
def see_memory():
	mem = psutil.virtual_memory()
	print(u'总内存：%.2f G' % (mem.total/1024/1024/1024))
	print(u'可用内存：%.2f G' % (mem.available/1024/1024/1024))
	print(u'未使用的内存：%.2f G' % (mem.free/1024/1024/1024))

	#下面为linux参数
	# print(u'正在使用的内存：',mem.active)
	# print(u'标记为未使用的内存：',mem.inactive)
	# print(u'缓存文件系统元数据使用的内存：',mem.buffers)
	# print(u'缓存各种文件的内存：',mem.cached)
	# print(u'被多个进程同时访问的内存：',mem.shared)
	# print(u'内核数据结构缓存的内存：',mem.slab)

#查看虚拟内存
def swap_memory():
	mem = psutil.swap_memory()
	print(u'总交换内存 ：%.2f M' % (mem.total/1024/1024))
	print(u'使用交换内存 ：%.2f M' % (mem.used/1024/1024))
	print(u'可用交换内存 ：%.2f M' % (mem.free/1024/1024))
	print(u'百分比 ：',mem.percent)
	print(u'系统从磁盘交换的内存 ：%.2f M' % (mem.sin/1024/1024))
	print(u'系统从磁盘换出的内存 :%.2f M' % (mem.sout/1024/1024))

#查看进程信息
def see_process():
	p = psutil.Process(os.getpid())
	print("进程名 ：",p.name())
	print("进程开启的线程数 ：",p.num_threads())
	print("进程内存利用率 ：%.2f" % p.memory_percent())

	# print("进程内存rss、vms信息 ：",p.memory_info())
	# print("进程IO信息包括读写IO数及字节数 ：",p.io_counters())

	#下面为linux参数
	# print("进程UID信息 ：",p.uids())
	# print("进程GID信息 ：",p.gids())	

if __name__ == '__main__':
	see_memory()
	print("")
	swap_memory()
	print("")
	see_process()
	
	# 查看当前进程内存消耗
	print('当前进程内存消耗：%.2f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
```


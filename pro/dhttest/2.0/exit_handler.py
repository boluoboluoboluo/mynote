import atexit
import signal
from types import FrameType
import sys

_callback = None	#程序退出时调用的回调函数
_flag = False	#标志，避免重复调用

#程序正常退出
def normal_exit():
	global _callback
	global _flag
	if not _flag:
		atexit.register(_callback)	#程序正常退出
		_flag = True
#信号处理
def signal_handler(signum:int,frame:FrameType):
	global _callback
	global _flag
	print(f'接收到终止信号{signal.Signals(signum).name}')
	if not _flag:
		_callback()
		_flag = True
	sys.exit(signum + 128)
#异常处理
def exception_handler(exc_type,exc_value,traceback):
	global _callback
	global _flag
	print(f'未处理异常{exc_type.__name__}:{exc_value}')
	if not _flag:
		_callback()
		_flag = True
	sys.__excepthook__(exc_type,exc_value,traceback)
	sys.exit(1)

# 程序正常，异常，中断时的处理
def handler(callback):
	global _callback 
	_callback = callback
	#程序正常退出
	normal_exit()
	#中断信号，ctrl+c 或 kill
	for sig in [signal.SIGINT,signal.SIGTERM]:
		signal.signal(sig,signal_handler)
	#异常全局捕获(不包括子进程)
	sys.excepthook = exception_handler
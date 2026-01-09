import logging
from flask.logging import default_handler

# from logging.handlers import TimedRotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler

#日志初始化设置
#说明：（下面应该是框架默认规则）
# 1、生产模式下，系统报错日志会打印在log文件，浏览器显示500页面(未定义则提示server eroor之类)
# 2、debug模式下，系统报错日志不会打印到log文件，浏览器会显示报错信息
#	 --注意：2中的debug是项目以debug模式启动，不是日志handler里的参数debug=True
#	 --注意2：用户自己编写的error级别日志，都会打印到log文件
def init(app):
	logpath = "logs/flaskr.log"
	formatter = logging.Formatter("[%(asctime)s][%(thread)d][%(filename)s:%(lineno)d][%(levelname)s]: %(message)s")

	########################
	#此代码会日志分割时会出现多进程报错问题，故不采用
	# handler = TimedRotatingFileHandler(logpath,when="D",interval=1,backupCount=15,encoding="UTF-8",delay=False,utc=True)
	########################

	#解决日志分割多进程报错
	#日志超过5M分割，保留30份日志
	handler = ConcurrentRotatingFileHandler(logpath,"a",5*1024*1024,30,encoding="UTF-8",delay=False)

	handler.setFormatter(formatter)


	#设置默认日志级别为INFO （注意，不添加此句，生产模式不会打印INFO级别日志，仅debug模式会打印）
	app.logger.setLevel(logging.INFO)	

	default_handler.setLevel(logging.WARNING)	#设置控制台只记录WARNING级别以上的日志

	# 移除默认handler后，生产模式下，控制台不打印日志
	# 但是调试模式(项目以debug模式启动)控制台还是会打印系统报错日志（不过不会打印代码里手动编写的warning，error等日志）
	app.logger.removeHandler(default_handler)	

	app.logger.addHandler(handler)
from loguru import logger #type:ignore
import os
# import sys

# 高效异步日志库,需安装: pip install loguru

# 使用该模块打日志,引入下面语句即可:
# from log import logger

# 基础打印（5 个常用级别）
# logger.debug("低级别的调试信息")
# logger.info("普通的日常流水日志")
# logger.warning("警告信息")
# logger.error("程序遇到了错误")



# 导出
logger = logger

# 设置 logger 配置
def setup_global_logger(is_debug):
	if is_debug:	#如果是debug模式,使用默认的logger,即输出到控制台
		return

	"""
	初始化全局日志配置
	只要在项目启动入口执行一次即可，所有其他文件直接使用 logger 就会自动遵循这套规则
	"""
	# 1. 彻底清除 Loguru 默认的控制台输出，防止多处打印导致杂乱
	logger.remove()

	# 2. 日志路径 (需先创建日志目录/var/log/blobvideo)
	log_path = "/var/log/blobvideo/app.log"

	# 3. 核心配置：添加通用的文件输出 Handler
	logger.add(
		log_path,
		# 定义通用的、美观的日志格式（支持跨线程/跨文件的行号追踪）
		format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}] [PID:{process}] [{file}:{line}] {message}",
		level="INFO",			# 记录 INFO 及以上级别
		rotation="20 MB",		# 满 20MB 自动在后台切割
		retention="10 days",	# 只保留最近 10 天的历史文件
		enqueue=True			# 核心：开启异步无锁内存队列！所有场景通用，绝不卡主线程
	)

	# 4. 顺便加上控制台输出（带 enqueue 异步，生产环境若追求极致性能可注释掉这一行）
	# logger.add(sys.stdout, level="INFO", enqueue=True)





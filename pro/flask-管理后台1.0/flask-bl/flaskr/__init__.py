
from flask import Flask, render_template

#应用工厂
def create_app(test_config=None):

	app = Flask(__name__,instance_relative_config=True)	#instance_relative_config ：告诉应用配置文件相对位置

	secretkey = "dfwefsdfo978987"

	# app.config["xxx"] = "xxx"	#注册全局配置，在html模板里，可通过{{ config["xxx"] }}访问

	#缺省配置
	app.config.from_mapping(	
		SECRET_KEY=secretkey,
	)

	if test_config is None:
		app.config.from_pyfile('config.py',silent=True)		#silent=True ：表示即使报错，也静默 
	else:
		app.config.from_mapping(test_config)

	#数据库
	from . import db
	db.init_app(app)	#应用初始化数据库一些操作

	#日志
	from . import log
	log.init(app)

	@app.errorhandler(404)
	def page_not_found(e):
		# note that we set the 404 status explicitly
		return render_template('huicommon/404.html'), 404

	@app.errorhandler(500)
	def internal_server_error(e):
		# note that we set the 500 status explicitly
		return render_template('huicommon/500.html'), 500

	from .admin import base
	app.register_blueprint(base.bp)		#管理后台基础蓝图

	from .admin import sys
	app.register_blueprint(sys.bp)		#管理后台 系统管理蓝图

	
	#hello world
	@app.route('/hello')
	@app.route('/')
	def hello():

		app.logger.debug("debug log")
		app.logger.info("info 日志")
		app.logger.warning("警告 日志")
		app.logger.error("错误 日志")

		# error = None
		# 消息闪现一次，前端用下面语句获取：
		# {% for message in get_flashed_messages() %}
		#	{{ message }}
		# {% endfor %}
		# flash(error)
		return render_template('test/hello.html')
	return app
import psycopg2
from flask import abort, current_app,g


def init_app(app):
	app.teardown_appcontext(close_db)	#告诉 Flask 在返回响应后进行清理的时候调用此函数。

def connect():
	conn = psycopg2.connect(database="tianxuan",user="postgres",password="root",host="127.0.0.1",port="5432")
	return conn

def get_db():
	if 'db' not in g:
		g.db = connect()
	return g.db

def close_db(e=None):
	db = g.pop('db',None)
	if db is not None:
		db.close()

#获取数据，返回dict数组
def get_data(sql,params):
	try:
		cursor = get_db().cursor()
		cursor.execute(sql,params)
		coloumns = [row[0] for row in cursor.description]
		result = [[str(item) for item in row] for row in cursor.fetchall()]
		return [dict(zip(coloumns, row)) for row in result]
	except Exception as e:
		print(e)
		current_app.logger.error(e)		#打印错误日志
		abort(500)
	finally:
		close_db()

# 操作数据，支持增删改
# sql结尾需要RETURNING id,否则返回None
# params:参数(元组)
# mode:默认为add，"add"=>新增，"update"=>修改，"del"=>删除
def operate_data(sql,params,mode="add"):
	try:
		cursor = get_db().cursor()
		cursor.execute(sql,params)

		re_id = None
		if mode == "add":
			g.db.commit()
			re_id = cursor.fetchone()[0]		#获取数据的id（add时，需要先提交才能获取到id）
		else:
			re_id = cursor.fetchone()[0]		#获取数据的id （先获取id，再提交。否则如果是del操作，先提交将无法获取id
			g.db.commit()
		
		
		return re_id
	except Exception as e:
		print(e)
		current_app.logger.error(e)		#打印错误日志
		abort(500)
	finally:
		close_db()
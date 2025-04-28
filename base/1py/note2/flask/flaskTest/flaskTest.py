from flask import Flask,redirect,url_for,render_template,request
app = Flask(__name__)

@app.route("/")
def hello():
	return "hello world4"

#参数，通过name接受参数，访问localhost:5000/v/flask  -> 输出：hello flask
@app.route("/v/<name>")		
def test(name):
	return "hello %s" % name

#动态构建
@app.route("/v2/<name2>")	
def test2(name2):
	# return "v2:hello,%s" % name2
	return redirect(url_for("test",name=name2))	#test为函数名称,name为参数

#模板渲染
@app.route('/v3')
def test3():
	return render_template("login.html")

#post方法（默认get）
@app.route('/v4',methods = ['POST', 'GET'])
def test4():
	if request.method == 'POST':
		print(1)
		# user = request.form['nm']
	else:
		print(2)
		# user = request.args.get('nm')
	return "test4"






#app.add_url_rule("/","hello",hello)		#也可以通过这种方式添加路由
if __name__ == "__main__":
	app.debug = True	#调试支持，代码更改将自动重启
	# app.run()
	app.run(debug=True) #debug模式
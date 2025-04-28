from flask import Flask, make_response, request # 注意需导入 make_response

app = Flask(__name__)

@app.route("/set_cookies")
def set_cookie():
    resp = make_response("success")
    resp.set_cookie("w3cshool", "w3cshool",max_age=3600)		#max_age:秒
    return resp

@app.route("/get_cookies")
def get_cookie():
    cookie_1 = request.cookies.get("w3cshool")  # 获取名字为Itcast_1对应cookie的值
    return cookie_1

@app.route("/delete_cookies")
def delete_cookie():
    resp = make_response("del success")
    resp.delete_cookie("w3cshool")

    return resp

if __name__ == '__main__':
    app.run(debug=True)
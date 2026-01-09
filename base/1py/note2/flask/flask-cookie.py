
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)


#蓝图
bp = Blueprint('base',__name__,url_prefix='')	#url_prefix 会添加到所有与该蓝图关联的 URL 前面。


#说明：
#使用jwt方式验证（需安装: pip install flask-jwt-extended）
#默认headers，支持4种方式：["headers", "cookies", "json", "query_string"]
#如使用cookies的方式，（即jwt生成的token保存在cookie，用户访问时，jwt解密token，取得用户标识信息，实现登录
#如用户端采用vue3前后端分离，jwt使用默认headers，token放在localstorage，用户访问时通过请求headers里传递到后端
# app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]		#配置token存放读取模式
# app.config["JWT_SECRET_KEY"] = secretkey		#建议单独配置
# jwt = JWTManager(app)
# jwt.init_app(app)


#设置cookie
@bp.route('/cookietest',methods=('GET',))
def cookietest():

	# html = render_template('hello.html')
	# response = Response(html) 
	# response.set_cookie('mooc', 'www.imooc.com')
	# return response

	response = jsonify({'name':"xxx"})
	response.set_cookie('name', 'www.imooc.com')
	return response


#登录，jwt设置cookie
@bp.route('/token/auth', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({'login': False}), 401

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    # Set the JWT cookies in the response
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

@bp.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the JWT access cookie in the response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200

@bp.route('/api/example', methods=['GET'])
@jwt_required
@bp.route('/token/remove', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

def protected():
    username = get_jwt_identity()
    return jsonify({'hello': 'from {}'.format(username)}), 200
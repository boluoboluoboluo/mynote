import functools
import re
from flask import (
	Blueprint, Response,flash,g,jsonify, make_response,redirect,render_template,request,session,url_for,current_app
)
from werkzeug.security import check_password_hash,generate_password_hash
from flaskr import db
from flaskr.utils import common
from . import sys_model

#用于基础功能的蓝图，包括登录，验证码，跳转首页
bp = Blueprint('base',__name__,url_prefix='')	#url_prefix 会添加到所有与该蓝图关联的 URL 前面。

#装饰器，登录检查
def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if session.get("admin_id") is None:
			return redirect(url_for('base.login'))
		return view(**kwargs)
	return wrapped_view

#装饰器，权限检查
# mode_code : 权限标识
# type：1网页，2接口
def auth_check(mode_code,type=1):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			admin_id = session.get("admin_id")
			role_sql = "select r.role_action from bl_sys_admin a left join bl_sys_role r on a.role_id=r.id "\
				" where a.id=%s"
			role_action = db.get_data(role_sql,(admin_id,))[0]["role_action"]		#获取当前登录管理员拥有的权限节点
			role_action_data = role_action.split(",")	#分割列表

			auth_sql = "select id from bl_sys_tab where mode_code=%s"
			node_id = db.get_data(auth_sql,(mode_code,))[0]["id"]

			if node_id not in role_action_data:		#无权限
				if type == 1:
					return common.bl_err_page("您没有权限")
				else:
					return common.bl_msg(-1,"","您没有权限")
			return func(*args, **kwargs)
		return wrapper
	return decorator

#获取验证码
@bp.route('/admin/captcha',methods=('GET',))
def get_captcha():
	captcha_data = common.bl_gen_captcha()
	response = Response(captcha_data["image"], mimetype='image/png')
	response.headers['Content-Type'] = 'image/png'
	session['captcha'] = captcha_data["code"] # 将验证码字符存入 session 中
	
	return response

#管理后台登录页
@bp.route('/admin/login',methods=('GET','POST'))
def login():
	if request.method == "GET":
		# if "paramsname" in request.args:		#判断get参数是否存在
		return render_template('admin/base/login.html',params=None)
	if request.method == 'POST':
		params = {}
		# if "username" in request.form:		#判断form表单参数是否存在
		params['username'] = request.form['username'].strip()
		params['password'] = request.form['password'].strip()
		params['captcha'] = request.form['captcha'].strip()		#验证码

		if params['username'] == '':
			flash("用户名不能为空")
			return render_template('admin/base/login.html',params=params)

		if "captcha" not in session:
			# abort(500)
			return render_template('admin/base/login.html',params=params)

		if params['captcha'].lower() != session.get("captcha").lower() :
			flash("验证码输入错误")
			return render_template('admin/base/login.html',params=params)
		
		sql = "select * from bl_sys_admin where admin_name = %s and is_del=0" 
		userdata = db.get_data(sql,(params['username'],))
		if len(userdata) == 0 :
			flash('用户名不存在')
			return render_template('admin/base/login.html',params=params)
		
		if not check_password_hash(userdata[0]['password'],params["password"]):
			flash('密码输入错误')
			return render_template('admin/base/login.html',params=params)
		
		session.clear()
		session['admin_id'] = userdata[0]['id']
		current_app.logger.info("管理员(" + params['username'] + ")登录了...")
		return redirect(url_for('base.index'))

#管理后台首页
@bp.route('/admin/index')
@login_required
def index():

	admin_info_sql = "select id,admin_name,nick_name from bl_sys_admin where id=%s"
	admin_info = db.get_data(admin_info_sql,(session.get("admin_id"),))[0]

	menu_data = session.get("menu_data")
	if menu_data is None:
		menu_data = sys_model.get_authmenu(session.get("admin_id"))		#获取权限菜单
		session["menu_data"] = menu_data

	return render_template('admin/base/index.html',admin_info=admin_info,menu_data=menu_data)

#退出登录
@bp.route('/admin/logout')
@login_required
def logout():
	session.clear()
	return redirect(url_for('base.login'))

#修改密码页
@bp.route('/admin/change_pass',methods=('GET','POST'))
@login_required
def change_pass():
	return render_template('admin/base/change_pass.html')

#修改密码提交
@bp.route('/admin/change_pass_sub',methods=('GET','POST'))
@login_required
def change_pass_sub():
		
		old_password = request.form.get("old_password","")
		new_password = request.form.get("new_password","")
		new_password2 = request.form.get("new_password2","")

		pt = re.compile(r"^[a-zA-Z0-9]{6,16}$")
		if not re.match(pt,new_password):

			return common.bl_msg(-1,"","新密码需要6-16位字母数字")
		if not re.match(pt,new_password2):
			return common.bl_msg(-1,"","确认密码需要6-16位字母数字")
		if new_password != new_password2:
			return common.bl_msg(-1,"","两次输入密码不一致")
		
		sql = "select password from bl_sys_admin where id = %s" 
		password = db.get_data(sql,(session.get("admin_id"),))[0]['password']
		if not check_password_hash(password,old_password):
			return common.bl_msg(-1,"","旧密码输入有误")

		#执行修改密码操作
		change_pass_sql = "update bl_sys_admin set password=%s where id=%s RETURNING id"
		operate_params = (generate_password_hash(new_password),session.get("admin_id"))
		re_id = db.operate_data(change_pass_sql,operate_params)
		if re_id:
			return common.bl_msg(1,"","操作成功")
		else:
			return common.bl_msg(-1,"","操作失败")





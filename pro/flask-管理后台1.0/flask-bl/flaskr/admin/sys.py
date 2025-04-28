from datetime import datetime
import re
from flask import Blueprint, abort, current_app, jsonify, render_template, request
from werkzeug.security import check_password_hash,generate_password_hash

from flaskr import db
from flaskr.admin.base import login_required,auth_check
from flaskr.utils import common
from . import sys_model

#用于系统管理的蓝图
bp = Blueprint('sys',__name__,url_prefix='')	#url_prefix 会添加到所有与该蓝图关联的 URL 前面。

#============================================管理员模块 start================================================
#管理列表
@bp.route('/admin/sys/admin_list')
@login_required
def admin_list():
	return render_template('admin/sys/admin_list.html')

#管理列表data
@bp.route('/admin/sys/admin_list_data',methods=('GET','POST'))
@login_required
def admin_list_data():
	
	#分页参数（暂时不用）
	# page = request.args.get("page",1)			#第几页，默认1
	# page_size = 10							#每页显示条数
	# offset = (int(page)-1) * page_size		#索引

	#前端h-ui框架datatable固定格式的参数
	draw = request.form.get("draw",1)			#h-ui参数，请求次数
	offset = request.form.get("start",0)		#索引
	limit = request.form.get("length",10)		#查询数量，相当于每页显示数量

	#查询参数
	start_date = request.form.get("start_date")
	end_date = request.form.get("end_date")
	admin_name = request.form.get("admin_name").strip()

	query_params = []	#查询参数
	param_sql = " where 1=1 "		#需要拼接的参数sql

	#参数相关逻辑
	if admin_name:
		param_sql += " and ba.admin_name like %s "		#模糊查询
		query_params.append("%" + admin_name + "%")		#模糊查询写法
	if start_date:
		start_stamp = int(datetime.strptime(start_date,"%Y-%m-%d").timestamp())	#字符串转秒时间戳
		param_sql += " and ba.createtime >= %s "
		query_params.append(start_stamp)
	if end_date:
		end_stamp = int(datetime.strptime(end_date,"%Y-%m-%d").timestamp())		#字符串转秒时间戳
		param_sql += " and ba.createtime <= %s "
		query_params.append(end_stamp)

	#查询总数据条数
	count_sql = "select count(*) from bl_sys_admin ba " + param_sql
	count = db.get_data(count_sql,tuple(query_params))[0]['count']

	#查询字段的sql（使用预编译语句，防止sql注入）
	#to_char(to_timestamp(ba.createtime),'yyyy-mm-dd hh24:mi:ss')  => 秒时间戳转换成字符串
	#coalesce(bar.role_name,'')  => 如果字段为空，则替换为空字符
	#注意：pgsql默认使用asc排序，所以分页查找时结果会和预期不一致，所以建议查询时使用自定义排序
	select_sql = "select ba.id,ba.admin_name,ba.nick_name,ba.email,ba.role_id,to_char(to_timestamp(ba.createtime),'yyyy-mm-dd hh24:mi:ss') as createtime,"\
			"to_char(to_timestamp(ba.updatetime),'yyyy-mm-dd hh24:mi:ss') as updatetime,ba.is_del, "\
			"coalesce(bar.role_name,'') role_name from bl_sys_admin ba "\
			"left join bl_sys_role bar on bar.id=ba.role_id "
	
	orderby_sql = " order by ba.id desc "
	limit_sql = " limit %s offset %s"
	query_params.append(limit)
	query_params.append(offset)

	query_sql = select_sql + param_sql + orderby_sql + limit_sql		#最终查询sql
	admin_list = db.get_data(query_sql,tuple(query_params))	#查询数据

	#前端h-ui框架datatable固定格式的返回
	info = {
			'draw':int(draw),			# ajax请求次数，作为标识符
			'recordsTotal':len(admin_list),	# 获取到的结果数(每页显示数量)
			'recordsFiltered':count,		# 符合条件的总数据量
			'data':admin_list					#获取到的数据结果
	}

	return info

#管理员新增或修改页
@bp.route('/admin/sys/admin_addupdate')
@login_required
def admin_addupdate():

	#角色数据
	role_sql = "select id,role_name from bl_sys_role"
	role_data = db.get_data(role_sql,None)

	if "id" in request.args:		#如果有id参数，则为修改
		id = request.args.get("id")		#id
		admin_sql = "select id,admin_name,nick_name,role_id,email from bl_sys_admin where id=%s"
		admin_data = db.get_data(admin_sql,(id,))
		if len(admin_data) == 0:		#id查到数据，返回一个错误页面，400为http状态码
			return common.bl_err_page("参数错误",400)
		else:
			return render_template('admin/sys/admin_addupdate.html',admin_data=admin_data[0],role_data=role_data)
	else:
		return render_template('admin/sys/admin_addupdate.html',admin_data={},role_data=role_data)

#管理员新增或修改
@bp.route('/admin/sys/admin_doaddupdate',methods=('GET','POST'))
@login_required
def admin_doaddupdate():

	if request.method == "POST":

		id = request.form.get("id",None)		#根据id参数判断新增还是修改

		admin_name = request.form.get("admin_name").strip()
		nick_name = request.form.get("nick_name").strip()
		password = request.form.get("password").strip()
		password2 = request.form.get("password2").strip()
		admin_role = request.form.get("admin_role")
		email = request.form.get("email").strip()
		createtime = int(datetime.now().timestamp())	#时间戳，秒
		updatetime = createtime

		if not re.match(r"^[a-zA-Z0-9]{1,20}$",admin_name):
			return common.bl_msg(-1,"","管理员名称由字母数字组成，小于20位")
		
		# 2个密码框满足有一个有值 或者 id为空(即新增),此时需要校验密码
		# 换句话说，就是如果是修改，密码框不输入，就不校验，旧密码不修改
		if (password or password2) or (not id):
			pt = re.compile(r"^[a-zA-Z0-9]{6,16}$")
			if not re.match(pt,password):
				return common.bl_msg(-1,"","密码需要6-16位字母数字")
			if not re.match(pt,password2):
				return common.bl_msg(-1,"","确认密码需要6-16位字母数字")
			if password != password2:
				return common.bl_msg(-1,"","两次输入密码不一致")
		
		if not admin_role:
			return common.bl_msg(-1,"","请选择角色")
		
		if email  and not common.bl_check_email(email) :
			return common.bl_msg(-1,"","邮箱格式不正确")
		
		#如果是新增
		if not id:
			#检查是否管理员名称是否已经存在
			rpt_ck_sql = "select count(*) from bl_sys_admin where admin_name=%s"
			count = db.get_data(rpt_ck_sql,(admin_name,))[0]["count"]
			if int(count)  > 0:
				return common.bl_msg(-1,"","该管理员名称已经存在！")

			# RETURNING id => 获取插入数据的id
			add_sql = "insert into bl_sys_admin (admin_name,nick_name,password,role_id,email,createtime,updatetime) "\
						"values(%s,%s,%s,%s,%s,%s,%s) RETURNING id"
			query_params = (admin_name,nick_name,generate_password_hash(password),admin_role,email,createtime,updatetime)
			re_id = db.operate_data(add_sql,query_params)

			if re_id:
				return common.bl_msg(1,"","添加成功")
			else:
				return common.bl_msg(-1,"","添加失败")
			
		#修改 (说明：修改时不允许修改管理员名称)
		else:
			update_sql = None
			query_params = None
			#如果有输入密码
			if password:
				update_sql = "update bl_sys_admin set password=%s,nick_name=%s,role_id=%s,email=%s,updatetime=%s where id=%s RETURNING id"
				query_params = (generate_password_hash(password),nick_name,admin_role,email,updatetime,id)
			else:
				update_sql = "update bl_sys_admin set nick_name=%s,role_id=%s,email=%s,updatetime=%s where id=%s RETURNING id"
				query_params = (nick_name,admin_role,email,updatetime,id)

			re_id = db.operate_data(update_sql,query_params,mode="update")
			if re_id:
				return common.bl_msg(1,"","修改成功")
			else:
				return common.bl_msg(-1,"","修改失败")
		
#管理员删除
@bp.route('/admin/sys/admin_del',methods=("POST",))
@login_required
def admin_del():
	id = request.values.get("id",None)
	if id:
		del_sql = "delete from bl_sys_admin where id=%s RETURNING id"
		db.operate_data(del_sql,(id,),mode="del")
		return common.bl_msg(1,"","删除成功")
	else:
		return common.bl_msg(-1,"","参数错误")
	
#管理员停用
@bp.route('/admin/sys/admin_stop',methods=("POST",))
@login_required
def admin_stop():
	id = request.values.get("id",None)
	if id:
		stop_sql = "update bl_sys_admin set is_del=1 where id=%s RETURNING id"
		db.operate_data(stop_sql,(id,),mode="update")
		return common.bl_msg(1,"","操作成功")
	else:
		return common.bl_msg(-1,"","参数错误")

#管理员启用
@bp.route('/admin/sys/admin_start',methods=("POST",))
@login_required
def admin_start():
	id = request.values.get("id",None)
	if id:
		start_sql = "update bl_sys_admin set is_del=0 where id=%s RETURNING id"
		db.operate_data(start_sql,(id,),mode="update")
		return common.bl_msg(1,"","操作成功")
	else:
		return common.bl_msg(-1,"","参数错误")

#============================================管理员模块 end================================================

#============================================菜单模块 start================================================
#菜单列表
@bp.route('/admin/sys/tab_list')
@login_required
def tab_list():
	return render_template('admin/sys/tab_list.html')

#菜单列表data
@bp.route('/admin/sys/tab_list_data',methods=('GET','POST'))
@login_required
def tab_list_data():

	#前端h-ui框架datatable固定格式的参数
	draw = request.form.get("draw",1)			#h-ui参数，请求次数
	offset = request.form.get("start",0)		#索引
	limit = request.form.get("length",10)		#查询数量，相当于每页显示数量

	query_params = []	#查询参数
	param_sql = " where 1=1 and ba.parent_id=0 "		#需要拼接的参数sql

	#查询总数据条数
	count_sql = "select count(*) from bl_sys_tab ba" + param_sql
	count = db.get_data(count_sql,tuple(query_params))[0]['count']

	select_sql = "select ba.id,ba.tab_name,ba.tab_level,ba.mode_code,ba.ordering,to_char(to_timestamp(ba.createtime),'yyyy-mm-dd hh24:mi:ss') as createtime,"\
				"to_char(to_timestamp(ba.updatetime),'yyyy-mm-dd hh24:mi:ss') as updatetime,ba.jmp_url from bl_sys_tab ba"
	orderby_sql = " order by ba.ordering desc "
	limit_sql = " limit %s offset %s"
	query_params.append(limit)
	query_params.append(offset)

	query_sql = select_sql + param_sql + orderby_sql + limit_sql		#最终查询sql
	data_list = db.get_data(query_sql,tuple(query_params))	#查询数据

	#前端h-ui框架datatable固定格式的返回
	info = {
			'draw':int(draw),			# ajax请求次数，作为标识符
			'recordsTotal':len(data_list),	# 获取到的结果数(每页显示数量)
			'recordsFiltered':count,		# 符合条件的总数据量
			'data':data_list					#获取到的数据结果
	}

	return info

#菜单新增或修改页
@bp.route('/admin/sys/tab_addupdate')
@login_required
@auth_check("menu-addupdate")
def tab_addupdate():

	if "id" in request.args:		#如果有id参数，则为修改
		id = request.args.get("id")		#id
		query_sql = "select * from bl_sys_tab where id=%s"
		data = db.get_data(query_sql,(id,))
		if len(data) == 0:		#id未查到数据，返回一个错误页面，400为http状态码
			return common.bl_err_page("参数错误",400)
		else:
			return render_template('admin/sys/tab_addupdate.html',data=data[0])
	else:
		# tab_level = 
		return render_template('admin/sys/tab_addupdate.html',data={})
	
#菜单新增或修改
@bp.route('/admin/sys/tab_doaddupdate',methods=('GET','POST'))
@login_required
def tab_doaddupdate():
	if request.method == "POST":

		id = request.form.get("id",None)		#根据id参数判断新增还是修改

		tab_name = request.form.get("tab_name").strip()
		mode_code = request.form.get("mode_code").strip()
		icon = request.form.get("icon").strip()
		ordering = request.form.get("ordering",'0').strip() 
		# ordering = '0' if request.form.get("ordering").strip() == '' else request.form.get("ordering").strip()
		
		createtime = int(datetime.now().timestamp())	#时间戳，秒
		updatetime = createtime

		if not tab_name:
			return common.bl_msg(-1,"","菜单名称不能为空")
		
		pt = re.compile(r"^[a-zA-Z0-9_-]{1,50}$")
		if not re.match(pt,mode_code):
			return common.bl_msg(-1,"","仅限于字母数字下划线中划线")
		
		if len(icon) > 10:
			return common.bl_msg(-1,"","菜单编码不合法！")
		
		if not ordering:
			ordering = 0
		if not ordering.isdigit():
			return common.bl_msg(-1,"","请输入非负数数字")

		#如果是新增
		if not id:
			#检查权限标识是否已经存在
			mc_ck_sql = "select count(*) from bl_sys_tab where mode_code=%s"
			mc_count = db.get_data(mc_ck_sql,(mode_code,))[0]["count"]
			if int(mc_count)  > 0:
				return common.bl_msg(-1,"","该权限标识已经存在！")

			add_sql = "insert into bl_sys_tab (tab_name,mode_code,icon,ordering,createtime,updatetime) "\
						"values(%s,%s,%s,%s,%s,%s) RETURNING id"
			query_params = (tab_name,mode_code,icon,ordering,createtime,updatetime)
			re_id = db.operate_data(add_sql,query_params)

			if re_id:
				return common.bl_msg(1,"","添加成功")
			else:
				return common.bl_msg(-1,"","添加失败")
		#修改
		else:

			#检查权限标识是否已经存在
			mc_ck_sql = "select count(*) from bl_sys_tab where mode_code=%s and id !=%s"
			mc_count = db.get_data(mc_ck_sql,(mode_code,id))[0]["count"]
			if int(mc_count)  > 0:
				return common.bl_msg(-1,"","该权限标识已经存在！")

			update_sql = "update bl_sys_tab set tab_name=%s,mode_code=%s,icon=%s,ordering=%s,updatetime=%s where id=%s RETURNING id"
			query_params = (tab_name,mode_code,icon,ordering,updatetime,id)

			re_id = db.operate_data(update_sql,query_params,mode="update")
			if re_id:
				return common.bl_msg(1,"","修改成功")
			else:
				return common.bl_msg(-1,"","修改失败")

#菜单删除
@bp.route('/admin/sys/tab_del',methods=("POST",))
@login_required
@auth_check("menu-del",2)		#权限检查
def tab_del():
	id = request.values.get("id",None)
	if id:
		#查询是否存在子菜单，如果有，无法删除
		ck_sub_sql = "select count(*) from bl_sys_tab where parent_id=%s"
		ck_count = db.get_data(ck_sub_sql,(id,))[0]["count"]
		if int(ck_count) > 0:
			return common.bl_msg(-1,"","该菜单下还有子菜单，无法删除！")

		del_sql = "delete from bl_sys_tab where id=%s RETURNING id"
		db.operate_data(del_sql,(id,),mode="del")
		return common.bl_msg(1,"","删除成功")
	else:
		return common.bl_msg(-1,"","参数错误")
	

#子菜单列表
@bp.route('/admin/sys/subtab_list')
@login_required
@auth_check("sub-menu")		#权限检查
def subtab_list():
	pid = request.args.get("pid",0)
	return render_template('admin/sys/subtab_list.html',pid=pid)

#子菜单列表data
@bp.route('/admin/sys/subtab_list_data',methods=('GET','POST'))
@login_required
def subtab_list_data():

	#前端h-ui框架datatable固定格式的参数
	draw = request.form.get("draw",1)			#h-ui参数，请求次数
	offset = request.form.get("start",0)		#索引
	limit = request.form.get("length",10)		#查询数量，相当于每页显示数量

	pid = request.form.get("pid",0)			#父菜单id

	query_params = [pid]	#查询参数
	param_sql = " where 1=1 and ba.parent_id=%s"		#需要拼接的参数sql

	#查询总数据条数
	count_sql = "select count(*) from bl_sys_tab ba" + param_sql
	count = db.get_data(count_sql,tuple(query_params))[0]['count']

	select_sql = "select ba.id,ba.tab_name,ba.tab_level,ba.mode_code,ba.ordering,to_char(to_timestamp(ba.createtime),'yyyy-mm-dd hh24:mi:ss') as createtime,"\
				"to_char(to_timestamp(ba.updatetime),'yyyy-mm-dd hh24:mi:ss') as updatetime,ba.jmp_url from bl_sys_tab ba"
	orderby_sql = " order by ba.id desc "
	limit_sql = " limit %s offset %s"
	query_params.append(limit)
	query_params.append(offset)

	query_sql = select_sql + param_sql + orderby_sql + limit_sql		#最终查询sql
	data_list = db.get_data(query_sql,tuple(query_params))	#查询数据

	#前端h-ui框架datatable固定格式的返回
	info = {
			'draw':int(draw),			# ajax请求次数，作为标识符
			'recordsTotal':len(data_list),	# 获取到的结果数(每页显示数量)
			'recordsFiltered':count,		# 符合条件的总数据量
			'data':data_list					#获取到的数据结果
	}

	return info

#子菜单新增或修改页
@bp.route('/admin/sys/subtab_addupdate')
@login_required
def subtab_addupdate():

	pid = request.args.get("pid",0)		#父菜单id

	if "id" in request.args:		#如果有id参数，则为修改
		id = request.args.get("id")		#id
		query_sql = "select * from bl_sys_tab where id=%s"
		data = db.get_data(query_sql,(id,))
		if len(data) == 0:		#id未查到数据，返回一个错误页面，400为http状态码
			return common.bl_err_page("参数错误",400)
		else:
			return render_template('admin/sys/subtab_addupdate.html',data=data[0],pid=pid)
	else:
		# tab_level = 
		return render_template('admin/sys/subtab_addupdate.html',data={},pid=pid)
	
#子菜单新增或修改
@bp.route('/admin/sys/subtab_doaddupdate',methods=('GET','POST'))
@login_required
def subtab_doaddupdate():
	if request.method == "POST":

		pid = request.form.get("pid",None)		#父菜单id
		id = request.form.get("id",None)		#根据id参数判断新增还是修改

		tab_name = request.form.get("tab_name").strip()
		mode_code = request.form.get("mode_code").strip()
		jmp_url = request.form.get("jmp_url").strip()
		ordering = request.form.get("ordering",'0').strip()
		
		createtime = int(datetime.now().timestamp())	#时间戳，秒
		updatetime = createtime
		tab_level = 1

		if not tab_name:
			return common.bl_msg(-1,"","子菜单名称不能为空")
		
		pt = re.compile(r"^[a-zA-Z0-9_-]{1,50}$")
		if not re.match(pt,mode_code):
			return common.bl_msg(-1,"","仅限于字母数字下划线中划线")
		
		if not ordering.isdigit():
			return common.bl_msg(-1,"","请输入非负数数字")

		#如果是新增
		if not id:
			#检查权限标识是否已经存在
			mc_ck_sql = "select count(*) from bl_sys_tab where mode_code=%s"
			mc_count = db.get_data(mc_ck_sql,(mode_code,))[0]["count"]
			if int(mc_count)  > 0:
				return common.bl_msg(-1,"","该权限标识已经存在！")

			add_sql = "insert into bl_sys_tab (tab_name,mode_code,tab_level,jmp_url,parent_id,ordering,createtime,updatetime) "\
						"values(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
			query_params = (tab_name,mode_code,tab_level,jmp_url,int(pid),ordering,createtime,updatetime)
			re_id = db.operate_data(add_sql,query_params)

			if re_id:
				return common.bl_msg(1,"","添加成功")
			else:
				return common.bl_msg(-1,"","添加失败")
		#修改
		else:

			#检查权限标识是否已经存在
			mc_ck_sql = "select count(*) from bl_sys_tab where mode_code=%s and id !=%s"
			mc_count = db.get_data(mc_ck_sql,(mode_code,id))[0]["count"]
			if int(mc_count)  > 0:
				return common.bl_msg(-1,"","该权限标识已经存在！")

			update_sql = "update bl_sys_tab set tab_name=%s,mode_code=%s,jmp_url=%s,ordering=%s,updatetime=%s where id=%s RETURNING id"
			query_params = (tab_name,mode_code,jmp_url,ordering,updatetime,id)

			re_id = db.operate_data(update_sql,query_params,mode="update")
			if re_id:
				return common.bl_msg(1,"","修改成功")
			else:
				return common.bl_msg(-1,"","修改失败")
			
#权限节点列表
@bp.route('/admin/sys/subnode_list')
@login_required
def subnode_list():
	pid = request.args.get("pid",0)
	return render_template('admin/sys/subnode_list.html',pid=pid)

#权限节点列表data
@bp.route('/admin/sys/subnode_list_data',methods=('GET','POST'))
@login_required
def subnode_list_data():

	#前端h-ui框架datatable固定格式的参数
	draw = request.form.get("draw",1)			#h-ui参数，请求次数
	offset = request.form.get("start",0)		#索引
	limit = request.form.get("length",10)		#查询数量，相当于每页显示数量

	pid = request.form.get("pid",0)			#父菜单id

	query_params = [pid]	#查询参数
	param_sql = " where 1=1 and ba.parent_id=%s"		#需要拼接的参数sql

	#查询总数据条数
	count_sql = "select count(*) from bl_sys_tab ba" + param_sql
	count = db.get_data(count_sql,tuple(query_params))[0]['count']

	select_sql = "select ba.id,ba.tab_name,ba.tab_level,ba.mode_code,ba.ordering,to_char(to_timestamp(ba.createtime),'yyyy-mm-dd hh24:mi:ss') as createtime,"\
				"to_char(to_timestamp(ba.updatetime),'yyyy-mm-dd hh24:mi:ss') as updatetime,ba.jmp_url from bl_sys_tab ba"
	orderby_sql = " order by ba.id desc "
	limit_sql = " limit %s offset %s"
	query_params.append(limit)
	query_params.append(offset)

	query_sql = select_sql + param_sql + orderby_sql + limit_sql		#最终查询sql
	data_list = db.get_data(query_sql,tuple(query_params))	#查询数据

	#前端h-ui框架datatable固定格式的返回
	info = {
			'draw':int(draw),			# ajax请求次数，作为标识符
			'recordsTotal':len(data_list),	# 获取到的结果数(每页显示数量)
			'recordsFiltered':count,		# 符合条件的总数据量
			'data':data_list					#获取到的数据结果
	}

	return info

#权限节点新增或修改页
@bp.route('/admin/sys/subnode_addupdate')
@login_required
def subnode_addupdate():

	pid = request.args.get("pid",0)		#父菜单id

	if "id" in request.args:		#如果有id参数，则为修改
		id = request.args.get("id")		#id
		query_sql = "select * from bl_sys_tab where id=%s"
		data = db.get_data(query_sql,(id,))
		if len(data) == 0:		#id未查到数据，返回一个错误页面，400为http状态码
			return common.bl_err_page("参数错误",400)
		else:
			return render_template('admin/sys/subnode_addupdate.html',data=data[0],pid=pid)
	else:
		return render_template('admin/sys/subnode_addupdate.html',data={},pid=pid)
	
#权限节点新增或修改
@bp.route('/admin/sys/subnode_doaddupdate',methods=('GET','POST'))
@login_required
def subnode_doaddupdate():
	if request.method == "POST":

		pid = request.form.get("pid",None)		#父菜单id
		id = request.form.get("id",None)		#根据id参数判断新增还是修改

		tab_name = request.form.get("tab_name").strip()
		mode_code = request.form.get("mode_code").strip()
		ordering = request.form.get("ordering",'0').strip()
		
		createtime = int(datetime.now().timestamp())	#时间戳，秒
		updatetime = createtime
		tab_level = 2

		if not tab_name:
			return common.bl_msg(-1,"","权限节点名称不能为空")
		
		pt = re.compile(r"^[a-zA-Z0-9_-]{1,50}$")
		if not re.match(pt,mode_code):
			return common.bl_msg(-1,"","仅限于字母数字下划线中划线")
		
		if not ordering.isdigit():
			return common.bl_msg(-1,"","请输入非负数数字")

		#如果是新增
		if not id:
			#检查权限标识是否已经存在
			mc_ck_sql = "select count(*) from bl_sys_tab where mode_code=%s"
			mc_count = db.get_data(mc_ck_sql,(mode_code,))[0]["count"]
			if int(mc_count)  > 0:
				return common.bl_msg(-1,"","该权限标识已经存在！")

			add_sql = "insert into bl_sys_tab (tab_name,mode_code,tab_level,parent_id,ordering,createtime,updatetime) "\
						"values(%s,%s,%s,%s,%s,%s,%s) RETURNING id"
			query_params = (tab_name,mode_code,tab_level,int(pid),ordering,createtime,updatetime)
			re_id = db.operate_data(add_sql,query_params)

			if re_id:
				return common.bl_msg(1,"","添加成功")
			else:
				return common.bl_msg(-1,"","添加失败")
		#修改
		else:

			#检查权限标识是否已经存在
			mc_ck_sql = "select count(*) from bl_sys_tab where mode_code=%s and id !=%s"
			mc_count = db.get_data(mc_ck_sql,(mode_code,id))[0]["count"]
			if int(mc_count)  > 0:
				return common.bl_msg(-1,"","该权限标识已经存在！")

			update_sql = "update bl_sys_tab set tab_name=%s,mode_code=%s,ordering=%s,updatetime=%s where id=%s RETURNING id"
			query_params = (tab_name,mode_code,ordering,updatetime,id)

			re_id = db.operate_data(update_sql,query_params,mode="update")
			if re_id:
				return common.bl_msg(1,"","修改成功")
			else:
				return common.bl_msg(-1,"","修改失败")
	
#============================================菜单模块 end================================================

#============================================角色模块 start================================================
#角色列表
@bp.route('/admin/sys/role_list')
@login_required
def role_list():
	return render_template('admin/sys/role_list.html')

#角色列表data
@bp.route('/admin/sys/role_list_data',methods=('GET','POST'))
@login_required
def role_list_data():

	#前端h-ui框架datatable固定格式的参数
	draw = request.form.get("draw",1)			#h-ui参数，请求次数
	offset = request.form.get("start",0)		#索引
	limit = request.form.get("length",10)		#查询数量，相当于每页显示数量

	query_params = []	#查询参数
	param_sql = " where 1=1 "		#需要拼接的参数sql

	#查询总数据条数
	count_sql = "select count(*) from bl_sys_role ba" + param_sql
	count = db.get_data(count_sql,tuple(query_params))[0]['count']

	select_sql = "select ba.id,ba.role_name,ba.role_desc,to_char(to_timestamp(ba.createtime),'yyyy-mm-dd hh24:mi:ss') as createtime,"\
				"to_char(to_timestamp(ba.updatetime),'yyyy-mm-dd hh24:mi:ss') as updatetime from bl_sys_role ba"
	orderby_sql = " order by ba.id desc "
	limit_sql = " limit %s offset %s"
	query_params.append(limit)
	query_params.append(offset)

	query_sql = select_sql + param_sql + orderby_sql + limit_sql		#最终查询sql
	data_list = db.get_data(query_sql,tuple(query_params))	#查询数据

	#前端h-ui框架datatable固定格式的返回
	info = {
			'draw':int(draw),			# ajax请求次数，作为标识符
			'recordsTotal':len(data_list),	# 获取到的结果数(每页显示数量)
			'recordsFiltered':count,		# 符合条件的总数据量
			'data':data_list					#获取到的数据结果
	}

	return info

#角色新增或修改页
@bp.route('/admin/sys/role_addupdate')
@login_required
def role_addupdate():

	tab_data = sys_model.get_tab_data()

	if "id" in request.args:		#如果有id参数，则为修改
		id = request.args.get("id")		#id
		query_sql = "select * from bl_sys_role where id=%s"
		data = db.get_data(query_sql,(id,))
		if len(data) == 0:		#id未查到数据，返回一个错误页面，400为http状态码
			return common.bl_err_page("参数错误",400)
		else:
			action_data = data[0]['role_action'].split(",")
			return render_template('admin/sys/role_addupdate.html',role_data=data[0],tab_data=tab_data,action_data=action_data)
	else:
		return render_template('admin/sys/role_addupdate.html',role_data={},tab_data=tab_data,action_data=[])
	
#角色新增或修改
@bp.route('/admin/sys/role_doaddupdate',methods=('GET','POST'))
@login_required
def role_doaddupdate():
	if request.method == "POST":

		id = request.form.get("id",None)		#根据id参数判断新增还是修改

		role_name = request.form.get("role_name").strip()
		role_desc = request.form.get("role_desc").strip()
		role_action = request.form.getlist("role_action")		#获取多选框表单数据
		role_action = ",".join(role_action)		#转成字符串

		createtime = int(datetime.now().timestamp())	#时间戳，秒
		updatetime = createtime

		if not role_name:
			return common.bl_msg(-1,"","角色名称不能为空")

		#如果是新增
		if not id:

			add_sql = "insert into bl_sys_role (role_name,role_desc,role_action,createtime,updatetime) "\
						"values(%s,%s,%s,%s,%s) RETURNING id"
			query_params = (role_name,role_desc,role_action,createtime,updatetime)
			re_id = db.operate_data(add_sql,query_params)

			if re_id:
				return common.bl_msg(1,"","添加成功")
			else:
				return common.bl_msg(-1,"","添加失败")
		#修改
		else:

			update_sql = "update bl_sys_role set role_name=%s,role_desc=%s,role_action=%s,updatetime=%s where id=%s RETURNING id"
			query_params = (role_name,role_desc,role_action,updatetime,id)

			re_id = db.operate_data(update_sql,query_params,mode="update")
			if re_id:
				return common.bl_msg(1,"","修改成功")
			else:
				return common.bl_msg(-1,"","修改失败")
			
#菜单删除
@bp.route('/admin/sys/role_del',methods=("POST",))
@login_required
def role_del():
	id = request.values.get("id",None)
	if id:
		del_sql = "delete from bl_sys_role where id=%s RETURNING id"
		db.operate_data(del_sql,(id,),mode="del")
		return common.bl_msg(1,"","删除成功")
	else:
		return common.bl_msg(-1,"","参数错误")

#============================================角色模块 end================================================
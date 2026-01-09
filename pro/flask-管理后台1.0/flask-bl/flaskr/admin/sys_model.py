from flaskr import db

########################
#模型层，一些模块的方法
########################

#获取菜单数据（一级菜单，二级菜单，三级权限节点）
def get_tab_data(pid=0):

	query_params = []
	sql = "select id,tab_name from bl_sys_tab "
	param_sql = " where 1=1 and parent_id=%s"
	order_by_sql = " order by ordering desc"
	query_sql = sql + param_sql + order_by_sql

	query_params.append(pid)
	data_list = db.get_data(query_sql,tuple(query_params))	#查询数据

	for index in range(len(data_list)):
		sub_data = get_tab_data(data_list[index]["id"])
		data_list[index]['sub_data'] = sub_data

	return data_list

#获取权限菜单
#admin_id : 管理员id
def get_authmenu(admin_id):
	role_sql = "select r.role_action from bl_sys_admin a left join bl_sys_role r on a.role_id=r.id "\
			" where a.id=%s"
	role_action = db.get_data(role_sql,(admin_id,))[0]["role_action"]		#获取管理员权限节点
	role_action_data = role_action.split(",")	#分割列表

	#获取一级菜单
	tab_sql = "select id,tab_name,icon from bl_sys_tab where tab_level=0 order by ordering desc"
	tab_data = db.get_data(tab_sql,None)

	re_data = []
	for d in tab_data:
		if d["id"] in role_action_data:
			sub_tab_sql = "select id,tab_name,jmp_url from bl_sys_tab where parent_id=%s order by ordering desc"
			sub_tab_data = db.get_data(sub_tab_sql,(d["id"],))		#获取二级菜单
			for dd in sub_tab_data:
				if dd["id"] not in role_action_data:
					sub_tab_data.remove(dd)
			d["sub_data"] = sub_tab_data
			re_data.append(d)

	return re_data
<?php
namespace app\admin\controller;
use app\BaseController;
use think\facade\Db;
use think\facade\View;
use app\admin\service\SysService;
use app\admin\middleware\LoginMiddleware;
use app\admin\middleware\AuthMiddleware;

//后台系统管理模块。包括菜单管理，角色管理，用户管理
class Sys extends BaseController{

	//登录中间件，权限中间件
	protected $middleware = [LoginMiddleware::class,AuthMiddleware::class];

	//菜单列表
	public function tab_list(){
		return view();
	}
	//菜单列表数据
	public function tab_list_data(){
		//前端h-ui框架datatable固定格式的参数
		$draw = input("get.draw",1);			//h-ui参数，请求次数
		$offset = input("get.start",0);			//索引
		$limit = input("get.length",10);		//查询数量，相当于每页显示数量

		$where["ba.parent_id"] = 0;
		$data_list = Db::name("sys_tab")
				->alias("ba")
				->field(" ba.id,ba.tab_name,ba.tab_level,ba.mode_code,ba.ordering,from_unixtime(ba.createtime,'%Y-%m-%d %H:%i:%s') as createtime,".
				"from_unixtime(ba.updatetime,'%Y-%m-%d %H:%i:%s') as updatetime,ba.jmp_url")
				->where($where)
				->order("ba.ordering","desc")
				->limit($offset,$limit)
				// ->fetchsql(true)
				->select();

		$count = Db::name("sys_tab")
				->alias("ba")
				->where($where)
				->count();

		#前端h-ui框架datatable固定格式的返回
		$info = [
			'draw'=>$draw,			# ajax请求次数，作为标识符
			'recordsTotal'=>count($data_list),	# 获取到的结果数(每页显示数量)
			'recordsFiltered'=>$count,		# 符合条件的总数据量
			'data'=>$data_list					#获取到的数据结果
		];
		return $info;
	}
	//菜单添加编辑
	public function tab_addupdate(){
		$data = [];
		$id = input("get.id");
		if($id){
			$data = Db::name("sys_tab")->where("id",$id)->find();
		}
		return view("",["data"=>$data]);
	}
	//菜单添加编辑提交
	public function tab_doaddupdate(){
		$id = input("post.id");
		$data["tab_name"] = trim(input("post.tab_name"));
		$data["mode_code"] = trim(input("post.mode_code"));
		$data["icon"] = trim(input("post.icon"));
		$data["ordering"] = trim(input("post.ordering",0));
		$stamp = time();

		if(!$data["tab_name"]){
			return msg(-1,"","菜单名称不能为空");
		}
		if(!preg_match("/^[0-9a-zA-Z_\-\/]{1,50}$/",$data["mode_code"])){
			return msg(-1,"","权限标识仅限于斜杠字母数字下划线中划线");
		}
		if(strlen($data["icon"]) > 10){
			return msg(-1,"","图标代码不合法");
		}
		if(!is_numeric($data["ordering"])){
			return msg(-1,"","排序请输入数字");
		}

		if($id){	//修改
			$f = Db::name("sys_tab")
				->where("mode_code",$data["mode_code"])
				->where("id","<>",$id)
				->find();
			if($f){
				return msg(-1,"","该权限标识已存在！");
			}

			$data["updatetime"] = $stamp;
			$re = Db::name("sys_tab")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","编辑成功");
			}
		}else{
			$f = Db::name("sys_tab")
				->where("mode_code",$data["mode_code"])
				->find();
			if($f){
				return msg(-1,"","该权限标识已存在！");
			}

			$data["createtime"] = $stamp;
			$data["updatetime"] = $stamp;
			$re2 = Db::name("sys_tab")->insert($data);
			if($re2){
				return msg(1,"","添加成功");
			}
		}
		return msg(-1,"","操作失败");
	}
	//菜单删除
	public function tab_del(){
		$id = input("post.id");
		if(!$id){
			return msg(-1,"","参数错误");
		}
		$sub_data = Db::name("sys_tab")->field("id")->where("parent_id",$id)->select();
		if(count($sub_data) > 0){
			return msg(-1,"","该菜单下还有子菜单或子节点，无法删除！");
		}
		$re = Db::name("sys_tab")->where("id",$id)->delete();
		if($re){
			return msg(1,"","删除成功");
		}else{
			return msg(1,"","操作失败");
		}
	}
	//子菜单列表
	public function subtab_list(){
		$pid = input("get.pid",0);
		return view("",["pid"=>$pid]);
	}
	//子菜单列表数据
	public function subtab_list_data(){
		//前端h-ui框架datatable固定格式的参数
		$draw = input("get.draw",1);			//h-ui参数，请求次数
		$offset = input("get.start",0);			//索引
		$limit = input("get.length",10);		//查询数量，相当于每页显示数量

		$pid = input("post.pid");

		$where["ba.parent_id"] = $pid;
		$data_list = Db::name("sys_tab")
				->alias("ba")
				->field(" ba.id,ba.tab_name,ba.tab_level,ba.mode_code,ba.ordering,from_unixtime(ba.createtime,'%Y-%m-%d %H:%i:%s') as createtime,".
				"from_unixtime(ba.updatetime,'%Y-%m-%d %H:%i:%s') as updatetime,ba.jmp_url")
				->where($where)
				->order("ba.ordering","desc")
				->limit($offset,$limit)
				// ->fetchsql(true)
				->select();

		$count = Db::name("sys_tab")
				->alias("ba")
				->where($where)
				->count();

		#前端h-ui框架datatable固定格式的返回
		$info = [
			'draw'=>$draw,			# ajax请求次数，作为标识符
			'recordsTotal'=>count($data_list),	# 获取到的结果数(每页显示数量)
			'recordsFiltered'=>$count,		# 符合条件的总数据量
			'data'=>$data_list					#获取到的数据结果
		];
		return $info;
	}
	//子菜单添加编辑
	public function subtab_addupdate(){
		$pid = input("get.pid",'');	//父菜单
		$id = input("get.id");		//子菜单id

		$data = [];
		if($id){
			$data = Db::name("sys_tab")->where("id",$id)->find();
		}
		return view("",["data"=>$data,"pid"=>$pid]);
	}
	//子菜单添加编辑提交
	public function subtab_doaddupdate(){
		$id = input("post.id");
		$pid = input("post.pid");

		$data["tab_name"] = trim(input("post.tab_name"));
		$data["mode_code"] = trim(input("post.mode_code"));
		$data["jmp_url"] = trim(input("post.jmp_url"));
		$data["ordering"] = trim(input("post.ordering",0));
		$stamp = time();

		if(!$data["tab_name"]){
			return msg(-1,"","菜单名称不能为空");
		}
		if(!preg_match("/^[0-9a-zA-Z_\-\/]{1,50}$/",$data["mode_code"])){
			return msg(-1,"","权限标识仅限于斜杠字母数字下划线中划线");
		}
		if(!is_numeric($data["ordering"])){
			return msg(-1,"","排序请输入数字");
		}
		
		if($id){	//修改
			$f = Db::name("sys_tab")
			->where("mode_code",$data["mode_code"])
			->where("id","<>",$id)
			->find();
			if($f){
				return msg(-1,"","该权限标识已存在！");
			}

			$data["updatetime"] = $stamp;
			$re = Db::name("sys_tab")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","编辑成功");
			}
		}else{
			$f = Db::name("sys_tab")
			->where("mode_code",$data["mode_code"])
			->find();
			if($f){
				return msg(-1,"","该权限标识已存在！");
			}

			$data["createtime"] = $stamp;
			$data["updatetime"] = $stamp;
			$data["tab_level"] = 1;	//1代表子菜单
			$data["parent_id"] = $pid;
			$re2 = Db::name("sys_tab")->insert($data);
			if($re2){
				return msg(1,"","添加成功");
			}
		}
		return msg(-1,"","操作失败");
	}
	//权限节点列表
	public function subnode_list(){
		$pid = input("get.pid",0);
		return view("",["pid"=>$pid]);
	}
	//子菜单列表数据
	public function subnode_list_data(){
		//前端h-ui框架datatable固定格式的参数
		$draw = input("get.draw",1);			//h-ui参数，请求次数
		$offset = input("get.start",0);			//索引
		$limit = input("get.length",10);		//查询数量，相当于每页显示数量

		$pid = input("post.pid");

		$where["ba.parent_id"] = $pid;
		$data_list = Db::name("sys_tab")
				->alias("ba")
				->field(" ba.id,ba.tab_name,ba.tab_level,ba.mode_code,ba.ordering,from_unixtime(ba.createtime,'%Y-%m-%d %H:%i:%s') as createtime,".
				"from_unixtime(ba.updatetime,'%Y-%m-%d %H:%i:%s') as updatetime,ba.jmp_url")
				->where($where)
				->order("ba.ordering","desc")
				->limit($offset,$limit)
				// ->fetchsql(true)
				->select();

		$count = Db::name("sys_tab")
				->alias("ba")
				->where($where)
				->count();

		#前端h-ui框架datatable固定格式的返回
		$info = [
			'draw'=>$draw,			# ajax请求次数，作为标识符
			'recordsTotal'=>count($data_list),	# 获取到的结果数(每页显示数量)
			'recordsFiltered'=>$count,		# 符合条件的总数据量
			'data'=>$data_list					#获取到的数据结果
		];
		return $info;
	}
	//权限节点添加编辑
	public function subnode_addupdate(){
		$pid = input("get.pid",'');	//父菜单
		$id = input("get.id");		//子菜单id

		$data = [];
		if($id){
			$data = Db::name("sys_tab")->where("id",$id)->find();
		}
		return view("",["data"=>$data,"pid"=>$pid]);
	}
	//权限节点添加编辑提交
	public function subnode_doaddupdate(){
		$id = input("post.id");
		$pid = input("post.pid");

		$data["tab_name"] = trim(input("post.tab_name"));
		$data["mode_code"] = trim(input("post.mode_code"));
		$data["ordering"] = trim(input("post.ordering",0));
		$stamp = time();

		if(!$data["tab_name"]){
			return msg(-1,"","菜单名称不能为空");
		}
		if(!preg_match("/^[0-9a-zA-Z_\-\/]{1,50}$/",$data["mode_code"])){
			return msg(-1,"","权限标识仅限于斜杠字母数字下划线中划线");
		}
		if(!is_numeric($data["ordering"])){
			return msg(-1,"","排序请输入数字");
		}
		
		if($id){	//修改
			$f = Db::name("sys_tab")
			->where("mode_code",$data["mode_code"])
			->where("id","<>",$id)
			->find();
			if($f){
				return msg(-1,"","该权限标识已存在！");
			}

			$data["updatetime"] = $stamp;
			$re = Db::name("sys_tab")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","编辑成功");
			}
		}else{
			$f = Db::name("sys_tab")
			->where("mode_code",$data["mode_code"])
			->find();
			if($f){
				return msg(-1,"","该权限标识已存在！");
			}

			$data["createtime"] = $stamp;
			$data["updatetime"] = $stamp;
			$data["tab_level"] = 2;	//2代表权限节点
			$data["parent_id"] = $pid;
			$re2 = Db::name("sys_tab")->insert($data);
			if($re2){
				return msg(1,"","添加成功");
			}
		}
		return msg(-1,"","操作失败");
	}

	//角色列表
	public function role_list(){
		return view();
	}
	//角色列表数据
	public function role_list_data(){
		//前端h-ui框架datatable固定格式的参数
		$draw = input("get.draw",1);			//h-ui参数，请求次数
		$offset = input("get.start",0);			//索引
		$limit = input("get.length",10);		//查询数量，相当于每页显示数量

		$data_list = Db::name("sys_role")
				->alias("ba")
				->field(" ba.id,ba.role_name,ba.role_desc,from_unixtime(ba.createtime,'%Y-%m-%d %H:%i:%s') as createtime,".
				"from_unixtime(ba.updatetime,'%Y-%m-%d %H:%i:%s') as updatetime")
				->order("ba.id","desc")
				->limit($offset,$limit)
				// ->fetchsql(true)
				->select();

		$count = Db::name("sys_role")
				->alias("ba")
				->count();

		#前端h-ui框架datatable固定格式的返回
		$info = [
			'draw'=>$draw,			# ajax请求次数，作为标识符
			'recordsTotal'=>count($data_list),	# 获取到的结果数(每页显示数量)
			'recordsFiltered'=>$count,		# 符合条件的总数据量
			'data'=>$data_list					#获取到的数据结果
		];
		return $info;
	}
	//角色添加编辑
	public function role_addupdate(){
		$ss = new SysService();
		$tab_data = $ss->get_tab_data();
		$role_data = [];
		$action_data = [];

		$id = input("get.id");		//id

		if($id){
			$role_data = Db::name("sys_role")->where("id",$id)->find();
			$action_data = explode(",",$role_data["role_action"]);

		}
		return view("",["tab_data"=>$tab_data,"role_data"=>$role_data,"action_data"=>$action_data]);
	}
	//角色添加编辑提交
	public function role_doaddupdate(){
		$id = input("post.id");

		$data["role_name"] = trim(input("post.role_name"));
		$data["role_desc"] = trim(input("post.role_desc"));
		$data["role_action"] = input("post.role_action");
		$data["role_action"] = implode(",",$data["role_action"]);

		$stamp = time();

		if(!$data["role_name"]){
			return msg(-1,"","角色名称不能为空");
		}
		
		if($id){	//修改
			$data["updatetime"] = $stamp;
			$re = Db::name("sys_role")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","编辑成功");
			}
		}else{
			$data["createtime"] = $stamp;
			$data["updatetime"] = $stamp;
			$re2 = Db::name("sys_role")->insert($data);
			if($re2){
				return msg(1,"","添加成功");
			}
		}
		return msg(-1,"","操作失败");
	}
	//角色删除
	public function role_del(){
		$id = input("post.id");
		if($id){
			$re = Db::name("sys_role")->where("id",$id)->delete();
			if($re){
				return msg(1,"","删除成功");
			}else{
				return msg(-1,"","删除失败");
			}
		}else{
			return msg(-1,"","参数错误");
		}
	}
	//管理员列表
	public function admin_list(){
		return view();
	}
	//管理员列表数据
	public function admin_list_data(){
		//前端h-ui框架datatable固定格式的参数
		$draw = input("get.draw",1);			//h-ui参数，请求次数
		$offset = input("get.start",0);			//索引
		$limit = input("get.length",10);		//查询数量，相当于每页显示数量

		$start_date = input("post.start_date");
		$end_date = input("post.end_date");
		$admin_name = trim(input("post.admin_name"));

		$map = [];
		if($start_date){
			$map[] = ["ba.createtime",">",strtotime($start_date)];
		}
		if($end_date){
			$map[] = ["ba.createtime","<=",strtotime($end_date)];
		}
		if($admin_name){
			$map[] = ["ba.admin_name","like","%".$admin_name."%"];
		}

		$data_list = Db::name("sys_admin")
				->alias("ba")
				->leftjoin("sys_role bar","ba.role_id=bar.id")
				->field(" ba.id,ba.admin_name,ba.nick_name,ba.email,ba.role_id,from_unixtime(ba.createtime,'%Y-%m-%d %H:%i:%s') as createtime,".
				"from_unixtime(ba.updatetime,'%Y-%m-%d %H:%i:%s') as updatetime,ba.is_del,bar.role_name")
				->where($map)
				->order("ba.id","desc")
				->limit($offset,$limit)
				// ->fetchsql(true)
				->select();

		$count = Db::name("sys_admin")
				->alias("ba")
				->leftjoin("sys_role bar","ba.role_id=bar.id")
				->where($map)
				->count();

		#前端h-ui框架datatable固定格式的返回
		$info = [
			'draw'=>$draw,			# ajax请求次数，作为标识符
			'recordsTotal'=>count($data_list),	# 获取到的结果数(每页显示数量)
			'recordsFiltered'=>$count,		# 符合条件的总数据量
			'data'=>$data_list					#获取到的数据结果
		];
		return $info;
	}
	//admin add or update
	public function admin_addupdate(){
		$role_data = Db::name("sys_role")->field("id,role_name")->select();		//role data
		$admin_data = [];
		$id = input("get.id");		//id

		if($id){
			$admin_data = Db::name("sys_admin")->where("id",$id)->find();
		}
		return view("",["admin_data"=>$admin_data,"role_data"=>$role_data]);
	}
	//admin add or update submit 提交
	public function admin_doaddupdate(){
		$id = input("post.id");

		$data["admin_name"] = trim(input("post.admin_name"));
		$data["nick_name"] = trim(input("post.nick_name"));
		$data["password"] = trim(input("post.password"));
		$data["role_id"] = trim(input("post.admin_role"));
		$data["email"] = trim(input("post.email"));

		$stamp = time();

		if(!$data["admin_name"]){
			return msg(-1,"","管理员名称不能为空");
		}
		
		if($data["email"] && !reg_email($data["email"])){
			return msg(-1,"","邮箱格式不正确");
		}
		if($id){	//update
			$f = Db::name("sys_admin")
				->where("admin_name",$data["admin_name"])
				->where("id","<>",$id)
				->find();
			if($f){
				return msg(-1,"","管理员名称已存在！");
			}

			if($data["password"]){
				if(!preg_match("/^[\S]{6,16}$/",$data["password"])){
					return msg(-1,"","密码6-16个字符");
				}
				$data["password"] = password_hash($data["password"],PASSWORD_DEFAULT);
			}else{
				unset($data["password"]);	//if not input password,then keep old
			}

			$data["updatetime"] = $stamp;
			$re = Db::name("sys_admin")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","编辑成功");
			}
		}else{
			$f = Db::name("sys_admin")
				->where("admin_name",$data["admin_name"])
				->find();
			if($f){
				return msg(-1,"","管理员名称已存在！");
			}
			
			if(!preg_match("/^[\S]{6,16}$/",$data["password"])){
				return msg(-1,"","密码6-16个字符");
			}
			$data["password"] = password_hash($data["password"],PASSWORD_DEFAULT);	//encipher
			$data["createtime"] = $stamp;
			$data["updatetime"] = $stamp;
			$re2 = Db::name("sys_admin")->insert($data);
			if($re2){
				return msg(1,"","添加成功");
			}
		}
		return msg(-1,"","操作失败");
	}
	//admin delete
	public function admin_del(){
		$id = input("post.id");
		if($id){
			$re = Db::name("sys_admin")->where("id",$id)->delete();
			if($re){
				return msg(1,"","删除成功");
			}else{
				return msg(-1,"","删除失败");
			}
		}else{
			return msg(-1,"","参数错误");
		}
	}
	//admin enable
	public function admin_start(){
		$id = input("post.id");
		if($id){
			$data["is_del"] = 0;
			$re = Db::name("sys_admin")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","已启用");
			}else{
				return msg(-1,"","操作失败");
			}
		}else{
			return msg(-1,"","参数错误");
		}
	}
	//admin stop
	public function admin_stop(){
		$id = input("post.id");
		if($id){
			$data["is_del"] = 1;
			$re = Db::name("sys_admin")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","已停用");
			}else{
				return msg(-1,"","操作失败");
			}
		}else{
			return msg(-1,"","参数错误");
		}
	}
	//auth_check 权限验证（前端ajax验证，方便做弹窗优化）
	public function auth_check(){
		$param["auth_url"] = input("post.auth_url");
		$param["admin_id"] = session("admin_id");
		$param["admin_role_action"] = session("admin_role_action");
		$sysService = new SysService();
		$re = $sysService->auth_url_check($param);
		if($re){
			return msg(1,"","");
		}else{
			return msg(-1,"","对不起，您没有权限");
		}
	}
}

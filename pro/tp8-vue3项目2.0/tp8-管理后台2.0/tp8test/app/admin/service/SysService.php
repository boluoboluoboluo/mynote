<?php
namespace app\admin\service;
use think\facade\Db;

//后台系统管理业务方法
class SysService{

	//获取菜单数据
	public function get_tab_data($pid=0){
		$data = Db::name("sys_tab")
				->alias("ba")
				->field("ba.id,ba.tab_name")
				->where("ba.parent_id",$pid)
				->order("ba.ordering","desc")
				->select();

		$data = $data->toArray();

		if(count($data) > 0){
			foreach($data as $k=>$v){
				$sub_data = $this->get_tab_data($data[$k]["id"]);
				$data[$k]["sub_data"] = $sub_data;
			}
		}
		
		return $data;
	}
	//get currnet admin's authmenu data
	public function get_authmenu($admin_id){
		$role_action = Db::name("sys_admin")
					->alias("a")
					->leftjoin("sys_role r","a.role_id=r.id")
					->where("a.id",$admin_id)
					->value("r.role_action");
		$role_action_arr = explode(",",$role_action);
		//get first level menu data
		$tab_data = Db::name("sys_tab")->field("id,tab_name,icon")->where("tab_level",0)->order("ordering","desc")->select();

		$authmenu_data = [];
		foreach($tab_data as $k=>$v){
			if(in_array($v["id"],$role_action_arr)){
				$sub_tab_data = Db::name("sys_tab")->field("id,tab_name,jmp_url")->where("parent_id",$v["id"])->order("ordering","desc")->select();
				$tmp_sub_data = [];		//second level menu data
				foreach($sub_tab_data as $kk=>$vv){
					if(in_array($vv["id"],$role_action_arr)){
						array_push($tmp_sub_data,$vv);
					}
				}
				$v["sub_data"] = $tmp_sub_data;
				array_push($authmenu_data,$v);
			}
		}

		return $authmenu_data;
	}
	//auth_url_check:验证当前url权限，和角色管理的权限路径对应
	public function auth_url_check($param){
		$url = urldecode($param["auth_url"]);
		$url = preg_replace("/[\/]+/","/",$url);
		$url = explode("?",$url)[0];

		$where["mode_code"] = $url;
		$tab_id = Db::name("sys_tab")->where($where)->value("id");
		if($tab_id){
			$where2["sa.id"] = $param["admin_id"];
			$role_action = $param["admin_role_action"];
			$role_action_arr = explode(",",$role_action);
			if(!in_array($tab_id,$role_action_arr)){
				return false;
			}
		}
		return true;
	}
}
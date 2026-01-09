<?php
namespace app\admin\controller;
use app\BaseController;
use think\Request;
use think\facade\Db;
use think\facade\View;
use think\captcha\facade\Captcha;
use think\exception\ValidateException;
use app\admin\validate\AdminValidate;
use app\admin\service\SysService;

//后台基础登录相关模块
class Base extends BaseController{
	//验证码
	public function captcha(){
		return Captcha::create();
	}
	//后台登录页面
	public function login(){
		return view();
	}
	//后台提交登录
	public function sub_login(){
		$params = input("post.");

		try{
			$result = validate(AdminValidate::class)->check($params);		//验证

		}catch(ValidateException $e){
			return msg(-1,"",$e->getError());
		}
		if(!captcha_check($params["captcha"])){
			return msg(-1,"","验证码有误");
		}

		$where["admin_name"] = trim($params["admin_name"]);
		$where["is_del"] = 0;
		$re = Db::name("sys_admin")->where($where)->find();
		//密码加密方式
		//password_hash("xxx", PASSWORD_DEFAULT);
		//密码验证方式
		if($re && password_verify($params["password"],$re["password"])){
			$role_action = Db::name("sys_role")->where("id",$re["role_id"])->value("role_action");
			session("admin_id",$re["id"]);
			session("admin_name",$re["admin_name"]);
			session("admin_role_action",$role_action);
			trace("管理员[".$re["admin_name"]."]已登录...");		//log
			return msg(1,"/admin/base/index","登录成功");
		}else{
			return msg(-1,"","用户名或密码错误");
		}
	}
	//后台首页
	public function index(){
		$admin_id = session("admin_id");
		if($admin_id){
			$admin_info = Db::name("sys_admin")->where("id",$admin_id)->find();
			if(!session("?menu_data")){
				$sysService = new SysService();
				 session("menu_data",$sysService->get_authmenu($admin_id)); 
			}
			return view("base/index",["admin_info"=>$admin_info,"menu_data"=>session("menu_data")]);
		}else{
			return redirect("/admin/base/login");
		}
	}

	//admin logout
	public function logout(){
		$admin_id = session("admin_id");
		if($admin_id){
			session(null);
		}
		return redirect("/admin/base/login");
	}
	//change password
	public function change_pass(){
		$admin_id = session("admin_id");
		if($admin_id){
			return view();
		}else{
			return redirect("/admin/base/login");
		}
	}
	//change password submit
	public function change_pass_sub(){

		$admin_id = session("admin_id");
		if(!$admin_id){
			return msg(-1,"","非法操作");	//not login,refused
		}

		$old_pass = trim(input("post.old_password"));
		$new_pass = trim(input("post.new_password"));
		$new_pass2 = trim(input("post.new_password2"));

		$where["id"] = $admin_id;
		$re = Db::name("sys_admin")->where($where)->find();
		//密码加密方式
		//password_hash("xxx", PASSWORD_DEFAULT);
		//密码验证方式
		if(!password_verify($old_pass,$re["password"])){
			return msg(-1,"","旧密码不正确");
		}

		if(!preg_match("/^[\S]{6,16}$/",$new_pass)){
			return msg(-1,"","新密码6-16个字符");
		}
		if($new_pass != $new_pass2){
			return msg(-1,"","2次输入新密码不一致");
		}
		$data["password"] = password_hash($new_pass,PASSWORD_DEFAULT);
		$re = Db::name("sys_admin")->where($where)->update($data);
		if($re){
			return msg(1,"","修改成功");
		}else{
			return msg(-1,"","修改失败");
		}

	}

	

}

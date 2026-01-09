<?php

namespace app\test\controller;

use app\BaseController;
use think\Request;
use think\facade\Db;
use think\facade\View;
use think\facade\Cache;
use think\facade\Filesystem;
use \Firebase\JWT\JWT;
use Firebase\JWT\Key;

class ApiTest extends BaseController{

    public function test(){
        // sleep(5);
        return view('',["name"=>"ddd"]); 
    }

	
	//用户端模拟登录
	public function act_login(){

		$param = input("post.");

		//模拟数据
		$data["id"] = 1;
		$data["username"] = "test";
		$password = "123456";
		$md5_pass = md5($password);

		if(!trim($param["username"])){
			return msg(-1,"","用户名不能为空");
		}

		if($data["username"] != trim($param["username"])){
			return msg(-1,"","用户名不正确");
		}
		if($md5_pass != trim($param["password"])){
			return msg(-1,"","密码错误");
		}

		//--start 登录成功后，生成jwt-token
		$key = "my_secret_key";		//密钥
		$payload = array(
			"id" => $data["id"],
			"username" => $data["username"],
			"iat" => time(),
			// "exp" => time() + 60*60*24	//有效期1天
			"exp" => time() + 1	//有效期1秒
		);
		$jwt = JWT::encode($payload,$key,'HS256');
		//---end

		$re_data["data"] = $data;
		$re_data["token"] = $jwt;
		return msg(1,$re_data,"登录成功");
	}

	//jwt_check
	public function jwt_check_test(){
		$jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1dsfwefewfNiJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJ0ZXN0IiwiaWF0IjoxNjk5ODY3NDgzLCJleHAiOjE2OTk4Njc0ODR9.3USNV6vsL0BCPTDOMGNSptJerZSxA_M_-fglplC6xEA";
		$key = "my_secret_key";

		try{
			$decoded = JWT::decode($jwt, new Key($key, 'HS256'));
			// echo $decoded->username;
			// echo "<br>";
			// var_dump($decoded);
		} catch (\Firebase\JWT\ExpiredException $e) {
			echo "已过期";
		}catch(\Exception $e){
			echo "验证失败";
		}
	}

}

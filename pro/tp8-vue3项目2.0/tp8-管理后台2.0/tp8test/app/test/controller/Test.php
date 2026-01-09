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

class Test extends BaseController{

    public function test(){
        // sleep(5);
        return view('',["name"=>"ddd"]); 
    }

	public function test2(){
		// ini_set("session.gc_maxlifetime",5);
		// ini_set("session.cookie_lifetime",5);
		session("ccc","333");
		echo "session set done..";
		dump(ini_get_all());
	}

	public function test3(){
		echo session("ccc");
		dump(session());
	}

	public function test4(){
		return view("dist/index");
	}


	//一些
    public function some(Request $request){

        $arr = ["id"=>3,"name"=>"sdfwefwefsdfew"];
        // return json($arr);

        // dump($request);

        // halt("调试...");
        // halt($request);
        
        // input("get.id");     //助手函数
        
        // session("x");       //session 默认关闭
        
         // return download(root_path().'image.jpg', 'my.jpg');    //下载
         
         // return view("index/test");      //需安装tihnk-view扩展
         
         //Log::write("");              //记日志，需要use think\facade\Log;
		 echo "eeeee";
         trace("mihao");        //记日志助手函数
		 echo "ddd";
    }

    //route/app.php定义了路由规则，导致该路由 http://localhostindex/hello 失效
    //正确访问方式：http://localhost/hello/xxx
    public function hello($name = 'ThinkPHP8'){
        return 'hello,' . $name;
    }


	public function hash_test(){
		$password = '123456';
		// $options = array('salt' => 'salt_value', 'cost' => 12);
 
		$hashedPassword = password_hash($password, PASSWORD_BCRYPT);
		echo "哈希密码: " . $hashedPassword;
		echo "<br>";
		$f = password_verify("123456",$hashedPassword);

        echo $f;
	}


    public function uploadtest(){
        return view();
    }
     
    //文件上传
    public function upload(){
        // 获取表单上传文件 例如上传了001.jpg
        $file = request()->file('image');

        // 上传到本地服务器,/runtime/starage
        // $savename = \think\facade\Filesystem::putFile( 'topic', $file);

        //上传到/public/storage
        $savename = \think\facade\Filesystem::disk('public')->putFile( 'topic', $file);
    }

    //多文件上传
    public function uploadFiles(){
        // 获取表单上传文件
        $files = request()->file('images');
        $savename = [];
        foreach($files as $file){
            $savename[] = \think\facade\Filesystem::putFile( 'topic', $file);
        }
    }

    public function uploads(){
        // 获取表单上传文件
        $files = request()->file();
        try {
            validate(['images'=>'fileSize:10240|fileExt:jpg|image:200,200,jpg'])
                ->check($files);
            $savename = [];
            foreach($files as $file) {
                $savename[] = \think\facade\Filesystem::putFile( 'topic', $file);
            }
        } catch (\think\exception\ValidateException $e) {
            echo $e->getMessage();
        }
    }


	//大文件下载
	public function download_test(){
		$file = root_path()."public/test.mp4";

		if(!file_exists($file)){
			echo "file not exists,please check..";
			exit;
		}

		$chunkSize = 1024 * 1024; // 每次读取1M
		$handle = fopen($file, 'rb');
		header('Content-Type: application/octet-stream');	//流文件
		header('Content-Disposition: attachment; filename="'.basename($file).'"');		//attachment：方式为下载
		header('Content-Transfer-Encoding: binary');		//二进制文件，此方式可支持巨大文件的下载
		header('Accept-Ranges: bytes');		//范围请求，表示支持分块下载，续传
		header('Cache-Control: must-revalidate');	//缓存过期后，需向服务器校验。而no-cache为每次请求缓存都需要校验
		header('Pragma: public');	//公开缓存，共享式。而private为私有，即单用户缓存
		$i = 0;
		while (!feof($handle)) {
			$buffer = fread($handle, $chunkSize);
			echo $buffer;
			ob_flush();
			flush();
			if ($i++ > 2000) { // 每2秒检查一次是否超时
				if (connection_aborted()) {
					break;
				}
				$i = 0;
			}
		}
		fclose($handle);
	}

	//jwt
	public function jwt_test(){
		$key = "my_secret_key";		//密钥
		$payload = array(
			"id" => 1,
			"username" => "test",
			"iat" => time(),
			// "exp" => time() + 60*60*24	//有效期1天
			"exp" => time() + 1	//有效期1秒
		);
		$jwt = JWT::encode($payload,$key,'HS256');

		echo $jwt;
	}
	public function jwt_decode_test(){
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

	//执行sql脚本
	private function exe_sqlscript(){
		$sql_file = app()->getRootPath()."/sqlscripts/bl_media_data.sql";	//sql file path

		// $file_content = file_get_contents($sql_file);	//read file content.
		// $sqls = explode(";",$file_content);

		try{
			Db::startTrans();
			$fin = fopen($sql_file,"r") or exit("unable to open sql script file.");
			$sql = "";
			while(!feof($fin)){
				$line = trim(fgets($fin));		//read a line
				if(empty($line)){
					continue;
				}
				if(substr($line,0,2) == "--"){			//ignore comment
					continue;
				}
				$sql .= $line;
				if(substr($line,-1,1) != ";"){
					continue;
				}
				Db::execute($sql);
				$sql = "";
			}
			Db::commit();
		}catch(\Exception $e){
			Db::rollback();
			echo "sql script execute error:".$e->getMessage();
		}
	}
	private function exe_sql(){
		$timestamp = time();
		$sql2 = "insert into `bl_media_data` (`title`,`desc`,`createtime`,`updatetime`) values('test','test...',$timestamp,$timestamp)";
		try{
			Db::execute($sql2);
			echo "sql execute success.";
		}catch(\Exception $e){
			echo "sql execute error:".$e->getMessage();
		}
	}
	public function find_sql(){
		$data = Db::name("media_data")
				->where("id",3)
				->select();
		var_dump($data);
	}



}

<?php

namespace app\api\controller;

use app\BaseController;
use think\Request;
use think\facade\Db;

class Media extends BaseController{
	//articlelist data
	public function articleList(){
		$where["type"] = 0;
		$data = Db::name("media_data")
		->field("id,title,desc,updatetime")
		->where($where)
		->select();
		return msg(1,$data,"success");
	}
	public function articleDetail(){
		$id = input("get.id");
		$where["id"] = $id;
		$data = Db::name("media_data")
		->field("id,title,desc,context,updatetime")
		->where($where)
		->find();
		return msg(1,$data,"success");
	}
	public function videoList(){
		$where["type"] = 1;
		$data = Db::name("media_data")
		->field("id,title,desc,url,updatetime")
		->where($where)
		->select();
		return msg(1,$data,"success");
	}
	public function videoDetail(){
		$id = input("get.id");
		$where["id"] = $id;
		$data = Db::name("media_data")
		->field("id,title,desc,url,updatetime")
		->where($where)
		->find();
		return msg(1,$data,"success");
	}
	public function musicList(){
		$where["type"] = 2;
		$data = Db::name("media_data")
		->field("id,title,desc,url,updatetime")
		->where($where)
		->select();
		return msg(1,$data,"success");
	}
	public function picList(){
		$where["type"] = 3;
		$data = Db::name("media_data")
		->field("id,title,desc,url,updatetime")
		->where($where)
		->select();
		return msg(1,$data,"success");
	}
	//加载视频
	public function loadVideo(){
		// trace("dddddddddddddddddddddddddddddd");
		// $url = input("get.url");
		$url = app()->getRootPath()."z_mediadata/".input("get.url");
		trace("url:".$url);
		if(file_exists($url)){
			header("Content-Type:video/mp4");
			readfile($url);
			exit;
		}else{
			echo "not found.";
		}

	}
}


<?php
namespace app\admin\controller;
use app\BaseController;
use think\facade\Db;
use think\facade\View;
use app\admin\service\SysService;
use app\admin\middleware\LoginMiddleware;
use app\admin\middleware\AuthMiddleware;

//admin media module
class Media extends BaseController{

	//====================================article start=========================
	public function article_list(){
		return view();
	}
	
	//文章列表数据
	public function article_list_data(){
		//前端h-ui框架datatable固定格式的参数
		$draw = input("get.draw",1);			//h-ui参数，请求次数
		$offset = input("get.start",0);			//索引
		$limit = input("get.length",10);		//查询数量，相当于每页显示数量

		$where["ba.type"] = 0;		//type:article(0)
		$data_list = Db::name("media_data")
				->alias("ba")
				->where($where)
				->field(" ba.id,ba.title,ba.desc,ba.ordering,from_unixtime(ba.createtime,'%Y-%m-%d %H:%i:%s') as createtime,".
				"from_unixtime(ba.updatetime,'%Y-%m-%d %H:%i:%s') as updatetime")
				->order("ba.ordering","desc")
				->limit($offset,$limit)
				// ->fetchsql(true)
				->select();

		$count = Db::name("media_data")
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
	//文章添加编辑
	public function article_addupdate(){
		$data = [];
		$id = input("get.id");
		if($id){
			$data = Db::name("media_data")->where("id",$id)->find();
		}
		return view("",["data"=>$data]);
	}
	//文章添加编辑提交
	public function article_doaddupdate(){
		$id = input("post.id");
		$data["title"] = trim(input("post.title"));
		$data["desc"] = trim(input("post.desc"));
		$data["ordering"] = trim(input("post.ordering",0));
		$data["context"] = trim(input("post.context",0));
		$stamp = time();

		if(!$data["title"]){
			return msg(-1,"","文章标题不能为空");
		}
		if(!is_numeric($data["ordering"])){
			return msg(-1,"","排序请输入数字");
		}

		if($id){	//修改
			$data["updatetime"] = $stamp;
			$re = Db::name("media_data")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","编辑成功");
			}
		}else{
			$data["createtime"] = $stamp;
			$data["updatetime"] = $stamp;
			$data["type"] = 0;	//0表示文章
			$re2 = Db::name("media_data")->insert($data);
			if($re2){
				return msg(1,"","添加成功");
			}
		}
		return msg(-1,"","操作失败");
	}
	//文章删除
	public function article_del(){
		$id = input("post.id");
		if(!$id){
			return msg(-1,"","参数错误");
		}
		$re = Db::name("media_data")->where("id",$id)->delete();
		if($re){
			return msg(1,"","删除成功");
		}else{
			return msg(1,"","操作失败");
		}
	}
	//====================================article end=========================

	//====================================video start=================
	public function video_list(){
		return view();
	}
	
	//列表数据
	public function video_list_data(){
		//前端h-ui框架datatable固定格式的参数
		$draw = input("get.draw",1);			//h-ui参数，请求次数
		$offset = input("get.start",0);			//索引
		$limit = input("get.length",10);		//查询数量，相当于每页显示数量

		$where["ba.type"] = 1;		//type:video(1)
		$data_list = Db::name("media_data")
				->alias("ba")
				->where($where)
				->field(" ba.id,ba.title,ba.desc,ba.ordering,from_unixtime(ba.createtime,'%Y-%m-%d %H:%i:%s') as createtime,".
				"from_unixtime(ba.updatetime,'%Y-%m-%d %H:%i:%s') as updatetime,url")
				->order("ba.ordering","desc")
				->limit($offset,$limit)
				// ->fetchsql(true)
				->select();

		$count = Db::name("media_data")
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
	//添加编辑
	public function video_addupdate(){
		$data = [];
		$id = input("get.id");
		if($id){
			$data = Db::name("media_data")->where("id",$id)->find();
		}
		return view("",["data"=>$data]);
	}
	//添加编辑提交
	public function video_doaddupdate(){
		$id = input("post.id");
		$data["title"] = trim(input("post.title"));
		$data["desc"] = trim(input("post.desc"));
		$data["ordering"] = trim(input("post.ordering",0));
		$stamp = time();

		if(!$data["title"]){
			return msg(-1,"","视频标题不能为空");
		}
		if(!is_numeric($data["ordering"])){
			return msg(-1,"","排序请输入数字");
		}
		

		if($id){	//修改
			$data["updatetime"] = $stamp;
			$re = Db::name("media_data")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","编辑成功");
			}
		}else{
			//上传文件
			$file = request()->file();
			if($file){
				
				$filesize =  100 * 1024 * 1024;	//100M
				validate(['file'=>'fileSize:'.$filesize.'|fileExt:mp4,avi,rmvb,ts'])->check($file);
				$savename = \think\facade\Filesystem::putFile( 'video', $file["file"]);
				$data["url"] = $savename;
			}
			
			$data["createtime"] = $stamp;
			$data["updatetime"] = $stamp;
			$data["type"] = 1;	//1表示视频
			$re2 = Db::name("media_data")->insert($data);
			if($re2){
				return msg(1,"","添加成功");
			}
		}
		return msg(-1,"","操作失败");
	}
	//删除
	public function video_del(){
		$id = input("post.id");
		if(!$id){
			return msg(-1,"","参数错误");
		}

		$url = Db::name("media_data")->where("id",$id)->value("url");
		trace("url:".$url);
		$path = app()->getRootPath()."z_mediadata/".$url;
		if(file_exists($path)){
			unlink($path);
			trace("已删除视频：".$path);
		}

		$re = Db::name("media_data")->where("id",$id)->delete();
		if($re){
			return msg(1,"","删除成功");
		}else{
			return msg(1,"","操作失败");
		}
	}
	//play video
	public function play_video(){
		$url = app()->getRootPath()."z_mediadata/".input("get.url");
		// trace("url:".$url);
		if(file_exists($url)){
			header("Content-Type:video/mp4");
			readfile($url);
			exit;
		}else{
			echo "not found.";
		}
	}
	//=====================================video end============================

	//====================================music start=================
	public function music_list(){
		return view();
	}
	
	//列表数据
	public function music_list_data(){
		//前端h-ui框架datatable固定格式的参数
		$draw = input("get.draw",1);			//h-ui参数，请求次数
		$offset = input("get.start",0);			//索引
		$limit = input("get.length",10);		//查询数量，相当于每页显示数量

		$where["ba.type"] = 2;		//type:music(2)
		$data_list = Db::name("media_data")
				->alias("ba")
				->where($where)
				->field(" ba.id,ba.title,ba.desc,ba.ordering,from_unixtime(ba.createtime,'%Y-%m-%d %H:%i:%s') as createtime,".
				"from_unixtime(ba.updatetime,'%Y-%m-%d %H:%i:%s') as updatetime,url")
				->order("ba.ordering","desc")
				->limit($offset,$limit)
				// ->fetchsql(true)
				->select();

		$count = Db::name("media_data")
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
	//添加编辑
	public function music_addupdate(){
		$data = [];
		$id = input("get.id");
		if($id){
			$data = Db::name("media_data")->where("id",$id)->find();
		}
		return view("",["data"=>$data]);
	}
	//添加编辑提交
	public function music_doaddupdate(){
		$id = input("post.id");
		$data["title"] = trim(input("post.title"));
		$data["desc"] = trim(input("post.desc"));
		$data["ordering"] = trim(input("post.ordering",0));
		$stamp = time();

		if(!$data["title"]){
			return msg(-1,"","标题不能为空");
		}
		if(!is_numeric($data["ordering"])){
			return msg(-1,"","排序请输入数字");
		}
		

		if($id){	//修改
			$data["updatetime"] = $stamp;
			$re = Db::name("media_data")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","编辑成功");
			}
		}else{
			//上传文件
			$file = request()->file();
			if($file){
				
				$filesize =  100 * 1024 * 1024;	//100M
				validate(['file'=>'fileSize:'.$filesize.'|fileExt:m4a,mp3'])->check($file);
				$savename = \think\facade\Filesystem::putFile( 'music', $file["file"]);
				$data["url"] = $savename;
			}
			
			$data["createtime"] = $stamp;
			$data["updatetime"] = $stamp;
			$data["type"] = 2;	//2表示音频
			$re2 = Db::name("media_data")->insert($data);
			if($re2){
				return msg(1,"","添加成功");
			}
		}
		return msg(-1,"","操作失败");
	}
	//删除
	public function music_del(){
		$id = input("post.id");
		if(!$id){
			return msg(-1,"","参数错误");
		}

		$url = Db::name("media_data")->where("id",$id)->value("url");
		trace("url:".$url);
		$path = app()->getRootPath()."z_mediadata/".$url;
		if(file_exists($path)){
			unlink($path);
			trace("已删除音频：".$path);
		}

		$re = Db::name("media_data")->where("id",$id)->delete();
		if($re){
			return msg(1,"","删除成功");
		}else{
			return msg(1,"","操作失败");
		}
	}
	//play
	public function play_music(){
		$url = app()->getRootPath()."z_mediadata/".input("get.url");
		// trace("url:".$url);
		if(file_exists($url)){
			header('Content-Type: audio/mpeg');
			header('Content-Disposition: inline; filename="' . basename($url) . '"');
			header('Content-Transfer-Encoding: binary');
			header('Content-Length: ' . filesize($url));
			header('Accept-Ranges: bytes');
			readfile($url);
			exit;
		}else{
			echo "not found.";
		}

	}
	//=====================================music end============================

	//====================================pic start=================
	public function pic_list(){
		return view();
	}
	
	//列表数据
	public function pic_list_data(){
		//前端h-ui框架datatable固定格式的参数
		$draw = input("get.draw",1);			//h-ui参数，请求次数
		$offset = input("get.start",0);			//索引
		$limit = input("get.length",10);		//查询数量，相当于每页显示数量

		$where["ba.type"] = 3;		//type:pic(3)
		$data_list = Db::name("media_data")
				->alias("ba")
				->where($where)
				->field(" ba.id,ba.title,ba.desc,ba.ordering,from_unixtime(ba.createtime,'%Y-%m-%d %H:%i:%s') as createtime,".
				"from_unixtime(ba.updatetime,'%Y-%m-%d %H:%i:%s') as updatetime,url")
				->order("ba.ordering","desc")
				->limit($offset,$limit)
				// ->fetchsql(true)
				->select();

		$count = Db::name("media_data")
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
	//添加编辑
	public function pic_addupdate(){
		$data = [];
		$id = input("get.id");
		if($id){
			$data = Db::name("media_data")->where("id",$id)->find();
		}
		return view("",["data"=>$data]);
	}
	//添加编辑提交
	public function pic_doaddupdate(){
		$id = input("post.id");
		$data["title"] = trim(input("post.title"));
		$data["desc"] = trim(input("post.desc"));
		$data["ordering"] = trim(input("post.ordering",0));
		$stamp = time();

		if(!$data["title"]){
			return msg(-1,"","标题不能为空");
		}
		if(!is_numeric($data["ordering"])){
			return msg(-1,"","排序请输入数字");
		}
		

		if($id){	//修改
			$data["updatetime"] = $stamp;
			$re = Db::name("media_data")->where("id",$id)->update($data);
			if($re){
				return msg(1,"","编辑成功");
			}
		}else{
			//上传文件
			$file = request()->file();
			if($file){
				
				$filesize =  100 * 1024 * 1024;	//10M
				validate(['file'=>'fileSize:'.$filesize.'|fileExt:jpg,png'])->check($file);
				$savename = \think\facade\Filesystem::putFile( 'pic', $file["file"]);
				$data["url"] = $savename;
			}
			
			$data["createtime"] = $stamp;
			$data["updatetime"] = $stamp;
			$data["type"] = 3;	//3表示图片
			$re2 = Db::name("media_data")->insert($data);
			if($re2){
				return msg(1,"","添加成功");
			}
		}
		return msg(-1,"","操作失败");
	}
	//删除
	public function pic_del(){
		$id = input("post.id");
		if(!$id){
			return msg(-1,"","参数错误");
		}

		$url = Db::name("media_data")->where("id",$id)->value("url");
		trace("url:".$url);
		$path = app()->getRootPath()."z_mediadata/".$url;
		if(file_exists($path)){
			unlink($path);
			trace("已删除图片：".$path);
		}

		$re = Db::name("media_data")->where("id",$id)->delete();
		if($re){
			return msg(1,"","删除成功");
		}else{
			return msg(1,"","操作失败");
		}
	}
	//play 
	public function play_pic(){
		$url = app()->getRootPath()."z_mediadata/".input("get.url");
		// trace("url:".$url);
		if(file_exists($url)){
			header("Content-Type:image/jpeg");
			readfile($url);
			exit;
		}else{
			echo "not found.";
		}

	}
	//=====================================video end============================
}


####  执行sql文件

建表脚本：

```php
<?php
    //执行sql脚本
	public function exe_sql(){
		$sql_file = app()->getRootPath()."/sqlscripts/xxx.sql";	//sql file path
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
```

#### 执行插入sql

```php
<?php
    function find_sql(){
    	$timestamp = time();
		$sql2 = "insert into `xxx_table_data` (`title`,`desc`,`createtime`,`updatetime`) values('test','test...',$timestamp,$timestamp)";

		try{
			Db::execute($sql2);
			echo "sql execute success.";
		}catch(\Exception $e){
			echo "sql execute error:".$e->getMessage();
		}
	}
```

#### 文件上传error问题

```sh
#说明
$_FILES先获取表单名称为myfile的input上传的文件数据，然后再访问name、type、size、error等数据。
$_FILES["myfile"]["error"]用来处理文件没有正常上传的情况，例如超过限定上传的文件大小。
$_FILES["myfile"]["error"]=0，表示文件正常上传。
$_FILES["myfile"]["error"]>0表示文件没有正常上传。 
	=1		#上传文件超过服务器限定的值，比如超过服务器空间大小。
	=2 		#超过浏览器限定上传的值 
	=3		#文件只有部分被上传
	=4		#没有文件本上传。
$_FILES[“myfile”][“error”]还可以为5、6、7、8，这里不做深究，只需知道其大于0时就意味这文件上传出错即可。

#服务器上传限制解决：
修改php.ini如下参数:
	upload_max_filesize = 100M
	post_max_size = 100M
	
```

#### 上传代码

```php
//上传目录在config/filesystem.php配置
//上传文件
$file = request()->file();
//trace("eeeee");		//日志
if($file){
    $filesize =  100 * 1024 * 1024;	//100M
    validate(['file'=>'fileSize:'.$filesize.'|fileExt:mp4,avi,rmvb'])->check($file);
    $savename = \think\facade\Filesystem::putFile( 'video', $file["file"]);		//video子目录
    $data["video_url"] = $savename;
}
```


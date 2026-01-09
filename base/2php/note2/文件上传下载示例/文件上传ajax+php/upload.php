    <?php

    //上传报告
    public function other_report_upload(){
        $result = array("error"=>1,"content"=>"系统错误");

        $month_str = date("Ym");    

        $file_data = $_FILES['file_data'];          //获取上传的报告文件
        $tmp_file_name = $file_data["name"];        //上传文件的文件名
        $file_size = $file_data["size"] / 1024;       //上传文件的大小:kb
        $tmp_file_path = $file_data["tmp_name"];       //上传文件临时路径
        
        //=====生成文件名 start=====
        $tmp_arr = explode(".",$tmp_file_name);     //上传的文件名处理
        $file_sufix = $tmp_arr[count($tmp_arr)-1];      //文件后缀
        $file_name = time().strtolower(hy_rand(6)).".".$file_sufix;     //新文件名：时间戳+6位随机数+文件后缀
        //=====生成文件名 end=====
        
        //=====文件格式校验 start=====
        $tmp_format = ['pdf'];                //文件格式
        // debuglog("name:".$tmp_file_name,1);
        if(!in_array(strtolower($file_sufix),$tmp_format)){
            $result["content"] = "文件格式错误";
            $this->showMsg($result);
        }
        //=====文件格式校验 end=====
        
        //=====文件大小校验 end=====
        if($file_size > 5 * 1024){
            $result["content"] = "文件大小不能超过5M";
            $this->showMsg($result);
        }
        //=====文件大小校验 end=====

        $dir_path = ROOT_PATH."Uploads/docx/".$month_str;      //保存目录
        if(!file_exists($dir_path)){     //目录不存在，创建目录  （若不能创建，则服务器无操作权限）
            mkdir($dir_path,0777,true);
        }

        $file_path = $dir_path."/".$file_name;          //文件路径
        $re = move_uploaded_file($tmp_file_path, $file_path);        //移动文件
        if($re){
            $result["error"] = 0;
            $result["content"] = "上传成功";
            $file_save_path = "/Uploads/docx/".$month_str."/".$file_name;       //该路径用于返回页面
            $result["file_path"] = $file_save_path;
        }
        
        $this->showMsg($result);

    }



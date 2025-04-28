<?php
// 应用公共文件

//返回方法
//code：1正常，-1异常
function msg($code,$data,$msg){
	return json(["code"=>$code,"data"=>$data,"msg"=>$msg]);
}
//email regex
function reg_email($s){
	$reg = "/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/";
	if(preg_match($reg,$s)){
		return true;
	}else{
		return false;
	}
}
//error
function error_page(){
	return view("../huicommon/error");
}

<?php
namespace app\admin\validate;
use think\Validate;

//后台管理员验证器
class AdminValidate extends Validate
{
    protected $rule = [
		'admin_name'=>['require','regex'=>'/[\w]{1,25}/'],
		'password'=>['require','regex'=>'/[a-zA-Z0-9]{6,16}/'],
	];
    
    protected $message = [
        'admin_name.require' => '用户名必须',
        'admin_name.regex'=> '用户名字母数字下划线，不能超过25个字符',
        'password.require' => '密码必须',
        'password.regex' => '密码6-16位字母数字',
    ];
    
}
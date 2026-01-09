<?php

namespace app\p\controller;

use app\BaseController;
use think\Request;
use think\facade\Db;
use think\facade\View;

class Index extends BaseController{
    public function index(){
    	echo "index";
    	return; 

        // return '<style>*{ padding: 0; margin: 0; }</style><iframe src="https://www.thinkphp.cn/welcome?version=' . \think\facade\App::version() . '" width="100%" height="100%" frameborder="0" scrolling="auto"></iframe>';
    }


    public function test(){

        echo "wefwefwef";
       

    }



    //一些
    public function some(Request $request){

        $arr = ["id"=>3,"name"=>"sdfwefwefsdfew"];
        // return json($arr);

        // dump($request);

        halt("调试...");
        // halt($request);
        

        // input("get.id");     //助手函数
        
        // session("x");       //session 默认关闭
        
         // return download(root_path().'image.jpg', 'my.jpg');    //下载
         
         // return view("index/test");      //需安装tihnk-view扩展
    }


    //route/app.php定义了路由规则，导致该路由 http://localhostindex/hello 失效
    //正确访问方式：http://localhost/hello/xxx
    public function hello($name = 'ThinkPHP8'){
        return 'hello,' . $name;
    }

}

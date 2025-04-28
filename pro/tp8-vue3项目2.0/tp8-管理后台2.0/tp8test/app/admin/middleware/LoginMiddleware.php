<?php
namespace app\admin\middleware;

//登录中间件
class LoginMiddleware{
	public function handle($request, \Closure $next){
		$admin_id = session("admin_id");
		if(!$admin_id){
			if($request->isAjax()){
				return msg(-1,"","未登录");
			}else{
				return redirect("/admin/base/login");
			}
		}
		
		return $next($request);
	}
}
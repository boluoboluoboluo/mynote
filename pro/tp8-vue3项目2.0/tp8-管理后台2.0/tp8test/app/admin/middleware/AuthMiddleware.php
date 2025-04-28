<?php
namespace app\admin\middleware;

use think\facade\Db;
use app\admin\service\SysService;

//权限中间件
class AuthMiddleware{
	public function handle($request, \Closure $next){

		$param["auth_url"] = $request->baseUrl();
		$param["admin_id"] = session("admin_id");
		$param["admin_role_action"] = session("admin_role_action");
		$sysService = new SysService();
		$re = $sysService->auth_url_check($param);

		if(!$re){
			return msg(-1,"","对不起，您没有权限");
		}
		
		return $next($request);
	}
}
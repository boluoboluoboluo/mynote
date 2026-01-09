import service from "./service";

//登录
export function api_act_login(params:any){
	let url = "/test/apiTest/act_login"
	return service.post(url,params)
}

export function api_media_data(param:any,id?:any){
	let url = "/api/media/" + param
	if(id){
		url += "?id="+id
	}
	
	return service.post(url,param)
}
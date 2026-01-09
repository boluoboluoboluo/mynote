import { Md5 } from "ts-md5"


//判断是移动端还是 pc 端 ，true 表示是移动端，false 表示是 pc 端
export function isMobileOrPc() {
	if (/Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)) {
	  return true
	} else {
	  return false
	}
}

//登录检查
export function login_check(){
	if(localStorage.getItem("token")){
		return true
	}else{
		return false
	}
}

//md5加密
export function md5(str:string){
	const md5:any = new Md5()
	md5.appendAsciiStr(str)
	const restr = md5.end()
	return restr
}
//时间戳(s)转日期
export function timestampToDate(stamp:any){
	const date = new Date(stamp*1000);
	const year = date.getFullYear();
	const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，所以加1，并用0填充
	const day = String(date.getDate()).padStart(2, '0'); // 用0填充
	const hours = String(date.getHours()).padStart(2, '0'); // 用0填充
	const minutes = String(date.getMinutes()).padStart(2, '0'); // 用0填充
	return `${year}-${month}-${day} ${hours}:${minutes}`;
}


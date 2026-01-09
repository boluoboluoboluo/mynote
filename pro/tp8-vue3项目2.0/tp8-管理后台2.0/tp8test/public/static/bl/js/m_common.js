//权限验证
function m_auth_check(url){
	//================== ajax提前请求，用于权限验证时提示权限不足做弹窗优化(避免打开选项卡) start ================
	let f_pass = 0;
	$.ajax({
		type : 'post',
		dataType : 'json',
		url : "/admin/sys/auth_check",
		data : {auth_url:url},
		async: false,
		success : function(res){
			if(res.code == 1){
				f_pass = 1;
			}else{
				f_pass = 0;
				layer.msg(res.msg,{icon:2,time:1500});
			}
		},
		error : function(){
			// layer.msg('系统出错',{icon:2,time:1500});
		}
	});
	if(f_pass){
		return true;
	}else{
		return false;
	}
	//================== ajax提前请求，用于权限验证时提示权限不足做弹窗优化(避免打开选项卡) end ================
}

function m_Hui_admin_tab(obj){
	href = $(obj).attr('data-href');
	if(m_auth_check(href)){
		Hui_admin_tab(obj);
	}
}

function m_layer_show(title,url,w,h){
	href = url;
	if(m_auth_check(href)){
		layer_show(title,url,w,h);
	}
}
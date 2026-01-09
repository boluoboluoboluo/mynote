##### H-ui框架弹窗优化

说明：关于点击链接打开页面或者请求ajax方法权限不足时弹窗不统一的优化

1. 在H-ui.admin.js的选项卡导航代码注释`Hui_admin_tab`

   ```js
   /*选项卡导航*/
   $(".Hui-aside").on("click",".menu_dropdown a",function(){
       // Hui_admin_tab(this);		//注释此行
       $(".Hui-aside").find(".menu_dropdown dl dd ul li").removeClass("current");
       $(this).parent().addClass("current");
   });
   ```

   主页文件`index.html`菜单项添加`class="sub_menu"`自定义菜单点击事件：

   ```html
   <li><a class="sub_menu" data-href="/admin/sys/tab_list" data-title="菜单管理" href="javascript:void(0)">菜单管理</a></li>
   
   <script type="text/javascript">
   $(function(){
   	$(".sub_menu").click(function(){
   		m_Hui_admin_tab(this);		//此处用重写的方法覆盖Hui_admin_tab方法
   	});
   });
   ```

2. 新增`m_common.js`文件，代码如下：

   ```js
   //权限验证
   function m_auth_check(url){
   	//==== ajax提前请求，用于权限验证时提示权限不足做弹窗优化(避免打开选项卡) start =====
   	let f_pass = 0;
   	$.ajax({
   		type : 'post',
   		dataType : 'json',
   		url : "/admin/sys/auth_check",	//此为后端校验方法，自行编写
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
   	//======= ajax提前请求，用于权限验证时提示权限不足做弹窗优化(避免打开选项卡) end ======
   }
   //取代Hui_admin_tab方法
   function m_Hui_admin_tab(obj){
   	href = $(obj).attr('data-href');
   	if(m_auth_check(href)){
   		Hui_admin_tab(obj);
   	}
   }
   //取代layer_show方法
   function m_layer_show(title,url,w,h){
   	href = url;
   	if(m_auth_check(href)){
   		layer_show(title,url,w,h);
   	}
   }
   ```

3. 系统中打开页面需要做权限验证的地方，用`m_Hui_admin_tab`取代`Hui_admin_tab`，用`m_layer_show`取代`layer_show`

   注意：此为弹窗优化做的专门校验，通过组件访问具体的后端方法时仍需二次校验




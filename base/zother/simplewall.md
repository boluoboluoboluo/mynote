```sh
替代windos防火墙,默认阻止全部连接,只挡出站,不挡入站,它启动后,会自动切断未批准的连接

#安装
github搜索simplewall

#使用
运行程序,点击 "开启过滤" 即可
#允许访问			
点 "程序" 放行需要出站的程序即可

#取消弹窗通知		  
点 图标 "启用丢弃数据包通知"

#设为开机启动(设置里面)
#安装为windows服务(略)

#允许 dns
#允许 icmp* icmp6*
#添加规则允许 ssh
```

```sh
#关于时间同步，怎么处理?	(手动同步吧)
	新建规则：Filters → 新建 → 程序 = svchost.exe
	远程地址 = time.windows.com 或 time.nist.gov
	端口 = 123
	协议 = UDP → Allow

#关于无线网
	无线网主要依赖mac层,simplewall主要限制ip层,所以不影响wifi的连接
	但是wifi的前提需要dhcp和dns,所以要先配置好dhcp和dns能出站才行	#或设置静态ip
```


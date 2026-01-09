

思路：

```
1.在kali使用metasploit对正常的工具putty.ext生成后门程序putty_backdoor.exe
2.使用upx免杀工具对putty_backdoor.exe进行免杀升级
3.puttybackdoor.exe放入靶机
4.kali监听
```



冰河木马案例

```
1.攻击机运行冰河木马客户端g_client.exe
2.修改本地服务器配置，配置在肉鸡的安装路径，进程名称，端口xxxx，访问口令，自动删除，关联txt自动复活等
3.生成g_server.exe，即木马，将木马拷入靶机
4.靶机运行木马
5.攻击机运行g_client.exe,扫描网段，若提示ok，输入口令即可以连接
```


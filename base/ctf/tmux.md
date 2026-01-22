终端复用器,可通过复制的方式,创建多个终端,即使当前会话关闭退出,它也会再后台执行

ssh会话断开,它也会存在,只要服务器在运行

安装命令: `sudo apt install tmux `

```sh
tmux	#创建并进入一个会话,名字默认数字
tmux new -s <会话名>	#新建会话
tmux detach		#后台运行,或者Ctrl + b,然后松开前者,再按d
tmux ls			#查看所有会话
tmux attach -t <会话名>	#恢复/进入会话
tmux kill-session -t <会话名>	#关闭/杀死会话 或在当前会话输入exit


#分屏操作	(一个会话分多个屏)
左右平分屏幕：Ctrl + b 然后再按 %		#按完松开ctrl和b,然后按%
上下平分屏幕：Ctrl + b 然后再按 "
切换光标所在的窗口：Ctrl + b 然后再按 方向键
全屏/取消全屏当前小窗口：Ctrl + b 然后再按 z
调整窗口大小：按住 Ctrl + b 的同时按 方向键
关闭当前小窗口：输入 exit 或 Ctrl + b 然后按 x

```


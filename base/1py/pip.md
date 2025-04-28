#### pip

```sh
#pip更新
python -m pip install --upgrade pip

#查看配置
pip config list

#查看安装的包
pip list

#查看安装某个包，如未安装则无信息
pip show package_name

#设置全局源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

#恢复默认软件包源
pip config unset global.index-url

#查看某个包可用版本
pip install packge_name==

#安装指定版本
pip install pyside6==6.4.1

#从某个源安装pyside6包
pip install --index-url=https://pypi.tuna.tsinghua.edu.cn/simple pyside6 

#卸载
pip uninstall packge_name
```

#### 常见源

```
官方源：https://pypi.python.org/simple

阿里云镜像源：http://mirrors.aliyun.com/pypi/simple/
 
清华大学镜像源：https://pypi.tuna.tsinghua.edu.cn/simple/
 
中国科技大学镜像源：http://pypi.mirrors.ustc.edu.cn/simple/
 
华中理工大学镜像源：http://pypi.hustunique.com/
 
山东理工大学镜像源：http://pypi.sdutlinux.org/
 
豆瓣镜像源：https://pypi.douban.com/simple/
```


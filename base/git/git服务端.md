#### 说明

```sh
# git 是去中心化的,没有服务端和客户端之分
# 只要一个安装了 Git 的服务器开启了 SSH 服务，它就天然具备了“服务端”的功能。

```

#### 安装

```sh
# 安装
sudo apt install git
```

#### 创建 Git 裸仓库

```sh
 # 裸仓库没有工作区（看不到直接的代码文件），只保存版本历史，非常适合作为服务端中转

# 创建统一的管理目录
sudo mkdir -p /z_data/git

# 初始化一个名为 project.git 的裸仓库
sudo git init --bare /z_data/git/project.git
```

#### 创建 git 用户

```sh
# 为了服务器安全，不建议直接用 root 用户存取代码。我们创建一个专门的 git 用户来管理：

# 创建 git 用户
# -s /usr/bin/git-shell 可以让这个用户只能用来传输 Git 代码，禁止通过 SSH 登录服务器搞破坏，非常安全。
sudo useradd -m -s /usr/bin/git-shell git

# 将仓库的所有权交个 git 用户
sudo chown -R git:git /z_data/git/project.git
```

#### 配置 SSH 密钥

```sh
# 配置ssh密钥,用于本地与服务端通信

# 本地 通过ssh-keygen 生成密钥,将公钥 id_rsa.pub 的内容写入服务器:

====================
# 写入步骤:
# 登录服务器,切换到 git 用户
sudo su - git

# 创建并进入 .ssh 目录
mkdir -p ~/.ssh && chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys

# 用 nano 或 vi 打开文件，把本地公钥粘进去并保存
nano ~/.ssh/authorized_keys


```

#### 本地推送

```sh
# 本地初始化git仓库,示例:
git init
git add .
git commit -m "feat: 首次完整提交项目代码"

# 关联你的远程服务器
# 命令格式：git remote add <名字> ssh://<用户名>@<服务器IP>:<SSH端口>/<仓库绝对路径>
# 如果你的服务器修改了默认的 SSH 端口（比如变成了 2222），命令里要写成 ssh://git@IP:2222/...
git remote add prod ssh://git@你的服务器公网IP:/z_data/git/project.git

# 推送
git push -u prod main

```

#### 项目自动拉取(可选)

```sh
# 因为 project.git 是裸仓,不显示具体的文件
# 可通过 Git Hooks 实现git代码自动同步 checkout 到项目目录

# Git Hooks :
Git 内置了一个叫 post-receive的钩子脚本。它的逻辑是：一旦服务器的裸仓库（project.git）成功接收到本地推过来的代码，就立刻自动触发一个脚本，把代码“检出（Checkout）”到你的项目实际运行目录。
=========================
# 配置 git hooks:

# 1.切换git账户
	sudo su - git
# 2.创建钩子文件
	nano /z_data/git/project.git/hooks/post-receive
	-------------
	# 内容:
    #!/bin/bash
    # 定义代码实际运行目录
    DEPLOY_DIR="/z_data/wkspace/python/pyv_blobvideo/blobvideo"

    # 强制将代码同步到运行目录（--work-tree 指定目标，checkout -f 强制覆盖）
    git --work-tree=$DEPLOY_DIR --git-dir=/z_data/git/project.git checkout -f main

    # (可选) 如果你用了虚拟环境，可以顺便让它自动安装新库并重启服务
    # cd $DEPLOY_DIR
    # source env/bin/activate && pip install -r requirements.txt
    # sudo systemctl restart my_flask_app
	--------------

# 3.保存退出，并赋予该脚本执行权限
	chmod +x /z_data/git/project.git/hooks/post-receive


# 效果:
以后你在本地电脑只要执行 git push prod main，代码会在 1 秒内自动同步到你的 服务器项目运行目录中。
```

#### 多用户连接及权限(可选)

```sh
# 多个用户需要连接的场景:
公钥写入 authorized_keys:
每行一个公钥即可		

# 公钥后可添加对应用户的名字,空格隔开,作为注释,示例:
ssh-rsa AAAAB3NzaC1yc2E...[一长串代码]...== zhangsan@macbook
ssh-ed25519 AAAAC3NzaC1lZDI...[一长串代码]...== lisi@windows_pc
ssh-rsa AAAAB3NzaC1yc2E...[一长串代码]...== wangwu@company_laptop

# 公钥的内容格式,由三部分组成，用空格隔开：
[加密算法] [超长密钥字符串] [注释]
```

```sh
# 权限: 通过git的权限管理工具 Gitolite 配置

sudo apt install gitolite3	#安装

# 步骤
1.初始化, 需指定管理员
	# 切换到你的 git 用户
	sudo su - git
	# 使用你的管理员公钥初始化 Gitolite
	gitolite setup -pk /tmp/admin.pub		# 确保该公钥之前未被添加到 authorized_keys
	# 此命令后,~/.ssh/authorized_keys 里面会自动写入管理员公钥数据
	# 家目录下会自动生成一个名为 gitolite-admin.git 的管理仓库
2.管理员本地拉取管理仓库
	git clone git@服务器IP:gitolite-admin
	cd gitolite-admin
	# 里面有: 
		keydir/ 			#文件夹（存放用户公钥的地方）
		conf/gitolite.conf 	#文件（配置文件，已经自动新建好了）
3.将团队成员公钥，直接放入本地的 keydir/ 目录中
	keydir/zhangsan.pub
	keydir/lisi.pub
	...
	# 确保这些公钥之前不在 authorized_keys 中
4.配置权限,修改 conf/gitolite.conf 文件
	# 内容示例:
	--------------------
	# 
	repo gitolite-admin
   		RW+     =   admin
	# my-repo 仓库权限:
	repo my-repo
    	RW+     =   lisi
    	R       =   zhangsan
    --------------------
	# RW+ 代表有读、写、删除分支的最高权限
	# R 代表只有只读（clone/pull）权限，不能推送
5.提交到管理仓库即可
	git add .
	git commit -m "添加了张三和李四的公钥，并配置了 my-repo 的权限"
	git push origin master



# 说明:
提交后,服务器端的 Gitolite 脚本会被触发,读取 keydir/ 下的内容,写入 authorized_keys 中



```


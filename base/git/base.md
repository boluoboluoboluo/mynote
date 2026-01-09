

### 初始化

```sh 
#空目标目录下
git init		#初始化git仓库
```

### 拉取远程分支

```sh
git remote add origin git@xx.com:test/test.git		#添加远程仓库

git fetch	#获取远程最新
git merge	#合并到本地

#相当于git fetch 和 git merge
git pull origin master	#拉取main分支
```

### 克隆

```sh
git clone url			#克隆一个远程仓库
```

### 提交

```sh
git add .				#添加文件到暂存区
git commit -am "注释"		#提交代码到本地仓库	（需要双引号）
git push				#推送代码到远程仓库
```

### 日志

```sh
git log -3				#查看最近3次提交历史
git log --stat -2		#查看最近的2次提交，显示文件名
git log --pretty=oneline
git log origin/分支名 -3		#查看远程仓库3次提交历史
git reflog 				#查看提交记录

git show --raw			#查看最近的一次提交
git show 				#查看本次提交详情
git show <commitid>		#查看某次提交详情 commitid为版本id前7位
```

### 查看远程仓库

```sh
git remote -v				#查看远程仓库地址
git remote show origin		#查看远程的完整详细信息

# 格式:https://github.com/username/repo.git
git remote add origin git@xx.com:test/test.git		#添加远程仓库
git push -u origin master		#推送至远程仓库，（使用了u参数，下次可直接用git push推送
```

### 查看历史

```sh
#切换到具体的某个提交,用于查看当时的版本和文件内容,状态等
#此时head悬空,看完了记得切换回来
git checkout commit-id		
git checkout master		#切回主分支
```

### 回退

```sh
git restore	[file]	#恢复
git restore --stage [file]	#恢复在暂存区的改动

git log			#查看版本号
git reset --hard d8fc1e10c9exxxxxxxxxxxxxx	#恢复到指定版本 hard后面为版本id
git reset --hard x	#回退到某个本地版本,x为git log中出现的hash值的前七位。hard表示丢弃工作区和暂存区改动
git push -f origin master			#强制push
```



### 补充

```sh
git diff		#工作区和暂存区差异
git diff branch1 branch2 	#2个分支对比
git diff commit1 commit2			#2次提交记录对比 commitid为版本id前7位
git diff commit1 commit2 --/xx/xx.xx			#2次提交的某文件对比

git clean -nf		#如果莫名生成Untracked files，使用此命令查看
git clean -f			#删除untracked files 
git clean -fd		#删除untracked files (连同untracked目录)

git rm <file>	#删除文件

git reset head~		#撤销上一次的commit和add
```

### 分支

```sh
git branch 			#查看本地所有分支
git branch -r		#查看远程所有分支
git branch <branchname>		#新建分支
git branch -d <branchname>	#删除本地分支

git branch -M main		#分支重命名为 main

git checkout <branchname>	#切换分支

#以下命令将本地的 master 分支推送到 origin 主机的 master 分支。
git push origin master



git log branchname		#查看分支日志
```

### 合并

```sh
#合并开发分支 到当前分支
git merge branchname

#关于冲突
Git 冲突的真正标准不是“改了同一个文件”，而是“从共同祖先开始，两边对文件的同一块地方做了互斥/矛盾的修改”。

#发生冲突:
a.修改了文件的同个地方
b.一方修改,一方删除文件

#不冲突:
a.一方没动,一方删		#最后删
b.两方都删			#删

#处理完冲突后
#使用: git add. | git commit 提交
#或 git merge --continue
```



### 导出

```sh
git archive --format zip --output "./output.zip" master -0
git archive -v --format=zip v0.1 > v0.1.zip		#将tag为v0.1的版本导出
git archive -o ../version-1.0.0.tar 9976c24		#导出指定提交记录
```

```sh
#导出日志清单
git log --date=iso --pretty=format:’"%h","%an","%ad","%s"’ >> c:/gitcommit.txt
#导出日志清单 根据日期
git log --date=iso --pretty=format:’"%h","%an","%ad","%s"’ --since="2023-07-01" --until="2023-12-31" >> c:/gitcommit.txt
#%d表示显示ref，分支、tag 名称，带括号
git log --date=iso --pretty=format:’"%h","%an","%ad","%s","%d"’ >> c:/gitcommit.txt	
#只导出带标签的日志
git log --no-walk --tags --date=iso --pretty=format:’"%h","%an","%ad","%s","%d"’ >> c:/gitcommit.txt
```

### tag

```sh
git tag -a v1.0 -m "tag test.."		#当前提交打标签
git tag -a v1.0 -m "tag test.."	 9976c24	#给指定提交打标签
git tag 	#查看所有tag
git show v1.0	#查看某个tag
git tag -d v1.0		#删除tag
git push origin <Tag 名字> 	#推送单个Tag
git push origin --tags		#推送所有tag

git log --no-walk --tags	#显示标签的log
git log --no-walk --tags --oneline	#单行显示
git log --no-walk --tags=*some_string*	#字符串匹配
```

### 邮箱

```sh
#查看当前仓库用户名和邮箱 在git项目目录下:
git config user.name
git config user.email

#配置当前仓库用户名和邮箱 在git项目目录下:
git config user.name "xxx"
git config user.email "xx@xxx.com"

#配置全局用户名和邮箱
git config --global user.name
git config --global user.email

```

### ignore

```sh
#排除文件或目录可以通过.gitignore文件来实现。.gitignore文件位于Git仓库的根目录下，
#其中列出的文件或模式会被Git忽略，不会被纳入版本控制。

#.gitignore文件使用简单的模式匹配规则来排除文件或目录：
1.空行或者以#开头的行会被忽略。
2.可以使用标准的shell glob模式匹配。
3.以/结尾的模式表示目录。
4.以!开头的模式表示例外规则，即不排除该模式匹配的文件或目录。
5.使用**可以匹配任意中间目录。
```

**`.gitignore`文件示例：** 

```sh
# 忽略所有 .log 文件
*.log
# 忽略所有 .tmp 文件，但保留 todo.tmp
*.tmp
!todo.tmp
# 忽略所有在 build/ 目录下的文件
build/
# 忽略所有在 doc/ 目录及其子目录下的文件
doc/*
# 忽略所有在 .gitignore 文件当前目录下的 .env 文件
.env
# 忽略所有在 test/ 目录下的 .txt 文件
test/**/*.txt
```

在创建或更新`.gitignore`后，需要运行`git add`命令来重新加入不被忽略的文件，这样才能被Git跟踪。

如果想要清除已经缓存的文件（即使它们被`.gitignore`忽略），可以使用以下命令：

```sh
git rm -r --cached .
git add .
```








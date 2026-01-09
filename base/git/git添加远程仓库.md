
### github添加远程仓库

要在GitHub上添加远程仓库，首先确保你已经安装了Git。然后，在命令行中使用以下步骤：

1. 打开终端（在Windows上为Git Bash，在Mac或Linux上为终端）。
2. 切换到你的本地项目目录。

```bash
cd /path/to/your/project
```

1. 初始化本地仓库（如果你还没有一个本地仓库）。

```bash
git init
```

1. 添加文件到本地仓库。

```bash
git add .
```

1. 提交你的更改到本地仓库。

```bash
git commit -m "Initial commit"
```

1. 在GitHub上创建一个新的远程仓库，不要初始化任何文件。
2. 在终端中，将远程仓库添加到你的本地配置中。将`<URL>`替换为你的GitHub仓库的URL。

```bash
git remote add origin <URL>
```

1. 推送你的本地更改到GitHub远程仓库。

```bash
git push -u origin master
```

这里的`<URL>`是你的GitHub仓库的URL，通常看起来像这样：`https://github.com/username/repository.git`。`master`是你想要推送的分支名称，如果你使用的是主分支，就用`master`，如果使用的是其他分支，比如`main`，就用`main`。



### github配置sshkey

```sh
#将生成的sshkey 如~/.ssh/id_rsa.pub 内容复制
#在github项目目录->settings->deploy keys
#新增(add key)
#注意勾选 write access
```


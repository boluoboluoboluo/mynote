

#### 保留最新版

```sh
git checkout --orphan latest_branch		#创建并切换到孤儿分支 latest_branch

git add -A		#添加所有文件
git commit -m "清理历史，重新开始"	#提交

git branch -D main	#删除旧分支 (main为您的主分支名)
git branch -m main	#将当前分支命名为main
git push -f origin main	#强制推送远程仓库

#===========
#gc
# 1. 彻底删除引用记录
git reflog expire --expire=now --all
# 2. 彻底清理并压缩数据库
git gc --prune=now --aggressive

# =====================

#验证：
#检查历史是否缩短：
git log --oneline
#查看仓库体积变化：
git count-objects -vH
```

- **托管平台（GitHub/GitLab）：** 一旦你完成了 `--force` 推送，那些不再被任何分支引用的旧对象（孤儿对象）会变成“不可达”。GitHub 等平台通常会**在 24 小时内或定期**自动运行垃圾回收程序。

- **手动触发（如果你是私有服务器）：** 如果你是通过 SSH 自己搭建的 Git 服务器，你需要登录到服务器的仓库目录下手动运行：

  ```sh
  git gc --prune=now --aggressive
  ```

  


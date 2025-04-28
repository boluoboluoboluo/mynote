```sh
#慎重操作！

#使用 git rebase 重置根提交
git rebase -i --root a1b2c3d		#a1b2c3d:提交的哈希id
#(在编辑器中保留目标提交及之后的记录，删除之前的提交行。)

#如果变基过程出现冲突，解决后继续
git rebase --continue

#运行 git gc 清理本地仓库 (残留对象)
git reflog expire --expire=now --all
git gc --prune=now

#本地清理后，覆盖远程历史：（强制推送更改到远程仓库）
git push origin main --force


# =====================

#验证：
#检查历史是否缩短：
git log --oneline
#查看仓库体积变化：
git count-objects -vH
```




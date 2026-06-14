

```sh

# 说明:
-- 软官方的命令行数据恢复工具 Windows File Recovery（WinFR）
-- 免费,命令行操作

# 下载地址: 
https://apps.microsoft.com/detail/9n26s50ln705?hl=zh-CN&gl=CN

# 注意:
准备另1个盘,恢复的文件不能保存原盘

# 操作:
1.右键 管理员身份 运行工具
2.命令语法:
winfr 来源盘符: 目标盘符: /恢复模式 /n 过滤条件
	# 参数:
	# 恢复模式:
	/regular	#（常规模式）：适用于 最近刚删除 且磁盘格式为 NTFS 的情况。
	/extensive	#（广泛模式）：适用于 删除很久、磁盘被格式化 或非 NTFS（如 U 盘/SD 卡的 FAT32、exFAT）的情况	
	
# 示例:
	# 场景1: 把 C 盘中刚删掉的某个特定文件恢复到 E 盘
	winfr C: E: /regular /n \Users\您的用户名\Documents\重要报告.docx
	# 场景2: 把 C 盘中刚删掉的所有 Word 和 PDF 文件恢复到 E 盘
	winfr C: E: /regular /n *.docx /n *.pdf
	# 场景3: 把 D 盘中误删的某个特定文件夹恢复到 E 盘（适合大批量）
	winfr D: E: /regular /n \照片\2026年旅游\
	# 场景4: 深度搜索 D 盘里文件名包含“发票”的所有文件（不限格式）
	winfr D: E: /extensive /n *发票*
	# 场景5: 从 U 盘（假设是 G 盘）深度恢复所有的 JPEG 图片到 E 盘
	winfr G: E: /extensive /n *.jpg
```


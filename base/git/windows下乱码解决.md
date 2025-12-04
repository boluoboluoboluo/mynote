### win下git log 中文乱码解决
```sh
#设置环境变量：
set LESSCHARSET=UTF8
set LANG=zh_CN.UTF-8

# 当显示内容是中文文件名时文件名变成了八进制序列
# 设置Git不转义非ASCII字符
git config --global core.quotepath false

#git bash不显示中文
git config --global i18n.logOutputEncoding utf8
git config --global i18n.commitEncoding utf8
git config --global gui.encoding utf-8
git config --global i18n.statusEncoding utf8
```


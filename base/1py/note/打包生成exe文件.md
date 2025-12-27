#### python 3.7

+ 安装pywin32，2个命令：

  ```
  pip install pywin32
  pip install pyinstaller
  ```

+ 打包命令：

  ```
  pyinstaller -F -w -i manage.ico app.py
  ```

  说明：

  -F  ：打包为单文件

  -w ：Windows程序，不显示命令行窗口

  -i   ：程序图标

  app.py ：要打包的文件



#### python 3.14

```sh
pip install pyinstaller	#安装
```

```sh
# 基本打包（会生成一个文件夹）
pyinstaller your_script.py

# 打包成单个exe文件
pyinstaller --onefile your_script.py

# 打包时隐藏控制台窗口（适合GUI程序）
pyinstaller --onefile --windowed your_script.py

# 指定图标
pyinstaller --onefile --icon=your_icon.ico your_script.py

# 添加数据文件
pyinstaller --add-data "data/*;data/" your_script.py
```


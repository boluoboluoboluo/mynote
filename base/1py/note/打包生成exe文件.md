#### windows下打包生成exe

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


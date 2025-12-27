

#### 混淆

```sh
pip install pyarmor		#安装
```

```sh
#将 src/ 目录下的所有 Python 文件混淆到 dist/ 目录，并在 2025年12月31日过期。
pyarmor gen --expired "2025-12-31" -r -O dist src/

#绑定硬件（如 MAC 地址）：
pyarmor gen --bind-mac XX:XX:XX:XX:XX:XX your_script.py
```



#### 混淆+打包

```sh
pip install pyinstaller		#安装
```

```sh
#自动加密+用PyInstaller打包成单个exe文件
#自动处理依赖
#打包命令:
pyarmor gen --pack onefile -e "2025-12-31" your_script.py

-e "YYYY-MM-DD"：设置具体过期日期（过期后运行报错）。
-e ".30"：从当前日期起 30 天后过期（前面加 . 表示检查本地时间，不联网验证）。
-e "30"：从当前日期起 30 天后过期（默认可能联网验证时间）。

#其他 PyInstaller 选项（如 --windowed、--icon=icon.ico）可以通过配置添加：
#先运行：pyarmor cfg pack:pyi_options = " --windowed --icon=app.ico"
#然后再运行上面的打包命令。

```


 ### 日志logging模块分割多进程报错问题

问题：日志logging模块，打印日志报错：**PermissionError: [WinError 32] 另一个程序正在使用此文件，进程无法访问**

解决办法：
```sh
#使用另一个模块：
pip install concurrent_log_handler
```

py文件：

```python
from concurrent_log_handler import ConcurrentRotatingFileHandler

handler = ConcurrentRotatingFileHandler(logpath,"a",512*1024,30,encoding="UTF-8",delay=False)
```


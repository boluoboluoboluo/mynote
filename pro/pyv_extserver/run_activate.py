import os
import sys
import subprocess

# 激活虚拟环境
def activate():
    # 获取当前目录的绝对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # 动态拼接不同系统的环境变量和激活命令
    if sys.platform == "win32":
        # Windows 路径与命令
        activate_path = os.path.join(base_dir, "env", "Scripts","activate.bat")
        print("正在 Windows 环境下激活虚拟环境...")
        subprocess.run(["cmd", "/k", activate_path])
    else:
        # Linux / macOS 路径与命令
        activate_path = os.path.join(base_dir, "env", "bin","activate")
        print("正在 Linux 环境下激活虚拟环境...")
        # 启动一个新的 bash 并加载虚拟环境
        subprocess.run(["bash", "--rcfile", activate_path])
# 主入口
if __name__ == "__main__":
    activate()

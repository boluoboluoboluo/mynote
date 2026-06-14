import os
import sys
import subprocess

PRO_NAME = "extserver2"      #项目目录名
APP_NAME = "app.py"         #项目入口文件名
COMMAND = "uvicorn app:app --host 127.0.0.1 --port 8000"    #运行命令
base_dir = os.path.abspath(os.path.dirname(__file__))
app_path = os.path.join(base_dir, PRO_NAME, APP_NAME)
os.chdir(fr"{base_dir}/{PRO_NAME}")

# 运行项目
def run_project():
    # 1. 检查项目主文件是否存在
    if not os.path.exists(app_path):
        raise FileNotFoundError(f"未找到项目主文件，请检查路径: {app_path}")
    # 2. 根据系统动态定位虚拟环境的 Python 解释器
    if sys.platform == "win32":
        print(f"正在使用虚拟环境启动项目: {app_path}")
        # cmd /k 后面如果要接一个带空格的程序和参数，cmd 的标准语法是用 & 连接命令，或者直接传入
        cmd_command = os.path.join(base_dir, "env", "Scripts", COMMAND)
        subprocess.run(["cmd", "/k", cmd_command])  # /k 保持窗口开启
    else:
        python_exe = os.path.join(base_dir, "env", "bin", "python")
        print(f"正在使用虚拟环境启动项目: {app_path}")
        cmd_command = os.path.join(base_dir, "env", "Scripts", COMMAND)
        # Linux 下同样保持纯净路径拼接
        subprocess.run(["bash", "-c", f"{cmd_command}; exec bash"])
# 入口
if __name__ == "__main__":
    try:
        run_project()
    except Exception as e:
        print(f"[启动失败] 错误信息:\n{e}")
        if sys.platform == "win32":
            os.system("pause")
        else:
            input("按 [Enter] 键退出...")

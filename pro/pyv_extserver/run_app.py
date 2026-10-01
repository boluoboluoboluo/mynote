import os
import sys
import subprocess

PRO_NAME = "extserver"      #项目目录名
APP_NAME = "app.py"         #项目入口文件名

# 运行项目
def run_project():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app_path = os.path.join(base_dir, PRO_NAME, APP_NAME)
    # 1. 检查项目主文件是否存在
    if not os.path.exists(app_path):
        raise FileNotFoundError(f"未找到项目主文件，请检查路径: {app_path}")
    # 2. 根据系统动态定位虚拟环境的 Python 解释器
    if sys.platform == "win32":
        python_exe = os.path.join(base_dir, "env", "Scripts", "python.exe")
        print(f"正在使用虚拟环境启动项目: {app_path}")
        # cmd /k 后面如果要接一个带空格的程序和参数，cmd 的标准语法是用 & 连接命令，或者直接传入
        cmd_command = f"{python_exe} {app_path}"
        subprocess.run(["cmd", "/k", cmd_command])  # /k 保持窗口开启
    else:
        python_exe = os.path.join(base_dir, "env", "bin", "python")
        print(f"正在使用虚拟环境启动项目: {app_path}")
        # Linux 下同样保持纯净路径拼接
        subprocess.run(["bash", "-c", f"{python_exe} {app_path}; exec bash"])
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

import os
import subprocess

def main():
    # 定义构建目录
    build_dir = os.path.abspath(os.path.join("..", "build", "Release"))
    
    # 定义可执行文件的路径
    executable_path = os.path.join(build_dir, "hello_world.exe")
    # 执行生成的可执行文件
    if os.path.exists(executable_path):
        print(f"Running the executable: {executable_path}")
        subprocess.run([executable_path], check=True)
    else:
        print(f"Executable not found: {executable_path}")

if __name__ == "__main__":
    main()
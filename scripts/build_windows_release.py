import os
import subprocess

# mkdir -p ../build/Release
# cd  ../build/Release
# cmake ../..
# cmake --build .  执行这些

def main():
    # 定义构建目录
    build_dir = os.path.abspath(os.path.join("..", "build", "Release"))

    # 创建构建目录（如果不存在）
    os.makedirs(build_dir, exist_ok=True)#相当于命令:   mkdir -p ../build/Release
    print(f"Created build directory: {build_dir}")

    # 切换到构建目录
    os.chdir(build_dir)#相当于命令:   cd  ../build/Release

    # 运行 CMake 配置
    print("Configuring project with CMake...")
    subprocess.run(["cmake", "../.."], check=True)#相当于命令:  cmake ../..

    # 编译项目
    print("Building project...")
    subprocess.run(["cmake", "--build", "."], check=True)#相当于命令:  cmake --build .

    print("Build complete!")

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

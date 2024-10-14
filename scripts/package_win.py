import subprocess
import os
import shutil
import re
import zipfile

def get_msys2_root():
    """获取 PATH 环境变量中的 MSYS2 根路径。"""
    msys2_paths = [path for path in os.environ['PATH'].split(os.pathsep) if 'msys64' in path]
    
    if msys2_paths:
        # 获取第一个找到的 MSYS2 路径，并保留到 msys64 根目录
        return os.path.normpath(msys2_paths[0].split('msys64')[0] + 'msys64')
    return None

def run_msys_command():
    """运行 MSYS2 命令以检查可执行文件的依赖关系。"""
    msys2_root = get_msys2_root()
    if not msys2_root:
        print("没有找到 MSYS2 的路径。")
        return

    # 定义 MSYS2 shell 脚本的路径
    msys_shell_path = os.path.join(msys2_root, "msys2_shell.cmd")
    print(f"MSYS2 Shell Path: {msys_shell_path}")
    msys_shell_path = msys_shell_path.replace('\\\\', '\\')

    # 获取当前脚本的路径
    current_script_path = os.path.dirname(os.path.abspath(__file__))
    
    # 获取项目路径（当前脚本的父目录的父目录）
    project_path = os.path.abspath(os.path.join(current_script_path, "../"))
    print(f"Project Path: {project_path}")

    # 构建可执行文件的路径并使用正斜杠
    executable_path = os.path.join(project_path, "build", "Release", "hello_world.exe").replace('\\', '/')
    print(f"Executable Path: {executable_path}")

    # 要执行的 MSYS2 命令
    msys_command = f"ldd {executable_path}"

    try:
        # 调用 MSYS2 Mingw64 并运行 ldd 命令，并捕获输出
        result = subprocess.run(
            [msys_shell_path, "-mingw64", "-defterm", "-here", "-no-start", "-c", msys_command],
            stdout=subprocess.PIPE,  # 捕获标准输出
            stderr=subprocess.PIPE,   # 捕获标准错误
            text=True,                # 将输出解码为字符串
            check=True
        )
        print(f"Command '{msys_command}' executed successfully!")
        print("Output:")
        print(result.stdout)  # 打印 ldd 命令的输出
        
        # 获取项目名称作为目标目录的一部分
        project_name ="helloworld"
        target_directory = os.path.join(project_path, "build", "package", project_name)
        
        # 提取并复制 DLL 文件
        dll_files = extract_and_copy_dlls(result.stdout, target_directory)

        # 复制可执行文件到目标目录
        copy_executable(executable_path, target_directory)

        zip_directory = os.path.join(project_path, "build", "package")
        print(zip_directory)
        # 打包成 ZIP 压缩包
        zip_file_path = create_zip_package(zip_directory, project_name)
        print(f"Created ZIP package at: {zip_file_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command: {e}")
        print(f"Error output: {e.stderr}")  # 打印错误输出

def extract_and_copy_dlls(ldd_output, target_directory):
    """从 ldd 输出中提取 mingw64 目录下的 DLL 文件并复制到目标目录。"""
    # 确保目标目录存在
    os.makedirs(target_directory, exist_ok=True)

    # 匹配 mingw64 目录下的 DLL 文件
    dll_pattern = re.compile(r'^\s*(\S+\.dll)\s*=>\s*/mingw64/bin/(.+\.dll)', re.MULTILINE)
    dll_files = dll_pattern.findall(ldd_output)

    for _, dll_name in dll_files:
        # 构建源路径
        source_path = os.path.join(get_msys2_root(), "mingw64", "bin", dll_name)
        target_path = os.path.join(target_directory, dll_name)
        # 复制 DLL 文件
        shutil.copy2(source_path, target_path)
        print(f"Copied: {source_path} to {target_path}")

    return [os.path.join(target_directory, dll_name) for _, dll_name in dll_files]

def copy_executable(executable_path, target_directory):
    """复制可执行文件到目标目录。"""
    # 构建目标路径
    target_path = os.path.join(target_directory, os.path.basename(executable_path))
    # 复制可执行文件
    shutil.copy2(executable_path, target_path)
    print(f"Copied executable: {executable_path} to {target_path}")

def create_zip_package(target_directory, project_name):
    """压缩指定文件夹为 ZIP 包。"""
    zip_file_path = os.path.join(target_directory, f"{project_name}.zip")
    
    # 只压缩 project_name 文件夹
    project_folder_path = os.path.join(target_directory, project_name)

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        # 遍历 project_name 文件夹中的所有文件
        for foldername, _, filenames in os.walk(project_folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                # 计算相对路径相对于 project_folder_path
                arcname = os.path.relpath(file_path, project_folder_path)
                zipf.write(file_path, arcname)

    return zip_file_path

if __name__ == "__main__":
    run_msys_command()

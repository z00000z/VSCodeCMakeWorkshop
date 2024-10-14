# VSCodeCMakeWorkshop
vscode+cmake Fundamentals of Program Development

<!-- use msys2 -->
need install 

<!-- gcc编译器 -->
pacman -S mingw-w64-x86_64-gcc

<!-- gdb调试器 -->
pacman -S mingw-w64-x86_64-gdb

<!-- cmake -->
pacman -S mingw-w64-x86_64-cmake

# 使用 pacman 安装多个软件包
# --needed 选项确保只安装尚未安装的包，避免重复安装
# mingw-w64-x86_64-gcc 是 GCC 编译器，mingw-w64-x86_64-gdb 是调试器，mingw-w64-x86_64-cmake 是构建工具
#只需要运行下面一行就行
pacman -S --needed mingw-w64-x86_64-gcc mingw-w64-x86_64-gdb mingw-w64-x86_64-cmake



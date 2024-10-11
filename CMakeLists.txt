cmake_minimum_required(VERSION 3.10)

# 设置项目名称
project(HelloWorld)

# 指定 C++ 标准
set(CMAKE_CXX_STANDARD 17)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()

# 添加可执行文件
add_executable(hello_world src/main.cpp)

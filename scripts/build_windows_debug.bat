@echo off
if not exist "..\build\Debug" (
    mkdir "..\build\Debug"
)

cd "..\build\Debug"
cmake -DCMAKE_BUILD_TYPE=Debug ../..
cmake --build .

hello_world.exe

pause

@echo off
if not exist "..\build\Release" (
    mkdir "..\build\Release"
)

cd "..\build\Release"
cmake -DCMAKE_BUILD_TYPE=Release ../..
cmake --build .
hello_world.exe

pause

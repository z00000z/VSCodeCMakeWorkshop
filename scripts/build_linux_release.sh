#!/bin/bash
mkdir -p ../build/Release
cd ../build/Release
cmake -DCMAKE_BUILD_TYPE=Release ../.. 
cmake --build .
./hello_world
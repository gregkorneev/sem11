cmake_minimum_required(VERSION 3.10)

project(Sem11_MatrixMultiplication CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include_directories(include)

set(SRC_COMMON
    src/matrix_utils.cpp
    src/strassen.cpp
)

add_executable(app
    src/main.cpp
    ${SRC_COMMON}
)

add_executable(benchmark
    src/benchmark.cpp
    ${SRC_COMMON}
)

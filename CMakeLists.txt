cmake_minimum_required(VERSION 3.10)

project(Sem11_MatrixMultiplication CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Заголовки
include_directories(include)

# Общие исходники
set(SRC_COMMON
    src/matrix_utils.cpp
    src/strassen.cpp
)

# Основное приложение
add_executable(app
    src/main.cpp
    ${SRC_COMMON}
)

# Бенчмарк
add_executable(benchmark
    src/benchmark.cpp
    ${SRC_COMMON}
)

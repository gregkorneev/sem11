cmake_minimum_required(VERSION 3.10)

project(Sem11_MatrixMultiplication CXX)

# Стандарт C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Указываем директорию с .h файлами
include_directories(include)

# Источники проекта
set(SOURCES
    src/main.cpp
    src/matrix_utils.cpp
    src/strassen.cpp
)

# Создаём исполняемый файл
add_executable(app ${SOURCES})

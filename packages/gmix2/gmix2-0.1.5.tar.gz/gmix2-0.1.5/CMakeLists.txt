cmake_minimum_required(VERSION 3.16)
project(gmix2 LANGUAGES CXX)
set(PROJECT_VERSION 0.1.5)

if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)
    enable_testing()
endif()

if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)
    add_subdirectory(tests_cpp)
endif()

add_subdirectory(src)

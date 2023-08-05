cmake_minimum_required(VERSION 2.8.12)
project(ctextlib)

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
   set(CMAKE_CXX_STANDARD 17)
else()
   set(CMAKE_CXX_STANDARD 14)
endif()

add_subdirectory(pybind11)
pybind11_add_module(ctextlib src/module.cpp)

cmake_minimum_required(VERSION 2.8)
# 指定使用c++14进行 编译， 否则会报错
set (CMAKE_CXX_STANDARD 14)
project( LearnOpencv )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( ImageShow.out src/ImageShow.cpp )
target_link_libraries( ImageShow.out ${OpenCV_LIBS} )

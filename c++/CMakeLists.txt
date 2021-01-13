cmake_minimum_required(VERSION 3.10)

project(RoverCam)

find_package( OpenCV REQUIRED )

include_directories("${PROJECT_SOURCE_DIR}")

file(GLOB SOURCES "*.cpp")

add_executable(RoverCam ${SOURCES})

target_link_libraries( RoverCam ${OpenCV_LIBS})
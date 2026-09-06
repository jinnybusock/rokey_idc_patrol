cmake_minimum_required(VERSION 3.8)
project(idc_bringup)
find_package(ament_cmake REQUIRED)
# 코드 없음: launch/·config/·scripts/ 를 그대로 install
install(DIRECTORY launch config scripts DESTINATION share/${PROJECT_NAME})
ament_package()

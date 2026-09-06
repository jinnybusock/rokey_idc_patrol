cmake_minimum_required(VERSION 3.8)
project(idc_msgs)
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# STEP 2(REP-02)에서 msg/·srv/ 파일을 추가하고 아래 목록을 채움.
# 골격 단계에서는 빈 목록이면 rosidl이 실패하므로 Ping.msg 하나만 임시 등록(REP-02에서 제거).
set(msg_files
  "msg/Ping.msg"
)
set(srv_files
)
rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  ${srv_files}
  DEPENDENCIES std_msgs geometry_msgs sensor_msgs
)
ament_export_dependencies(rosidl_default_runtime)
ament_package()

# perception.launch.py — 로봇 1대분 인식 노드(yolo/aruco/localizer/led) 기동.
# 사용: ros2 launch idc_bringup perception.launch.py namespace:=robot1
# 네임스페이스 = 로봇마다 토픽 앞에 붙는 접두사(/robot1/scan). launch에서 한 번만 지정하고 노드 코드엔 넣지 않음.
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    ns = LaunchConfiguration('namespace')
    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='robot1', description='robot1 | robot2'),
        Node(package='idc_perception', executable='yolo_node', namespace=ns, name='yolo_node', output='screen'),
        # STEP 11(PER-01) 이후 aruco_node / detection_localizer / led_classifier 추가
    ])

#!/usr/bin/env python3
"""
IDC 순찰로봇 통합 bringup.

모듈이 완성될 때마다 아래 Node 블록 주석을 해제한다.
담당자는 자기 모듈 블록만 건드리고, 구조 변경은 사전 공지한다. (CONTRIBUTING 3-3)
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace  # noqa: F401  (Node는 주석 해제 시 사용)


def generate_launch_description():
    params_file = os.path.join(
        get_package_share_directory('idc_bringup'), 'config', 'params.yaml')

    robot1 = LaunchConfiguration('robot1_ns')
    robot2 = LaunchConfiguration('robot2_ns')

    return LaunchDescription([
        DeclareLaunchArgument('robot1_ns', default_value='/robot1'),
        DeclareLaunchArgument('robot2_ns', default_value='/robot2'),
        DeclareLaunchArgument('params_file', default_value=params_file),

        LogInfo(msg=['[idc_bringup] params: ', LaunchConfiguration('params_file')]),

        # --- 로봇별 네임스페이스 그룹 ---
        GroupAction([
            PushRosNamespace(robot1),
            # Node(package='idc_nav',     executable='patrol_node',  parameters=[params_file]),
            # Node(package='idc_percept', executable='detect_node',  parameters=[params_file]),
        ]),
        GroupAction([
            PushRosNamespace(robot2),
            # Node(package='idc_nav',     executable='patrol_node',  parameters=[params_file]),
            # Node(package='idc_percept', executable='detect_node',  parameters=[params_file]),
        ]),

        # --- 전역(네임스페이스 없음) ---
        # Node(package='idc_explore', executable='fleet_explore_node', parameters=[params_file]),
        # Node(package='idc_event',   executable='event_engine_node',  parameters=[params_file]),
        # Node(package='idc_server',  executable='control_server',     parameters=[params_file]),
        # Node(package='idc_cctv',    executable='entrance_node',      parameters=[params_file]),
    ])

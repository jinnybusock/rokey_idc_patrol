# rokey_idc_patrol — 코로케이션 IDC 순찰 로봇 MVP

TurtleBot4 2대(robot1/robot2) 협업 탐사·순찰·E5 도어 개방·E7 LED 이상 감지. 마감 **2026-09-11(금)** 발표.

## 워크스페이스 구조 (SDD 부록 B)
| 패키지 | 빌드 | 내용 | 주담당 |
|---|---|---|---|
| `idc_msgs` | ament_cmake | ObjectArray·SecurityEvent·MissionState·MarkerArray·Candidate / Snapshot·GenerateRoute·DockOrder.srv — **REP-02 승인 후 변경 금지** | P |
| `idc_perception` | ament_python | yolo_node, aruco_node, detection_localizer, led_classifier | P/A1/A2 |
| `idc_event` | ament_python | event_engine (E5·E7) | A3 |
| `idc_mission` | ament_python | mission_manager, fleet_coordinator, patrol_planner, map_cleaner, dock_client, verify_candidate | R2/R3 |
| `idc_server` | ament_python | control_server(Flask+SocketIO+rclpy), init_db, audit | W |
| `idc_bringup` | ament_cmake | launch/, config/(nav2_robot.yaml, explore.yaml, super_client.xml, zones.yaml), scripts/ | R1 |
| `idc_entrance` | COLCON_IGNORE | 확장백로그(EXT-04) 골격만 | — |
| `idc_sim` | COLCON_IGNORE | Gazebo 제외 골격만 | — |

## 최초 셋업 (내 PC, venv 활성 상태)
```bash
git clone https://github.com/yujh5537/rokey_idc_patrol.git ~/idc_ws
cd ~/idc_ws
bash src/idc_bringup/scripts/check_env.sh      # 함정 점검 — 모두 ✅ 여야 빌드 진행
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash                       # 이 워크스페이스(overlay)를 ROS 기본(underlay) 위에 덧씌움
ros2 pkg list | grep idc_                        # 6개 표시되면 성공
```
> `--symlink-install`: 파이썬 파일을 복사하지 않고 링크 → 코드 수정 후 재빌드 없이 바로 반영.

## 네임스페이스 규칙
- 로봇 토픽은 항상 `/robot1/...`, `/robot2/...` — 노드 코드에 접두사를 쓰지 말고 launch `namespace:=` 로 주입.
- 전역 토픽(모든 로봇 공용)은 `/event/events`, `/fleet/*`, `/server/*`, `/map` 만 허용 (SDD 4.2.1).

## 협업 규칙
`.github/CONTRIBUTING.md` 참조. 브랜치 `{이름}/{YYYYMMDD}-{기능}-{설명}`, main은 PR + 리뷰 1인 승인 필수(PM 포함).
공통 파일(idc_msgs, config/*.yaml, launch) 변경은 사전 공유 필수.

## 데이터·모델
rosbag·이미지·`.pt`는 Git에 올리지 않음(.gitignore). 공유 드라이브 경로는 Notion "데이터 수집" 페이지 참조.

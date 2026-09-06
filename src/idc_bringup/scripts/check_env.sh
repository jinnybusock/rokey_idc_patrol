#!/usr/bin/env bash
# check_env.sh — 팀원 PC 공통 사전 점검 (환경설정 md 함정 1·2·3·5 + numpy/cv_bridge)
# 사용: bash src/idc_bringup/scripts/check_env.sh
set -u
ok(){ echo "  ✅ $1"; }; ng(){ echo "  ❌ $1"; FAIL=1; }; FAIL=0
echo "[1] 함정1 Fast DDS 화이트리스트"
grep -q '^[^#]*FASTRTPS_DEFAULT_PROFILES_FILE' ~/.bashrc && ng ".bashrc에 활성 FASTRTPS_DEFAULT_PROFILES_FILE 있음 → 주석 처리" || ok "없음"
echo "[2] 함정2 ROS_DOMAIN_ID 중복"
N=$(grep -c '^[^#]*export ROS_DOMAIN_ID' ~/.bashrc); [ "$N" -le 1 ] && ok "활성 정의 ${N}개" || ng "활성 정의 ${N}개 → 하나만 남길 것"
echo "    현재 ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-<미설정>} (팀 값: 2)"
echo "[3] 함정3 colcon 위치"
which colcon | grep -q venvs && ok "$(which colcon)" || ng "$(which colcon) → venv 안에 --force-reinstall"
echo "[4] 함정5 VPN"
ip link 2>/dev/null | grep -q tailscale && ng "tailscale 인터페이스 활성 → sudo tailscale down" || ok "VPN 없음"
echo "[5] 파이썬 스택"
python3 - <<'PY' && ok "torch/ultralytics/rclpy/cv_bridge/numpy import OK" || ng "import 실패 (위 메시지 확인)"
import torch, numpy, rclpy
from ultralytics import YOLO
from cv_bridge import CvBridge
assert numpy.__version__.startswith("1.26"), f"numpy {numpy.__version__} → 1.26.4 필요"
print(f"    torch={torch.__version__} numpy={numpy.__version__}")
PY
echo "[6] RMW"
[ "${RMW_IMPLEMENTATION:-}" = "rmw_fastrtps_cpp" ] && ok "rmw_fastrtps_cpp" || ng "RMW_IMPLEMENTATION=${RMW_IMPLEMENTATION:-<미설정>} (Discovery Server는 fastrtps 필수)"
[ $FAIL -eq 0 ] && echo "== 모두 통과 ==" || { echo "== 실패 항목 있음 =="; exit 1; }

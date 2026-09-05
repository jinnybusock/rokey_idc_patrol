# rokey_idc_patrol

코로케이션 IDC 무인 시간대 **다중 AMR 자율 순찰 및 보안 이상 탐지 시스템**

무인 시간대(야간·주말)의 코로케이션 데이터센터를 2대 이상의 AMR이 협업 탐사로 지도화하고,
정해진 순찰 경로를 돌며 랙 상태·출입 인원·이상 상황을 탐지해 관제 서버로 에스컬레이션합니다.

---

## 1. 시스템 구성

```
┌─────────────────────────────────────────────────────────────────┐
│                        관제 (idc_server)                         │
│              Flask 웹 UI · SQLite · 감사 로그                     │
└───────────────▲─────────────────────────────▲───────────────────┘
                │ SecurityEvent               │ 인원/인증 이벤트
        ┌───────┴────────┐            ┌───────┴────────┐
        │   idc_event    │            │    idc_cctv    │
        │  판정·에스컬   │            │ 출입 인원 카운팅│
        └───────▲────────┘            └────────────────┘
                │ 탐지 결과
        ┌───────┴────────┐
        │  idc_percept   │  YOLO 탐지 · 마커 · map 좌표 변환
        └───────▲────────┘
                │ 이미지/TF
   ┌────────────┴────────────┐
   │  idc_nav   ·  idc_explore│  순찰 주행·정렬·재측위 / 협업 탐사·지도 병합
   └────────────▲────────────┘
                │
        ┌───────┴────────┐         ┌──────────────┐
        │  TurtleBot4 ×N │◀────────│  idc_bringup │ 통합 launch · 파라미터
        │ /robot1 /robot2│         └──────────────┘
        └────────────────┘
                                   idc_msgs : 전 패키지 공통 인터페이스
```

## 2. 패키지 구성

| 패키지 | 담당 범위 | SRD 연결 | 담당자 |
|---|---|---|---|
| `idc_msgs` | `SecurityEvent` 등 커스텀 인터페이스 | 8절 | (미정) |
| `idc_explore` | 협업 탐사·지도 병합 | SR-F01~F04 | (미정) |
| `idc_nav` | 순찰 주행·정렬·재측위 | SR-F05~F13 | (미정) |
| `idc_percept` | YOLO 탐지·마커·좌표 변환 | SR-F14~F19 | (미정) |
| `idc_cctv` | 출입구 인원 카운팅·가상 인증 | SR-F20 계열 | (미정) |
| `idc_event` | 이벤트 판정·에스컬레이션 | SR-F21~F26 | (미정) |
| `idc_server` | Flask 관제·SQLite·감사 로그 | SR-F29~F31 | (미정) |
| `idc_bringup` | 통합 launch·파라미터 yaml | Day 8~9 | (미정) |

> `idc_msgs`는 모든 패키지가 참조하는 **공통 파일**입니다.
> 필드 추가·변경은 [CONTRIBUTING 3-3](.github/CONTRIBUTING.md) 규칙에 따라 반드시 사전 공지 후 진행하세요.

## 3. 설치 및 빌드

전제: Ubuntu 24.04 + ROS 2 Jazzy, 워크스페이스는 `~/rokey_ws`

```bash
# 1) clone
cd ~/rokey_ws/src
git clone git@github.com:yujh5537/rokey_idc_patrol.git

# 2) 의존성 설치
cd ~/rokey_ws
rosdep install --from-paths src --ignore-src -r -y

# 3) 빌드
colcon build --symlink-install
source install/setup.bash
```

`.bashrc`에 `~/rokey_ws/install/setup.bash` 소싱이 이미 되어 있다면 3)의 `source`만 새 터미널에서 생략 가능합니다.

## 4. 실행

```bash
# 환경 변수 준비 (최초 1회)
cd ~/rokey_ws/src/rokey_idc_patrol
cp .env.example .env      # 값 채워 넣기, .env 는 커밋 금지

# 통합 실행
ros2 launch idc_bringup patrol.launch.py
```

> 각 패키지의 개별 실행 명령어는 담당자가 이 절에 추가합니다.
> [CONTRIBUTING 9-3](.github/CONTRIBUTING.md) — **누구나 복사해서 그대로 실행 가능한 형태**여야 하며,
> 절대 경로(`/home/...`) 하드코딩은 금지입니다.

## 5. 모델 가중치 (.pt) — 저장소에 포함되지 않음

`.gitignore`가 `*.pt`, `*.onnx`, `*.engine`, `datasets/`, `runs/`를 제외합니다 (GitHub 100MB 제한).
학습된 가중치는 아래에서 내려받아 각자 로컬에 배치하세요.

| 모델 | 용도 | 배치 경로 | 다운로드 |
|---|---|---|---|
| `idc_percept.pt` | 랙/이상 상황 탐지 | `idc_percept/models/` | (TODO: 공유 드라이브 링크) |
| `idc_cctv.pt` | 출입구 인원 탐지 | `idc_cctv/models/` | (TODO: 공유 드라이브 링크) |

```bash
mkdir -p idc_percept/models idc_cctv/models
# 내려받은 .pt 파일을 위 경로에 복사
```

> 가중치 담당자는 링크를 확정한 뒤 이 표를 갱신해 주세요. 표가 비어 있으면 팀원이 실행할 수 없습니다.

## 6. 지도(maps)

병합된 지도(`.pgm` / `.yaml`)는 **저장소에 커밋합니다**. 8명이 동일한 지도를 써야
순찰 경로와 점검 지점 좌표가 일치합니다. → [`maps/`](maps/)

## 7. 저장하지 않는 것 (개인정보·보안)

- `evidence/` — 이벤트 증적 이미지. BRD 4장 개인정보 요구(원본 미저장·90일 만료 삭제)에 따라 **Public 저장소에 절대 올리지 않습니다.**
- `*.db` / `*.sqlite` — 실행할 때마다 바뀌어 충돌을 유발합니다. 스키마(`schema.sql`)와 시드 데이터만 커밋하세요.
- `.env`, 인증서, 키 파일 — [CONTRIBUTING 7장](.github/CONTRIBUTING.md) 참조.

## 8. 협업 규칙

작업 시작 전 반드시 읽어주세요 → **[.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)**

- 브랜치: `{이름}/{YYYYMMDD}-{기능}` (예: `injae/20260904-percept-yolo-node`)
- `main` 직접 push 금지 — PR + Code Owner 승인 1건 필수
- Merge 방식: **Squash and merge** 전용, 브랜치는 merge 후에도 유지
- 트러블슈팅은 Issue 템플릿(`bug_report.md`)으로 기록

## 9. 라이선스

각 패키지는 Apache-2.0 (각 패키지의 `LICENSE` 파일 참조).

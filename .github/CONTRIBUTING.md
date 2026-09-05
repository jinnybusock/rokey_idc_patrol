# 🌿 GitHub 협업 규칙

팀원 전원(8명)이 동일한 방식으로 Branch / PR / Issue를 다루기 위한 규칙입니다.
프로젝트 마감(9/11)까지 관리 부담은 줄이되, 나중에 문제를 추적할 수 있는 최소한의 기록은 남기는 것을 목표로 합니다.

---

## 1. Branch 전략

### 1-1. Branch Naming

```
{이름}/{날짜(YYYYMMDD)}-{기능}-{간단설명}
```

| 항목 | 설명 |
| --- | --- |
| 이름 | 작업자 이름 또는 영문 아이디 (예: `injae`, `uiseok`) |
| 날짜 | 브랜치를 만든 날짜, `YYYYMMDD` |
| 기능 | 작업 중인 기능/모듈 이름 (예: `lidar`, `navigation`, `ui`) |
| 간단설명 | 무엇을 하는 작업인지 kebab-case로 짧게 |

**예시**

```
injae/20260905-lidar-mapping-node
uiseok/20260905-navigation-cmdvel-delay-fix
donghwi/20260906-docs-network-guide
```

- `이름/`으로 시작하면 GitHub Branch 목록에서 사람별로 그룹화되어 보여서 찾기 쉬움
- 설명에 한글 대신 영문 kebab-case 사용 (공백·특수문자로 인한 문제 방지)
- 같은 사람이 같은 기능을 여러 날 나눠 작업하면 날짜만 갱신해서 새 브랜치 생성

### 1-2. Branch 보호 설정 (`main`)

`Settings → Branches → Add branch protection rule` (대상: `main`)

- ✅ **Require a pull request before merging** — `main`에는 PR을 통해서만 반영
- ✅ **Require approvals: 1** — 리뷰어 1명 이상 승인 필요
- ✅ **Do not allow bypassing the above settings** — 관리자도 예외 없이 규칙 적용
- ✅ **Restrict who can push to matching branches** — `main` 직접 push 차단 (PR만 허용)
- ✅ **Require review from Code Owners** — `CODEOWNERS`에 등록된 PM의 승인 없이는 Merge 불가 (자세한 내용은 10장 참고)
- 그 외 브랜치(`injae/...`, `uiseok/...` 등)는 보호 설정 대상이 아니므로 자유롭게 push 가능 — 별도 설정 불필요

---

## 2. Merge 규칙

### 2-1. 작업 중 수시로 Fetch

PR을 올릴 때만 몰아서 맞추면 충돌이 커집니다. 작업 중에도 최소 오전/오후 1회 이상 원격 상태를 확인하는 것을 습관화합니다.

```bash
git fetch origin
git status      # 내 브랜치가 origin 대비 얼마나 뒤처졌는지 확인
```

- 여러 명이 같은 기간에 관련된 작업을 하고 있다면, `fetch` 후 뒤처진 정도가 클 때 바로바로 `git merge origin/main`으로 조금씩 반영
- 하루 이상 브랜치를 붙잡고 있을 경우 반드시 그날 안에 한 번은 `fetch`로 원격 변경 사항을 확인

### 2-2. Merge 전 체크리스트 — main 최신화

PR을 만들기 전(또는 리뷰 요청 전), 자신의 브랜치에 `main`을 먼저 반영해서 최신 상태로 맞춥니다.

```bash
git checkout {내 브랜치}
git fetch origin
git merge origin/main      # 충돌 발생 시 이 시점에 해결
git push
```

- 이 작업 없이 PR을 열면 리뷰어가 최신 `main` 기준으로 diff를 확인하기 어려움
- 충돌은 PR을 올리기 **전에** 로컬에서 먼저 해결하는 것을 원칙으로 함
- CI/자동 테스트가 없는 현재 단계에서는 GitHub이 강제하는 기능이 아니라 **작업자가 직접 지키는 프로세스 규칙**입니다. (나중에 테스트가 생기면 `Require branches to be up to date before merging` 옵션으로 기술적으로 강제 가능)

### 2-3. Merge 방식

- `Squash and merge` 권장 — 브랜치 내 여러 커밋을 하나로 정리해서 `main` 히스토리를 깔끔하게 유지

### 2-4. Merge 후 브랜치 처리

- Merge된 브랜치는 **기본적으로 삭제하지 않고 유지**
- 삭제가 꼭 필요한 경우에만 **PM 승인 후 수동 삭제**
- Repository 설정의 `Automatically delete head branches` 옵션은 **꺼둔 상태 유지**

---

## 3. 충돌 예방 수칙

### 3-1. 작업 범위 명확히 분리

- 같은 파일/모듈을 여러 명이 동시에 건드리지 않도록, 작업 시작 전 Notion(ToDo List)에 오늘 담당할 파일·기능을 기록해서 공유
- ROS2 패키지 단위로 담당을 나누면 자연스럽게 파일 단위 충돌이 줄어듦

### 3-2. 브랜치 수명은 짧게, 커밋은 작게

- 브랜치를 오래 붙잡고 있을수록 `main`과의 차이가 커져서 충돌 위험도 커짐
- 기능을 작은 단위로 쪼개서 자주 PR을 올리고 Merge — 하루 이상 걸리는 큰 작업은 중간 단위로 쪼갤 수 없는지 먼저 검토

### 3-3. 공통 파일은 사전 협의 후 수정

- README, 공통 Config, ROS2 Interface, Launch 파일 등은 혼자 판단으로 구조를 바꾸지 않고 사전 공유
- 특히 `package.xml`, `CMakeLists.txt`처럼 여러 패키지가 같이 참조하는 파일은 수정 전 반드시 공지

### 3-4. 진행 중인 작업은 Draft PR로 미리 공개

- 완성 전이라도 Draft PR을 열어두면 팀원이 "이 파일은 지금 누가 작업 중인지" 미리 확인 가능
- 같은 파일을 동시에 손대는 상황을 사전에 예방

### 3-5. 자동 생성 파일은 절대 커밋하지 않기

- `build/`, `install/`, `log/`, `__pycache__/`는 이미 `.gitignore`로 제외됨 — `git add -f`로 강제 추가하지 않기
- 사람마다 빌드 결과물 내용이 달라서 불필요한 충돌의 원인이 됨

### 3-6. 공유 브랜치에서 rebase / force-push 금지

- `rebase`는 자기 혼자만 쓰는 개인 브랜치에서만 사용
- 다른 사람과 같이 쓰는 브랜치에서 `rebase` 후 `force-push`하면 팀원의 커밋 히스토리가 깨질 수 있음

---

## 4. Commit 메시지

| Prefix | 사용 목적 | 예시 |
| --- | --- | --- |
| `feat` | 새로운 기능 추가 (기능 스크립트 작성 시 가장 많이 사용) | `feat: LiDAR 매핑 노드 추가` |
| `fix` | 버그 수정 또는 오류 코드 수정 | `fix: cmd_vel 지연 문제 수정` |
| `refactor` | 코드 구조 개선 | `refactor: 타임라인 이벤트 연동 및 리셋 로직 리팩토링` |
| `chore` | 설정 파일 추가, 패키지 구성 등 자잘한 작업 | `chore: gitignore 설정 추가` |
| `docs` | README, 명세서 등 문서 수정 | `docs: 네트워크 설정 가이드 추가` |

- 하나의 Commit에는 하나의 의미 있는 작업만 담기
- `수정`, `update`, `123` 같은 의미 없는 메시지 금지

### 4-1. 코드 리뷰를 위한 상세 커밋 메시지

PM이 커밋만 보고도 변경 배경을 파악할 수 있도록, 단순 작업이 아니면 제목 한 줄로 끝내지 않고 본문을 덧붙입니다.

```
feat: LiDAR 매핑 노드 추가

- 라이다 스캔 데이터를 받아 occupancy grid로 변환하는 노드 신규 작성
- 기존 mapping_node와 분리해서 별도 프로세스로 실행되도록 구성 (성능 이슈 때문)
```

- 제목: `type: 무엇을 했는지` (한 줄, 위 표의 Prefix 사용)
- 본문(변경이 단순하지 않을 때만): 왜 이렇게 했는지, 영향 범위는 무엇인지 2~3줄로 추가

---

## 5. Pull Request 규칙

- PR 제목에는 어떤 작업인지 명확히 표기 (Branch명과 동일한 맥락으로)
- PR 본문은 `.github/PULL_REQUEST_TEMPLATE.md` 양식 사용 (변경 내용 / 확인 사항)
- 리뷰어 1명 이상 승인 후에만 Merge 가능 (Branch 보호 설정으로 강제됨)
- 관련된 Issue가 있으면 PR 본문에 `Closes #이슈번호` 작성 → Merge 시 해당 Issue 자동 종료
- Merge 전 확인:
  - `Files changed` 전체 확인
  - Conflict 여부 확인
  - 다른 기능에 영향 있는지 확인
  - 공통 파일(README, 공통 Config, ROS2 Interface 등) 변경 시 담당자와 사전 확인

---

## 6. Issue 규칙

Issue는 **작업 관리용이 아니라 트러블슈팅 기록용**으로 제한적으로 사용합니다.
(작업/할 일 관리는 기존처럼 Notion ToDo List를 그대로 사용 — 이중 관리 방지)

### 6-1. 언제 만드는가

- 원인 파악에 시간이 걸렸거나, 팀원이 같이 알아야 할 에러/버그가 발생했을 때
- 사소한 오타 수정, 단순 반복 작업에는 만들지 않음

### 6-2. 작성 방법

제목: `[문제] 어떤 상황에서 어떤 에러가 발생했는지`

본문은 아래 양식을 사용합니다 (`.github/ISSUE_TEMPLATE/bug_report.md` 참고).

```
문제
- 어떤 기능에서 문제가 발생했는지
환경
- PC / Branch
Error
- Error Message / Screenshot
시도
- 지금까지 확인한 내용
현재 상태
- 해결 / 미해결
```

- 해결되면 댓글에 **해결 방법**을 남기고 Close
- 관련 PR이 있다면 PR 본문에 `Closes #이슈번호`를 적어 Merge 시 자동으로 Close되게 함
- 라벨/담당자 지정 등은 생략 (마감이 얼마 남지 않아 관리 오버헤드를 늘리지 않기 위함)

---

## 7. 보안

### GitHub 업로드 금지 목록
- GitHub PAT
- Password
- API Key
- Secret Key
- 인증서
- 개인 계정정보

### `.gitignore`
```
# ROS2 / Python 빌드 산출물
build/
install/
log/
__pycache__/
*.pyc
*.egg-info/

# 민감 정보 - 절대 커밋 금지
.env
.env.*
!.env.example
*.pem
*.key
*.crt
*.p12
credentials.json
secrets.yaml
secrets.yml

# 모델 가중치·학습 산출물 (GitHub 100MB 제한)
*.pt
*.onnx
*.engine
datasets/
runs/

# 런타임 생성물
*.db
*.sqlite
*.sqlite3
evidence/
rosbag2_*/
*.bag
*.mp4
*.avi

# Editor / OS
.vscode/
.idea/
*.swp
.DS_Store
```
- 위 목록은 실수로라도 Git에 잡히지 않도록 `.gitignore`에 기본 등록
- 그래도 실제로 Secret 값이 든 파일을 커밋하기 전에는 항상 `git status`로 한 번 더 확인

---

## 8. `.github` 폴더 구성

```
.github/
├── CONTRIBUTING.md              # 이 문서 (Git/GitHub 협업 규칙)
├── PULL_REQUEST_TEMPLATE.md     # PR 작성 시 자동으로 삽입되는 양식
├── CODEOWNERS                   # PM을 모든 PR의 리뷰어로 자동 지정
└── ISSUE_TEMPLATE/
    └── bug_report.md            # 트러블슈팅 기록용 Issue 양식
```

- `workflows/`(CI)는 지금 단계에서는 생략 — 필요해지면(예: 10-3의 push 알림 자동화) 추가 검토

---

## 9. 경로(Path) 작성 규칙

팀원마다 계정명과 워크스페이스 위치가 다르므로(`/home/injae/...`, `/home/uiseok/...` 등), 코드·config·launch 파일에 **절대 경로를 하드코딩하지 않습니다**. 누구나 저장소를 clone/pull 받은 뒤 **동일한 명령어**로 실행할 수 있어야 합니다.

### 9-1. 원칙

- 코드 내 파일 경로는 항상 **상대 경로** 또는 **패키지 기준 동적 경로**로 작성
- 본인 PC의 개인 경로(`/home/{사용자명}/...`)를 코드에 그대로 넣지 않기
- 경로가 필요한 값은 코드에 박아 넣지 말고, 인자·파라미터·환경 변수로 주입

### 9-2. ROS2 / Python 권장 방법

```python
# 금지 - 본인 환경에서만 동작
config_path = "/home/injae/rokey_ws/src/rokey_idc_patrol/idc_bringup/config/params.yaml"

# 권장 - 패키지 기준 동적 경로
from ament_index_python.packages import get_package_share_directory
config_path = os.path.join(get_package_share_directory('idc_bringup'), 'config', 'params.yaml')

# 스크립트 파일 기준 상대 경로가 필요할 때
from pathlib import Path
config_path = Path(__file__).resolve().parent / "config" / "params.yaml"
```

- Launch 파일도 동일하게 `get_package_share_directory()`로 경로 구성
- 워크스페이스 루트 기준 경로가 꼭 필요하면 환경 변수나 ROS2 파라미터로 주입 (코드에 직접 하드코딩 금지)

### 9-3. 실행 명령어 통일

- 각 패키지/기능의 실행 명령어는 README(또는 패키지 내 `README.md`)에 그대로 복사해서 쓸 수 있게 명시
  - 예: `ros2 launch idc_bringup patrol.launch.py`
- 사용자명, 설치 경로에 관계없이 누구나 위 명령어 그대로 실행되면 통과
- PR 리뷰 시 하드코딩된 절대 경로가 있는지 확인

---

## 10. PM 알림 & 코드 리뷰

### 10-1. CODEOWNERS로 PM을 모든 PR의 리뷰어로 자동 지정

`.github/CODEOWNERS` 파일에 아래처럼 작성하면, PR이 열릴 때마다 PM이 자동으로 리뷰어로 지정되고 GitHub이 즉시 알림(이메일/웹/모바일)을 보냅니다.

```
# PM + 백업 리뷰어 1명을 Code Owner로 지정
* @yujh5537 @EuiseokJeongNZ
```

- 1-2의 **Require review from Code Owners** 설정과 함께 사용하면, 목록에 있는 사람(PM 또는 백업)의 승인 없이는 Merge 자체가 불가능해짐
- `main`에 반영되는 모든 변경은 PR을 거치므로, 이 설정만으로 PM이 놓치는 변경 없이 전부 확인·리뷰 가능
- 팀원이 승인(Approve)해도 목록에 없는 사람이면 이 조건은 채워지지 않음 — **사실상 최종 승인권은 PM(+백업)에게만 있는 구조**

> ⚠️ **PM 본인이 PR을 올리는 경우 주의**: GitHub은 본인이 올린 PR을 스스로 승인해도 그 승인이 Branch 보호 규칙에는 카운트되지 않습니다. PM이 유일한 Code Owner면 PM 본인 PR을 승인해 줄 사람이 없어서 Merge가 영원히 막힐 수 있습니다. 그래서 위처럼 **백업 리뷰어 1명을 함께 등록**해두면, PM이 직접 올린 PR은 백업 리뷰어가 승인해서 해결할 수 있습니다.

### 10-2. GitHub 알림 설정 (PM이 직접 설정)

1. Repository 페이지 우측 상단 **Watch → Custom → All Activity** 선택 (PR, Issue, 코멘트 등 모든 활동 알림 수신)
2. GitHub 계정 **Settings → Notifications**에서 Email 또는 Web 알림 활성화
3. GitHub 모바일 앱을 설치하면 PR 생성/리뷰 요청 알림을 휴대폰 Push로도 받을 수 있음

> GitHub은 PR·Issue·리뷰 요청·코멘트에 대해서는 알림을 보내지만, **PR 없이 개인 브랜치에만 올라가는 단순 push는 기본적으로 알림 대상이 아닙니다.** 그래서 10-1처럼 CODEOWNERS로 PR 단계에서 반드시 PM이 걸리도록 하는 것이 핵심입니다.

### 10-3. (선택) 개인 브랜치 push까지 실시간으로 알고 싶다면

- 3-4의 Draft PR 습관과 병행하면, 개인 브랜치의 작업도 빠르게 PR로 노출되어 PM이 조기에 확인 가능
- 그래도 모든 raw push까지 실시간 알림이 꼭 필요하다면, `.github/workflows/`에 `push` 트리거로 이메일을 보내는 GitHub Actions를 추가하는 방법이 있음 (SMTP 계정/Secret 등 별도 설정 필요 — 필요하면 별도로 구성 요청) (PR 템플릿 체크리스트 참고)

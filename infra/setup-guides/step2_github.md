# Step 2 — GitHub Repo 생성 + 시스템 파일 업로드

> 본인 PC 의 `investing-agent-v2` 폴더를 GitHub private repo 로 만들어 EC2 와 동기화 가능하게 함.
> 예상 시간: 20분.

---

## 1. GitHub 에서 Private Repo 생성 (5분)

### 1.1 새 repo 만들기
1. https://github.com 로그인
2. 우측 상단 `+` 아이콘 → "New repository"
3. 다음 항목 입력:
   - **Repository name**: `investing-agent-v2` (또는 본인 원하는 이름)
   - **Description**: `Personal investment analysis system` (선택)
   - **Public / Private**: ★ **반드시 Private 선택** (시스템 파일이 본인 투자 thesis 라 외부 노출 X)
   - **Initialize this repository with**:
     - ❌ Add a README file — 체크 해제 (본인이 이미 README.md 있음)
     - ❌ Add .gitignore — 체크 해제 (나중에 추가)
     - ❌ Choose a license — 체크 해제
4. "Create repository" 클릭

### 1.2 repo URL 메모
- 생성 후 페이지의 URL 메모 (예: `https://github.com/sunyonge/investing-agent-v2`)
- 또는 페이지에 표시되는 SSH/HTTPS URL 복사 (HTTPS 추천 — 본인이 git 첫 경험이라)
  - 형식: `https://github.com/sunyonge/investing-agent-v2.git`

- [ ] GitHub repo 생성 완료
- [ ] Repo URL 메모

---

## 2. 본인 PC 에서 PowerShell 열기 (1분)

1. Windows 검색에서 "PowerShell" 또는 "Windows Terminal" 검색
2. 실행
3. **본인이 zip 해제한 폴더로 이동**:
   ```powershell
   cd C:\Users\본인\Documents\investing-agent-v2
   ```
   (본인 실제 경로로 변경)

4. 현재 위치 확인:
   ```powershell
   dir
   ```
   → `methodology.md`, `mega-change-map/`, `watchlist/` 등 폴더·파일 보여야 함.

- [ ] PowerShell 에서 올바른 폴더 이동 확인

---

## 3. .gitignore 파일 생성 (5분)

> **중요**: git 에 push 하면 안 되는 파일들을 미리 지정. API 키 같은 비밀 정보 보호.

### 3.1 .gitignore 파일 만들기

VS Code 또는 메모장으로 `.gitignore` 파일 생성 (확장자 없음, 파일명 정확히 `.gitignore`).

위치: `investing-agent-v2` 폴더 최상단 (methodology.md 와 같은 레벨)

내용:
```
# Environment variables / API keys
.env
.env.*
*.env
secrets.json
credentials.json

# Python
__pycache__/
*.pyc
*.pyo
venv/
.venv/
env/
.python-version

# OS
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.swp

# Logs
*.log
logs/

# AWS local config
.aws/

# Output cache (다이제스트 생성 후 cache)
.cache/
```

### 3.2 PowerShell 로 만드는 방법 (편한 옵션)

VS Code 없으면 PowerShell 에서:
```powershell
@"
# Environment variables / API keys
.env
.env.*
*.env
secrets.json
credentials.json

# Python
__pycache__/
*.pyc
*.pyo
venv/
.venv/
env/

# OS
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.swp

# Logs
*.log
logs/

# AWS
.aws/

# Cache
.cache/
"@ | Out-File -FilePath .gitignore -Encoding utf8
```

확인:
```powershell
type .gitignore
```
→ 위 내용 출력되면 OK.

- [ ] .gitignore 파일 생성 완료

---

## 4. Git 초기화 + 첫 commit (5분)

### 4.1 git 초기화
PowerShell 에서 (계속 `investing-agent-v2` 폴더 위치):

```powershell
git init
```

→ `Initialized empty Git repository in C:/Users/.../investing-agent-v2/.git/` 출력.

### 4.2 모든 파일을 commit 대상으로 추가
```powershell
git add .
```

→ 출력 없거나 일부 LF/CRLF 경고 (무시 가능).

### 4.3 추가된 파일 확인
```powershell
git status
```

→ `methodology.md`, `mega-change-map/` 등 `new file:` 으로 표시되어야 함.
→ `.gitignore` 도 포함되어 있는지 확인.

### 4.4 첫 commit 만들기
```powershell
git commit -m "Initial commit - investing agent system v2.1"
```

→ `[master (root-commit) XXXXXXX] Initial commit ...` 같은 출력.
→ X 개 files changed 같은 통계 나옴.

- [ ] git init 성공
- [ ] git add . 성공
- [ ] git commit 성공

---

## 5. GitHub repo 와 연결 + push (5분)

### 5.1 remote 추가
PowerShell 에서 (본인 repo URL 로 변경):

```powershell
git remote add origin https://github.com/sunyonge/investing-agent-v2.git
```

→ 출력 없음 (정상).

확인:
```powershell
git remote -v
```
→ origin 두 줄 출력되면 OK.

### 5.2 브랜치 이름 main 으로 변경 (현대 GitHub 표준)
```powershell
git branch -M main
```

### 5.3 GitHub 로 push
```powershell
git push -u origin main
```

→ **첫 push 시 GitHub 인증 창 뜸**. 본인 PC 의 기본 브라우저에서 GitHub 로그인 페이지가 자동 열림.
→ "Sign in with browser" 클릭 → GitHub 로그인 → 권한 승인 → 자동으로 PowerShell 에 토큰 전달.

→ 잘 진행되면:
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
To https://github.com/sunyonge/investing-agent-v2.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

- [ ] git remote add 성공
- [ ] git push 성공
- [ ] GitHub 인증 완료

---

## 6. GitHub 에서 확인 (1분)

1. 브라우저에서 본인 GitHub repo 페이지로 이동:
   `https://github.com/sunyonge/investing-agent-v2`
2. 다음 모두 보여야 함:
   - `README.md` (페이지 하단에 자동 렌더)
   - `methodology.md`
   - `mega-change-map/` 폴더
   - `watchlist/` 폴더
   - `digests/` 폴더
   - `calendar/` 폴더
   - `templates/` 폴더
   - `infra/` 폴더
   - `.gitignore`
3. README.md 가 페이지 하단에 보기 좋게 렌더되어 있어야 함.

- [ ] GitHub 페이지에 모든 파일 확인됨

---

## 7. (선택) GitHub Personal Access Token 발급 — Step 3·6 에서 사용

> EC2 에서 git pull 할 때 매번 GitHub 로그인 하기 번거로움. Personal Access Token (PAT) 으로 자동 인증 가능.

### 7.1 GitHub 에서 PAT 발급
1. https://github.com → 우측 상단 본인 아바타 → "Settings"
2. 좌측 메뉴 하단 "Developer settings"
3. 좌측 "Personal access tokens" → "Tokens (classic)"
4. "Generate new token" → "Generate new token (classic)"
5. 다음 설정:
   - **Note**: `investing-agent-v2-ec2`
   - **Expiration**: 1 year (또는 본인 원하는 기간)
   - **Scopes** (권한): ✅ `repo` 만 체크 (전체 권한)
6. "Generate token" 클릭
7. **즉시 토큰 복사·메모** (페이지 떠나면 다시 못 봄)
8. 토큰 형식: `ghp_XXXXXXXXXXXXXXXXXX`

- [ ] GitHub PAT 발급
- [ ] 토큰 메모 (절대 외부 노출 X, .gitignore 처럼 commit 도 X)

---

## 8. Step 2 완료 ✅

다음 모두 ✅ 되었으면 Step 3 진행 가능:

- [ ] GitHub private repo 생성
- [ ] .gitignore 파일 생성
- [ ] git init + commit + push 성공
- [ ] GitHub 페이지에 시스템 파일 확인됨
- [ ] (권장) GitHub Personal Access Token 발급·메모

---

## 트러블슈팅

### `git: command not found` 에러
- Git for Windows 가 PATH 에 등록 안 됨
- PowerShell 재시작 또는 PC 재부팅
- 그래도 안 되면 Git for Windows 재설치

### git push 시 "Authentication failed"
- GitHub 비밀번호 인증은 2021년 이후 deprecated
- 위 5.3 의 브라우저 인증 사용 (GitHub Credential Manager)
- 또는 위 7 의 PAT 사용:
  ```powershell
  git push -u origin main
  Username: 본인 GitHub username
  Password: PAT 토큰 입력 (ghp_XXXXX...)
  ```

### "fatal: remote origin already exists"
- 이전에 remote 추가한 게 남아있음
- 제거 후 다시:
  ```powershell
  git remote remove origin
  git remote add origin https://github.com/사용자명/repo이름.git
  ```

### LF/CRLF 경고 메시지
- 무시 가능 (Windows ↔ Linux 줄바꿈 자동 변환 메시지)
- Step 1 에서 "Checkout Windows-style, commit Unix-style" 선택했다면 자동 처리

### git status 에서 너무 많은 파일 보임 (수십·수백 개)
- node_modules 나 다른 임시 파일이 추적되고 있을 가능성
- `.gitignore` 파일이 제대로 위치하고 있는지 확인 (investing-agent-v2 최상단)
- 잘못 commit 한 경우 git rm --cached <파일명>

### git push 가 진행 안 되고 멈춤
- 인증 창이 다른 browser 에서 떴을 수 있음 (background 확인)
- Ctrl+C 로 중단 후 다시 시도

---

## 본인이 지금 가진 것 정리

```
=== 본인 자산 (Step 1·2 후) ===

[로컬]
- Windows PC 에 investing-agent-v2 폴더
- Git 설치, 첫 commit 완료

[GitHub]
- Private repo: https://github.com/사용자명/investing-agent-v2
- 시스템 파일 전체 업로드됨

[API 키 메모]
- Claude API 키
- Telegram Bot token, 본인 user ID
- (NewsAPI 안 함)
- (선택) GitHub PAT
```

---

## 완료 후

본인이 위 ✅ 다 했으면:
> "Step 2 완료. Step 3 진행."

또는 막힌 부분 있으면:
> "Step 2 의 X.X 에서 막힘. 에러: [에러 메시지]"

다음 Step 3 (AWS EC2 인스턴스 생성·SSH 접속) — **가장 어려운 단계** 안내 드립니다.

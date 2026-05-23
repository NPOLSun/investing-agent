# Step 4 — Python 환경 + 패키지 설치 + 시스템 파일 클론

> EC2 안에 Python·필요 패키지·본인 GitHub repo 가져오기.
> 본인이 Python 익숙한 영역. 약 20분.

---

## 0. 시작 — EC2 에 SSH 접속

PowerShell 에서:

```powershell
ssh investing-agent
```

(또는 `ssh -i ...pem ubuntu@본인IP`)

→ `ubuntu@ip-...:~$` 프롬프트 보여야 함. 이후 모든 명령은 **EC2 안에서** 실행.

---

## 1. 시스템 업데이트 + 기본 보안 강화 (5분)

### 1.1 시스템 업데이트
```bash
sudo apt update
sudo apt upgrade -y
```

→ 1~2분 소요. 패키지 업데이트 진행.

### 1.2 (권장) SSH 비밀번호 인증 차단
본인이 보안 그룹 Anywhere 로 했으니 추가 보안 권장:

```bash
# SSH 비밀번호 인증 차단 (key only 허용)
sudo sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

# SSH 서비스 재시작
sudo systemctl restart ssh
```

→ 출력 없으면 OK.

### 1.3 (권장) Fail2ban 설치
```bash
sudo apt install -y fail2ban
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

→ brute-force SSH 시도 자동 차단.

### 1.4 Timezone 한국 시간으로
```bash
sudo timedatectl set-timezone Asia/Seoul
```

확인:
```bash
date
```
→ 한국 시간 표시 확인.

- [ ] 시스템 업데이트 완료
- [ ] SSH 비밀번호 차단
- [ ] Fail2ban 설치
- [ ] Timezone 한국

---

## 2. Python 환경 확인 + pip 설치 (3분)

### 2.1 Python 버전 확인
```bash
python3 --version
```

→ `Python 3.12.X` 또는 `3.10.X` 정도. 어느 버전이든 3.10+ 이면 OK.

### 2.2 pip 설치
```bash
sudo apt install -y python3-pip python3-venv
```

확인:
```bash
pip3 --version
```

- [ ] Python 3.10+ 확인
- [ ] pip3 설치 완료

---

## 3. Git 설치 + GitHub repo 클론 (5분)

### 3.1 Git 설치
```bash
sudo apt install -y git
```

확인:
```bash
git --version
```

### 3.2 GitHub repo 클론

**Personal Access Token (PAT) 방식 (Step 2 의 섹션 7 에서 발급한 토큰 사용)**:

```bash
cd ~
git clone https://github.com/본인username/investing-agent-v2.git
```

→ Username·Password 요청 시:
- Username: 본인 GitHub username
- Password: ★ **PAT 토큰** (ghp_XXXXXX...) — GitHub 비밀번호 X

PAT 없으면 GitHub 에서 비밀번호 입력 시도하다 거절될 거예요. 그러면 Step 2 의 섹션 7 다시 해서 PAT 발급 후 시도.

### 3.3 클론 확인
```bash
ls -la investing-agent-v2/
```

→ 다음 보여야 함:
```
README.md
methodology.md
mega-change-map/
watchlist/
digests/
calendar/
templates/
infra/
.gitignore
```

### 3.4 (권장) Git credentials 저장
매번 PAT 입력 번거로움. 캐시 설정:

```bash
git config --global credential.helper store
```

이후 한 번 git push/pull 시 PAT 입력하면 영구 저장.

⚠️ 주의: PAT 가 평문으로 저장됨. EC2 만 본인 접근 가능하면 OK.

- [ ] Git 설치
- [ ] GitHub repo 클론 성공
- [ ] 시스템 파일 ls 로 확인
- [ ] (권장) Credentials 저장

---

## 4. Python 가상 환경 (venv) 생성 (3분)

가상 환경은 본 프로젝트만의 패키지 환경. 시스템 전역에 영향 X.

### 4.1 가상 환경 생성
```bash
cd ~/investing-agent-v2
python3 -m venv venv
```

→ `venv/` 폴더 생성됨.

### 4.2 가상 환경 활성화
```bash
source venv/bin/activate
```

→ 프롬프트 앞에 `(venv)` 표시:
```
(venv) ubuntu@ip-...:~/investing-agent-v2$
```

### 4.3 가상 환경 비활성화 (참고)
```bash
deactivate
```

→ `(venv)` 표시 사라짐.

→ 이번 단계에서는 *활성화 상태* 유지.

- [ ] venv 생성·활성화

---

## 5. 핵심 패키지 설치 (5분)

가상 환경 활성화 상태에서:

```bash
# pip 업그레이드
pip install --upgrade pip

# 핵심 패키지 일괄 설치
pip install \
  anthropic \
  python-telegram-bot \
  python-dotenv \
  yfinance \
  pykrx \
  requests \
  pandas \
  pytz
```

각 패키지 용도:
- **anthropic**: Claude API SDK
- **python-telegram-bot**: 텔레그램 봇 라이브러리
- **python-dotenv**: .env 파일에서 환경변수 로드
- **yfinance**: Yahoo Finance 미국 주식 가격
- **pykrx**: 한국 주식 가격
- **requests**: HTTP 요청 (일반)
- **pandas**: 데이터 정리
- **pytz**: 시간대 처리 (한국 시간)

→ 1~2분 소요. 다 설치되면 출력 끝.

### 5.1 설치 확인
```bash
pip list
```

→ 위 패키지들 + 의존성 패키지 다 보여야 함.

### 5.2 (선택) requirements.txt 생성
나중에 같은 환경 재현용:
```bash
pip freeze > requirements.txt
```

→ `requirements.txt` 파일 생성됨. 이걸 git commit 하면 다른 PC 에서도 같은 환경 재현 가능.

- [ ] 모든 패키지 설치 완료
- [ ] pip list 확인
- [ ] (선택) requirements.txt 생성

---

## 6. .env 파일 생성 (API 키 보관) (3분)

본인 키들을 EC2 에 저장. 절대 git commit X.

### 6.1 .env 파일 생성
```bash
cd ~/investing-agent-v2
nano .env
```

→ nano 텍스트 에디터 열림.

### 6.2 .env 내용 입력

다음 내용 그대로 복사·붙여넣기 (본인 키로 변경):

```
# Anthropic Claude API
ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXXXXXXXXXX

# Telegram Bot
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklmnoPQRstuVWXyz
TELEGRAM_CHAT_ID=123456789

# GitHub (선택, 자동 sync 용)
GITHUB_USERNAME=본인username
GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXX

# 시스템 설정
TIMEZONE=Asia/Seoul
DIGEST_TIME=07:00
```

### 6.3 저장·종료
- `Ctrl + O` (저장) → Enter
- `Ctrl + X` (종료)

### 6.4 권한 제한 (본인만 읽기)
```bash
chmod 600 .env
```

### 6.5 .gitignore 에 .env 가 있는지 재확인
```bash
cat .gitignore | grep .env
```

→ `.env` 가 출력되면 OK (git 이 무시함).

⚠️ 만약 .env 가 .gitignore 에 없으면 즉시 추가:
```bash
echo ".env" >> .gitignore
```

- [ ] .env 파일 생성
- [ ] 모든 API 키 입력
- [ ] chmod 600 권한 제한
- [ ] .gitignore 에 .env 포함 확인

---

## 7. 연결 테스트 (5분)

### 7.1 Claude API 테스트

```bash
cd ~/investing-agent-v2
python3 -c "
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

response = client.messages.create(
    model='claude-sonnet-4-5-20250929',
    max_tokens=50,
    messages=[{'role': 'user', 'content': 'Hello in Korean'}]
)
print(response.content[0].text)
"
```

→ "안녕하세요" 같은 한국어 응답 나오면 성공.

⚠️ 에러:
- `Authentication failed` → ANTHROPIC_API_KEY 잘못
- `insufficient_quota` → Claude API 결제 충전 부족
- `model_not_found` → 모델 이름 오타 (위 정확)

### 7.2 Telegram Bot 테스트

```bash
python3 -c "
import os
import requests
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
data = {'chat_id': chat_id, 'text': '🚀 Investing Agent v2 셋업 테스트 — Step 4 완료!'}
response = requests.post(url, data=data)
print(response.json())
"
```

→ 본인 텔레그램에 메시지 도착하면 성공.

⚠️ 에러:
- `Bad Request: chat not found` → TELEGRAM_CHAT_ID 잘못 (본인 user ID 다시 확인 — @userinfobot)
- `Unauthorized` → TELEGRAM_BOT_TOKEN 잘못
- 메시지 안 옴 → 본인이 봇한테 `/start` 안 보낸 경우

### 7.3 Yahoo Finance 테스트 (미국 주식)

```bash
python3 -c "
import yfinance as yf
ticker = yf.Ticker('GEV')
info = ticker.info
print(f\"GE Vernova: \${info.get('currentPrice', 'N/A')}\")
"
```

→ `GE Vernova: $XXX.XX` 같이 가격 출력되면 성공.

### 7.4 pykrx 테스트 (한국 주식)

```bash
python3 -c "
from pykrx import stock
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
df = stock.get_market_ohlcv_by_date(yesterday, yesterday, '298040')
print('효성중공업:')
print(df)
"
```

→ 효성중공업 OHLCV 데이터 출력.

⚠️ 에러:
- `EmptyDataError` → 어제가 휴장일. 최근 거래일로 변경 시도

- [ ] Claude API 응답 성공
- [ ] Telegram 메시지 도착
- [ ] Yahoo Finance 가격 출력
- [ ] pykrx 데이터 출력

---

## 8. Step 4 완료 ✅

다음 모두 ✅ 면 Step 5 진행:

- [ ] EC2 시스템 업데이트·보안 강화
- [ ] Python·pip·venv 설치
- [ ] GitHub repo 클론
- [ ] venv 생성·활성화
- [ ] 모든 패키지 설치
- [ ] .env 파일에 API 키 보관
- [ ] 4가지 연결 테스트 모두 성공

---

## 트러블슈팅

### `git clone` 시 "Authentication failed"
- Personal Access Token (PAT) 사용 필수 (Step 2 의 섹션 7)
- 본인 GitHub 비밀번호 입력 X. PAT 토큰 입력.

### `pip install` 너무 느림 또는 실패
- 일시적 네트워크 문제. 재시도.
- 또는 `pip install --upgrade pip` 먼저 다시 실행.

### `nano` 사용법 모름
- 입력: 일반 키보드처럼
- 저장: `Ctrl + O` → Enter
- 종료: `Ctrl + X`
- 잘못 입력 시: `Ctrl + K` (현재 줄 삭제)
- 다른 에디터 선호: `sudo apt install -y vim` 후 `vim .env`

### Claude API 테스트 시 model 에러
- 모델 이름 변경 가능. `claude-sonnet-4-5-20250929` 또는 최신.
- https://docs.claude.com/en/docs/about-claude/models 에서 현재 모델 확인.

### Telegram chat_id 못 찾음
- @userinfobot 에서 본인 user ID 확인 (숫자만)
- 본인이 봇한테 `/start` 메시지 보낸 적 있어야 함
- 또는 봇 https://api.telegram.org/bot[TOKEN]/getUpdates 호출하면 본인 chat_id 확인 가능

### pykrx 한국 주식 안 됨
- 한국 시간 휴장일 (주말·공휴일)
- 최근 평일로 변경: `yesterday` 변수의 날짜 변경

### .env 파일에 한글 들어감
- 영문·숫자만 사용. 한글 X.

---

## 본인이 지금 가진 것 정리

```
=== Step 4 완료 시점 ===

[EC2 안에]
- Ubuntu 시스템 업데이트 완료
- Python 3.X + pip + venv
- 시스템 파일 클론 (~/investing-agent-v2/)
- venv 활성화 상태
- 모든 패키지 설치
- .env 파일 (모든 API 키)

[테스트 완료]
- Claude API 작동
- Telegram Bot 작동
- 미국 주식 데이터 작동
- 한국 주식 데이터 작동

[준비된 다음]
- Step 5: Telegram Bot 의 명령어 연결 (선택적)
- Step 6: 메인 다이제스트 스크립트 작성
```

---

## 완료 후

본인이 위 ✅ 다 했으면:
> "Step 4 완료. Step 5 진행."

또는 막힌 부분 있으면:
> "Step 4 의 X.X 에서 막힘. 에러: [에러 메시지]"

다음 Step 5 (Telegram Bot 명령어 연결 — 선택적) 또는 직접 Step 6 (메인 스크립트) 안내 드립니다.

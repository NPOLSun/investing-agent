# Step 1 — Pre-flight Checklist

> 본격 셋업 들어가기 전에 본인이 *준비물* 다 갖추는 단계.
> 여기 막히면 뒤 단계 다 막힘. **꼼꼼히 한 번에 끝내기**.
> 예상 시간: 30분

---

## 1. 계정 확인 (5분)

### 1.1 AWS 계정
- [ ] 계정 로그인 가능 (https://console.aws.amazon.com)
- [ ] 결제 카드 등록되어 있음 (개인 카드)
- [ ] **Region 확인**: 본인은 한국 거주, **서울 리전 (ap-northeast-2)** 사용 권장
  - 콘솔 우측 상단에서 "Asia Pacific (Seoul)" 선택
  - 한국 거주자가 미국 리전 쓰면 latency 커서 cron 실행 시 약간 느림

### 1.2 GitHub 계정
- [ ] 계정 로그인 가능 (https://github.com)
- [ ] 없으면 신규 가입 (무료)

### 1.3 텔레그램
- [ ] 본인 텔레그램 앱 설치
- [ ] 본인 텔레그램 user ID 알아내기:
  1. 텔레그램에서 `@userinfobot` 검색
  2. `/start` 입력
  3. 표시되는 user ID 메모 (예: `123456789`)
  - **이 ID 가 나중에 봇이 본인에게 메시지 보낼 때 사용**

---

## 2. API 키 발급 (15분)

### 2.1 Claude API 키 ★ 가장 중요
1. https://console.anthropic.com 접속
2. 우측 상단 본인 계정 → "API Keys"
3. "Create Key" 클릭
4. 이름 입력 (예: "investing-agent-v2")
5. 키 생성됨 → **복사해서 메모장에 저장** (다시 못 봄)
6. **결제 카드 등록** (Billing → Add payment method)
   - 개인 카드 사용
   - 최초 $5~10 credit 충전 권장 (테스트용)
   - Auto-reload 안 켜는 게 안전 (예상 못 한 청구 방지)

**예상 비용**: Track 1 일간만 작동 시 **월 $5~15** (Sonnet 4.6 기준)

- [ ] Claude API 키 발급 완료
- [ ] 결제 카드 등록 완료
- [ ] 초기 credit $10 충전 완료
- [ ] 키를 안전한 곳에 메모 (절대 외부 노출 X)

### 2.2 NewsAPI 키 (무료 tier)
1. https://newsapi.org 접속
2. "Get API Key" 클릭
3. 가입 후 키 발급
4. **무료 tier 제한**: 100 requests/일, 비상업 용도

- [ ] NewsAPI 키 발급 완료
- [ ] 키 메모

### 2.3 Telegram Bot 생성
1. 텔레그램에서 `@BotFather` 검색
2. `/newbot` 입력
3. 봇 이름 입력 (예: "Investing Agent Bot")
4. 봇 username 입력 (예: "your_investing_agent_bot" - 반드시 `_bot` 으로 끝나야 함, unique)
5. BotFather 가 발급한 **HTTP API token** 메모 (형식: `1234567890:ABCdefGHIjklmnoPQRstuVWXyz`)

**중요**: 봇 본인 텔레그램에 추가:
1. 봇 username 검색 (`@your_investing_agent_bot`)
2. `/start` 입력
3. 본인의 user ID (위 1.3에서 메모) 가 이 봇에 인식됨

- [ ] Telegram Bot 생성 완료
- [ ] Bot API token 메모
- [ ] 본인이 봇에 `/start` 메시지 보냄 (필수)

---

## 3. 본인 PC 준비 (10분)

### 3.1 Windows Terminal 설치 (없으면)
- Microsoft Store 에서 "Windows Terminal" 검색·설치
- 또는 기본 PowerShell·CMD 사용 가능

### 3.2 SSH 클라이언트 (선택)
- Windows 10 이상: 기본 내장 SSH 사용 가능 (별도 설치 불필요)
- 추가 GUI 도구 원하면: PuTTY (https://www.putty.org)

### 3.3 텍스트 에디터
- 추천: **VS Code** (무료, https://code.visualstudio.com)
- 또는 Notepad++, Sublime Text 등
- 메모장 (Notepad) 도 가능하지만 줄바꿈 문제 발생 가능 → VS Code 권장

### 3.4 Git for Windows
- https://git-scm.com/download/win 다운로드·설치
- 설치 시 옵션 거의 다 기본값 OK
- 설치 후 PowerShell 또는 cmd 에서 `git --version` 확인

- [ ] Windows Terminal 또는 PowerShell 작동
- [ ] VS Code 설치 완료
- [ ] Git for Windows 설치 완료 (`git --version` 작동 확인)

---

## 4. 키·정보 정리 (5분)

본인 메모장 또는 안전한 곳에 다음 정리:

```
=== Investing Agent v2 — 키 메모 (절대 외부 노출 X) ===

[Claude API]
키: sk-ant-api03-XXXXXXXXXXXXXXXX
충전 잔액: $10 (2026-MM-DD 기준)

[NewsAPI]
키: XXXXXXXXXXXXXXXX
무료 tier: 100 req/일

[Telegram]
Bot username: @your_investing_agent_bot
Bot token: 1234567890:ABCdefGHIjklmnoPQRstuVWXyz
본인 user ID: 123456789

[GitHub]
계정: your_username
(repo URL은 Step 2에서 생성)

[AWS]
계정 이메일: ...
Region: ap-northeast-2 (서울)
(EC2 인스턴스 정보는 Step 3에서 생성)
```

- [ ] 모든 키·정보 안전한 곳에 메모
- [ ] **이 메모를 절대 GitHub repo 에 commit 하지 말 것** (실수 자주 발생)
- [ ] 가능하면 비밀번호 관리자 (1Password, Bitwarden) 사용

---

## 5. 시스템 파일 준비 (5분)

본 작업 완료 시점에 본인 PC 에 다음 폴더 있어야 함:

### 5.1 zip 다운로드
- 본인이 받은 `investing-agent-v2-with-digests.zip` 본인 PC 적절한 위치에 저장
- 예: `C:\Users\본인\Documents\investing-agent-v2\`

### 5.2 압축 해제
- zip 우클릭 → "Extract All" 또는 7-Zip 사용
- 결과 폴더 구조:
  ```
  C:\Users\본인\Documents\investing-agent-v2\
  ├── README.md
  ├── methodology.md
  ├── mega-change-map/
  ├── watchlist/
  ├── digests/
  ├── calendar/
  └── ...
  ```

- [ ] zip 다운로드·해제 완료
- [ ] 폴더 위치 메모

---

## 6. Pre-flight 최종 확인 ✅

다음 모두 ✅ 되었으면 Step 2 진행 가능:

- [ ] AWS 계정 로그인 가능, 결제 카드 등록, 서울 리전 확인
- [ ] GitHub 계정 로그인 가능
- [ ] 텔레그램 user ID 메모 완료
- [ ] Claude API 키 발급, $10 충전, 메모
- [ ] NewsAPI 키 발급, 메모
- [ ] Telegram Bot 생성, token 메모, 본인이 봇에 /start 함
- [ ] Windows Terminal·VS Code·Git 설치
- [ ] 모든 키 안전하게 메모 (외부 노출 안 한 곳)
- [ ] 시스템 파일 (zip 해제) 본인 PC 보관

→ 다 ✅ 면 Step 2 (GitHub repo 생성) 진행.
→ 한 개라도 ❌ 면 그것부터 해결.

---

## 트러블슈팅

### Claude API 결제 카드 등록 실패
- 한국 발급 카드 일부 (체크카드·일부 카드사) 거절 가능
- 대안: 다른 카드, 또는 PayPal 연결
- 최후의 수단: 가족·지인 카드 (본인 명의 카드 권장)

### Telegram Bot 생성 시 "username unavailable"
- 이미 사용 중인 이름. 다른 이름 시도 (예: `_investing_agent_bot_2`)

### Git for Windows 설치 후 명령 안 됨
- PowerShell·cmd 재시작 (PATH 갱신)
- 그래도 안 되면 PC 재부팅

### NewsAPI 무료 tier 너무 작음
- 100 req/일 면 충분 (Track 1 일간만 → 약 20 req/일 사용)
- 부족 시 유료 ($449/월) 또는 RSS 직접 파싱 (대안 마련)

---

## 완료 후

본인이 위 ✅ 다 했으면 Claude 에게 알려주세요:
> "Step 1 완료. Step 2 진행."

또는 막힌 부분 있으면:
> "Step 1 의 X.X 에서 막힘. 에러: [에러 메시지]"

다음 Step 2 (GitHub repo 생성) 안내 드립니다.

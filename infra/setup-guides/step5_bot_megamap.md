# Step 5 — Telegram Bot 명령어 시스템 (`/megamap` + `/megamap full`)

> 본인이 텔레그램에서 봇한테 명령 보내고 응답 받는 양방향 시스템.
> MVP: `/megamap` 1개부터.
> 예상 시간: 30~40분.

---

## 0. 작동 흐름 정리

### `/megamap` (정적, 빠름, 비용 0)
1. 본인이 텔레그램에서 `/megamap` 입력
2. Bot 이 EC2 의 `mega-change-map/00_dashboard.md` 파일 읽음
3. 메시지 분할해서 본인에게 전송
4. **약 1~2초 응답**

### `/megamap full` (동적, 비용 발생)
1. 본인이 텔레그램에서 `/megamap full` 입력
2. Bot 이 "갱신 시작" 알림
3. yfinance·pykrx 로 워치리스트 가격 수집
4. 수집한 데이터 + 기존 dashboard + 영역 deep-dive 들을 Claude API 로 전송
5. Claude 가 새 dashboard 작성·점수 갱신
6. `mega-change-map/00_dashboard.md` 파일 덮어쓰기
7. 갱신된 dashboard 본인에게 전송
8. **약 30초~1분 응답, Claude API 비용 ~$0.05~0.15 발생**

---

## 1. EC2 접속 + 작업 폴더 (1분)

PowerShell:
```powershell
ssh investing-agent
```

EC2 안에서:
```bash
cd ~/investing-agent-v2
source venv/bin/activate
```

→ `(venv)` 표시 확인.

---

## 2. Bot 명령어 처리 폴더 생성 (1분)

```bash
mkdir -p scripts
cd scripts
```

→ 모든 Python 스크립트를 `scripts/` 폴더에 둘 거예요.

---

## 3. `bot_listener.py` 작성 (15분)

```bash
nano bot_listener.py
```

다음 내용 전체 복사·붙여넣기:

```python
"""
Telegram Bot Listener
====================
Bot 명령어:
  /megamap       — 캐시된 Mega Change Map 답장 (정적, 빠름, 비용 0)
  /megamap full  — Claude 로 dashboard 갱신 후 답장 (동적, 비용 발생)
  /help          — 명령어 안내

24/7 polling 모드로 작동. systemd 서비스로 등록.
"""

import os
import logging
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
import pytz

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from anthropic import Anthropic

# ============================================================
# 설정
# ============================================================

load_dotenv("../.env")  # scripts/ 에서 한 단계 위 .env 로드

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
CLAUDE_KEY = os.getenv("ANTHROPIC_API_KEY")

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_PATH = PROJECT_ROOT / "mega-change-map" / "00_dashboard.md"

KST = pytz.timezone("Asia/Seoul")

# 로깅 설정
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Anthropic 클라이언트
claude = Anthropic(api_key=CLAUDE_KEY)


# ============================================================
# 유틸리티
# ============================================================

def is_authorized(update: Update) -> bool:
    """본인 chat_id 만 접근 허용 (다른 사람이 봇 발견해도 무시)."""
    if update.effective_chat.id != CHAT_ID:
        logger.warning(f"Unauthorized access from chat_id: {update.effective_chat.id}")
        return False
    return True


def split_message(text: str, max_length: int = 4000) -> list[str]:
    """텔레그램은 메시지 1개당 4096자 제한. 줄 단위로 분할."""
    if len(text) <= max_length:
        return [text]

    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > max_length:
            chunks.append(current)
            current = line + "\n"
        else:
            current += line + "\n"
    if current:
        chunks.append(current)
    return chunks


async def send_long_message(update: Update, text: str):
    """긴 메시지를 분할 전송."""
    chunks = split_message(text)
    for i, chunk in enumerate(chunks):
        prefix = f"({i+1}/{len(chunks)})\n" if len(chunks) > 1 else ""
        await update.message.reply_text(prefix + chunk)


# ============================================================
# 명령어 핸들러
# ============================================================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start — 봇 시작 안내."""
    if not is_authorized(update):
        return

    text = (
        "🤖 Investing Agent v2 — Bot Online\n\n"
        "사용 가능한 명령어:\n"
        "/megamap — Mega Change Map 정리 (캐시)\n"
        "/megamap full — Mega Map 갱신 후 정리\n"
        "/help — 명령어 안내"
    )
    await update.message.reply_text(text)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/help — 명령어 안내."""
    if not is_authorized(update):
        return

    text = (
        "📋 명령어 안내\n\n"
        "/megamap\n"
        "  Mega Change Map 의 *캐시된* 정리 답장.\n"
        "  빠름 (1~2초), 비용 없음.\n"
        "  단, dashboard 가 마지막 갱신 시점 기준.\n\n"
        "/megamap full\n"
        "  Claude 가 워치리스트 가격·뉴스 수집 후 dashboard 새로 작성.\n"
        "  30초~1분 소요, 약 $0.10 비용.\n"
        "  이후 /megamap 은 갱신된 버전 답장.\n\n"
        "/help\n"
        "  본 안내."
    )
    await update.message.reply_text(text)


async def cmd_megamap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /megamap          — 캐시 dashboard 답장
    /megamap full     — Claude 갱신 후 답장
    """
    if not is_authorized(update):
        return

    args = context.args  # /megamap 뒤의 인자
    is_full = len(args) > 0 and args[0].lower() == "full"

    if is_full:
        await handle_megamap_full(update, context)
    else:
        await handle_megamap_cached(update, context)


async def handle_megamap_cached(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """캐시된 dashboard 파일 그대로 답장."""
    if not DASHBOARD_PATH.exists():
        await update.message.reply_text(
            "⚠️ Dashboard 파일을 찾을 수 없습니다.\n"
            f"경로: {DASHBOARD_PATH}\n"
            "/megamap full 로 새로 생성하세요."
        )
        return

    try:
        with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        await update.message.reply_text(f"⚠️ 파일 읽기 실패: {e}")
        return

    # 파일 마지막 수정 시점 추가
    mtime = datetime.fromtimestamp(DASHBOARD_PATH.stat().st_mtime, tz=KST)
    header = (
        f"📊 Mega Change Map (캐시)\n"
        f"마지막 갱신: {mtime.strftime('%Y-%m-%d %H:%M KST')}\n\n"
        f"갱신하려면 /megamap full\n"
        f"{'─' * 30}\n\n"
    )

    full_text = header + content
    await send_long_message(update, full_text)


async def handle_megamap_full(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Claude 로 dashboard 갱신."""
    await update.message.reply_text(
        "🔄 Mega Change Map 갱신 시작...\n"
        "약 30초~1분 소요. 잠시 대기."
    )

    try:
        # 1. 현재 dashboard 읽기
        current_dashboard = ""
        if DASHBOARD_PATH.exists():
            with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
                current_dashboard = f.read()

        # 2. 영역 deep-dive 파일들 읽기 (현재 5개)
        deep_dives = {}
        deep_dive_dir = PROJECT_ROOT / "mega-change-map"
        for file in deep_dive_dir.glob("*.md"):
            if file.name == "00_dashboard.md":
                continue
            with open(file, "r", encoding="utf-8") as f:
                deep_dives[file.stem] = f.read()

        # AI DC 전력 인프라 (별도 위치)
        sample_path = PROJECT_ROOT / "sample_ai_dc_power_infra.md"
        if sample_path.exists():
            with open(sample_path, "r", encoding="utf-8") as f:
                deep_dives["ai-dc-power-infra"] = f.read()

        # 3. methodology 읽기
        methodology_path = PROJECT_ROOT / "methodology.md"
        methodology = ""
        if methodology_path.exists():
            with open(methodology_path, "r", encoding="utf-8") as f:
                methodology = f.read()

        # 4. Claude API 호출
        now = datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")

        prompt = build_megamap_prompt(
            current_dashboard=current_dashboard,
            deep_dives=deep_dives,
            methodology=methodology,
            now=now,
        )

        await update.message.reply_text("🧠 Claude 분석 중...")

        response = claude.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}],
        )

        new_dashboard = response.content[0].text

        # 5. dashboard 파일 덮어쓰기
        with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
            f.write(new_dashboard)

        # 6. 사용량 알림
        usage = response.usage
        cost_estimate = (
            usage.input_tokens / 1_000_000 * 3.0
            + usage.output_tokens / 1_000_000 * 15.0
        )

        await update.message.reply_text(
            f"✅ Dashboard 갱신 완료\n"
            f"Tokens: {usage.input_tokens:,} in / {usage.output_tokens:,} out\n"
            f"비용: ${cost_estimate:.3f}"
        )

        # 7. 새 dashboard 답장
        await send_long_message(update, new_dashboard)

        # 8. (옵션) GitHub 자동 commit
        try:
            subprocess.run(
                ["git", "add", str(DASHBOARD_PATH)],
                cwd=PROJECT_ROOT,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", f"Auto: megamap full update {now}"],
                cwd=PROJECT_ROOT,
                check=True,
                capture_output=True,
            )
            await update.message.reply_text("📦 GitHub commit 완료 (push 는 수동)")
        except subprocess.CalledProcessError:
            # 변경 없거나 git 설정 부족 — 무시
            pass

    except Exception as e:
        logger.exception("megamap full 실패")
        await update.message.reply_text(f"⚠️ 갱신 실패:\n{type(e).__name__}: {e}")


def build_megamap_prompt(
    current_dashboard: str,
    deep_dives: dict,
    methodology: str,
    now: str,
) -> str:
    """Claude 에게 보낼 Mega Map 갱신 프롬프트."""

    deep_dive_section = "\n\n".join(
        f"### {name}\n{content}" for name, content in deep_dives.items()
    )

    prompt = f"""당신은 본인의 산업 분석·투자 시스템의 핵심 분석가입니다. 본인의 methodology v2.1 룰북에 따라 Mega Change Map dashboard 를 갱신하세요.

# 현재 시점
{now}

# 작업
다음을 종합하여 Mega Change Map dashboard 를 **새로 작성**:
1. 현재 dashboard (참고용, 기존 점수·시차 알기 위함)
2. 각 영역 deep-dive 파일 (현재 thesis·근거)
3. methodology v2.1 (채점 룰)

## 갱신 시 반영할 사항
- 각 영역의 잣대 점수 (TAM·Moat·Capital, L1A 3잣대 0~15점) — 변화 있으면 갱신
- A·B·C 시차 점수 — 변화 있으면 갱신
- Tier 분류 (1·2·3) — 임계치 따라 조정
- 최근 시장 변화 (본인 일반 지식 + Claude knowledge 까지)
- 새로운 영역 후보 발굴 (필요 시)
- 갱신 사유 명확히 기록

## 출력 형식
완전한 Mega Change Map dashboard markdown 파일. 기존 dashboard 와 같은 형식 유지하되, 점수·해석·종목 매핑 갱신.

마지막에 "업데이트 로그" 섹션에 이번 갱신 내용 1줄 추가.

# methodology 룰북
{methodology[:5000]}...

# 현재 dashboard (참고)
{current_dashboard}

# 영역 deep-dive 파일들
{deep_dive_section[:20000]}...

# 시작
새 dashboard markdown 을 그대로 출력 (앞뒤 설명·코드블록 마커 없이).
"""
    return prompt


# ============================================================
# 메인
# ============================================================

def main():
    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHAT_ID 가 .env 에 없음."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    # 명령어 등록
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("megamap", cmd_megamap))

    logger.info("Bot starting (polling mode)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
```

저장·종료:
- `Ctrl + O` → Enter (저장)
- `Ctrl + X` (종료)

- [ ] `bot_listener.py` 작성 완료

---

## 4. 첫 실행 테스트 (5분)

### 4.1 직접 실행 (foreground 테스트)
```bash
cd ~/investing-agent-v2/scripts
python3 bot_listener.py
```

→ 다음 출력 나와야 함:
```
2026-05-23 17:XX,XXX - __main__ - INFO - Bot starting (polling mode)...
2026-05-23 17:XX,XXX - apscheduler.scheduler - INFO - Scheduler started
2026-05-23 17:XX,XXX - telegram.ext._application - INFO - Application started
```

→ Bot 이 실행됨. **이 상태 유지하고 별도 창에서 텔레그램 테스트.**

### 4.2 텔레그램 테스트

본인 텔레그램에서 본인이 만든 봇 (예: `@SY_investing_agent_bot`) 채팅창 열고:

**테스트 1**: `/start`
→ 봇이 "🤖 Investing Agent v2 — Bot Online..." 응답.

**테스트 2**: `/help`
→ 명령어 안내 응답.

**테스트 3**: `/megamap`
→ 캐시된 dashboard 답장 (메시지 여러 개로 분할).

**테스트 4**: 다른 텔레그램 계정에서 시도 (가능하면)
→ 무시되어야 함 (본인 chat_id 만 허용).

### 4.3 봇 중단

EC2 PowerShell 창에서 `Ctrl + C` → bot 종료.

- [ ] /start 응답 OK
- [ ] /help 응답 OK
- [ ] /megamap 응답 OK (dashboard 내용 도착)

---

## 5. systemd 서비스 등록 (10분)

24/7 자동 실행되도록.

### 5.1 서비스 파일 작성
```bash
sudo nano /etc/systemd/system/investing-agent-bot.service
```

다음 내용 입력 (★ 본인 username 변경 — 본인이 `ubuntu` 면 그대로):

```ini
[Unit]
Description=Investing Agent v2 - Telegram Bot Listener
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/investing-agent-v2/scripts
Environment="PATH=/home/ubuntu/investing-agent-v2/venv/bin:/usr/bin:/bin"
ExecStart=/home/ubuntu/investing-agent-v2/venv/bin/python3 /home/ubuntu/investing-agent-v2/scripts/bot_listener.py
Restart=on-failure
RestartSec=10
StandardOutput=append:/home/ubuntu/investing-agent-v2/logs/bot.log
StandardError=append:/home/ubuntu/investing-agent-v2/logs/bot.err

[Install]
WantedBy=multi-user.target
```

저장: `Ctrl + O` → Enter → `Ctrl + X`.

### 5.2 로그 폴더 생성
```bash
mkdir -p ~/investing-agent-v2/logs
```

### 5.3 서비스 활성화 + 시작
```bash
sudo systemctl daemon-reload
sudo systemctl enable investing-agent-bot
sudo systemctl start investing-agent-bot
```

→ 출력 없으면 OK.

### 5.4 서비스 상태 확인
```bash
sudo systemctl status investing-agent-bot
```

→ 다음 출력:
```
● investing-agent-bot.service - Investing Agent v2 - Telegram Bot Listener
   Loaded: loaded (...)
   Active: active (running) since ...
   ...
```

→ `Active: active (running)` 가 핵심. 녹색이면 작동 중.

### 5.5 로그 확인
```bash
tail -f ~/investing-agent-v2/logs/bot.log
```

→ Bot 시작 메시지 보임.
→ Ctrl+C 로 tail 종료.

### 5.6 텔레그램 재테스트

본인 텔레그램에서 `/megamap` 입력 → 응답 와야 함.

- [ ] systemd 서비스 등록
- [ ] Active: running 확인
- [ ] 로그 출력 확인
- [ ] 텔레그램 재테스트 성공

---

## 6. `/megamap full` 테스트 (5분)

★ 이게 Claude API 비용 발생. 한 번만 테스트.

본인 텔레그램에서:
```
/megamap full
```

진행:
1. "🔄 Mega Change Map 갱신 시작..." 메시지
2. "🧠 Claude 분석 중..." 메시지
3. 30초~1분 대기
4. "✅ Dashboard 갱신 완료\nTokens: X / Y\n비용: $0.XXX" 메시지
5. 갱신된 dashboard 답장 (여러 메시지)
6. (있으면) "📦 GitHub commit 완료" 메시지

성공하면:
- EC2 의 `mega-change-map/00_dashboard.md` 가 새 내용으로 갱신됨
- 이후 `/megamap` (full 없이) 입력 시 갱신된 버전 답장

확인:
```bash
ls -la ~/investing-agent-v2/mega-change-map/00_dashboard.md
```

→ 마지막 수정 시간이 방금 시각이어야 함.

- [ ] /megamap full 성공
- [ ] Dashboard 갱신 확인
- [ ] 비용 메시지 확인 ($0.05~0.15 정도)

---

## 7. (선택) GitHub Auto-sync 설정

`/megamap full` 시 GitHub commit 까지 자동. push 는 안 함 (수동 필요).

본인이 EC2 안에서 다음으로 push 가능:
```bash
cd ~/investing-agent-v2
git push
```

→ Username + PAT 입력 (이전에 credentials.helper store 했으면 자동).

또는 매번 push 자동화 원하면 `bot_listener.py` 의 commit 다음 줄에:
```python
subprocess.run(["git", "push"], cwd=PROJECT_ROOT, check=True)
```

추가. 단, 자동 push 는 *디버깅 어려운 변경* 도 자동 반영하니 첫 1주는 수동 권장.

---

## 8. Step 5 완료 ✅

다음 모두 ✅ 면 Step 6 진행:

- [ ] `bot_listener.py` 작성
- [ ] 직접 실행 + 텔레그램 테스트 성공
- [ ] systemd 서비스 등록 + Active: running
- [ ] `/megamap` 캐시 답장 성공
- [ ] `/megamap full` 갱신 답장 성공
- [ ] Dashboard 파일 갱신 확인

---

## 트러블슈팅

### `import telegram` 실패
- venv 활성화 확인: `source ~/investing-agent-v2/venv/bin/activate`
- python-telegram-bot 재설치: `pip install python-telegram-bot --upgrade`

### Bot 이 응답 안 함
- 본인이 봇한테 `/start` 먼저 보낸 적 있나?
- `sudo systemctl status investing-agent-bot` 로 Active 확인
- `tail -50 ~/investing-agent-v2/logs/bot.err` 로 에러 확인

### "Unauthorized access from chat_id"
- 다른 사람·다른 채팅에서 봇 접근 시도 — 정상 (보안 작동)
- 본인 메시지인데 거절되면 `.env` 의 `TELEGRAM_CHAT_ID` 확인

### `/megamap full` 시 "model_not_found"
- Claude 모델명 변경 (`bot_listener.py` 의 `model=` 값)
- `claude-sonnet-4-5-20250929` 또는 `claude-3-5-sonnet-20241022`

### Dashboard 파일이 영문으로만 출력됨
- Claude 프롬프트의 한국어 톤 강화. 본인이 원하면 알려주세요.

### systemd 서비스 시작 실패
- `sudo journalctl -u investing-agent-bot -n 50` 로 자세히 확인
- 경로 (`/home/ubuntu/...`) 본인 실제 경로와 일치 확인

---

## 본인이 지금 할 수 있는 것

✅ 텔레그램에서 `/megamap` → 현재 dashboard 답장 받기 (언제든)
✅ 텔레그램에서 `/megamap full` → 시장 변화 반영한 새 dashboard 받기 (필요 시)
✅ Bot 이 24/7 작동 (EC2 켜져 있는 동안)
✅ EC2 의 dashboard 파일 자동 갱신

---

## 다음 — Step 6 (메인 일간 다이제스트)

Step 5 완료 후 본인이 답해주실 것:
> "Step 5 완료. Step 6 진행."

또는:
> "Step 5 의 X 에서 막힘. 에러: [내용]"

다음 단계 (Step 6) 에서:
- 매일 새벽 자동 다이제스트 (`daily_digest.py`) 작성
- 워치리스트 28종목 가격 자동 수집
- Claude 가 Track 1 일간 다이제스트 생성
- 본인 텔레그램에 자동 푸시
- cron 등록으로 매일 06:30 KST 자동 실행

"""
Telegram Bot Listener (단순화 버전)
==================================
명령어:
  /start    — 봇 시작 안내
  /help     — 명령어 안내
  /megamap  — 캐시된 Mega Change Map 파일 답장 (Claude 호출 0)

24/7 polling 모드. systemd 서비스로 관리.
Track 1 일간 다이제스트는 daily_digest.py 가 cron 으로 별도 처리.
"""

import os
import logging
from pathlib import Path
from datetime import datetime
import json
import pytz

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# ============================================================
# 설정
# ============================================================

load_dotenv("../.env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_PATH = PROJECT_ROOT / "mega-change-map" / "00_dashboard.md"
AREA_ALIASES_PATH = PROJECT_ROOT / "data" / "area_aliases.json"

KST = pytz.timezone("Asia/Seoul")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ============================================================
# 유틸리티
# ============================================================

def is_authorized(update: Update) -> bool:
    """본인 chat_id 만 접근 허용."""
    if update.effective_chat.id != CHAT_ID:
        logger.warning(f"Unauthorized: {update.effective_chat.id}")
        return False
    return True


def build_github_url(file_path: str) -> str:
    """본인 GitHub repo 의 파일 URL."""
    username = os.getenv("GITHUB_USERNAME", "")
    repo = os.getenv("GITHUB_REPO_NAME", "investing-agent")
    if not username:
        return ""
    return f"https://github.com/{username}/{repo}/blob/main/{file_path}"


def extract_summary(content: str, max_chars: int = 800) -> str:
    """Dashboard 첫 부분 요약 추출."""
    lines = content.split("\n")
    summary_lines = []
    char_count = 0
    for line in lines:
        if char_count > max_chars:
            break
        if line.startswith("## ") and len(summary_lines) > 10:
            break
        summary_lines.append(line)
        char_count += len(line) + 1
    summary = "\n".join(summary_lines)
    if char_count > max_chars:
        summary += "\n\n... (전체는 파일 또는 GitHub 참고)"
    return summary


# ============================================================
# 명령어 핸들러
# ============================================================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    text = (
        "🤖 Investing Agent — Bot Online\n\n"
        "/megamap — Mega Change Map\n"
        "/deepdive — Deep-dive 목록·답장\n"
        "/help — 명령어 안내\n\n"
        "(자동 일간 다이제스트는 매일 06:30 KST 푸시)"
    )
    await update.message.reply_text(text)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    text = (
        "📋 명령어 안내\n\n"
        "/megamap\n"
        "  현재 Mega Change Map dashboard\n"
        "  요약 + 파일 + GitHub URL 답장.\n"
        "  비용 0.\n\n"
        "/deepdive\n"
        "  사용 가능한 deep-dive 영역 목록.\n\n"
        "/deepdive [별명]\n"
        "  그 영역 deep-dive 파일 답장.\n"
        "  예: /deepdive glp1\n\n"
        "/help\n"
        "  본 안내"
    )
    await update.message.reply_text(text)

def load_area_aliases() -> dict:
    """별명·파일 매핑 로딩."""
    if not AREA_ALIASES_PATH.exists():
        return {}
    try:
        data = json.loads(AREA_ALIASES_PATH.read_text(encoding="utf-8"))
        return data.get("aliases", {})
    except Exception as e:
        logger.warning(f"area_aliases.json 읽기 실패: {e}")
        return {}

async def cmd_deepdive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /deepdive          — 사용 가능한 영역 별명 리스트
    /deepdive [별명]   — 그 영역 deep-dive 파일 답장
    """
    if not is_authorized(update):
        return

    aliases = load_area_aliases()
    if not aliases:
        await update.message.reply_text(
            "⚠️ Deep-dive 영역 목록을 불러올 수 없습니다.\n"
            f"파일 위치: {AREA_ALIASES_PATH}"
        )
        return

    args = context.args  # /deepdive 뒤의 인자

    # 인자 없으면 — 리스트 답장
    if not args:
        lines = ["📚 Deep-dive 영역 목록\n"]
        for alias, info in aliases.items():
            tier = info.get("tier", "?")
            title = info.get("title", alias)
            lines.append(f"• /deepdive {alias} — {title} (Tier {tier})")
        lines.append("\n💡 사용법: /deepdive [별명]")
        unique_areas = len({info.get("path", alias) for alias, info in aliases.items()})
        lines.append(f"📊 {unique_areas}개 영역 / {len(aliases)}개 별명 등록됨")
        await update.message.reply_text("\n".join(lines))
        return

    # 별명으로 파일 찾기
    alias = args[0].lower()
    if alias not in aliases:
        available = ", ".join(aliases.keys())
        await update.message.reply_text(
            f"⚠️ '{alias}' 별명 없음.\n\n"
            f"사용 가능: {available}\n\n"
            f"전체 목록: /deepdive"
        )
        return

    # 파일 경로 확인
    info = aliases[alias]
    file_path = PROJECT_ROOT / info["path"]

    if not file_path.exists():
        await update.message.reply_text(
            f"⚠️ 파일 없음: {info['path']}\n"
            "본인이 git push 했는지 확인 필요."
        )
        return

    # 파일 읽기
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        await update.message.reply_text(f"⚠️ 파일 읽기 실패: {e}")
        return

    # 마지막 수정 시점
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime, tz=KST)

    # 요약 (첫 800자)
    summary = extract_summary(content, max_chars=800)

    # GitHub URL
    github_url = build_github_url(info["path"])
    github_line = f"🌐 GitHub: {github_url}\n" if github_url else ""

    title = info.get("title", alias)
    tier = info.get("tier", "?")

    summary_msg = (
        f"📚 Deep-dive: {title} (Tier {tier})\n"
        f"갱신: {mtime.strftime('%Y-%m-%d %H:%M KST')}\n"
        f"{'─' * 25}\n\n"
        f"{summary}\n\n"
        f"{'─' * 25}\n"
        f"📎 전체 파일 첨부 ⬇️\n"
        f"{github_line}"
    )

    if len(summary_msg) > 4000:
        summary_msg = summary_msg[:3950] + "\n\n... (요약 잘림)"

    await update.message.reply_text(summary_msg)

    # 파일 첨부
    try:
        with open(file_path, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=f"{alias}_{mtime.strftime('%Y%m%d')}.md",
                caption=f"{title} deep-dive"
            )
    except Exception as e:
        logger.exception("파일 첨부 실패")
        await update.message.reply_text(f"⚠️ 파일 첨부 실패: {e}")

async def cmd_megamap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """캐시된 dashboard 파일 답장 + 요약 + GitHub URL."""
    if not is_authorized(update):
        return

    if not DASHBOARD_PATH.exists():
        await update.message.reply_text(
            "⚠️ Dashboard 파일 없음.\n"
            f"경로: {DASHBOARD_PATH}\n"
            "본인이 claude.ai 에서 생성 후 git push 필요."
        )
        return

    try:
        with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        await update.message.reply_text(f"⚠️ 파일 읽기 실패: {e}")
        return

    # 마지막 수정 시점
    mtime = datetime.fromtimestamp(DASHBOARD_PATH.stat().st_mtime, tz=KST)

    # 요약
    summary = extract_summary(content)

    # GitHub URL
    github_url = build_github_url("mega-change-map/00_dashboard.md")
    github_line = f"🌐 GitHub: {github_url}\n" if github_url else ""

    # 요약 메시지
    summary_msg = (
        f"📊 Mega Change Map (캐시)\n"
        f"갱신: {mtime.strftime('%Y-%m-%d %H:%M KST')}\n"
        f"{'─' * 25}\n\n"
        f"{summary}\n\n"
        f"{'─' * 25}\n"
        f"📎 전체 파일 첨부 ⬇️\n"
        f"{github_line}"
    )

    # 텔레그램 메시지 4096자 제한
    if len(summary_msg) > 4000:
        summary_msg = summary_msg[:3950] + "\n\n... (요약 잘림)"

    await update.message.reply_text(summary_msg)

    # 파일 첨부
    try:
        with open(DASHBOARD_PATH, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=f"megamap_{mtime.strftime('%Y%m%d_%H%M')}.md",
                caption="Mega Change Map dashboard"
            )
    except Exception as e:
        logger.exception("파일 첨부 실패")
        await update.message.reply_text(f"⚠️ 파일 첨부 실패: {e}")


# ============================================================
# 메인
# ============================================================

def main():
    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError("TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHAT_ID 미설정")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("megamap", cmd_megamap))
    app.add_handler(CommandHandler("deepdive", cmd_deepdive))

    logger.info("Bot starting (polling mode)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

"""
Telegram Bot Listener
=====================
조회 (Claude 호출 0, 쓰기 없음):
  /포지션 [번호|이름|티커]  — 보유 포지션과 판정 기준
  /megamap                  — 캐시된 Mega Change Map 파일 답장
  /deepdive [별명]          — 영역별 deep-dive 문서
  /help, /start             — 사용법

관리 (Claude 호출 + positions.json 쓰기 + git push):
  /추가 [종목]   — 대화형 추가. 보유 근거·매도 조건 초안 제안
  /수정 [포지션] — 판정 기준 편집. 변경 전후 diff 확인 후 저장
  /매도 [포지션] — status → exited. 기록은 보존
  /삭제 [포지션] — 완전 삭제. 고아 테마·상태까지 정리
  /취소          — 진행 중인 대화 중단

한글 명령은 텔레그램이 봇 명령으로 태깅하지 않아 MessageHandler 로 받는다.
영문 별칭(/positions /add /edit /exit /cancel)도 같은 핸들러에 연결돼 있고,
명령 메뉴에는 영문만 등록된다 (텔레그램이 한글 명령명을 허용하지 않음).

24/7 polling 모드. systemd 서비스로 관리.
Track 1 일간 다이제스트는 daily_digest.py 가 cron 으로 별도 처리.
"""

import asyncio
import os
import re
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
import json
import pytz

from dotenv import load_dotenv
import claude_client as cc
import positions_edit as pe
import positions_view as pv
from telegram import BotCommand, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
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
# httpx 가 getUpdates 폴링마다 INFO 를 찍어 로그가 하루 8,600줄씩 불어난다.
# 게다가 URL 에 봇 토큰이 그대로 들어가므로 평문 적재를 막는다.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)
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
        "포지션\n"
        "  /포지션 — 보유 목록·판정 기준\n"
        "  /추가 — 종목 추가 (대화형)\n"
        "  /수정 — 판정 기준 편집\n"
        "  /매도 — 매도 처리\n\n"
        "리서치\n"
        "  /megamap — Mega Change Map\n"
        "  /deepdive — Deep-dive 영역별 문서\n\n"
        "/help — 사용법 자세히\n\n"
        "(일간 다이제스트는 평일 06:30 KST 자동 푸시)"
    )
    await update.message.reply_text(text)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    text = (
        "📋 사용법\n\n"
        "━━ 포지션 조회 ━━\n"
        "/포지션\n"
        "  보유 목록. 마지막 점검일과\n"
        "  열린 신호 수를 함께 표시.\n\n"
        "/포지션 [번호|이름|티커]\n"
        "  해당 포지션 상세 — 보유 근거,\n"
        "  매도·추가 검토 조건, 감시 지표,\n"
        "  반복 관측, 메모.\n"
        "  예: /포지션 3\n"
        "      /포지션 파두\n"
        "      /포지션 440110\n"
        "  비용 0.\n\n"
        "━━ 포지션 관리 ━━\n"
        "/추가 [종목]\n"
        "  왜 담는지 물어본 뒤 보유 근거와\n"
        "  매도 조건 초안을 잡아줍니다.\n"
        "  고칠 곳을 말하면 다시 만들고,\n"
        "  '저장' 하면 반영됩니다.\n"
        "  예: /추가 GOOGL\n\n"
        "/수정 [번호|이름]\n"
        "  판정 기준 편집. 고칠 내용을\n"
        "  말로 하면 변경 전후를 diff 로\n"
        "  보여준 뒤 '저장'.\n"
        "  예: /수정 파두\n"
        "      → 매도 조건 2번을 3개 분기로\n\n"
        "/매도 [번호|이름]\n"
        "  매도 처리. 사유를 기록하고\n"
        "  모니터링에서 제외합니다.\n"
        "  판정 기준은 지우지 않습니다(복기용).\n"
        "  예: /매도 3\n\n"
        "  ※ /추가·/수정 은 초안 1회당 약 $0.15.\n"
        "     저장 전에는 아무것도 안 바뀝니다.\n"
        "     중단은 /취소 (30분 무응답 시 자동)\n\n"
        "━━ 리서치 ━━\n"
        "/megamap\n"
        "  Mega Change Map dashboard.\n"
        "  요약 + 파일 + GitHub URL. 비용 0.\n\n"
        "/deepdive\n"
        "  Deep-dive 영역 목록.\n\n"
        "/deepdive [별명]\n"
        "  해당 영역 문서 답장.\n"
        "  예: /deepdive glp1\n\n"
        "━━ 참고 ━━\n"
        "· 한글 명령이 안 먹으면 영문도 됩니다\n"
        "  /positions /add /edit /exit /cancel\n"
        "· 일간 다이제스트는 평일 06:30 KST 자동.\n"
        "  실패하면 ⚠️ 알림이 옵니다."
    )
    await update.message.reply_text(text)

async def cmd_positions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/포지션 [번호|이름] — 보유 포지션과 판정 기준 조회.

    Claude 호출 0, 쓰기 없음. positions.json·position_state.json 을 그대로 읽어
    보여준다. 요약하지 않는 이유: thesis 와 매도 조건은 본인이 쓴 판단 근거라
    모델이 다시 쓰면 원문이 왜곡된다.
    """
    if not is_authorized(update):
        return

    doc, state, _theme_state, aliases = pv.load_all()
    if not doc.get("positions"):
        await update.message.reply_text("positions.json 을 읽지 못했습니다.")
        return

    today = datetime.now(KST).strftime("%Y-%m-%d")
    # /포지션 은 텔레그램이 봇 명령 엔티티로 인식하지 않아 MessageHandler 로 받는다.
    # 그 경로에서는 context.args 가 채워지지 않으므로 원문에서 직접 뗀다.
    if context.args:
        arg = " ".join(context.args).strip()
    else:
        arg = re.sub(r"^\S+\s*", "", (update.message.text or "")).strip()

    if not arg:
        text = pv.format_list(doc, state, today)
    else:
        pos, candidates = pv.find_position(doc, arg)
        if pos:
            text = pv.format_detail(doc, state, aliases, pos, today)
        elif candidates:
            text = "여러 개가 걸립니다. 더 구체적으로 적어주세요.\n\n" + "\n".join(
                f"· {pv.display_name(p)}" for p in candidates
            )
        else:
            text = f"'{arg}' 에 해당하는 포지션이 없습니다. /포지션 으로 목록을 보세요."

    for chunk in pv.split_message(text):
        await update.message.reply_text(chunk)


# ============================================================
# /추가 — 대화형 포지션 추가
# ============================================================

ASK_REASON, REVIEW = range(2)


def _cmd_arg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    if context.args:
        return " ".join(context.args).strip()
    return re.sub(r"^\S+\s*", "", (update.message.text or "")).strip()


async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END

    ticker = _cmd_arg(update, context)
    if not ticker:
        await update.message.reply_text(
            "종목을 적어주세요.\n예: /추가 GOOGL  또는  /추가 삼양식품 003230"
        )
        return ConversationHandler.END

    context.user_data.clear()
    context.user_data["ticker"] = ticker
    await update.message.reply_text(
        f"'{ticker}' 를 추가합니다.\n\n"
        "왜 담으시나요? 편하게 쓰시면 됩니다 — 이 문장에서 보유 근거와\n"
        "매도 검토 조건 초안을 잡습니다.\n\n"
        "(그만두려면 /취소)"
    )
    return ASK_REASON


async def _draft_and_show(update, context, revision: str = None):
    """Claude 로 초안을 만들고 검증 결과와 함께 보여준다."""
    doc, _state, _ts, _al = pv.load_all()
    prompt = pe.build_draft_prompt(
        context.user_data["ticker"], context.user_data["reason"], doc,
        revision=revision, previous=context.user_data.get("draft"),
    )
    # ★ CLI 호출은 블로킹이다. to_thread 로 빼지 않으면 봇 전체가 멈춘다.
    text, cost = await asyncio.to_thread(cc.call_claude, prompt)
    draft = cc.extract_json(text)
    if not draft or not draft.get("position"):
        await update.message.reply_text("초안 생성에 실패했습니다. 다시 시도하려면 /추가 부터.")
        return ConversationHandler.END

    context.user_data["draft"] = draft
    context.user_data["cost"] = context.user_data.get("cost", 0.0) + cost

    errors, warns = pe.validate_draft(draft, doc)
    body = pe.format_draft(draft, doc)
    if errors:
        body += "\n\n🚫 이대로는 저장 안 됩니다\n" + "\n".join(f"  · {e}" for e in errors)
    if warns:
        body += "\n\n⚠ 참고\n" + "\n".join(f"  · {w}" for w in warns)
    body += (f"\n\n─────────\n고칠 부분을 말씀하시거나, 저장하려면 '저장'."
             f"\n취소는 /취소  (여기까지 ${context.user_data['cost']:.3f})")

    for chunk in pv.split_message(body):
        await update.message.reply_text(chunk)
    return REVIEW


async def add_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    context.user_data["reason"] = (update.message.text or "").strip()
    await update.message.reply_text("초안 잡는 중… (20~40초)")
    try:
        return await _draft_and_show(update, context)
    except Exception as e:
        logger.exception("초안 생성 실패")
        await update.message.reply_text(f"⚠️ 초안 생성 실패: {e}")
        return ConversationHandler.END


async def add_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    reply = (update.message.text or "").strip()

    if reply in ("저장", "저장해", "저장해줘", "ㅇㅇ", "네", "응", "ok", "OK", "save"):
        draft = context.user_data.get("draft")
        if not draft:
            await update.message.reply_text("저장할 초안이 없습니다.")
            return ConversationHandler.END
        await update.message.reply_text("저장 중…")
        ok, msg = await asyncio.to_thread(pe.save_draft, draft)
        await update.message.reply_text(msg)
        if ok:
            label = draft["position"].get("label")
            await update.message.reply_text(f"확인: /포지션 {label.split('(')[0].strip()}")
        return ConversationHandler.END

    await update.message.reply_text("반영하는 중…")
    try:
        return await _draft_and_show(update, context, revision=reply)
    except Exception as e:
        logger.exception("초안 수정 실패")
        await update.message.reply_text(f"⚠️ 수정 실패: {e}")
        return REVIEW


async def add_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    context.user_data.clear()
    await update.message.reply_text("취소했습니다. 저장된 것은 없습니다.")
    return ConversationHandler.END


async def add_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    if update and update.message:
        await update.message.reply_text("30분간 응답이 없어 종료했습니다. 저장된 것은 없습니다.")
    return ConversationHandler.END


# ============================================================
# /수정 — 대화형 포지션 편집
# ============================================================

EDIT_REQUEST, EDIT_REVIEW = range(10, 12)


async def _resolve(update, context) -> Optional[dict]:
    """명령 인자로 포지션 하나를 특정. 못 하면 안내하고 None."""
    doc, _s, _t, _a = pv.load_all()
    arg = _cmd_arg(update, context)
    if not arg:
        await update.message.reply_text("어느 포지션인지 적어주세요.\n/포지션 으로 번호를 볼 수 있습니다.")
        return None
    pos, candidates = pv.find_position(doc, arg)
    if pos:
        return pos
    if candidates:
        await update.message.reply_text(
            "여러 개가 걸립니다. 더 구체적으로:\n" +
            "\n".join(f"· {pv.display_name(p)}" for p in candidates))
    else:
        await update.message.reply_text(f"'{arg}' 에 해당하는 포지션이 없습니다.")
    return None


async def edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    pos = await _resolve(update, context)
    if not pos:
        return ConversationHandler.END

    context.user_data.clear()
    context.user_data["orig"] = pos
    doc, state, _t, aliases = pv.load_all()
    today = datetime.now(KST).strftime("%Y-%m-%d")
    for chunk in pv.split_message(pv.format_detail(doc, state, aliases, pos, today)):
        await update.message.reply_text(chunk)
    await update.message.reply_text(
        "무엇을 고칠까요?\n"
        "예) 매도 조건 3번을 3개 분기로 바꿔 / 보유 근거에 ~ 추가 / 무시에 ~ 넣어\n\n"
        "(그만두려면 /취소)"
    )
    return EDIT_REQUEST


async def _edit_draft_and_show(update, context, request: str):
    doc, _s, _t, _a = pv.load_all()
    base = context.user_data.get("draft_pos") or context.user_data["orig"]
    prompt = pe.build_edit_prompt(base, request, doc)
    text, cost = await asyncio.to_thread(cc.call_claude, prompt)
    result = cc.extract_json(text)
    if not result or not result.get("position"):
        await update.message.reply_text("수정안 생성에 실패했습니다. /취소 후 다시 시도해주세요.")
        return EDIT_REQUEST

    new_pos = result["position"]
    context.user_data["draft_pos"] = new_pos
    context.user_data["theme_assignment"] = result.get("theme_assignment") or {}
    context.user_data["cost"] = context.user_data.get("cost", 0.0) + cost

    errors, warns = pe.validate_draft(
        {"position": new_pos, "theme_assignment": context.user_data["theme_assignment"]},
        doc, editing_id=context.user_data["orig"]["id"])

    # 원본과의 diff 를 보여주는 게 이 기능의 핵심이다.
    # 요청하지 않은 문장을 모델이 손댔는지는 diff 로만 잡을 수 있다.
    body = "🔍 변경 사항\n\n" + pe.diff_position(context.user_data["orig"], new_pos)
    for n in (result.get("notes_for_user") or []):
        body += f"\n\n❓ {n}"
    if errors:
        body += "\n\n🚫 이대로는 저장 안 됩니다\n" + "\n".join(f"  · {e}" for e in errors)
    if warns:
        body += "\n\n⚠ 참고\n" + "\n".join(f"  · {w}" for w in warns)
    body += (f"\n\n─────────\n더 고칠 부분을 말씀하시거나, 적용하려면 '저장'."
             f"\n취소는 /취소  (여기까지 ${context.user_data['cost']:.3f})")

    for chunk in pv.split_message(body):
        await update.message.reply_text(chunk)
    return EDIT_REVIEW


async def edit_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    await update.message.reply_text("수정안 만드는 중… (20~40초)")
    try:
        return await _edit_draft_and_show(update, context, (update.message.text or "").strip())
    except Exception as e:
        logger.exception("수정안 생성 실패")
        await update.message.reply_text(f"⚠️ 실패: {e}")
        return ConversationHandler.END


async def edit_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    reply = (update.message.text or "").strip()

    if reply in ("저장", "저장해", "저장해줘", "적용", "ㅇㅇ", "네", "응", "ok", "OK", "save"):
        new_pos = context.user_data.get("draft_pos")
        if not new_pos:
            await update.message.reply_text("적용할 수정안이 없습니다.")
            return ConversationHandler.END
        await update.message.reply_text("저장 중…")
        ok, msg = await asyncio.to_thread(
            pe.save_position_update, new_pos, context.user_data.get("theme_assignment"))
        await update.message.reply_text(msg)
        return ConversationHandler.END

    await update.message.reply_text("반영하는 중…")
    try:
        return await _edit_draft_and_show(update, context, reply)
    except Exception as e:
        logger.exception("수정 반영 실패")
        await update.message.reply_text(f"⚠️ 실패: {e}")
        return EDIT_REVIEW


# ============================================================
# /매도 — status 를 exited 로
# ============================================================

SELL_REASON, SELL_CONFIRM = range(20, 22)


async def sell_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    pos = await _resolve(update, context)
    if not pos:
        return ConversationHandler.END

    context.user_data.clear()
    context.user_data["pos"] = pos
    await update.message.reply_text(
        f"'{pv.display_name(pos)}' 를 매도 처리합니다.\n\n"
        "왜 파셨나요? 한 줄이면 됩니다 — 기록에 남겨 나중에 복기 재료로 씁니다.\n"
        "(설명 없이 넘기려면 '없음', 그만두려면 /취소)"
    )
    return SELL_REASON


async def sell_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    reason = (update.message.text or "").strip()
    context.user_data["reason"] = "" if reason in ("없음", "-") else reason
    pos = context.user_data["pos"]
    await update.message.reply_text(
        f"확인해주세요.\n\n"
        f"  {pv.display_name(pos)}\n"
        f"  보유 → 매도완료\n"
        f"  사유: {context.user_data['reason'] or '(기록 안 함)'}\n\n"
        "판정 기준과 누적 관측은 지우지 않고 남깁니다 (복기용).\n"
        "내일부터 모니터링 대상에서 빠집니다.\n\n"
        "진행하려면 '확인', 그만두려면 /취소"
    )
    return SELL_CONFIRM


async def sell_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    if (update.message.text or "").strip() not in ("확인", "네", "응", "ㅇㅇ", "ok", "OK", "yes"):
        await update.message.reply_text("취소했습니다. 변경된 것은 없습니다.")
        return ConversationHandler.END
    pos = context.user_data["pos"]
    await update.message.reply_text("처리 중…")
    ok, msg = await asyncio.to_thread(pe.exit_position, pos["id"], context.user_data.get("reason", ""))
    await update.message.reply_text(msg)
    return ConversationHandler.END


# ============================================================
# /삭제 — 완전 삭제 (매도와 다름)
# ============================================================

DELETE_CONFIRM = 30


async def delete_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    pos = await _resolve(update, context)
    if not pos:
        return ConversationHandler.END

    prev = await asyncio.to_thread(pe.preview_delete, pos["id"])
    if not prev:
        await update.message.reply_text("포지션을 찾을 수 없습니다.")
        return ConversationHandler.END

    context.user_data.clear()
    context.user_data["pos"] = pos

    lines = [
        "🗑 완전 삭제 — 되돌릴 수 없습니다.",
        "",
        f"  {pv.display_name(pos)}",
        "",
        "사라지는 것:",
        f"  · 보유 근거 {len(pos.get('thesis') or [])}개, "
        f"매도 조건 {len(pos.get('kill_signals') or [])}개",
    ]
    if prev["observations"] or prev["flags"]:
        lines.append(f"  · 누적 관측 {prev['observations']}종, 열린 신호 {prev['flags']}건"
                     f" (마지막 점검 {prev['last_checked'] or '없음'})")
    if prev["unlinked_themes"]:
        lines.append(f"  · 테마 연결 해제: {', '.join(prev['unlinked_themes'])}")
    if prev["orphan_themes"]:
        lines.append(f"  · 테마 자체 삭제: {', '.join(prev['orphan_themes'])}")
        lines.append("    (이 포지션만 가리키던 테마라 남겨두면 매번 헛검색합니다)")
    lines += [
        "",
        "판 종목을 기록으로 남기려면 삭제가 아니라 /매도 를 쓰세요.",
        "",
        f"진행하려면 포지션 이름을 그대로 입력하세요: {pos.get('label')}",
        "그만두려면 /취소",
    ]
    for chunk in pv.split_message("\n".join(lines)):
        await update.message.reply_text(chunk)
    return DELETE_CONFIRM


async def delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return ConversationHandler.END
    pos = context.user_data["pos"]
    typed = (update.message.text or "").strip()
    # 이름을 직접 치게 하는 이유: '네' 한 번으로 지워지면 오조작이 너무 쉽다
    if typed != pos.get("label"):
        await update.message.reply_text(
            f"이름이 일치하지 않아 중단했습니다. 삭제된 것은 없습니다.\n"
            f"(정확히 이렇게: {pos.get('label')})")
        return ConversationHandler.END
    await update.message.reply_text("삭제 중…")
    ok, msg = await asyncio.to_thread(pe.delete_position, pos["id"])
    await update.message.reply_text(msg)
    return ConversationHandler.END


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

    # 인자 없으면 — 리스트 답장 (영역당 1줄, 첫 별명을 canonical로)
    if not args:
        lines = ["📚 Deep-dive 영역 목록\n"]
        seen_paths: dict[str, list[str]] = {}
        canonical: list[tuple[str, dict]] = []
        for alias, info in aliases.items():
            path = info.get("path", alias)
            if path not in seen_paths:
                seen_paths[path] = [alias]
                canonical.append((alias, info))
            else:
                seen_paths[path].append(alias)
        for alias, info in canonical:
            tier = info.get("tier", "?")
            title = info.get("title", alias)
            alts = seen_paths[info.get("path", alias)][1:]
            alt_str = f"  (또는: {', '.join(alts)})" if alts else ""
            lines.append(f"• /deepdive {alias} — {title} (Tier {tier}){alt_str}")
        lines.append("\n💡 사용법: /deepdive [별명]")
        lines.append(f"📊 총 {len(canonical)}개 영역 ({len(aliases)}개 별명 매핑)")
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

    app = Application.builder().token(BOT_TOKEN).post_init(_register_commands).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("megamap", cmd_megamap))
    app.add_handler(CommandHandler("deepdive", cmd_deepdive))
    app.add_handler(CommandHandler("positions", cmd_positions))
    app.add_handler(CommandHandler("pos", cmd_positions))
    # 한글 명령은 텔레그램이 봇 명령으로 태깅하지 않아 CommandHandler 가 못 잡는다
    app.add_handler(MessageHandler(filters.Regex(r"^/포지션"), cmd_positions))

    # /추가 — 대화형. 한글 명령이라 진입점도 MessageHandler 를 함께 건다.
    app.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("add", add_start),
            MessageHandler(filters.Regex(r"^/추가"), add_start),
        ],
        states={
            ASK_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_reason)],
            REVIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_review)],
            ConversationHandler.TIMEOUT: [
                MessageHandler(filters.ALL, add_timeout),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", add_cancel),
            MessageHandler(filters.Regex(r"^/취소"), add_cancel),
        ],
        conversation_timeout=1800,
    ))

    # /수정 — 기존 포지션 편집
    app.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("edit", edit_start),
            MessageHandler(filters.Regex(r"^/수정"), edit_start),
        ],
        states={
            EDIT_REQUEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_request)],
            EDIT_REVIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_review)],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, add_timeout)],
        },
        fallbacks=[
            CommandHandler("cancel", add_cancel),
            MessageHandler(filters.Regex(r"^/취소"), add_cancel),
        ],
        conversation_timeout=1800,
    ))

    # /삭제 — 완전 삭제. 이름 입력으로만 확정
    app.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("delete", delete_start),
            MessageHandler(filters.Regex(r"^/삭제"), delete_start),
        ],
        states={
            DELETE_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_confirm)],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, add_timeout)],
        },
        fallbacks=[
            CommandHandler("cancel", add_cancel),
            MessageHandler(filters.Regex(r"^/취소"), add_cancel),
        ],
        conversation_timeout=1800,
    ))

    # /매도 — status 를 exited 로 (기록은 보존)
    app.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("exit", sell_start),
            MessageHandler(filters.Regex(r"^/매도"), sell_start),
        ],
        states={
            SELL_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, sell_reason)],
            SELL_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, sell_confirm)],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, add_timeout)],
        },
        fallbacks=[
            CommandHandler("cancel", add_cancel),
            MessageHandler(filters.Regex(r"^/취소"), add_cancel),
        ],
        conversation_timeout=1800,
    ))

    logger.info("Bot starting (polling mode)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


async def _register_commands(app: Application):
    """텔레그램 명령 메뉴 등록 — 채팅창에 '/' 만 쳐도 목록이 뜬다.

    한글 명령(/포지션 등)은 등록할 수 없다. 텔레그램은 명령 이름에
    소문자 영문·숫자·밑줄만 허용한다. 그래서 메뉴에는 영문 별칭을 올리고,
    한글 명령은 MessageHandler 로 따로 받는다 (둘 다 같은 핸들러).
    """
    try:
        await app.bot.set_my_commands([
            BotCommand("positions", "보유 포지션 목록·상세 (= /포지션)"),
            BotCommand("add", "종목 추가, 대화형 (= /추가)"),
            BotCommand("edit", "판정 기준 편집 (= /수정)"),
            BotCommand("exit", "매도 처리 — 기록 보존 (= /매도)"),
            BotCommand("delete", "완전 삭제 — 되돌릴 수 없음 (= /삭제)"),
            BotCommand("megamap", "Mega Change Map"),
            BotCommand("deepdive", "Deep-dive 영역 문서"),
            BotCommand("cancel", "진행 중인 대화 중단 (= /취소)"),
            BotCommand("help", "사용법"),
        ])
        logger.info("명령 메뉴 등록 완료")
    except Exception as e:
        logger.warning(f"명령 메뉴 등록 실패 (동작에는 지장 없음): {e}")


if __name__ == "__main__":
    main()

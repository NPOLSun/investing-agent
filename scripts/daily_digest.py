"""
Daily Digest Generator
======================
매일 새벽 06:30 KST 자동 실행 (cron).

작동 순서:
1. 워치리스트·캘린더·dashboard·positions.json·position_state.json 로드
2. yfinance·pykrx 로 시장 데이터 수집
3. Layer 0 (포트폴리오 상위 변수) web_search 1회
4. 검색 대상 포지션 선별 (가격 ±3% / 7일 내 이벤트 / N일 미점검 rotation)
5. 선별된 포지션만 개별 web_search → RED·YELLOW·WHITE 판정
6. position_state.json 에 관측값·플래그 누적 (분기 연속 류 판정 근거)
7. 종합 호출로 일간 다이제스트 생성
8. 파일 저장 (digests/sent/YYYY-MM-DD.md)
9. 텔레그램 푸시 (요약 + 파일 첨부 + GitHub URL)

하루 API 호출: Layer 0 (1) + 선별 포지션 (0~4) + 종합 (1) = 2~6회
하루 검색: 호출당 상한(LAYER0_MAX_USES / POSITION_MAX_USES) + 총량 캡(DAILY_SEARCH_BUDGET)
"""

import os
import re
import json
import logging
import asyncio
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

import pytz
import requests
import yfinance as yf
from dotenv import load_dotenv
from anthropic import Anthropic, APIStatusError
from telegram import Bot
from telegram.constants import ParseMode

import warnings
warnings.filterwarnings("ignore")  # pykrx 경고 메시지 숨김

# 그리고 logging 부분에 추가:
logging.getLogger("pykrx").setLevel(logging.ERROR)

# pykrx 는 import 자체가 무거움 — 필요할 때만
try:
    from pykrx import stock as krx_stock
    PYKRX_AVAILABLE = True
except Exception:
    PYKRX_AVAILABLE = False


# ============================================================
# 설정
# ============================================================

load_dotenv("../.env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "investing-agent")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 경로
WATCHLIST_PATH = PROJECT_ROOT / "watchlist" / "00_first_watchlist_draft.md"
DASHBOARD_PATH = PROJECT_ROOT / "mega-change-map" / "00_dashboard.md"
CALENDAR_PATH = PROJECT_ROOT / "calendar" / "00_event_calendar_6months.md"
TEMPLATE_PATH = PROJECT_ROOT / "digests" / "templates" / "track1_daily_template.md"
TRACKED_STOCKS_PATH = PROJECT_ROOT / "data" / "tracked_stocks.json"
POSITIONS_PATH = PROJECT_ROOT / "data" / "positions.json"
POSITION_STATE_PATH = PROJECT_ROOT / "data" / "position_state.json"
DIGEST_OUTPUT_DIR = PROJECT_ROOT / "digests" / "sent"
DRY_RUN_OUTPUT_DIR = PROJECT_ROOT / "digests" / "dry-run"

KST = pytz.timezone("Asia/Seoul")

# 모델 (비용 통제 위해 Sonnet)
MODEL = "claude-sonnet-5"

# Sonnet 5 는 thinking 이 기본 ON 이며 max_tokens 가 thinking + 응답을 함께 덮음.
# 따라서 구형 3000 을 그대로 쓰면 응답이 중간에 잘림.
SEARCH_MAX_TOKENS = 8000       # 포지션별 검색 호출
SYNTHESIS_MAX_TOKENS = 16000   # 종합 호출 (TELEGRAM + FILE 전문)
SEARCH_EFFORT = "medium"       # 검색·판정용 (비용 통제)
SYNTHESIS_EFFORT = "high"      # 최종 작성용

# web_search
# _20260209 = dynamic filtering. 검색 결과를 코드로 걸러 컨텍스트에 넣으므로
# 검색이 많은 워크로드에서 입력 토큰이 크게 줄어든다 (Sonnet 4.6 / Opus 4.6 이상 필요).
# 구형 모델로 되돌릴 경우 web_search_20250305 으로 교체.
WEB_SEARCH_TOOL_TYPE = "web_search_20260209"

# max_uses 는 할당량이 아니라 천장이다. 모델은 필요한 만큼만 검색하므로
# 값을 올려도 평상시 비용은 그대로고 최악의 날만 비싸진다.
# 따라서 per-call 은 넉넉히 두고, 실제 통제는 아래 일일 총량 캡으로 한다.
LAYER0_MAX_USES = 6            # Layer 0: kill 신호 4개 + 여유
POSITION_MAX_USES = 8          # 포지션: watch.queries 4~5개 + 후속 확인 여유
DAILY_SEARCH_BUDGET = 25       # 하루 검색 총량 캡 (초과 시 남은 포지션 검색 생략)
MAX_PAUSE_CONTINUATIONS = 3    # pause_turn 재개 상한

# 모니터링 대상 status (exited·paused 는 기록만 남기고 판정 대상에서 제외)
MONITORED_STATUSES = ("holding", "watching")

# 검색 대상 선별 규칙
PRICE_MOVE_THRESHOLD = 3.0     # ±% 이상이면 검색 트리거 (내부 판단용, 출력 아님)
PRICE_DISPLAY_THRESHOLD = 5.0  # ±% 이상만 다이제스트 맨 아래 한 줄로 표기
EVENT_WINDOW_DAYS = 7          # 캘린더 이벤트 감시 창
SEARCH_ROTATION_DAYS = 14      # 이 기간 미점검이면 순번으로 강제 점검
MAX_SEARCH_POSITIONS = 4       # 하루 개별 검색 상한 (비용 캡)

# 상태 파일 관리
MAX_OBSERVATIONS = 12          # 지표당 보관할 관측 이력 개수
FLAG_EXPIRE_DAYS = 120         # 이 기간 재확인 안 된 플래그는 정리

# 단가 (USD per 1M tokens). 도입가 $2/$10 는 2026-08-31 만료라 정가 기준으로 계산
PRICE_IN_PER_MTOK = 3.0
PRICE_OUT_PER_MTOK = 15.0
PRICE_PER_SEARCH = 10.0 / 1000  # 웹 검색 $10 / 1,000회

# 로깅
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ============================================================
# 워치리스트 종목 (28개 — 워치리스트 markdown 에서 자동 추출도 가능하나 일단 하드코딩)
# ============================================================

US_TICKERS = [
    "NVDA",                                                          # AI Foundation (cross 다중)
    "LEU", "CEG", "BWXT",                                            # Nuclear
    "GEV", "VRT", "ETN", "PWR",                                      # AI DC Power
    "MTSI", "LITE", "COHR",                                          # 광인터커넥트
    "TSEM", "WOLF", "VICR", "STM", "POWI", "NVTS", "MPWR",          # 전력반도체
    "MOD", "CC",                                                     # 냉각
    "TSLA",                                                          # 휴머노이드 + 자율
]
KR_TICKERS = [
    "034020", "052690",                                              # Nuclear (K-원전)
    "298040",                                                        # AI DC Power (K-그리드)
    "425420",                                                        # 광인터커넥트 (Broadcom 납품)
    "000990", "009150",                                              # 전력반도체
    "005380", "058610",                                              # 휴머노이드 + 자율
    "087010",                                                        # GLP-1
    "141080",                                                        # 정밀 종양학
    "012450",                                                        # K-방산
]
KR_NAMES = {
    "034020": "두산에너빌리티", "052690": "한전기술",
    "298040": "효성중공업",
    "425420": "티에프이",
    "000990": "DB하이텍", "009150": "삼성전기",
    "005380": "현대차", "058610": "에스피지",
    "087010": "펩트론", "141080": "리가켐바이오", "012450": "한화에어로스페이스",
}

# ============================================================
# 시장 데이터 수집
# ============================================================

def get_last_kr_trading_day() -> str:
    """한국 마지막 거래일 (YYYYMMDD)."""
    today = datetime.now(KST)
    for back in range(1, 8):
        d = today - timedelta(days=back)
        if d.weekday() < 5:  # 0~4 = 월~금
            return d.strftime("%Y%m%d")
    return today.strftime("%Y%m%d")


def fetch_us_prices() -> list[dict]:
    """미국 종목 yfinance 데이터."""
    results = []
    for ticker in US_TICKERS:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="5d")
            if hist.empty or len(hist) < 2:
                continue
            current = hist["Close"].iloc[-1]
            prev = hist["Close"].iloc[-2]
            change_pct = (current - prev) / prev * 100
            volume = hist["Volume"].iloc[-1]
            avg_volume = hist["Volume"].mean()
            vol_ratio = volume / avg_volume if avg_volume > 0 else 1.0
            results.append({
                "ticker": ticker,
                "market": "US",
                "price": round(float(current), 2),
                "change_pct": round(float(change_pct), 2),
                "volume_ratio": round(float(vol_ratio), 2),
            })
        except Exception as e:
            logger.warning(f"{ticker} 수집 실패: {e}")
    return results


def fetch_kr_prices() -> list[dict]:
    """한국 종목 pykrx 데이터."""
    if not PYKRX_AVAILABLE:
        return []

    last_day = get_last_kr_trading_day()
    prev_day = (datetime.strptime(last_day, "%Y%m%d") - timedelta(days=7)).strftime("%Y%m%d")

    results = []
    for ticker in KR_TICKERS:
        try:
            df = krx_stock.get_market_ohlcv_by_date(prev_day, last_day, ticker)
            if df.empty or len(df) < 2:
                continue
            current = df["종가"].iloc[-1]
            prev = df["종가"].iloc[-2]
            change_pct = (current - prev) / prev * 100
            volume = df["거래량"].iloc[-1]
            avg_volume = df["거래량"].mean()
            vol_ratio = volume / avg_volume if avg_volume > 0 else 1.0
            results.append({
                "ticker": ticker,
                "name": KR_NAMES.get(ticker, ""),
                "market": "KR",
                "price": int(current),
                "change_pct": round(float(change_pct), 2),
                "volume_ratio": round(float(vol_ratio), 2),
            })
        except Exception as e:
            logger.warning(f"{ticker} ({KR_NAMES.get(ticker, '')}) 수집 실패: {e}")
    return results


# ============================================================
# 시스템 파일 로딩
# ============================================================

def load_text_file(path: Path, max_chars: Optional[int] = None) -> str:
    """파일 읽기 (선택적 크기 제한)."""
    if not path.exists():
        return ""
    try:
        content = path.read_text(encoding="utf-8")
        if max_chars and len(content) > max_chars:
            return content[:max_chars] + "\n\n... (이하 생략)"
        return content
    except Exception as e:
        logger.warning(f"{path} 읽기 실패: {e}")
        return ""


def load_tracked_stocks() -> list[dict]:
    """Track 4 등재 종목."""
    if not TRACKED_STOCKS_PATH.exists():
        return []
    try:
        data = json.loads(TRACKED_STOCKS_PATH.read_text(encoding="utf-8"))
        return data.get("tracked", [])
    except Exception as e:
        logger.warning(f"tracked_stocks.json 읽기 실패: {e}")
        return []


def load_positions() -> dict:
    """positions.json 로드 (meta / portfolio_level / positions)."""
    if not POSITIONS_PATH.exists():
        logger.error(f"{POSITIONS_PATH} 없음 — 포지션 기반 판정 없이 진행")
        return {}
    try:
        return json.loads(POSITIONS_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error(f"positions.json 파싱 실패 — 포지션 기반 판정 없이 진행: {e}")
        return {}


def load_position_state() -> dict:
    """position_state.json 로드. 없으면 빈 상태로 시작."""
    empty = {"meta": {"version": "1.0", "last_run": None}, "positions": {}, "portfolio_level": {}}
    if not POSITION_STATE_PATH.exists():
        logger.info("position_state.json 없음 — 새로 시작")
        return empty
    try:
        state = json.loads(POSITION_STATE_PATH.read_text(encoding="utf-8"))
        state.setdefault("meta", {"version": "1.0", "last_run": None})
        state.setdefault("positions", {})
        state.setdefault("portfolio_level", {})
        return state
    except Exception as e:
        logger.warning(f"position_state.json 파싱 실패 — 새로 시작: {e}")
        return empty


def save_position_state(state: dict, today_str: str, path: Optional[Path] = None):
    """상태 파일 저장. 실패해도 다이제스트 자체는 계속 진행.

    dry-run 은 실제 상태를 오염시키면 안 되므로(다음 정식 실행이 '점검 완료' 로 오인)
    별도 경로를 넘겨 사본으로만 저장한다.
    """
    target = path or POSITION_STATE_PATH
    try:
        state["meta"]["last_run"] = today_str
        state["meta"].setdefault("version", "1.0")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        logger.info(f"상태 저장: {target}")
    except Exception as e:
        logger.error(f"상태 파일 저장 실패 ({target}): {e}")


# ============================================================
# 캘린더 파싱 · 검색 대상 선별
# ============================================================

_SECTION_RE = re.compile(r"^#+\s.*?(20\d{2})\s*년?\s*(\d{1,2})\s*월")
_DATE_CELL_RE = re.compile(r"(\d{1,2})\s*/\s*(\d{1,2})")


def extract_upcoming_events(calendar_text: str, today: datetime, days: int = EVENT_WINDOW_DAYS) -> list[dict]:
    """캘린더 markdown 표에서 향후 N일 이벤트 추출.

    형식: '## 2. 2026 6월' 섹션 아래 '| 6/12 | 이벤트 | 영역·종목 | P1 |' 행.
    날짜가 '6월?' 처럼 미확정인 행은 창 판정이 불가하므로 제외.
    """
    events = []
    year, month = today.year, today.month

    for line in calendar_text.split("\n"):
        sec = _SECTION_RE.match(line)
        if sec:
            year, month = int(sec.group(1)), int(sec.group(2))
            continue

        stripped = line.strip()
        if not stripped.startswith("|"):
            continue

        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue

        date_cell = cells[0].replace("*", "").strip()
        if not date_cell or date_cell == "날짜" or set(date_cell) <= set("-: "):
            continue

        dm = _DATE_CELL_RE.search(date_cell)
        if not dm:
            continue

        mm, dd = int(dm.group(1)), int(dm.group(2))
        yy = year + 1 if (month >= 11 and mm <= 2) else year  # 연말 → 연초 넘어가는 섹션 보정
        try:
            event_date = datetime(yy, mm, dd).date()
        except ValueError:
            continue

        delta = (event_date - today.date()).days
        if 0 <= delta <= days:
            events.append({
                "date": event_date.strftime("%Y-%m-%d"),
                "event": cells[1] if len(cells) > 1 else "",
                "area": cells[2] if len(cells) > 2 else "",
                "priority": cells[3] if len(cells) > 3 else "",
                "line": stripped,
            })

    events.sort(key=lambda e: e["date"])
    return events


def days_since(date_str: Optional[str], today_str: str) -> Optional[int]:
    """마지막 점검일로부터 경과일. 기록 없으면 None."""
    if not date_str:
        return None
    try:
        return (datetime.strptime(today_str, "%Y-%m-%d") - datetime.strptime(date_str, "%Y-%m-%d")).days
    except Exception:
        return None


def position_keywords(pos: dict) -> list[str]:
    """포지션-이벤트 매칭용 키워드. 티커 + 라벨(괄호 안팎) + peers."""
    kws = list(pos.get("tickers", []))
    label = pos.get("label", "")
    paren = re.match(r"^(.*?)\s*\((.*)\)\s*$", label)
    if paren:
        kws.append(paren.group(1).strip())
        kws.extend(p.strip() for p in re.split(r"[/·,]", paren.group(2)))
    elif label:
        kws.append(label)
    kws.extend(pos.get("watch", {}).get("peers", []))
    return [k for k in dict.fromkeys(kws) if k and len(k) >= 2]


def select_positions(
    positions: list[dict],
    state: dict,
    prices: list[dict],
    upcoming: list[dict],
    today_str: str,
) -> tuple[list[dict], list[dict]]:
    """검색 대상 선별. (선별됨, 미선별) 리턴.

    트리거: 가격 ±3% / 7일 내 캘린더 이벤트 키워드 매칭 / N일 미점검 rotation.
    status 가 holding 이 아닌 포지션은 개별 검색 대상에서 제외.
    """
    moved = {p["ticker"] for p in prices if abs(p.get("change_pct", 0)) >= PRICE_MOVE_THRESHOLD}
    event_text = " ".join(e["line"] for e in upcoming)

    candidates = []
    for pos in positions:
        if pos.get("status") not in MONITORED_STATUSES:
            continue

        reasons = []
        price_hit = sorted(set(pos.get("tickers", [])) & moved)
        if price_hit:
            reasons.append(f"가격 ±{PRICE_MOVE_THRESHOLD}% 이상: {', '.join(price_hit)}")

        kw_hit = [k for k in position_keywords(pos) if k in event_text]
        if kw_hit:
            reasons.append(f"{EVENT_WINDOW_DAYS}일 내 이벤트 매칭: {', '.join(kw_hit[:3])}")

        stale = days_since(state["positions"].get(pos["id"], {}).get("last_checked"), today_str)
        if stale is None:
            reasons.append("최초 점검")
        elif stale >= SEARCH_ROTATION_DAYS:
            reasons.append(f"{stale}일 미점검 (rotation)")

        if reasons:
            candidates.append({
                "position": pos,
                "reasons": reasons,
                "stale": 9999 if stale is None else stale,
                "triggered": bool(price_hit or kw_hit),
            })

    # 가격·이벤트 트리거가 rotation 보다 우선, 그다음 오래 방치된 순
    candidates.sort(key=lambda c: (0 if c["triggered"] else 1, -c["stale"]))

    selected = candidates[:MAX_SEARCH_POSITIONS]
    selected_ids = {c["position"]["id"] for c in selected}
    unselected = [
        p for p in positions
        if p.get("status") in MONITORED_STATUSES and p["id"] not in selected_ids
    ]
    return selected, unselected


def numbered(items: list, prefix: str, indent: str = "  ") -> str:
    """thesis·kill_signals 에 번호를 매긴다.

    출력에서 '[K3]' 처럼 어떤 조건에 걸린 사실인지 역참조할 수 있게 하기 위함.
    번호는 positions.json 의 배열 순서를 그대로 따른다.
    """
    if not items:
        return f"{indent}(없음)"
    return "\n".join(f"{indent}{prefix}{i}. {t}" for i, t in enumerate(items, 1))


def format_position_config(pos: dict) -> str:
    """포지션 1개의 판정 기준을 번호 매겨 정리 (종합 프롬프트 컨텍스트용)."""
    watch = pos.get("watch", {})
    return "\n".join([
        f"### {pos.get('label')} [{pos.get('id')}] — {', '.join(pos.get('tickers', []))}"
        f" (status: {pos.get('status')})",
        " thesis:",
        numbered(pos.get("thesis", []), "T"),
        " kill_signals:",
        numbered(pos.get("kill_signals", []), "K"),
        " add_signals:",
        numbered(pos.get("add_signals", []), "A"),
        f" peers: {', '.join(watch.get('peers', [])) or '(없음)'}",
        f" indicators: {', '.join(watch.get('indicators', [])) or '(없음)'}",
        f" ignore(출력 금지): {'; '.join(pos.get('ignore', [])) or '(없음)'}",
    ])


# ============================================================
# Claude 호출
# ============================================================

def build_prompt(
    us_prices: list[dict],
    kr_prices: list[dict],
    tracked: list[dict],
    dashboard: str,
    calendar: str,
    template: str,
    now_str: str,
    positions_doc: dict,
    layer0_result: Optional[dict],
    position_results: list[dict],
    unchecked: list[dict],
    upcoming: list[dict],
    state: dict,
) -> str:
    """종합 호출 프롬프트.

    포지션 판정 기준(thesis·kill_signals·watch) + 오늘 검색 결과를 결합해
    3단계 등급 다이제스트를 작성시킨다. 판단·조치 제안은 시키지 않는다.
    """
    meta = positions_doc.get("meta", {})
    portfolio_level = positions_doc.get("portfolio_level", {})
    operating_rule = meta.get("operating_rule", "")

    monitored = [
        p for p in positions_doc.get("positions", [])
        if p.get("status") in MONITORED_STATUSES
    ]

    # ---- 포지션 판정 기준 (번호 부여) ----
    positions_config = "\n\n".join(format_position_config(p) for p in monitored) \
        or "(모니터링 대상 포지션 없음)"

    # ---- Layer 0 ----
    layer0_config = (
        f"{portfolio_level.get('concentration_note', '')}\n\n"
        f"layer0_kill_signals:\n{numbered(portfolio_level.get('layer0_kill_signals', []), 'L')}"
    ) if portfolio_level else "(portfolio_level 미정의)"

    # ---- 검색 결과 포맷 ----
    def fmt_findings(findings) -> str:
        if not findings:
            return "- (신호 없음)"
        out = []
        for f in findings:
            refs = ", ".join(f.get("refs") or []) or "연결 번호 없음"
            out.append(
                f"- [{f.get('level', '?')}] ({refs}) {f.get('summary', '')}\n"
                f"  해당 조건: {f.get('signal') or '-'}\n"
                f"  출처: {f.get('evidence_url', '-')} ({f.get('reported_at', '날짜 미상')})"
            )
        return "\n".join(out)

    layer0_section = (
        fmt_findings(layer0_result.get("findings"))
        if layer0_result else "- (Layer 0 검색 실패 또는 미실행 — 판정 없음)"
    )

    pos_blocks = []
    for item in position_results:
        pos = item["position"]
        result = item.get("result") or {}
        flags = state.get("positions", {}).get(pos["id"], {}).get("open_flags", [])
        repeated = [f for f in flags if f.get("count", 1) >= 2]
        repeat_line = ""
        if repeated:
            repeat_line = "\n  ※ 반복 관측(누적): " + "; ".join(
                f"{f.get('signal')} ×{f.get('count')}회 (최초 {f.get('first_seen')})" for f in repeated
            )

        if item.get("skipped"):
            body = f"- (미점검: {item['skipped']} — 신호 없음이 아니라 확인 안 함)"
        elif result:
            body = fmt_findings(result.get("findings"))
        else:
            body = "- (검색 실패 — 판정 없음)"

        pos_blocks.append(
            f"## {pos.get('label')} [{pos.get('id')}]\n"
            f"점검 사유: {'; '.join(item.get('reasons', []))}\n"
            f"{body}{repeat_line}"
        )
    position_section = "\n\n".join(pos_blocks) if pos_blocks else "(오늘 검색한 포지션 없음)"

    unchecked_section = "\n".join(
        f"- {p.get('label')} [{p.get('id')}]: 마지막 점검 "
        f"{state.get('positions', {}).get(p['id'], {}).get('last_checked') or '기록 없음'}"
        for p in unchecked
    ) or "(없음)"

    events_section = "\n".join(
        f"- {e['date']} [{e.get('priority', '')}] {e.get('event', '')} — {e.get('area', '')}"
        for e in upcoming
    ) or f"(향후 {EVENT_WINDOW_DAYS}일 내 캘린더 이벤트 없음)"

    # ---- 가격: 표시 임계치 이상만, 맨 아래 한 줄용 ----
    def price_str(p: dict) -> str:
        sign = "+" if p["change_pct"] >= 0 else ""
        name = p.get("name") or p["ticker"]
        return f"{name} {sign}{p['change_pct']}%"

    big_moves = [
        p for p in (us_prices + kr_prices)
        if abs(p.get("change_pct", 0)) >= PRICE_DISPLAY_THRESHOLD
    ]
    big_moves.sort(key=lambda p: abs(p["change_pct"]), reverse=True)
    price_section = (
        " / ".join(price_str(p) for p in big_moves)
        if big_moves else f"(±{PRICE_DISPLAY_THRESHOLD}% 이상 없음)"
    )

    tracked_ids = ", ".join(t.get("ticker", "") for t in tracked) or "(없음)"

    prompt = f"""당신은 본인의 포지션 모니터링 시스템의 분석가. 오늘의 신호 판정 다이제스트를 작성한다.

# 현재 시점
{now_str}

# 당신의 역할
각 포지션의 thesis 가 유지되는지, kill_signals 에 걸리는 사실이 나왔는지만 확인해 보고한다.
판단과 조치는 본인이 한다. 당신은 **사실과 연결관계만** 제시한다.

# 판정 등급 (출력에 이 표기 그대로 사용)
🔴 KILL 관련 — kill_signals 에 직접 해당하는 사실 (내부 레벨 RED)
🟡 주목 — thesis 에 영향 가능하나 확인 필요 (내부 레벨 YELLOW. add_signals 해당분도 여기, 사실만)
⚪ 참고 — 알아둘 만하나 판단 불필요 (내부 레벨 WHITE)

운영 원칙: {operating_rule}

아래 검색 결과는 이미 판정이 끝난 상태다. 등급을 임의로 올리거나 내리지 말 것.

# 모니터링 대상 포지션 — 판정 기준
status 가 holding 또는 watching 인 것만. T=thesis, K=kill_signals, A=add_signals 번호는 출력에서 역참조에 사용.

{positions_config}

# Layer 0 — 포트폴리오 상위 변수 (개별 포지션보다 우선)
{layer0_config}

## Layer 0 오늘 판정
{layer0_section}

# 오늘 검색한 포지션의 판정 결과
{position_section}

# 오늘 검색하지 않은 포지션
{unchecked_section}

# 향후 {EVENT_WINDOW_DAYS}일 캘린더 이벤트 (파싱 완료분)
{events_section}

# 가격 (±{PRICE_DISPLAY_THRESHOLD}% 이상만)
{price_section}

# 참고 데이터 (출력 요구 아님 — 이것만 보고 항목을 만들지 말 것)
Track 4 등재 티커: {tracked_ids}

Mega Change Map dashboard 발췌:
{dashboard[:1500]}

기존 다이제스트 템플릿 (markdown 관례 참고용. 형식이 충돌하면 아래 출력 스펙이 우선):
{template[:1200]}

# 출력 스펙 (★ 정확히 이대로)

두 블록을 순서대로 출력. 앞뒤 설명·코드블록 마커 없이 다이제스트만.

===TELEGRAM===
plain text, 표·markdown 문법 없이. 모바일 가독성 우선. 1500자 이내.

📊 포지션 신호 — YYYY-MM-DD

🔴 KILL 관련
- 포지션명 [K3] 사실 한 줄 (출처도메인, 보도일)
(해당 없으면 이 줄만: 없음)

🟡 주목
- 포지션명 [T1] 사실 한 줄 (출처도메인, 보도일)
(해당 없으면: 없음)

⚪ 참고
- 포지션명 사실 한 줄
(최대 3건까지만. 해당 없으면: 없음)

📅 향후 {EVENT_WINDOW_DAYS}일
- MM-DD 이벤트명 [P1]
(해당 없으면: 없음)

📈 가격 ±{PRICE_DISPLAY_THRESHOLD}%
- (한 줄로 이어서. 해당 없으면: 없음)

미점검: id, id, id

===FILE===
markdown. 헤더는 ##. 텔레그램 요약과 별개로 작성하되 사실이 서로 어긋나면 안 됨.

## 🔴 KILL 관련
포지션마다 아래 형식:
- **포지션명 (티커)** — [K3] 해당 kill_signal 원문 축약
  사실: 한 줄
  출처: URL (보도일)
  누적: N회째 관측, 최초 YYYY-MM-DD  ← 반복 관측 정보가 있을 때만
(해당 없으면 "없음" 한 단어)

## 🟡 주목
같은 형식. thesis 연결은 [T1], add_signals 연결은 [A2] 로 표기.
(해당 없으면 "없음")

## ⚪ 참고
같은 형식이되 2줄 이내로 짧게.
(해당 없으면 "없음")

## Layer 0
[L1]~[L4] 중 걸린 것만. 해당 없으면 "없음".
Layer 0 에 걸린 게 있으면 이 섹션을 문서 맨 위로 올릴 것.

## 향후 {EVENT_WINDOW_DAYS}일 이벤트
표 (날짜 / 이벤트 / 관련 포지션 / P). P1·P2만.

## 오늘 미점검 포지션
- 포지션명 [id] — 마지막 점검 YYYY-MM-DD (확인 안 함)

## 가격
±{PRICE_DISPLAY_THRESHOLD}% 이상만 한 줄. 문서 맨 아래.

# 작성 규칙 (위반 금지)

1. 각 항목에 반드시 연결 번호를 붙일 것: [K#] [T#] [A#] [L#].
   어느 번호에도 연결되지 않는 사실은 ⚪ 참고로만, 번호 없이.
2. ignore 목록에 해당하는 내용은 **아예 출력하지 말 것**. 언급조차 금지.
3. 해당 없으면 "없음" 한 단어로 끝낼 것. 억지로 채우거나 분량을 맞추려 하지 말 것.
   빈 섹션에 "특이사항 없으나 ..." 같은 사족 금지.
4. 판단·조치를 제안하지 말 것. "매수 검토", "비중 확대", "진입", "익절", "손절",
   "관심 필요", "대응 필요" 같은 표현 금지. 사실과 어떤 조건에 걸리는지만 쓴다.
5. 검색으로 확인되지 않은 사실을 쓰지 말 것. 가격 변동에 추측 사유를 갖다붙이지 말 것.
   모르면 "사유 미확인".
6. 미점검 포지션을 "이상 없음" 으로 쓰지 말 것. "확인 안 함" 이다.
7. 출처 URL 이 없는 항목은 만들지 말 것.
8. 가격은 반드시 맨 아래. 위쪽 섹션에서 가격 등락을 서술하지 말 것.

# 톤
직설·짧음. AI 특유의 모호함·"~할 수 있습니다" 금지. "~다" 또는 "~함" 위주.
수식어보다 숫자와 날짜.
"""
    return prompt


def new_usage() -> dict:
    return {"input": 0, "output": 0, "searches": 0}


def merge_usage(total: dict, part: dict) -> dict:
    for k in ("input", "output", "searches"):
        total[k] += part.get(k, 0)
    return total


def calc_cost(usage: dict) -> float:
    """토큰 + 웹 검색 요청 비용."""
    return (
        usage["input"] / 1_000_000 * PRICE_IN_PER_MTOK
        + usage["output"] / 1_000_000 * PRICE_OUT_PER_MTOK
        + usage["searches"] * PRICE_PER_SEARCH
    )


def _extract_text(content) -> str:
    """응답에서 text 블록만 추출.

    web_search 를 켜면 content 에 server_tool_use / web_search_tool_result 블록이
    섞여 들어오므로 content[0].text 로 접근하면 깨진다.
    """
    parts = [b.text for b in content if getattr(b, "type", None) == "text"]
    return "\n".join(parts).strip()


def call_claude(
    prompt: str,
    *,
    max_tokens: int,
    effort: str = SEARCH_EFFORT,
    use_search: bool = False,
    max_uses: int = POSITION_MAX_USES,
) -> tuple[str, dict]:
    """Claude 호출. (텍스트, usage) 리턴.

    web_search 사용 시 서버측 반복이 한도에 걸리면 stop_reason='pause_turn' 으로
    끊기므로, assistant 턴을 되붙여 재개한다.
    """
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    kwargs = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "output_config": {"effort": effort},
    }
    if use_search:
        kwargs["tools"] = [{
            "type": WEB_SEARCH_TOOL_TYPE,
            "name": "web_search",
            "max_uses": max_uses,
        }]

    messages = [{"role": "user", "content": prompt}]
    usage = new_usage()
    text = ""

    for _ in range(MAX_PAUSE_CONTINUATIONS + 1):
        response = client.messages.create(messages=messages, **kwargs)

        u = response.usage
        usage["input"] += u.input_tokens or 0
        usage["output"] += u.output_tokens or 0
        server_tool = getattr(u, "server_tool_use", None)
        if server_tool is not None:
            usage["searches"] += getattr(server_tool, "web_search_requests", 0) or 0

        chunk = _extract_text(response.content)
        if chunk:
            text = chunk

        if response.stop_reason == "refusal":
            logger.warning(f"거부 응답 (stop_reason=refusal): {getattr(response, 'stop_details', None)}")
            break
        if response.stop_reason == "max_tokens":
            logger.warning(f"max_tokens({max_tokens}) 도달 — 응답이 잘렸을 수 있음")
            break
        if response.stop_reason != "pause_turn":
            break

        logger.info("pause_turn — 검색 이어서 재개")
        messages = messages + [{"role": "assistant", "content": response.content}]
    else:
        logger.warning(f"pause_turn 재개 {MAX_PAUSE_CONTINUATIONS}회 초과 — 부분 결과 사용")

    return text, usage


def extract_json(text: str) -> Optional[dict]:
    """응답 텍스트에서 JSON 객체 추출 (코드블록·앞뒤 설명 허용)."""
    if not text:
        return None
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    candidate = fence.group(1) if fence else text
    start, end = candidate.find("{"), candidate.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        return json.loads(candidate[start:end + 1])
    except Exception as e:
        logger.warning(f"JSON 파싱 실패: {e}")
        return None


# ============================================================
# Layer 0 · 포지션별 검색
# ============================================================

_SIGNAL_RULE = """판정 기준:
- RED: kill_signals 또는 layer0_kill_signals 에 직접 해당. 판단 필요
- YELLOW: thesis 에 영향 가능하나 확인 필요
- WHITE: 알아둘 만하나 판단 불필요
- ignore 항목에 해당하면 아예 보고하지 말 것 (노이즈)

근거 없는 추측 금지. 검색으로 확인한 사실만. 각 항목에 출처 URL 과 보도일자 필수.
해당 신호가 없으면 findings 를 빈 배열로 두고 no_news 를 true 로 할 것."""

# 도구 미지원·인증 오류 등 구조적 실패가 나면 이후 검색 호출을 건너뛴다.
# (전송 오류·서버 오류 같은 일시적 실패는 해당 호출만 포기하고 계속 진행)
_search_disabled = False


def _run_search(prompt: str, max_uses: int, label: str) -> tuple[Optional[dict], dict]:
    """검색 호출 공통 래퍼.

    검색이 실패해도 예외를 밖으로 내보내지 않는다 — 판정만 비고 다이제스트는 계속 생성된다.
    호출자는 None 을 '판정 없음' 으로 처리한다.
    """
    global _search_disabled

    if _search_disabled:
        logger.warning(f"{label}: 앞선 검색이 구조적으로 실패해 건너뜀")
        return None, new_usage()

    try:
        text, usage = call_claude(
            prompt,
            max_tokens=SEARCH_MAX_TOKENS,
            effort=SEARCH_EFFORT,
            use_search=True,
            max_uses=max_uses,
        )
    except APIStatusError as e:
        status = getattr(e, "status_code", None)
        if status is not None and status < 500:
            _search_disabled = True
            logger.error(
                f"{label}: 요청 거부 (HTTP {status}) — 설정 문제로 판단해 이후 검색 생략. "
                f"다이제스트는 검색 없이 계속 생성: {e}"
            )
        else:
            logger.error(f"{label}: 서버 오류 (HTTP {status}) — 이 건만 건너뜀: {e}")
        return None, new_usage()
    except Exception as e:
        logger.error(f"{label}: 검색 호출 실패 — 이 건만 건너뜀: {e}")
        return None, new_usage()

    result = extract_json(text)
    if result is None:
        logger.warning(f"{label}: 응답 JSON 파싱 실패 — 판정 없음으로 처리")
    return result, usage


def search_layer0(portfolio_level: dict, prev_state: dict, now_str: str) -> tuple[Optional[dict], dict]:
    """포트폴리오 상위 변수 판정. 개별 포지션과 별도로 먼저 확인."""
    if not portfolio_level:
        return None, new_usage()

    kill_list = numbered(portfolio_level.get("layer0_kill_signals", []), "L", indent="")
    queries = ", ".join(portfolio_level.get("layer0_queries", []))
    prev = json.dumps(prev_state, ensure_ascii=False, indent=2) if prev_state else "(이전 관측 없음)"

    prompt = f"""당신은 투자 포트폴리오의 상위 변수(Layer 0)를 감시하는 분석가.

# 현재 시점
{now_str}

# 포트폴리오 집중 구조
{portfolio_level.get('concentration_note', '')}

# Layer 0 KILL 신호 (이게 사실이면 포트폴리오 전체가 흔들림)
{kill_list}

# 검색 키워드
{queries}

# 이전 관측 기록 (누적 판정용 — "2개 분기 연속" 류는 이 기록과 대조할 것)
{prev}

# 작업
web_search 로 위 KILL 신호 각각의 최신 상태를 확인하고 아래 JSON 만 출력.

{_SIGNAL_RULE}

각 finding 은 어떤 번호에 걸리는지 refs 로 반드시 명시할 것 (예: ["L2"]).

{{
  "findings": [
    {{"level": "RED|YELLOW|WHITE", "refs": ["L2"], "signal": "해당 KILL 신호 원문", "summary": "한 줄 사실 요약", "evidence_url": "출처 URL", "reported_at": "YYYY-MM-DD"}}
  ],
  "observations": {{"지표명": "관측값 (예: 리드타임 = 4~5년)"}},
  "no_news": false
}}

JSON 외 다른 텍스트 출력 금지."""

    return _run_search(prompt, LAYER0_MAX_USES, "Layer 0")


def search_position(
    candidate: dict,
    state_entry: dict,
    price_info: Optional[dict],
    now_str: str,
) -> tuple[Optional[dict], dict]:
    """포지션 1개 개별 검색 + RED/YELLOW/WHITE 판정."""
    pos = candidate["position"]
    watch = pos.get("watch", {})

    def bullets(items):
        return "\n".join(f"- {i}" for i in items) if items else "- (없음)"

    price_line = "(가격 데이터 없음)"
    if price_info:
        sign = "+" if price_info["change_pct"] >= 0 else ""
        price_line = (
            f"{price_info['ticker']} {price_info['price']} "
            f"({sign}{price_info['change_pct']}%) vol×{price_info.get('volume_ratio', '-')}"
        )

    prev = json.dumps(state_entry, ensure_ascii=False, indent=2) if state_entry else "(이전 관측 없음)"

    prompt = f"""당신은 특정 보유 포지션의 thesis 훼손 여부를 감시하는 분석가.

# 현재 시점
{now_str}

# 포지션
{pos.get('label')} ({', '.join(pos.get('tickers', []))})

# 오늘 이 포지션을 점검하는 이유
{bullets(candidate['reasons'])}

# 어제 가격
{price_line}

# thesis (이게 무너지면 보유 이유가 사라짐)
{numbered(pos.get('thesis', []), 'T', indent='')}

# KILL 신호 (해당하면 RED)
{numbered(pos.get('kill_signals', []), 'K', indent='')}

# ADD 신호 (해당하면 YELLOW 로 사실만 기록)
{numbered(pos.get('add_signals', []), 'A', indent='')}

# 감시 대상
경쟁사·비교대상: {', '.join(watch.get('peers', [])) or '(없음)'}
추적 지표: {', '.join(watch.get('indicators', [])) or '(없음)'}
검색 키워드: {', '.join(watch.get('queries', [])) or '(없음)'}

# 무시할 것 (노이즈 — 발견해도 보고 금지)
{bullets(pos.get('ignore', []))}

# 이전 관측 기록 (누적 판정용)
{prev}

# 메모
{pos.get('note', '')}

# 작업
web_search 로 위 KILL·ADD 신호와 추적 지표의 최신 상태를 확인하고 아래 JSON 만 출력.

{_SIGNAL_RULE}

"2개 분기 연속 감소" 처럼 누적이 필요한 신호는 오늘 1회 관측만으로 RED 로 올리지 말 것.
이전 관측 기록과 대조해 실제로 연속 조건이 충족될 때만 RED, 1회 관측이면 YELLOW.

각 finding 은 어떤 번호에 걸리는지 refs 로 반드시 명시할 것 (예: ["K3"], ["T1","K2"]).
어느 번호에도 연결되지 않으면 refs 를 빈 배열로 두고 level 은 WHITE.

{{
  "position_id": "{pos.get('id')}",
  "findings": [
    {{"level": "RED|YELLOW|WHITE", "refs": ["K3"], "signal": "해당 항목 원문 (없으면 null)", "kind": "kill|add|info", "summary": "한 줄 사실 요약", "evidence_url": "출처 URL", "reported_at": "YYYY-MM-DD"}}
  ],
  "observations": {{"지표명": "관측값"}},
  "no_news": false
}}

JSON 외 다른 텍스트 출력 금지."""

    return _run_search(prompt, POSITION_MAX_USES, f"포지션 {pos.get('id')}")


# ============================================================
# 상태 갱신
# ============================================================

def update_state_entry(entry: dict, result: dict, today_str: str) -> dict:
    """검색 결과를 상태 엔트리에 누적. 관측값 시계열 + 열린 플래그."""
    entry.setdefault("observations", {})
    entry.setdefault("open_flags", [])
    entry["last_checked"] = today_str

    # 관측값: 값이 바뀔 때만 새 항목 추가, 같으면 날짜만 갱신
    for key, value in (result.get("observations") or {}).items():
        if value in (None, "", "확인 불가", "불명"):
            continue
        series = entry["observations"].setdefault(key, [])
        if series and series[-1].get("value") == value:
            series[-1]["last_seen"] = today_str
        else:
            series.append({"date": today_str, "last_seen": today_str, "value": value})
        entry["observations"][key] = series[-MAX_OBSERVATIONS:]

    # 열린 플래그: 같은 신호가 반복 관측되면 count 증가 → 연속 조건 판정 근거
    flags = {f.get("signal"): f for f in entry["open_flags"] if f.get("signal")}
    for finding in (result.get("findings") or []):
        if finding.get("level") not in ("RED", "YELLOW"):
            continue
        signal = finding.get("signal") or (finding.get("summary") or "")[:60]
        if not signal:
            continue
        if signal in flags:
            flags[signal].update({
                "level": finding["level"],
                "last_seen": today_str,
                "count": flags[signal].get("count", 1) + 1,
                "summary": finding.get("summary", flags[signal].get("summary", "")),
                "evidence_url": finding.get("evidence_url", flags[signal].get("evidence_url", "")),
            })
        else:
            flags[signal] = {
                "signal": signal,
                "level": finding["level"],
                "first_seen": today_str,
                "last_seen": today_str,
                "count": 1,
                "summary": finding.get("summary", ""),
                "evidence_url": finding.get("evidence_url", ""),
            }

    # 오래 재확인 안 된 플래그 정리
    entry["open_flags"] = [
        f for f in flags.values()
        if (days_since(f.get("last_seen"), today_str) or 0) <= FLAG_EXPIRE_DAYS
    ]
    return entry

def parse_claude_response(response_text: str) -> tuple[str, str]:
    """Claude 응답에서 텔레그램 요약 + 파일 분리."""
    if "===TELEGRAM===" in response_text and "===FILE===" in response_text:
        parts = response_text.split("===FILE===", 1)
        telegram_part = parts[0].replace("===TELEGRAM===", "").strip()
        file_part = parts[1].strip()
        return telegram_part, file_part
    else:
        # 마커 없으면 전체를 둘 다 사용
        return response_text[:1500], response_text


# ============================================================
# 텔레그램 전송
# ============================================================

def build_summary_telegram(digest_md: str, cost: float, github_url: str) -> str:
    """텔레그램용 짧은 요약 추출."""
    lines = digest_md.split("\n")
    summary_lines = []
    char_count = 0
    for line in lines:
        if char_count > 1500:
            break
        summary_lines.append(line)
        char_count += len(line) + 1

    summary = "\n".join(summary_lines)

    footer = (
        f"\n\n{'─' * 25}\n"
        f"📎 전체 파일 첨부 ⬇️\n"
        f"🌐 GitHub: {github_url}\n"
        f"💰 비용: ${cost:.4f}"
    )
    return summary + footer


async def send_telegram(telegram_summary: str, file_path: Path, cost: float):
    """텔레그램에 짧은 요약 + 파일 첨부."""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    github_url = (
        f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO_NAME}/blob/main/"
        f"digests/sent/{file_path.name}"
        if GITHUB_USERNAME
        else ""
    )

    footer = (
        f"\n\n━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📎 전체: 파일 첨부 ⬇️"
    )
    if github_url:
        footer += f"\n🌐 GitHub: {github_url}"
    footer += f"\n💰 비용: ${cost:.4f}"

    full_message = telegram_summary + footer

    if len(full_message) > 4000:
        full_message = full_message[:3950] + "\n\n... (요약 잘림)"

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=full_message)

    with open(file_path, "rb") as f:
        await bot.send_document(
            chat_id=TELEGRAM_CHAT_ID,
            document=f,
            filename=file_path.name,
            caption=f"일간 다이제스트 전체 ({file_path.stem})",
        )

# ============================================================
# GitHub commit
# ============================================================

def git_commit_and_push(file_path: Path):
    """v2.3: git commit 비활성화. Digest 는 EC2 로컬에만 저장."""
    pass

# ============================================================
# 메인
# ============================================================

async def main(dry_run: bool = False):
    now = datetime.now(KST)
    now_str = now.strftime("%Y-%m-%d %H:%M KST")
    today_str = now.strftime("%Y-%m-%d")
    stamp = now.strftime("%Y-%m-%d_%H%M")

    mode = "DRY-RUN (텔레그램·git·상태갱신 없음)" if dry_run else "정식 실행"
    logger.info(f"=== Daily Digest {today_str} 시작 — {mode} ===")

    # 1. 시장 데이터
    logger.info("미국 종목 수집...")
    us_prices = fetch_us_prices()
    logger.info(f"미국 {len(us_prices)}종목 수집 완료")

    logger.info("한국 종목 수집...")
    kr_prices = fetch_kr_prices()
    logger.info(f"한국 {len(kr_prices)}종목 수집 완료")

    # 2. 시스템 파일 · 포지션 · 상태 로딩
    dashboard = load_text_file(DASHBOARD_PATH)
    calendar = load_text_file(CALENDAR_PATH)
    template = load_text_file(TEMPLATE_PATH)
    tracked = load_tracked_stocks()
    positions_doc = load_positions()
    state = load_position_state()

    positions = positions_doc.get("positions", [])
    all_prices = us_prices + kr_prices
    upcoming = extract_upcoming_events(calendar, now)

    logger.info(f"Track 4 등재 종목: {len(tracked)}개")
    logger.info(f"포지션 {len(positions)}개 로드 / 향후 {EVENT_WINDOW_DAYS}일 이벤트 {len(upcoming)}건 파싱")

    usage_total = new_usage()

    # 3. Layer 0 (포트폴리오 상위 변수) 검색
    layer0_result = None
    portfolio_level = positions_doc.get("portfolio_level", {})
    if portfolio_level:
        logger.info("Layer 0 검색 중...")
        layer0_result, u = search_layer0(portfolio_level, state.get("portfolio_level", {}), now_str)
        merge_usage(usage_total, u)
        if layer0_result:
            state["portfolio_level"] = update_state_entry(
                state.get("portfolio_level") or {}, layer0_result, today_str
            )
            findings = layer0_result.get("findings") or []
            reds = sum(1 for f in findings if f.get("level") == "RED")
            logger.info(f"Layer 0 완료: findings {len(findings)}건 (RED {reds})")
        else:
            logger.warning("Layer 0 결과 파싱 실패 — 판정 없음으로 진행")
    else:
        logger.warning("portfolio_level 없음 — Layer 0 검색 생략")

    # 4. 검색 대상 선별 (API 호출 없음)
    selected, unchecked = select_positions(positions, state, all_prices, upcoming, today_str)
    if selected:
        for c in selected:
            logger.info(f"선별: {c['position']['id']} — {'; '.join(c['reasons'])}")
    else:
        logger.info("트리거된 포지션 없음 — 개별 검색 생략")

    # 5. 선별된 포지션만 개별 검색
    position_results = []
    for cand in selected:
        pos = cand["position"]

        if usage_total["searches"] >= DAILY_SEARCH_BUDGET:
            logger.warning(
                f"일일 검색 예산 {DAILY_SEARCH_BUDGET}회 소진 "
                f"(현재 {usage_total['searches']}회) — {pos['id']} 이하 생략"
            )
            position_results.append({**cand, "result": None, "skipped": "일일 검색 예산 소진"})
            continue

        logger.info(f"포지션 검색 중: {pos['id']} (누적 검색 {usage_total['searches']}회)")
        price_info = next((p for p in all_prices if p["ticker"] in pos.get("tickers", [])), None)
        entry = state["positions"].setdefault(
            pos["id"], {"last_checked": None, "observations": {}, "open_flags": []}
        )
        result, u = search_position(cand, entry, price_info, now_str)
        merge_usage(usage_total, u)
        if result:
            state["positions"][pos["id"]] = update_state_entry(entry, result, today_str)
            findings = result.get("findings") or []
            reds = sum(1 for f in findings if f.get("level") == "RED")
            logger.info(f"{pos['id']} 완료: findings {len(findings)}건 (RED {reds})")
        else:
            logger.warning(f"{pos['id']} 결과 파싱 실패 — 판정 없음으로 처리")
        position_results.append({**cand, "result": result})

    # 6. 상태 저장 (종합 호출 실패해도 검색 결과는 남도록 먼저 저장)
    if dry_run:
        DRY_RUN_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        save_position_state(state, today_str, DRY_RUN_OUTPUT_DIR / f"{stamp}_position_state.json")
        logger.info("dry-run: 실제 position_state.json 은 건드리지 않음")
    else:
        save_position_state(state, today_str)

    # 7. 종합 호출 (검색 없음)
    logger.info("종합 다이제스트 생성 중...")
    prompt = build_prompt(
        us_prices=us_prices,
        kr_prices=kr_prices,
        tracked=tracked,
        dashboard=dashboard,
        calendar=calendar,
        template=template,
        now_str=now_str,
        positions_doc=positions_doc,
        layer0_result=layer0_result,
        position_results=position_results,
        unchecked=unchecked,
        upcoming=upcoming,
        state=state,
    )

    response_text, u = call_claude(
        prompt, max_tokens=SYNTHESIS_MAX_TOKENS, effort=SYNTHESIS_EFFORT, use_search=False
    )
    merge_usage(usage_total, u)
    cost = calc_cost(usage_total)
    logger.info(
        f"전체 완료. Tokens: {usage_total['input']:,} in / {usage_total['output']:,} out, "
        f"검색 {usage_total['searches']}회. 비용 ${cost:.4f}"
    )

    if not response_text.strip():
        logger.error("종합 응답이 비어 있음 — 전송 중단 (상태 파일은 저장됨)")
        return

    # 텔레그램용 요약 + 파일용 markdown 분리
    telegram_summary, file_md = parse_claude_response(response_text)

    # 8. 파일 저장
    if dry_run:
        DRY_RUN_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        digest_path = DRY_RUN_OUTPUT_DIR / f"{stamp}_digest.md"
        digest_path.write_text(file_md, encoding="utf-8")

        tg_path = DRY_RUN_OUTPUT_DIR / f"{stamp}_telegram.txt"
        tg_path.write_text(telegram_summary, encoding="utf-8")

        prompt_path = DRY_RUN_OUTPUT_DIR / f"{stamp}_synthesis_prompt.txt"
        prompt_path.write_text(prompt, encoding="utf-8")

        run_path = DRY_RUN_OUTPUT_DIR / f"{stamp}_run.json"
        run_path.write_text(json.dumps({
            "run_at": now_str,
            "model": MODEL,
            "web_search_tool": WEB_SEARCH_TOOL_TYPE,
            "usage": usage_total,
            "cost_usd": round(cost, 4),
            "layer0": layer0_result,
            "selected": [
                {
                    "id": r["position"]["id"],
                    "reasons": r.get("reasons", []),
                    "skipped": r.get("skipped"),
                    "result": r.get("result"),
                }
                for r in position_results
            ],
            "unchecked": [p["id"] for p in unchecked],
            "upcoming_events": upcoming,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        logger.info("dry-run 산출물:")
        for p in (digest_path, tg_path, prompt_path, run_path):
            logger.info(f"  {p}")
        logger.info("dry-run: 텔레그램 전송·git commit 생략")
        logger.info(f"=== Daily Digest {today_str} 완료 (DRY-RUN) ===")
        return

    DIGEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DIGEST_OUTPUT_DIR / f"{today_str}.md"
    output_path.write_text(file_md, encoding="utf-8")
    logger.info(f"파일 저장: {output_path}")

    # 9. 텔레그램 전송 (요약 + 파일 첨부)
    logger.info("텔레그램 전송 중...")
    await send_telegram(telegram_summary, output_path, cost)
    logger.info("텔레그램 전송 완료")
    # 10. Git commit
    git_commit_and_push(output_path)

    logger.info(f"=== Daily Digest {today_str} 완료 ===")


def parse_args():
    ap = argparse.ArgumentParser(description="Daily Digest Generator")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="텔레그램 전송·git commit·상태 갱신 없이 결과만 digests/dry-run/ 에 저장",
    )
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(dry_run=args.dry_run))

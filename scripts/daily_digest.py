"""
Daily Digest Generator
======================
매일 새벽 06:30 KST 자동 실행 (cron).

작동 순서:
1. positions.json·position_state.json·theme_state.json·캘린더 로드
2. 포지션 종목만 yfinance·pykrx 로 가격 수집 (레거시 워치리스트 32종목 미사용)
3. Layer 0 (포트폴리오 상위 변수) web_search 1회
4. 전 종목 소식 스윕 1회 (판정 아님)
5. 검색 대상 포지션 선별 (가격 ±3% / 7일 내 이벤트 / N일 미점검 rotation)
6. 선별된 포지션만 개별 web_search → RED·YELLOW·WHITE 판정
7. Layer 0.5 테마 검색 (판정 없음) → 결과를 affects 포지션으로 팬아웃
8. position_state.json·theme_state.json 에 관측값·플래그·흐름 누적
9. 종합 호출로 일간 다이제스트 생성 (각주 번호는 코드가 부여)
10. 파일 저장 (digests/sent/YYYY-MM-DD.md) + 📎 출처 블록 자동 첨부
11. 텔레그램 푸시 (요약 + 파일 첨부 + GitHub URL)

레이어 구분:
- 포지션 판정 (🔴🟡⚪) — kill_signals·thesis 에 실제로 걸릴 때만. 조치 판단 대상
- Layer 0.5 테마 (🔷) — 상위 변화 추적. 등급 없음. 반복 관측 누적만이 승격 경로
  포지션 검색은 하루 MAX_SEARCH_POSITIONS 개뿐이라 여러 포지션을 동시에 흔드는
  상위 변화가 통째로 새어나간다. 그 구멍을 메우는 레이어.

하루 API 호출: Layer 0 (1) + 스윕 (1) + 선별 포지션 (0~3) + 테마 (0~2) + 종합 (1)
하루 검색: 호출당 상한(LAYER0_MAX_USES / POSITION_MAX_USES / THEME_MAX_USES)
          + 총량 캡(DAILY_SEARCH_BUDGET)
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
THEME_STATE_PATH = PROJECT_ROOT / "data" / "theme_state.json"
DIGEST_OUTPUT_DIR = PROJECT_ROOT / "digests" / "sent"
DRY_RUN_OUTPUT_DIR = PROJECT_ROOT / "digests" / "dry-run"

KST = pytz.timezone("Asia/Seoul")

# 실행 경로: True = Claude Code CLI (구독 사용량), False = Anthropic API (종량과금)
# CLI 는 검색 건당 요금이 없어 검색 상한을 넉넉히 줄 수 있다.
USE_CLAUDE_CLI = os.getenv("USE_CLAUDE_CLI", "1") == "1"
CLAUDE_CLI_BIN = os.getenv("CLAUDE_CLI_BIN", "claude")
CLAUDE_CLI_TIMEOUT = 1200      # 초. 검색 13회에 206초였으므로 무거운 날 대비

MODEL = "claude-sonnet-5"

# Sonnet 5 는 thinking 이 기본 ON 이며 max_tokens 가 thinking + 응답을 함께 덮음.
# 따라서 구형 3000 을 그대로 쓰면 응답이 중간에 잘림.
SEARCH_MAX_TOKENS = 8000       # 포지션별 검색 호출
SYNTHESIS_MAX_TOKENS = 16000   # 종합 호출 (TELEGRAM + FILE 전문)
SEARCH_EFFORT = "medium"       # 검색·판정용
SYNTHESIS_EFFORT = "high"      # 최종 작성용

# web_search
# _20260209 = dynamic filtering. 검색 결과를 코드로 걸러 컨텍스트에 넣으므로
# 검색이 많은 워크로드에서 입력 토큰이 크게 줄어든다 (Sonnet 4.6 / Opus 4.6 이상 필요).
# 구형 모델로 되돌릴 경우 web_search_20250305 으로 교체.
WEB_SEARCH_TOOL_TYPE = "web_search_20260209"

# max_uses 는 할당량이 아니라 천장이다. 모델은 필요한 만큼만 검색하므로
# 값을 올려도 평상시 비용은 그대로고 최악의 날만 비싸진다.
# 따라서 per-call 은 넉넉히 두고, 실제 통제는 아래 일일 총량 캡으로 한다.
# 실측: 검색 1회당 입력 약 11K 토큰이 재과금되므로 검색 수가 비용을 지배한다.
# 검색 1회 ≈ $0.043 (입력 $0.033 + 검색료 $0.01).
LAYER0_MAX_USES = 6            # Layer 0
NEWS_SWEEP_MAX_USES = 12       # 전 종목 소식 스윕 (판정 아님, 훑기)
POSITION_MAX_USES = 20         # 포지션당 (실측: 가장 무거운 포지션이 13회에서 자연히 멈춤)
THEME_MAX_USES = 8             # 테마(Layer 0.5)당
DAILY_SEARCH_BUDGET = 90       # 하루 총량 캡 (Layer0 6 + 스윕 12 + 포지션 20x3 + 테마 8x2)
MAX_PAUSE_CONTINUATIONS = 3    # pause_turn 재개 상한

# 모니터링 대상 status (exited·paused 는 기록만 남기고 판정 대상에서 제외)
MONITORED_STATUSES = ("holding", "watching")

# 검색 대상 선별 규칙
PRICE_MOVE_THRESHOLD = 3.0     # ±% 이상이면 검색 트리거 (내부 판단용, 출력 아님)
PRICE_DISPLAY_THRESHOLD = 5.0  # ±% 이상만 다이제스트 맨 아래 한 줄로 표기
EVENT_WINDOW_DAYS = 7          # 캘린더 이벤트 감시 창
SEARCH_ROTATION_DAYS = 14      # 이 기간 미점검이면 순번으로 강제 점검
# 회당 검색을 줄이면 '확인 미완료' 가 잦아진다. 반쪽 점검 2개보다
# 제대로 된 1개가 낫고, 못 끝낸 건 last_checked 미갱신으로 내일 재시도된다.
MAX_SEARCH_POSITIONS = 3       # 하루 개별 검색 상한

# 테마 레이어 (Layer 0.5) 선별 규칙
# 포지션은 '내 thesis 가 깨졌나' 를 묻고, 테마는 '상위 변화가 어디로 가나' 를 묻는다.
# 포지션 검색은 하루 3개뿐이라, 여러 포지션을 동시에 흔드는 상위 변화는
# 그날 뽑힌 포지션에 우연히 걸리지 않으면 통째로 새어나간다. 그 구멍을 메우는 레이어.
MAX_SEARCH_THEMES = 2          # 하루 테마 검색 상한
THEME_ROTATION_DAYS_CORE = 3   # core 테마 재점검 주기
THEME_ROTATION_DAYS = 7        # 비 core 테마 재점검 주기

# 상태 파일 관리
MAX_OBSERVATIONS = 12          # 지표당 보관할 관측 이력 개수
# 같은 흐름이 이 횟수 이상 반복 관측되면 'thesis 갱신 후보' 로 승격한다.
# 테마 레이어는 판정을 하지 않으므로, 누적만이 유일한 승격 경로다.
THESIS_REVIEW_THRESHOLD = 3
THEME_SHIFT_EXPIRE_DAYS = 240  # 이 기간 재확인 안 된 테마 흐름은 정리

# 각주
MAX_SOURCES_PER_FINDING = 4    # finding 당 출처 상한 (모델에게 지시 + 코드에서 절단)
MAX_TELEGRAM_SOURCES = 14      # 텔레그램 📎 출처 블록 표기 상한 (4000자 제한 대비)
# 분기 실적은 약 90일 간격이다. 120일이면 Q1 플래그가 Q2 확인 전에 만료될 수 있어
# 분기 연속 판정이 성립하지 않는다. 1년 이상 버티게 잡는다.
FLAG_EXPIRE_DAYS = 400         # 이 기간 재확인 안 된 플래그는 정리

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


def fetch_us_prices(tickers: Optional[list[str]] = None) -> list[dict]:
    """미국 종목 yfinance 데이터. tickers 미지정 시 레거시 워치리스트."""
    results = []
    for ticker in (US_TICKERS if tickers is None else tickers):
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


def fetch_kr_prices(
    tickers: Optional[list[str]] = None, names: Optional[dict] = None
) -> list[dict]:
    """한국 종목 pykrx 데이터. tickers 미지정 시 레거시 워치리스트."""
    if not PYKRX_AVAILABLE:
        return []

    name_map = KR_NAMES if names is None else names
    last_day = get_last_kr_trading_day()
    prev_day = (datetime.strptime(last_day, "%Y%m%d") - timedelta(days=7)).strftime("%Y%m%d")

    results = []
    for ticker in (KR_TICKERS if tickers is None else tickers):
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
                "name": name_map.get(ticker, ""),
                "market": "KR",
                "price": int(current),
                "change_pct": round(float(change_pct), 2),
                "volume_ratio": round(float(vol_ratio), 2),
            })
        except Exception as e:
            logger.warning(f"{ticker} ({name_map.get(ticker, '')}) 수집 실패: {e}")
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


def load_theme_state() -> dict:
    """theme_state.json 로드. 없으면 빈 상태로 시작.

    포지션 상태와 파일을 나눈 이유: 테마는 판정(RED/YELLOW)을 하지 않고
    '흐름의 반복 관측' 만 쌓는다. 성격이 달라 섞으면 open_flags 의 의미가 흐려진다.
    """
    empty = {"meta": {"version": "1.0", "last_run": None}, "themes": {}}
    if not THEME_STATE_PATH.exists():
        logger.info("theme_state.json 없음 — 새로 시작")
        return empty
    try:
        state = json.loads(THEME_STATE_PATH.read_text(encoding="utf-8"))
        state.setdefault("meta", {"version": "1.0", "last_run": None})
        state.setdefault("themes", {})
        return state
    except Exception as e:
        logger.warning(f"theme_state.json 파싱 실패 — 새로 시작: {e}")
        return empty


def save_theme_state(state: dict, today_str: str, path: Optional[Path] = None):
    """테마 상태 저장. 실패해도 다이제스트는 계속 진행."""
    target = path or THEME_STATE_PATH
    try:
        state["meta"]["last_run"] = today_str
        state["meta"].setdefault("version", "1.0")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        logger.info(f"테마 상태 저장: {target}")
    except Exception as e:
        logger.error(f"테마 상태 파일 저장 실패 ({target}): {e}")


# ============================================================
# 출처 각주
# ============================================================

# 각주 마커. 하루 findings 30여 건 × 출처 최대 4개면 dedupe 후에도 20개를 훌쩍 넘는다.
# 실측(2026-08-15): 출처 참조 92건 → 고유 다수. 20개에서 끊으면 나머지 항목이
# 통째로 '출처 없음' 이 되어 근거 없는 문장으로 출력된다.
_CIRCLED = (
    "".join(chr(0x2460 + i) for i in range(20))    # ①..⑳
    + "".join(chr(0x3251 + i) for i in range(15))  # ㉑..㉟
    + "".join(chr(0x32B1 + i) for i in range(15))  # ㊱..㊿
)
_TIER_LABEL = {"S1": "1차", "S2": "언론", "S3": "미검증"}


def _marker(idx: int) -> str:
    """0-based 인덱스 → 각주 마커. 50 을 넘으면 [51] 형태로 이어간다."""
    return _CIRCLED[idx] if idx < len(_CIRCLED) else f"[{idx + 1}]"


# 본문에서 실제로 인용된 마커를 찾는 패턴.
# [K3]·[T1] 같은 조건 번호와 섞이지 않도록 대괄호형은 숫자만 허용한다.
_MARKER_RE = re.compile("[" + _CIRCLED + r"]|\[\d{1,3}\]")


def _outlet_from_url(url: str) -> str:
    """URL 에서 표시용 도메인 추출. 실패하면 원문 앞부분."""
    m = re.match(r"^\s*(?:https?://)?(?:www\.)?([^/\s?#]+)", url or "")
    return m.group(1) if m else (url or "").strip()[:40]


def normalize_sources(finding: dict) -> list[dict]:
    """finding 에서 출처 목록을 정규화한다.

    스키마를 sources 배열로 바꿨지만, 구형 evidence_url(단수)로 응답하는 경우와
    문자열 URL 만 던지는 경우가 섞여 들어온다. 셋 다 같은 모양으로 만든다.
    """
    raw = finding.get("sources")
    if not isinstance(raw, list) or not raw:
        url = finding.get("evidence_url")
        raw = [url] if url else []

    out = []
    for item in raw:
        if isinstance(item, str):
            item = {"url": item}
        if not isinstance(item, dict):
            continue
        url = (item.get("url") or "").strip()
        outlet = (item.get("outlet") or "").strip() or _outlet_from_url(url)
        if not url and not outlet:
            continue
        tier = (item.get("tier") or "S2").upper()
        out.append({
            "url": url,
            "outlet": outlet,
            "date": (item.get("date") or finding.get("reported_at") or "").strip(),
            "tier": tier if tier in _TIER_LABEL else "S2",
            "note": (item.get("note") or "").strip(),
        })
    return out[:MAX_SOURCES_PER_FINDING]


def max_tier(sources: list[dict]) -> str:
    """가장 신뢰도 높은 출처 등급. 없으면 S3."""
    for tier in ("S1", "S2", "S3"):
        if any(s.get("tier") == tier for s in sources):
            return tier
    return "S3"


class SourceRegistry:
    """각주 번호를 코드가 결정론적으로 매긴다.

    모델에게 번호를 매기게 하면 중복·누락·본문에만 있고 목록에 없는 각주가 생긴다.
    등록 순서대로 ①②③ 을 부여하고, 같은 URL 은 한 번호로 합친다.
    검색 호출이 여러 개라 같은 기사가 Layer 0 과 포지션 양쪽에서 나오는데,
    dedupe 를 코드가 하므로 출처 목록이 부풀지 않는다.
    """

    def __init__(self):
        self._by_key: dict[str, int] = {}
        self._items: list[dict] = []

    @staticmethod
    def _key(src: dict) -> str:
        url = (src.get("url") or "").strip().rstrip("/").lower()
        if url:
            return url
        return f"{src.get('outlet', '').lower()}|{src.get('date', '')}"

    def add(self, src: dict) -> Optional[str]:
        """출처 1건 등록. 각주 마커(①) 리턴. 상한 없음."""
        key = self._key(src)
        if key in self._by_key:
            idx = self._by_key[key]
            # 같은 URL 이 더 좋은 등급으로 다시 들어오면 등급만 올려준다
            if src.get("tier", "S3") < self._items[idx].get("tier", "S3"):
                self._items[idx]["tier"] = src["tier"]
            return _marker(idx)
        idx = len(self._items)
        self._by_key[key] = idx
        self._items.append(dict(src))
        return _marker(idx)

    def add_all(self, sources: list[dict]) -> str:
        """출처 여러 건 등록. 붙여쓴 마커 문자열(①②) 리턴."""
        marks = [m for m in (self.add(s) for s in sources) if m]
        return "".join(marks)

    def __len__(self) -> int:
        return len(self._items)

    def items(self) -> list[dict]:
        """번호 순 출처 목록 (dry-run 산출물·디버깅용)."""
        return [{"marker": _marker(i), **s} for i, s in enumerate(self._items)]

    def cited(self, text: str) -> list[tuple[str, dict]]:
        """text 에서 실제로 인용된 출처만 (마커, 출처) 순서대로 리턴.

        등록된 출처가 전부 다이제스트에 실리지는 않는다 — 모델이 항목을 추리기
        때문이다. 인용 안 된 것까지 목록에 넣으면 본문에 없는 번호가 줄줄이 남는다.
        번호는 재부여하지 않는다. 재부여하면 본문 마커와 어긋난다.
        """
        used = set(_MARKER_RE.findall(text or ""))
        return [(m, s) for m, s in
                ((_marker(i), s) for i, s in enumerate(self._items)) if m in used]

    def unknown_markers(self, text: str) -> list[str]:
        """본문에 있으나 등록되지 않은 마커 — 모델이 지어낸 각주."""
        known = {_marker(i) for i in range(len(self._items))}
        return sorted(set(_MARKER_RE.findall(text or "")) - known)

    def render_file(self, text: str) -> str:
        """파일용 📎 출처 블록 (URL 링크 포함). text 에 인용된 것만."""
        rows = self.cited(text)
        if not rows:
            return ""
        lines = ["", "---", "", "## 📎 출처", ""]
        for marker, s in rows:
            label = _TIER_LABEL.get(s["tier"], s["tier"])
            name = s["outlet"] or "출처 미상"
            body = f"[{name}]({s['url']})" if s["url"] else name
            bits = [b for b in (s["date"], label, s["note"]) if b]
            lines.append(f"{marker} {body} · {' · '.join(bits)}")
        lines.append("")
        return "\n".join(lines)

    def render_telegram(self, text: str, limit: int = MAX_TELEGRAM_SOURCES) -> str:
        """텔레그램용 📎 출처 블록 (URL 없이 도메인·날짜만 — 4000자 제한 대비)."""
        rows = self.cited(text)
        if not rows:
            return ""
        lines = ["", "", "📎 출처"]
        for marker, s in rows[:limit]:
            label = _TIER_LABEL.get(s["tier"], s["tier"])
            date = s["date"][5:] if len(s["date"]) == 10 else s["date"]
            bits = [b for b in (date, label) if b]
            lines.append(f"{marker} {s['outlet'] or '출처 미상'} · {' · '.join(bits)}")
        if len(rows) > limit:
            lines.append(f"(외 {len(rows) - limit}건은 첨부 파일 참조)")
        return "\n".join(lines)


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


def select_themes(
    themes: list[dict],
    theme_state: dict,
    upcoming: list[dict],
    today_str: str,
) -> tuple[list[dict], list[dict]]:
    """테마(Layer 0.5) 검색 대상 선별. (선별됨, 미선별) 리턴.

    포지션 선별과 같은 구조지만 트리거가 다르다. 테마는 가격으로 움직이지 않는다.
    - 캘린더 이벤트 매칭: OCP·GTC·OFC 같은 컨퍼런스에서 아키텍처 변경이 먼저 나온다.
      뉴스로 나올 땐 이미 늦으므로, 해당 주간에는 그 테마를 앞으로 당긴다.
    - rotation: core 는 3일, 나머지는 7일
    """
    event_text = " ".join(e["line"] for e in upcoming)
    entries = theme_state.get("themes", {})

    candidates = []
    for theme in themes:
        reasons = []

        hay = [theme.get("label", ""), *theme.get("queries", [])]
        kw_hit = [k for k in hay if k and len(k) >= 3 and k in event_text]
        if kw_hit:
            reasons.append(f"{EVENT_WINDOW_DAYS}일 내 이벤트 매칭: {', '.join(kw_hit[:2])}")

        rotation = THEME_ROTATION_DAYS_CORE if theme.get("core") else THEME_ROTATION_DAYS
        stale = days_since(entries.get(theme["id"], {}).get("last_checked"), today_str)
        if stale is None:
            reasons.append("최초 점검")
        elif stale >= rotation:
            reasons.append(f"{stale}일 미점검 (rotation, 주기 {rotation}일)")

        if reasons:
            candidates.append({
                "theme": theme,
                "reasons": reasons,
                "stale": 9999 if stale is None else stale,
                "triggered": bool(kw_hit),
            })

    # 이벤트 트리거 우선 → core 우선 → 오래 방치된 순
    candidates.sort(key=lambda c: (
        0 if c["triggered"] else 1,
        0 if c["theme"].get("core") else 1,
        -c["stale"],
    ))

    selected = candidates[:MAX_SEARCH_THEMES]
    selected_ids = {c["theme"]["id"] for c in selected}
    unselected = [t for t in themes if t["id"] not in selected_ids]
    return selected, unselected


def numbered(items: list, prefix: str, indent: str = "  ") -> str:
    """thesis·kill_signals 에 번호를 매긴다.

    출력에서 '[K3]' 처럼 어떤 조건에 걸린 사실인지 역참조할 수 있게 하기 위함.
    번호는 positions.json 의 배열 순서를 그대로 따른다.
    """
    if not items:
        return f"{indent}(없음)"
    return "\n".join(f"{indent}{prefix}{i}. {t}" for i, t in enumerate(items, 1))


def collect_position_tickers(positions_doc: dict) -> tuple[list[str], list[str], dict]:
    """모니터링 대상 포지션의 티커만 추출. (미국, 한국, 티커→이름)

    레거시 워치리스트 32종목 대신 이걸 쓴다. 포지션과 무관한 종목의 등락은
    다이제스트에서 노이즈일 뿐이고, 수집 대상도 11개로 줄어든다.
    """
    us, kr, names = [], [], {}
    for pos in positions_doc.get("positions", []):
        if pos.get("status") not in MONITORED_STATUSES:
            continue
        label = pos.get("label", "")
        for ticker in pos.get("tickers", []):
            (kr if ticker.isdigit() and len(ticker) == 6 else us).append(ticker)
            names[ticker] = KR_NAMES.get(ticker) or label
    return list(dict.fromkeys(us)), list(dict.fromkeys(kr)), names


def display_name(pos: dict) -> str:
    """출력용 포지션 표시명. 영문 슬러그(id)는 절대 노출하지 않는다."""
    tickers = ", ".join(pos.get("tickers", []))
    label = pos.get("label", "")
    if not tickers:
        return label
    # "SSD 컨트롤러 (파두)" + 티커 -> "SSD 컨트롤러 (파두 440110)" (괄호 중첩 방지)
    if label.endswith(")"):
        return f"{label[:-1]} {tickers})"
    return f"{label} ({tickers})"


def format_position_config(pos: dict) -> str:
    """포지션 1개의 판정 기준을 번호 매겨 정리 (종합 프롬프트 컨텍스트용)."""
    watch = pos.get("watch", {})
    return "\n".join([
        f"### {display_name(pos)} (status: {pos.get('status')})",
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
    now_str: str,
    positions_doc: dict,
    layer0_result: Optional[dict],
    news_sweep: Optional[dict],
    position_results: list[dict],
    unchecked: list[dict],
    upcoming: list[dict],
    state: dict,
    theme_results: Optional[list[dict]] = None,
    theme_state: Optional[dict] = None,
    registry: Optional[SourceRegistry] = None,
) -> str:
    """종합 호출 프롬프트.

    포지션 판정 기준(thesis·kill_signals·watch) + 오늘 검색 결과를 결합해
    3단계 등급 다이제스트를 작성시킨다. 판단·조치 제안은 시키지 않는다.

    출처는 본문에 URL 로 넣지 않고 각주 마커(①②)만 심는다. 번호 부여와
    📎 출처 목록 렌더링은 registry 가 전담한다 — 모델에게 번호를 매기게 하면
    중복·누락·목록에 없는 각주가 생긴다. 등록 순서가 곧 번호이므로
    아래에서 출력 순서(Layer 0 → RED → YELLOW → WHITE → 테마 → 소식)대로 등록한다.
    """
    theme_results = theme_results or []
    theme_state = theme_state or {}
    registry = registry if registry is not None else SourceRegistry()

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
    def fmt_detail(f: dict, indent: str = "  ") -> list[str]:
        """quant / qual / 각주 마커 — finding 공통 부속 줄."""
        lines = []
        quant = f.get("quant") or {}
        if isinstance(quant, dict) and quant:
            lines.append(f"{indent}정량: " + " · ".join(f"{k} = {v}" for k, v in quant.items()))
        for q in (f.get("qual") or [])[:3]:
            lines.append(f"{indent}맥락: {q}")
        sources = normalize_sources(f)
        marks = registry.add_all(sources)
        if marks:
            tier = max_tier(sources)
            warn = "  ※ 미검증 출처뿐 — RED 로 올리지 말 것" if tier == "S3" else ""
            lines.append(f"{indent}근거 {marks}{warn}")
        else:
            lines.append(f"{indent}근거 (출처 없음 — 출력하지 말 것)")
        return lines

    def fmt_findings(findings) -> str:
        if not findings:
            return "- (신호 없음)"
        out = []
        for f in findings:
            refs = ", ".join(f.get("refs") or []) or "연결 번호 없음"
            block = [
                f"- [{f.get('level', '?')}] ({refs}) {f.get('summary', '')}",
                f"  해당 조건: {f.get('signal') or '-'}",
            ]
            block += fmt_detail(f)
            out.append("\n".join(block))
        return "\n".join(out)

    # 각주 번호는 등록 순서를 따른다. 출력에서 Layer 0 이 맨 위로 가므로 먼저 등록.
    layer0_section = (
        fmt_findings(layer0_result.get("findings"))
        if layer0_result else "- (Layer 0 검색 실패 또는 미실행 — 판정 없음)"
    )

    # 포지션 findings 는 등급 순으로 등록해야 번호가 읽는 순서와 대체로 맞는다
    _LEVEL_ORDER = {"RED": 0, "YELLOW": 1, "WHITE": 2}
    for item in position_results:
        for f in sorted(
            ((item.get("result") or {}).get("findings") or []),
            key=lambda x: _LEVEL_ORDER.get(x.get("level"), 3),
        ):
            registry.add_all(normalize_sources(f))

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
            body = f"- ⚠️ 미점검: {item['skipped']} — 신호 없음이 아니라 확인 안 함"
        elif item.get("incomplete"):
            found = fmt_findings(result.get("findings")) if result else ""
            body = (
                f"- ⚠️ 확인 미완료: {item['incomplete']}\n"
                f"  아래 항목은 확인된 것만이며, 이 포지션을 '이상 없음' 으로 쓰면 안 된다.\n"
                f"{found}"
            )
        elif result:
            body = fmt_findings(result.get("findings"))
        else:
            body = "- ⚠️ 확인 미완료: 검색 실패 — 판정 없음"

        pos_blocks.append(
            f"## {display_name(pos)}\n"
            f"점검 사유: {'; '.join(item.get('reasons', []))}\n"
            f"{body}{repeat_line}"
        )
    position_section = "\n\n".join(pos_blocks) if pos_blocks else "(오늘 검색한 포지션 없음)"

    # ---- 테마 (Layer 0.5) ----
    by_id = {p["id"]: p for p in positions_doc.get("positions", [])}

    def fan_out(finding: dict, theme: dict) -> str:
        """테마 finding 이 닿는 포지션을 사람이 읽는 이름으로 펼친다.

        이게 '연결' 의 실체다. 오늘 그 포지션을 개별 검색했든 안 했든 나온다.
        모델이 엉뚱한 id 를 뱉을 수 있으므로 theme.affects 안으로 한정한다.
        """
        allowed = [pid for pid in theme.get("affects", []) if pid in by_id]
        picked = [pid for pid in (finding.get("affects") or []) if pid in allowed] or allowed
        return ", ".join(display_name(by_id[pid]) for pid in picked) or "(연결 포지션 없음)"

    theme_blocks = []
    for item in theme_results:
        theme = item["theme"]
        result = item.get("result") or {}
        entry = theme_state.get("themes", {}).get(theme["id"], {})
        shifts = entry.get("shifts", {})

        if item.get("skipped"):
            body = f"- ⚠️ 미점검: {item['skipped']}"
        elif not result or not (result.get("findings") or []):
            note = f" (확인 미완료: {item['incomplete']})" if item.get("incomplete") else ""
            body = f"- (새로운 흐름 없음){note}"
        else:
            lines = []
            for f in (result.get("findings") or [])[:4]:
                refs = ", ".join(f.get("refs") or []) or "-"
                head = f.get("headline") or f.get("shift") or ""
                lines.append(
                    f"- ({refs}) [{f.get('direction', '불명')}] {head} — {f.get('summary', '')}"
                )
                lines += fmt_detail(f)
                lines.append(f"  닿는 포지션: {fan_out(f, theme)}")
                rec = shifts.get(_shift_key(f))
                if rec and rec.get("count", 1) >= 2:
                    promo = " ★ thesis 갱신 후보" if rec.get("thesis_review") else ""
                    lines.append(
                        f"  누적: {rec['count']}회째 관측 (최초 {rec.get('first_seen')}){promo}"
                    )
                else:
                    lines.append("  누적: 신규 관측")
            body = "\n".join(lines)
            if item.get("incomplete"):
                body = f"- ⚠️ 확인 미완료: {item['incomplete']}\n" + body

        theme_blocks.append(
            f"## {theme.get('label')}\n"
            f"점검 사유: {'; '.join(item.get('reasons', []))}\n"
            f"{body}"
        )
    theme_section = "\n\n".join(theme_blocks) if theme_blocks else "(오늘 검색한 테마 없음)"

    # 오늘 안 본 테마 중 누적된 흐름 — 매일 재검색하지 않아도 승격분은 계속 보인다
    carry_lines = []
    checked_ids = {i["theme"]["id"] for i in theme_results}
    for tid, entry in (theme_state.get("themes") or {}).items():
        if tid in checked_ids:
            continue
        for rec in (entry.get("shifts") or {}).values():
            if not rec.get("thesis_review"):
                continue
            carry_lines.append(
                f"- {rec.get('headline')} [{rec.get('direction')}] "
                f"{rec['count']}회째, 최근 {rec.get('last_seen')} — {rec.get('summary', '')[:80]}"
            )
    carry_section = "\n".join(carry_lines[:5]) or "(없음)"

    sweep_lines = []
    for it in ((news_sweep or {}).get("items") or []):
        who = it.get("position_label") or it.get("position_id") or "?"
        block = [f"- {who}: {it.get('summary', '')}"]
        block += fmt_detail(it)
        sweep_lines.append(chr(10).join(block))
    sweep_section = chr(10).join(sweep_lines) or "(최근 소식 없음)"

    unchecked_section = "\n".join(
        f"- {display_name(p)}: 마지막 점검 "
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

# Layer 0.5 — 테마 (상위 변화 추적. ★ 판정 아님)
포지션 검색은 하루 {MAX_SEARCH_POSITIONS}개뿐이라, 여러 포지션을 동시에 흔드는
상위 변화는 그날 뽑힌 포지션에 우연히 걸리지 않으면 통째로 새어나간다.
이 레이어가 그 구멍을 메운다. **'닿는 포지션' 은 오늘 개별 검색했는지와 무관하게 나온다.**

등급(🔴🟡⚪)을 매기지 말 것. 여기 있는 내용은 kill_signals 에 걸린 것이 아니다.
🔷 흐름 섹션에만 쓸 것. 조치·판단 제안 금지.

{theme_section}

## 오늘 점검하지 않은 테마 중 누적 승격분
{carry_section}

# 전 종목 최근 소식 (판정 아님 — 알아둘 것)
오늘 깊이 점검하지 않은 종목도 포함된다. 📰 섹션 재료로 쓸 것.
{sweep_section}

# 오늘 개별 검색하지 않은 포지션
{unchecked_section}

# 향후 {EVENT_WINDOW_DAYS}일 캘린더 이벤트 (파싱 완료분)
{events_section}

# 가격 (±{PRICE_DISPLAY_THRESHOLD}% 이상만)
{price_section}

# 출력 스펙 (★ 정확히 이대로)

두 블록을 순서대로 출력. 앞뒤 설명·코드블록 마커 없이 다이제스트만.

===TELEGRAM===
plain text, 표·markdown 문법 없이. 모바일에서 그대로 읽히게. 2600자 이내.

★ 영문 슬러그를 절대 쓰지 말 것. us-transformer, point-of-load, ess-foil 같은
   내부 식별자는 사람이 읽는 글이 아니다. 항상 한글 포지션명 + 티커로 쓸 것.
★ 읽는 사람은 K3·T1 같은 번호를 외우고 있지 않다. 번호 대신
   어떤 조건에 걸리는지를 그 조건의 말로 인용해 풀어 쓸 것.
★ "L0", "ESS알박", "파두 [K5]" 같은 축약 금지. 완전한 문장으로.
   글자 수를 줄이려고 조사를 빼거나 단어를 붙여 쓰지 말 것.
★ 아래 서식을 그대로 따를 것. 섹션 사이 빈 줄 1개, 항목 사이 빈 줄 1개.
   들여쓰기는 공백 2칸으로 맞출 것.

★★ 출처는 본문에 쓰지 말 것. 도메인·URL·매체명을 문장에 넣지 말 것.
   위 검색 결과에 붙어 있는 각주 마커(①②③…)를 항목 마지막 줄에
   "근거 ①②" 형태로 **그대로 옮겨 적기만** 할 것.
   - 마커를 새로 만들거나 번호를 바꾸지 말 것. 위에 없는 번호를 쓰지 말 것.
   - 한 항목에 여러 사실을 합쳤으면 해당 마커를 모두 붙일 것.
   - "📎 출처" 목록은 시스템이 자동으로 붙인다. 직접 작성하지 말 것.

--- 좋은 예 (이 모양 그대로) ---
🔴 판단 필요

• 미국 변압기 (효성중공업 298040 / HD현대일렉트릭 267260)
  미국 상무부가 반덤핑 연례재심 예비판정에서 효성중공업 관세율을
  0%에서 4.32%로 인상했다. 최종판정은 4분기로 예정돼 있고, 멤피스
  증설분 가동은 2027년이라 관세 적용 구간과 1년 이상 겹친다.
  ↳ 매도 검토 조건: "한국산 반덤핑 관세 강화 + 미국 현지 capa 미확보"
  근거 ①②③

--- 나쁜 예 (이렇게 쓰지 말 것) ---
- 파두 [K5] SK하이닉스 eSSD컨트롤러 전량 인하우스화 확인, 핵심세그 수주경로 차단
- L0 [L2] WoodMac 파이프라인 3분기연속↓ vs ConstructConnect 착공액↑, 지표상충
⚠️ 확인 미완료: us-transformer (K6 미확인)
  federalregister.gov · 08-10        ← 본문에 출처를 쓰면 안 된다
  근거 ⑦                              ← 위 검색 결과에 ⑦ 이 없으면 안 된다

📊 포지션 신호 — YYYY-MM-DD

🔴 판단 필요
• 포지션명 (회사명 티커)
  무슨 일이 있었는지 완전한 문장으로. 숫자가 있으면 반드시 포함.
  ↳ 매도 검토 조건에 해당: "해당 kill_signal 원문을 그대로 인용"
  근거 ①②
(해당 없으면 이 줄만: 없음)

🟡 확인 필요
• 포지션명 (회사명 티커)
  무슨 일이 있었는지 완전한 문장으로
  ↳ 관련 근거: "해당 thesis 또는 add_signal 원문을 그대로 인용"
  근거 ③
(해당 없으면: 없음)

🔷 AI 인프라 흐름
• 흐름 제목 — 무엇이 어디서 어디로 움직였는지 2~3문장. 숫자 포함.
  ↳ 닿는 포지션: 포지션명 (회사명 티커), 포지션명 (회사명 티커)
  ↳ 신규 관측  (또는: 3회째 관측 — thesis 갱신 후보)
  근거 ④⑤
(판정이 아니다. 조치·판단을 쓰지 말 것. 최대 4건. 해당 없으면: 없음)

📰 보유 종목 소식
• 포지션명 (회사명 티커) — 한 문장 요약  근거 ⑥
(판정 조건에 안 걸려도 알아둘 만한 것. 오늘 깊이 점검하지 않은 종목도 포함.
 최대 8건. 해당 없으면: 없음)

📅 향후 {EVENT_WINDOW_DAYS}일
- MM-DD 이벤트명 (관련 종목) [P1]
(해당 없으면: 없음)

📈 가격 ±{PRICE_DISPLAY_THRESHOLD}%
- 회사명 +N% (한 줄로 이어서. 해당 없으면: 없음)

⚠️ 확인 미완료
- 포지션명 (회사명): 무엇을 확인 못 했는지 한 줄
(없으면 이 섹션 자체를 생략)

오늘 점검 안 함: 포지션명, 포지션명, ...

===FILE===
markdown. 헤더는 ##. 텔레그램 요약과 별개로 작성하되 사실이 서로 어긋나면 안 됨.
출처 규칙은 텔레그램과 동일 — 본문에 URL·도메인을 쓰지 말고 각주 마커만 옮길 것.

## 🔴 KILL 관련
포지션마다 아래 형식:
- **포지션명 (회사명 티커)** — [K3] 해당 kill_signal 원문 (번호는 추적용, 원문을 반드시 함께)
  사실: 2~3문장
  정량: 지표 = 이전 → 이후  ← 숫자가 있을 때만
  맥락: 숫자로 안 잡히는 것  ← 있을 때만
  근거: ①②
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

## 🔷 AI 인프라 흐름 (Layer 0.5)
판정이 아니다. 등급을 매기지 말 것. 테마별로:
- **흐름 제목** — [W2] 해당 watch_shift 원문
  사실: 무엇이 어디서 어디로 움직였는지 2~3문장
  정량: 지표 = 이전 → 이후
  맥락: 숫자로 안 잡히는 것
  닿는 포지션: 포지션명 (회사명 티커), ...
  누적: 신규 관측 / N회째 관측 (최초 YYYY-MM-DD) — thesis 갱신 후보
  근거: ④⑤
(해당 없으면 "없음")

'오늘 점검하지 않은 테마 중 누적 승격분' 이 있으면 이 섹션 끝에
"### 계속 쌓이는 중 (오늘 미점검 테마)" 소제목으로 한 줄씩 덧붙일 것.

## 향후 {EVENT_WINDOW_DAYS}일 이벤트
표 (날짜 / 이벤트 / 관련 포지션 / P). P1·P2만.

## ⚠️ 확인 미완료
검색을 시작했으나 끝내지 못한 포지션. 사유와 확인된 범위를 적을 것.
"신호 없음" 과 절대 섞어 쓰지 말 것. 해당 없으면 "없음".

## 오늘 미점검 포지션
- 포지션명 [id] — 마지막 점검 YYYY-MM-DD (확인 안 함)

## 가격
±{PRICE_DISPLAY_THRESHOLD}% 이상만 한 줄. 문서 맨 아래.

# 작성 규칙 (위반 금지)

0. 영문 슬러그(us-transformer, ess-foil 등)를 출력 어디에도 쓰지 말 것.
   포지션은 항상 한글명 + 티커로 표기한다.
1. 파일(===FILE===) 에서는 각 항목에 연결 번호를 붙일 것: [K#] [T#] [A#] [L#] [W#].
   단 번호만 쓰지 말고 조건 원문을 함께 인용할 것. 텔레그램에는 번호를 쓰지 않는다.
   어느 조건에도 연결되지 않는 사실은 📰 보유 종목 소식 또는 🔷 흐름에만 넣을 것.
2. ignore 목록에 해당하는 내용은 **아예 출력하지 말 것**. 언급조차 금지.
3. 해당 없으면 "없음" 한 단어로 끝낼 것. 억지로 채우거나 분량을 맞추려 하지 말 것.
   빈 섹션에 "특이사항 없으나 ..." 같은 사족 금지.
4. 판단·조치를 제안하지 말 것. "매수 검토", "비중 확대", "진입", "익절", "손절",
   "관심 필요", "대응 필요" 같은 표현 금지. 사실과 어떤 조건에 걸리는지만 쓴다.
5. 검색으로 확인되지 않은 사실을 쓰지 말 것. 가격 변동에 추측 사유를 갖다붙이지 말 것.
   모르면 "사유 미확인".
6. 상태를 3가지로 구분할 것. 절대 섞지 말 것.
   - 점검 완료 + 신호 없음 → "없음"
   - ⚠️ 확인 미완료 (검색을 끝내지 못함) → 별도 섹션에 사유와 함께
   - 미점검 (검색 자체를 안 함) → "확인 안 함"
   확인 미완료·미점검을 "이상 없음" 으로 쓰면 안 된다.
7. 각주 마커가 없는 항목은 만들지 말 것 (출처가 없다는 뜻이다).
   본문 어디에도 URL·도메인·매체명을 쓰지 말 것. 📎 출처 목록을 직접 만들지 말 것.
   위 검색 결과에 등장하지 않은 각주 번호를 쓰면 안 된다.
8. 가격은 반드시 맨 아래. 위쪽 섹션에서 가격 등락을 서술하지 말 것.
9. 🔷 흐름 섹션에 🔴🟡⚪ 등급을 매기지 말 것. 이 섹션은 판정이 아니라
   "이 방향이 계속되면 thesis 문장을 고쳐야 한다" 는 관찰이다.
   같은 사실이 포지션 판정(🔴🟡)에도 걸렸다면 판정 쪽에만 쓰고 여기서는 뺄 것.
10. 여러 출처가 같은 사건을 다뤘으면 **하나의 항목으로 합쳐** 쓸 것.
   출처 수만큼 항목을 쪼개지 말 것. 근거 마커만 여러 개 붙인다.

# 톤
직설·짧음. AI 특유의 모호함·"~할 수 있습니다" 금지. "~다" 또는 "~함" 위주.
수식어보다 숫자와 날짜.
"""
    return prompt


def new_usage() -> dict:
    return {"input": 0, "output": 0, "searches": 0, "reported_cost": 0.0}


def merge_usage(total: dict, part: dict) -> dict:
    for k in ("input", "output", "searches", "reported_cost"):
        total[k] = total.get(k, 0) + part.get(k, 0)
    return total


def calc_cost(usage: dict) -> float:
    """토큰 + 웹 검색 요청 비용. CLI 모드는 CLI 가 보고한 값을 그대로 쓴다."""
    if usage.get("reported_cost"):
        return usage["reported_cost"]
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


def call_claude_cli(prompt: str, *, use_search: bool) -> tuple[str, dict]:
    """Claude Code CLI 로 호출 (구독 사용량). (텍스트, usage) 리턴.

    API 와 달리 max_uses 를 강제할 수 없어 검색 횟수는 프롬프트로만 유도한다.
    비용은 CLI 가 보고하는 total_cost_usd 를 그대로 쓴다 (내부 서브에이전트 포함).
    """
    cmd = [CLAUDE_CLI_BIN, "-p", prompt, "--model", MODEL, "--output-format", "json"]
    if use_search:
        cmd += ["--allowedTools", "WebSearch", "WebFetch"]

    proc = subprocess.run(
        cmd, cwd=PROJECT_ROOT, capture_output=True, timeout=CLAUDE_CLI_TIMEOUT
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"claude CLI 실패 (exit {proc.returncode}): "
            f"{proc.stderr.decode(errors='replace')[:400]}"
        )

    payload = json.loads(proc.stdout.decode(errors="replace"))
    if payload.get("is_error"):
        raise RuntimeError(f"claude CLI 오류: {str(payload.get('result'))[:300]}")

    u = payload.get("usage") or {}
    server = u.get("server_tool_use") or {}
    usage = {
        "input": (u.get("input_tokens") or 0)
        + (u.get("cache_creation_input_tokens") or 0)
        + (u.get("cache_read_input_tokens") or 0),
        "output": u.get("output_tokens") or 0,
        "searches": server.get("web_search_requests") or 0,
        "reported_cost": payload.get("total_cost_usd") or 0.0,
    }
    # CLI 는 검색을 하위 모델에 위임하므로 server_tool_use 가 0 으로 올 수 있다.
    # modelUsage 쪽 집계로 보정한다.
    if not usage["searches"]:
        usage["searches"] = sum(
            (m.get("webSearchRequests") or 0)
            for m in (payload.get("modelUsage") or {}).values()
        )
    return str(payload.get("result") or ""), usage


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
    if USE_CLAUDE_CLI:
        return call_claude_cli(prompt, use_search=use_search)

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

근거 없는 추측 금지. 검색으로 확인한 사실만.
해당 신호가 없으면 findings 를 빈 배열로 두고 no_news 를 true 로 할 것."""

# 출처를 finding 당 여러 개 받는다. 예전에는 evidence_url 하나뿐이라
# "같은 사건을 여러 곳이 보도" 를 표현할 방법이 없어 항목이 쪼개졌다.
_SOURCE_RULE = f"""출처 규칙 (sources 배열):
- 같은 사실을 여러 곳에서 확인했으면 **한 finding 에 모아** sources 에 전부 넣을 것.
  같은 사건을 출처 수만큼 여러 finding 으로 쪼개지 말 것.
- 최대 {MAX_SOURCES_PER_FINDING}개. 1차 원문이 있으면 반드시 첫 번째에 둘 것.
- tier 구분:
  S1 = 1차 원문 (공시·기업 IR·실적발표·정부/규제기관 문서·법원 판결문)
  S2 = 언론 보도·업계 리서치 기관
  S3 = 미검증 (블로그·커뮤니티·추측성 보도·익명 소식통)
- ★ S3 만으로는 RED 를 매기지 말 것. S3 단독이면 최대 YELLOW 이고
  summary 에 "미검증" 을 명시할 것.
- 출처가 하나도 없는 항목은 아예 만들지 말 것.

내용 규칙 (summary / quant / qual):
- summary: 무슨 일이 있었는지 2~3문장. 여러 출처의 내용을 하나로 합쳐서 쓸 것.
- quant: 숫자로 확인된 것만 {{"지표명": "값"}} 으로. 변화면 "이전 → 이후" 형태로.
  숫자가 없으면 빈 객체.
- qual: 숫자로 안 잡히는 맥락·해석을 한 줄씩. 최대 3개. 없으면 빈 배열.
  추측이면 문장에 "미확인" 또는 "미검증" 을 붙일 것."""

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

    # CLI 모드는 max_uses 파라미터가 없어 API 처럼 강제할 수 없다. 프롬프트로 유도한다.
    if USE_CLAUDE_CLI:
        prompt = (
            f"{prompt}\n\n"
            f"웹 검색은 최대 {max_uses}회 이내로 쓸 것. "
            f"한도에 걸려 확인을 못 끝냈으면 search_complete=false 로 정직하게 보고할 것."
        )

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

{_SOURCE_RULE}

각 finding 은 어떤 번호에 걸리는지 refs 로 반드시 명시할 것 (예: ["L2"]).

{{
  "findings": [
    {{
      "level": "RED|YELLOW|WHITE",
      "refs": ["L2"],
      "signal": "해당 KILL 신호 원문",
      "summary": "무슨 일이 있었는지 2~3문장",
      "quant": {{"지표명": "값 또는 이전 → 이후"}},
      "qual": ["숫자로 안 잡히는 맥락 한 줄"],
      "sources": [
        {{"url": "출처 URL", "outlet": "도메인 또는 매체명", "date": "YYYY-MM-DD", "tier": "S1|S2|S3"}}
      ],
      "reported_at": "YYYY-MM-DD"
    }}
  ],
  "observations": {{"지표명": "관측값 (예: 리드타임 = 4~5년)"}},
  "no_news": false
}}

JSON 외 다른 텍스트 출력 금지."""

    return _run_search(prompt, LAYER0_MAX_USES, "Layer 0")


def search_news_sweep(positions: list[dict], now_str: str) -> tuple[Optional[dict], dict]:
    """모니터링 대상 전 종목의 최근 소식을 훑는다 (판정 아님).

    개별 검색은 하루 3개까지라 나머지 7개는 아무 정보도 안 나온다.
    kill/thesis 에 안 걸려도 보유 종목에 무슨 일이 있었는지는 알아야 하므로
    한 번의 호출로 전 종목 헤드라인 수준을 훑는다.
    """
    if not positions:
        return None, new_usage()

    lines = []
    for pos in positions:
        lines.append(
            f"- {pos.get('label')} / 티커 {', '.join(pos.get('tickers', []))}"
            f" / 무시할 것: {'; '.join(pos.get('ignore', [])) or '(없음)'}"
        )
    roster = chr(10).join(lines)

    prompt = f"""당신은 보유 종목의 최근 소식을 훑는 분석가.

# 현재 시점
{now_str}

# 대상 종목
{roster}

# 작업
각 종목의 최근 7일 이내 주목할 만한 소식을 web_search 로 찾아 정리.
매도·매수를 판정하는 자리가 아니다. **무슨 일이 있었는지 사실만** 모은다.

포함: 실적·수주·계약·증설·인허가·소송·경영권 변동·정책 변화·주요 고객사 동향
제외: 각 종목의 '무시할 것' 에 해당하는 내용, 단순 주가 등락, 목표주가 조정,
      증권사 투자의견, 근거 없는 추측성 보도

소식이 없는 종목은 items 에 넣지 말 것. 억지로 채우지 말 것.
종목당 최대 2건, 전체 최대 12건. position_label 은 위 목록의 포지션명과 정확히 일치시킬 것.

{_SOURCE_RULE}

아래 JSON 만 출력:

{{
  "items": [
    {{
      "position_label": "포지션명",
      "summary": "한두 문장 사실 요약",
      "quant": {{"지표명": "값"}},
      "sources": [
        {{"url": "출처 URL", "outlet": "도메인 또는 매체명", "date": "YYYY-MM-DD", "tier": "S1|S2|S3"}}
      ],
      "reported_at": "YYYY-MM-DD"
    }}
  ]
}}

JSON 외 다른 텍스트 출력 금지."""

    return _run_search(prompt, NEWS_SWEEP_MAX_USES, "종목 소식 스윕")


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

{_SOURCE_RULE}

"2개 분기 연속 감소" 처럼 누적이 필요한 신호는 오늘 1회 관측만으로 RED 로 올리지 말 것.
이전 관측 기록과 대조해 실제로 연속 조건이 충족될 때만 RED, 1회 관측이면 YELLOW.

각 finding 은 어떤 번호에 걸리는지 refs 로 반드시 명시할 것 (예: ["K3"], ["T1","K2"]).
어느 번호에도 연결되지 않으면 refs 를 빈 배열로 두고 level 은 WHITE.

★ search_complete 를 정직하게 채울 것.
검색 한도에 걸렸거나 필요한 확인을 끝내지 못했으면 search_complete=false, unchecked 에 못 본 항목 번호를 적을 것.
확인을 못 끝낸 것을 no_news=true (뉴스 없음) 로 보고하면 안 된다. 둘은 완전히 다른 상태다.

{{
  "position_id": "{pos.get('id')}",
  "search_complete": true,
  "unchecked": [],
  "findings": [
    {{
      "level": "RED|YELLOW|WHITE",
      "refs": ["K3"],
      "signal": "해당 항목 원문 (없으면 null)",
      "kind": "kill|add|info",
      "summary": "무슨 일이 있었는지 2~3문장",
      "quant": {{"지표명": "값 또는 이전 → 이후"}},
      "qual": ["숫자로 안 잡히는 맥락 한 줄"],
      "sources": [
        {{"url": "출처 URL", "outlet": "도메인 또는 매체명", "date": "YYYY-MM-DD", "tier": "S1|S2|S3"}}
      ],
      "reported_at": "YYYY-MM-DD"
    }}
  ],
  "observations": {{"지표명": "관측값"}},
  "no_news": false
}}

JSON 외 다른 텍스트 출력 금지."""

    return _run_search(prompt, POSITION_MAX_USES, f"포지션 {pos.get('id')}")


def search_theme(
    theme: dict,
    positions_by_id: dict,
    state_entry: dict,
    now_str: str,
) -> tuple[Optional[dict], dict]:
    """테마 1개 검색 (Layer 0.5). ★ 판정하지 않는다.

    포지션 검색이 "내 thesis 가 깨졌나" 를 묻는 방어적 질문이라면,
    이쪽은 "상위 변화가 어디로 얼마나 움직이나" 를 묻는다.
    등급을 매기지 않는 이유: 흥미로운 테크뉴스가 전부 YELLOW 로 올라오면
    판정 등급의 의미가 희석되고 다이제스트를 안 믿게 된다.
    승격 경로는 오직 '반복 관측 누적' 하나뿐이다.
    """
    affects = [pid for pid in theme.get("affects", []) if pid in positions_by_id]

    affected_lines = []
    for pid in affects:
        pos = positions_by_id[pid]
        thesis_head = (pos.get("thesis") or ["(thesis 미작성)"])[0]
        affected_lines.append(
            f"- {pid} — {display_name(pos)}\n  보유 근거 요지: {thesis_head}"
        )
    affected = chr(10).join(affected_lines) or "- (연결된 포지션 없음)"

    prev = json.dumps(state_entry, ensure_ascii=False, indent=2) if state_entry else "(이전 관측 없음)"

    prompt = f"""당신은 특정 기술·산업 테마의 '변화 방향과 속도' 를 추적하는 분석가.

# 현재 시점
{now_str}

# 테마
{theme.get('label')}

# 추적 대상 변화 (W번호로 역참조)
{numbered(theme.get('watch_shifts', []), 'W', indent='')}

# 검색 키워드
{', '.join(theme.get('queries', [])) or '(없음)'}

# 이 테마에 연결된 보유 포지션
{affected}

# 이전 관측 기록 (같은 흐름의 반복 여부 판정용)
{prev}

# 작업
web_search 로 위 추적 대상 변화 각각의 최신 상태를 확인하고 아래 JSON 만 출력.

★ 이 레이어는 **판정하지 않는다.**
- RED/YELLOW/WHITE 등급을 매기지 말 것. level 필드 자체가 없다.
- 매수·매도·비중·진입·손절 등 조치를 제안하지 말 것.
- "무엇이 어느 방향으로 얼마나 움직였는가" 만 쓴다.

최근 90일 이내 변화에 집중할 것. 이미 널리 알려진 배경 설명은 쓰지 말 것.
"변화가 없음" 도 유의미한 관측이다 — 억지로 findings 를 채우지 말고 no_news=true 로 둘 것.
finding 은 최대 4건. 중요도 순.

direction 은 **연결된 포지션 관점에서** 판단할 것:
  순풍 = 보유 근거를 강화하는 방향 / 역풍 = 약화하는 방향
  중립 = 방향성 없음 / 불명 = 판단 근거 부족

affects 에는 위 '연결된 포지션' 목록의 id 만 쓸 것. 그 변화가 실제로 닿는 것만
고를 것 — 테마에 속한다는 이유로 전부 나열하지 말 것.

{_SOURCE_RULE}

★ search_complete 를 정직하게 채울 것. 확인을 못 끝냈으면 false 와 unchecked.

{{
  "theme_id": "{theme.get('id')}",
  "search_complete": true,
  "unchecked": [],
  "findings": [
    {{
      "refs": ["W2"],
      "shift": "해당 watch_shifts 원문",
      "headline": "변화를 한 구절로 (15자 내외, 예: 랙 전력밀도)",
      "summary": "무엇이 어디서 어디로 움직였는지 2~3문장",
      "quant": {{"지표명": "이전 → 이후"}},
      "qual": ["숫자로 안 잡히는 맥락 한 줄"],
      "direction": "순풍|역풍|중립|불명",
      "affects": ["포지션 id"],
      "kind": "shift|issue|analysis",
      "sources": [
        {{"url": "출처 URL", "outlet": "도메인 또는 매체명", "date": "YYYY-MM-DD", "tier": "S1|S2|S3"}}
      ],
      "reported_at": "YYYY-MM-DD"
    }}
  ],
  "observations": {{"지표명": "관측값"}},
  "no_news": false
}}

JSON 외 다른 텍스트 출력 금지."""

    return _run_search(prompt, THEME_MAX_USES, f"테마 {theme.get('id')}")


# ============================================================
# 상태 갱신
# ============================================================

def is_search_incomplete(result: Optional[dict], searches_used: int, max_uses: int) -> Optional[str]:
    """이 포지션 점검이 '확인 미완료' 인지 판정. 사유 문자열 또는 None.

    검색 한도에 걸려 확인을 못 끝낸 것과 '뉴스가 없는 것' 은 완전히 다른 상태인데,
    모델이 후자로 보고해버리면 미점검이 '이상 없음' 으로 둔갑한다. 그걸 막는다.
    """
    if result is None:
        return "검색 호출 실패 또는 응답 파싱 실패"
    if result.get("search_complete") is False:
        unchecked = ", ".join(result.get("unchecked") or []) or "미상"
        return f"모델이 확인 미완료 보고 (미확인: {unchecked})"
    # 모델이 search_complete 를 안 채웠을 때의 안전망:
    # 검색을 상한까지 다 쓰고도 findings 가 비었으면 '뉴스 없음' 으로 보기 어렵다
    if searches_used >= max_uses and not (result.get("findings") or []):
        return f"검색 상한({max_uses}회) 소진 + findings 0건"
    return None


def merge_observations(entry: dict, observations: dict, today_str: str):
    """관측값 시계열 누적. 값이 바뀔 때만 새 항목, 같으면 last_seen 만 갱신."""
    entry.setdefault("observations", {})
    for key, value in (observations or {}).items():
        if value in (None, "", "확인 불가", "불명"):
            continue
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        series = entry["observations"].setdefault(key, [])
        if series and series[-1].get("value") == value:
            series[-1]["last_seen"] = today_str
        else:
            series.append({"date": today_str, "last_seen": today_str, "value": value})
        entry["observations"][key] = series[-MAX_OBSERVATIONS:]


def update_state_entry(
    entry: dict, result: dict, today_str: str, mark_checked: bool = True
) -> dict:
    """검색 결과를 상태 엔트리에 누적. 관측값 시계열 + 열린 플래그.

    mark_checked=False (확인 미완료) 면 last_checked 를 갱신하지 않는다 —
    갱신해버리면 rotation 이 '점검 완료' 로 보고 다음 순번에서 빼버린다.
    """
    entry.setdefault("observations", {})
    entry.setdefault("open_flags", [])
    if mark_checked:
        entry["last_checked"] = today_str

    merge_observations(entry, result.get("observations"), today_str)
    # finding 의 quant 도 관측값이다. observations 에만 의존하면
    # 모델이 quant 에만 숫자를 넣은 날의 시계열이 끊긴다.
    for finding in (result.get("findings") or []):
        merge_observations(entry, finding.get("quant"), today_str)

    # 열린 플래그: 같은 신호가 반복 관측되면 count 증가 → 연속 조건 판정 근거
    flags = {f.get("signal"): f for f in entry["open_flags"] if f.get("signal")}
    for finding in (result.get("findings") or []):
        if finding.get("level") not in ("RED", "YELLOW"):
            continue
        signal = finding.get("signal") or (finding.get("summary") or "")[:60]
        if not signal:
            continue
        sources = normalize_sources(finding)
        if signal in flags:
            flags[signal].update({
                "level": finding["level"],
                "last_seen": today_str,
                "count": flags[signal].get("count", 1) + 1,
                "summary": finding.get("summary", flags[signal].get("summary", "")),
                "sources": sources or flags[signal].get("sources", []),
            })
        else:
            flags[signal] = {
                "signal": signal,
                "level": finding["level"],
                "first_seen": today_str,
                "last_seen": today_str,
                "count": 1,
                "summary": finding.get("summary", ""),
                "sources": sources,
            }
        flags[signal].pop("evidence_url", None)  # 구형 스키마 잔재 정리

    # 오래 재확인 안 된 플래그 정리
    entry["open_flags"] = [
        f for f in flags.values()
        if (days_since(f.get("last_seen"), today_str) or 0) <= FLAG_EXPIRE_DAYS
    ]
    return entry


def _shift_key(finding: dict) -> str:
    """테마 흐름의 동일성 판정 키.

    같은 흐름을 매번 새 항목으로 쌓으면 count 가 안 올라가고
    'thesis 갱신 후보' 승격이 영영 일어나지 않는다. 그래서 표현이 조금 달라도
    같은 watch_shift 를 가리키면 한 항목으로 묶는다.
    """
    refs = ",".join(sorted(finding.get("refs") or []))
    base = (finding.get("shift") or finding.get("headline") or finding.get("summary") or "")
    base = re.sub(r"\s+", " ", base).strip().lower()[:80]
    return f"{refs}|{base}"


def update_theme_entry(
    entry: dict, result: dict, today_str: str, mark_checked: bool = True
) -> dict:
    """테마 검색 결과를 누적. 같은 흐름의 반복 관측 횟수를 센다.

    테마 레이어는 판정을 하지 않으므로 '몇 번째로 같은 방향을 봤는가' 가
    유일한 신호 강도다. THESIS_REVIEW_THRESHOLD 회 이상이면
    thesis 갱신 후보로 승격된다 (분기 리뷰 재료).
    """
    entry.setdefault("observations", {})
    entry.setdefault("shifts", {})
    if mark_checked:
        entry["last_checked"] = today_str

    merge_observations(entry, result.get("observations"), today_str)
    for finding in (result.get("findings") or []):
        merge_observations(entry, finding.get("quant"), today_str)

    shifts = entry["shifts"]
    for finding in (result.get("findings") or []):
        key = _shift_key(finding)
        if not key.strip("|"):
            continue
        prev = shifts.get(key)
        record = {
            "headline": finding.get("headline") or finding.get("shift") or "",
            "shift": finding.get("shift") or "",
            "refs": finding.get("refs") or [],
            "direction": finding.get("direction") or "불명",
            "affects": finding.get("affects") or [],
            "summary": finding.get("summary", ""),
            "sources": normalize_sources(finding),
            "last_seen": today_str,
        }
        if prev:
            # 방향이 뒤집히면 누적을 리셋한다. 순풍 2회 + 역풍 1회를
            # "3회 연속" 으로 세면 승격 판정이 거짓이 된다.
            flipped = (
                prev.get("direction") in ("순풍", "역풍")
                and record["direction"] in ("순풍", "역풍")
                and prev["direction"] != record["direction"]
            )
            record["first_seen"] = today_str if flipped else prev.get("first_seen", today_str)
            record["count"] = 1 if flipped else prev.get("count", 1) + 1
            if flipped:
                logger.info(f"테마 흐름 방향 전환 — 누적 리셋: {record['headline']}")
        else:
            record["first_seen"] = today_str
            record["count"] = 1
        record["thesis_review"] = record["count"] >= THESIS_REVIEW_THRESHOLD
        shifts[key] = record

    entry["shifts"] = {
        k: v for k, v in shifts.items()
        if (days_since(v.get("last_seen"), today_str) or 0) <= THEME_SHIFT_EXPIRE_DAYS
    }
    return entry

def build_thesis_appendix(
    positions_doc: dict,
    position_results: list[dict],
    news_sweep: Optional[dict],
    state: dict,
    today_str: str,
    theme_results: Optional[list[dict]] = None,
) -> str:
    """보유 근거(thesis) 대조표. positions.json 원문을 그대로 인용한다.

    모델에게 요약시키지 않는 이유: thesis 는 본인이 쓴 판단 근거라 왜곡되면 안 되고,
    매일 같은 내용이라 토큰을 쓸 이유도 없다. 오늘 나온 신호를 옆에 붙여
    "이 관점으로 들고 있다" 와 "오늘 뭐가 있었다" 가 한눈에 대조되게 한다.
    """
    monitored = [
        p for p in positions_doc.get("positions", [])
        if p.get("status") in MONITORED_STATUSES
    ]
    if not monitored:
        return ""

    by_id = {r["position"]["id"]: r for r in position_results}
    sweep_by_label = {}
    for it in ((news_sweep or {}).get("items") or []):
        sweep_by_label.setdefault(it.get("position_label", ""), []).append(it)

    # 테마 흐름을 포지션별로 뒤집어 붙인다 — 오늘 개별 검색하지 않은 포지션에도
    # 상위 변화가 닿았는지 이 표에서 바로 보이게 하는 것이 이 레이어의 목적이다.
    theme_by_position: dict[str, list[str]] = {}
    for item in (theme_results or []):
        theme = item["theme"]
        allowed = set(theme.get("affects", []))
        for f in ((item.get("result") or {}).get("findings") or []):
            hits = [pid for pid in (f.get("affects") or []) if pid in allowed] or list(allowed)
            head = f.get("headline") or f.get("shift") or ""
            for pid in hits:
                theme_by_position.setdefault(pid, []).append(
                    f"- 🔷 [{theme.get('label')}] {head} ({f.get('direction', '불명')}) "
                    f"— {f.get('summary', '')}"
                )

    out = ["", "---", "", "## 📌 보유 근거 대조표", "",
           "각 포지션을 어떤 관점으로 들고 있는지와 오늘 확인된 것을 나란히 둔다.", ""]

    for pos in monitored:
        name = display_name(pos)
        out.append(f"### {name}")
        out.append("")
        out.append("**보유 근거**")
        for i, t in enumerate(pos.get("thesis", []), 1):
            out.append(f"{i}. {t}")
        if not pos.get("thesis"):
            out.append("- (미작성)")
        out.append("")

        entry = state.get("positions", {}).get(pos["id"], {})
        item = by_id.get(pos["id"])
        out.append("**오늘**")
        if item is None:
            last = entry.get("last_checked") or "기록 없음"
            out.append(f"- 개별 점검 안 함 (마지막 점검 {last})")
        elif item.get("skipped"):
            out.append(f"- 점검 못 함: {item['skipped']}")
        else:
            findings = ((item.get("result") or {}).get("findings")) or []
            if findings:
                for f in findings:
                    refs = ", ".join(f.get("refs") or []) or "-"
                    out.append(f"- [{f.get('level', '?')}] ({refs}) {f.get('summary', '')}")
            else:
                out.append("- 걸린 신호 없음")
            if item.get("incomplete"):
                out.append(f"- ⚠️ 확인 미완료: {item['incomplete']}")

        for it in sweep_by_label.get(pos.get("label", ""), []):
            out.append(f"- 📰 {it.get('summary', '')} ({it.get('reported_at', '')})")

        out.extend(theme_by_position.get(pos["id"], []))

        flags = [f for f in entry.get("open_flags", []) if f.get("count", 1) >= 2]
        if flags:
            out.append("")
            out.append("**반복 관측 (누적)**")
            for f in flags:
                out.append(
                    f"- {f.get('signal')} — {f.get('count')}회째 "
                    f"(최초 {f.get('first_seen')}, 최근 {f.get('last_seen')})"
                )
        out.append("")

    return chr(10).join(out)


def build_theme_appendix(
    positions_doc: dict, theme_state: dict, today_str: str
) -> str:
    """테마 흐름 누적표. 판정이 아니라 '무엇이 계속 쌓이고 있는가' 의 기록.

    테마 레이어는 등급을 매기지 않으므로, 이 표가 유일한 신호 강도 표시다.
    thesis 갱신 후보를 맨 위로 올려 분기 리뷰 때 바로 집히게 한다.
    """
    entries = (theme_state or {}).get("themes") or {}
    if not entries:
        return ""

    by_id = {p["id"]: p for p in positions_doc.get("positions", [])}
    themes_by_id = {t["id"]: t for t in positions_doc.get("themes", [])}

    rows = []
    for tid, entry in entries.items():
        for rec in (entry.get("shifts") or {}).values():
            rows.append((tid, rec))
    if not rows:
        return ""

    # thesis 갱신 후보 우선 → 누적 횟수 → 최근 관측 순
    rows.sort(key=lambda r: (
        0 if r[1].get("thesis_review") else 1,
        -r[1].get("count", 1),
        r[1].get("last_seen", ""),
    ), reverse=False)

    out = ["", "---", "", "## 🔷 테마 흐름 누적", "",
           f"같은 방향의 변화가 {THESIS_REVIEW_THRESHOLD}회 이상 반복되면 thesis 갱신 후보로 표시된다. "
           "판정이 아니라 분기 리뷰 재료다.", "",
           "| 테마 | 흐름 | 방향 | 누적 | 최초 | 최근 | 닿는 포지션 |",
           "|---|---|---|---|---|---|---|"]
    for tid, rec in rows[:20]:
        label = themes_by_id.get(tid, {}).get("label", tid)
        names = ", ".join(
            display_name(by_id[pid]) for pid in (rec.get("affects") or []) if pid in by_id
        ) or "-"
        star = " ★" if rec.get("thesis_review") else ""
        head = (rec.get("headline") or rec.get("shift") or "-").replace("|", "／")
        out.append(
            f"| {label} | {head}{star} | {rec.get('direction', '불명')} | "
            f"{rec.get('count', 1)}회 | {rec.get('first_seen', '-')} | "
            f"{rec.get('last_seen', '-')} | {names} |"
        )
    out.append("")
    out.append("★ = thesis 갱신 후보")
    out.append("")
    return "\n".join(out)


def build_cost_footer(usage: dict, cost: float, now_str: str) -> str:
    """다이제스트 하단 토큰·비용 표기. 모델이 쓰게 하지 않고 코드가 붙인다."""
    cost_in = usage["input"] / 1_000_000 * PRICE_IN_PER_MTOK
    cost_out = usage["output"] / 1_000_000 * PRICE_OUT_PER_MTOK
    cost_search = usage["searches"] * PRICE_PER_SEARCH
    return (
        "\n\n---\n\n"
        f"🔢 토큰: {usage['input']:,} in / {usage['output']:,} out · 웹 검색 {usage['searches']}회\n\n"
        f"💰 비용: ${cost:.4f} "
        f"(입력 ${cost_in:.4f} / 출력 ${cost_out:.4f} / 검색 ${cost_search:.4f})\n\n"
        f"🤖 {MODEL} · {now_str}\n"
    )


def parse_claude_response(response_text: str) -> tuple[str, str]:
    """Claude 응답에서 텔레그램 요약 + 파일 분리.

    ★ 첫 마커 '앞' 은 버린다. 프롬프트로 금지해도 모델이 "다이제스트를
    작성했습니다..." 같은 서두를 붙일 때가 있는데, replace 로 마커만 지우면
    그 서두가 텔레그램 맨 위에 그대로 실린다 (실측 2026-08-15).
    """
    if "===TELEGRAM===" in response_text and "===FILE===" in response_text:
        after = response_text.split("===TELEGRAM===", 1)[1]
        telegram_part, file_part = after.split("===FILE===", 1)
        preamble = response_text.split("===TELEGRAM===", 1)[0].strip()
        if preamble:
            logger.warning(f"모델이 서두를 붙임 — 버림: {preamble[:80]}")
        return telegram_part.strip(), file_part.strip()
    else:
        # 마커 없으면 전체를 둘 다 사용
        logger.warning("===TELEGRAM===/===FILE=== 마커 없음 — 응답 전문을 그대로 사용")
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


async def send_telegram(
    telegram_summary: str, file_path: Path, cost: float, usage: Optional[dict] = None
):
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
    if usage:
        footer += f"\n🔢 {usage['input']:,} in / {usage['output']:,} out · 검색 {usage['searches']}회"
    footer += f"\n💰 비용: ${cost:.4f}"

    full_message = telegram_summary + footer

    if len(full_message) > 4000:
        # 뒤에서 자르면 맨 끝에 붙은 📎 출처 블록이 통째로 날아간다.
        # 각주 마커만 있고 출처가 없는 메시지가 되므로 본문을 먼저 줄인다.
        marker = "\n📎 출처"
        notice = "\n\n... (본문 잘림 — 전체는 첨부 파일)"
        head, sep, sources = telegram_summary.partition(marker)
        if sep:
            budget = 4000 - len(sep + sources) - len(footer) - len(notice)
            if budget > 500:
                full_message = head[:budget] + notice + sep + sources + footer
            else:
                # 출처 블록만으로도 넘치는 비정상 상황 — 기존 방식으로 후퇴
                full_message = full_message[:3950] + "\n\n... (요약 잘림)"
        else:
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
    """상태 파일만 커밋. digest 본문은 gitignore 대상이라 제외.

    누적 상태를 EC2 로컬에만 두면 서버 유실 시 분기 판정 근거와
    테마 흐름 누적이 통째로 날아간다.
    실패해도 다이제스트 자체는 이미 전송됐으므로 예외를 삼킨다.
    """
    targets = [p for p in (POSITION_STATE_PATH, THEME_STATE_PATH) if p.exists()]
    if not targets:
        return
    try:
        subprocess.run(["git", "add", *[str(p) for p in targets]],
                       cwd=PROJECT_ROOT, check=True, capture_output=True, timeout=30)
        staged = subprocess.run(["git", "diff", "--cached", "--quiet"],
                                cwd=PROJECT_ROOT, capture_output=True, timeout=30)
        if staged.returncode == 0:
            logger.info("상태 변경 없음 — 커밋 생략")
            return
        subprocess.run(
            ["git", "commit", "-m", f"Update monitoring state {datetime.now(KST):%Y-%m-%d}"],
            cwd=PROJECT_ROOT, check=True, capture_output=True, timeout=30)
        subprocess.run(["git", "push", "origin", "main"],
                       cwd=PROJECT_ROOT, check=True, capture_output=True, timeout=120)
        logger.info("position_state.json 커밋·푸시 완료")
    except subprocess.CalledProcessError as e:
        logger.error(f"상태 커밋 실패: {e.stderr.decode(errors='replace')[:300]}")
    except Exception as e:
        logger.error(f"상태 커밋 실패: {e}")

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

    # 1. 포지션 · 상태 · 캘린더 로딩 (가격 수집 대상이 여기서 나옴)
    calendar = load_text_file(CALENDAR_PATH)
    positions_doc = load_positions()
    state = load_position_state()
    theme_state = load_theme_state()

    positions = positions_doc.get("positions", [])
    themes = positions_doc.get("themes", [])
    upcoming = extract_upcoming_events(calendar, now)
    us_tickers, kr_tickers, ticker_names = collect_position_tickers(positions_doc)

    logger.info(
        f"포지션 {len(positions)}개 / 테마 {len(themes)}개 로드 / "
        f"향후 {EVENT_WINDOW_DAYS}일 이벤트 {len(upcoming)}건 파싱"
    )

    # 2. 시장 데이터 (포지션 종목만)
    logger.info(f"가격 수집: 미국 {len(us_tickers)} / 한국 {len(kr_tickers)}종목")
    us_prices = fetch_us_prices(us_tickers)
    kr_prices = fetch_kr_prices(kr_tickers, ticker_names)
    all_prices = us_prices + kr_prices
    logger.info(f"가격 수집 완료: {len(all_prices)}종목")

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

    # 3-2. 전 종목 소식 스윕 (개별 검색은 하루 3개뿐이라 나머지는 이걸로 커버)
    monitored = [p for p in positions if p.get("status") in MONITORED_STATUSES]
    logger.info(f"전 종목 소식 스윕 중... ({len(monitored)}종목)")
    news_sweep, u = search_news_sweep(monitored, now_str)
    merge_usage(usage_total, u)
    if news_sweep:
        logger.info(f"소식 스윕 완료: {len((news_sweep.get('items') or []))}건")
    else:
        logger.warning("소식 스윕 실패 — 📰 섹션 없이 진행")

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

        incomplete = is_search_incomplete(result, u["searches"], POSITION_MAX_USES)
        if result:
            findings = result.get("findings") or []
            # 부분 확인도 점검으로 친다. 모델은 사소한 미확인 항목까지 정직하게 보고하는데,
            # 그때마다 last_checked 를 막으면 같은 포지션만 매일 재선별되고
            # rotation 이 영영 안 돌아 나머지 포지션이 방치된다.
            state["positions"][pos["id"]] = update_state_entry(
                entry, result, today_str,
                mark_checked=(incomplete is None) or bool(findings),
            )
            reds = sum(1 for f in findings if f.get("level") == "RED")
            if incomplete:
                logger.warning(
                    f"{pos['id']} 확인 미완료 ({incomplete}) — findings {len(findings)}건. "
                    f"last_checked 미갱신, 내일 재점검 대상"
                )
            else:
                logger.info(f"{pos['id']} 완료: findings {len(findings)}건 (RED {reds})")
        else:
            logger.warning(f"{pos['id']} 결과 없음 ({incomplete}) — 확인 미완료로 처리")

        position_results.append({**cand, "result": result, "incomplete": incomplete})

    # 5-2. 테마 검색 (Layer 0.5)
    # 포지션 뒤에 두는 이유: 검색 예산이 빠듯한 날에는 포지션 점검이 우선이다.
    # 포지션 미점검은 '이상 없음' 으로 오인될 위험이 있지만, 테마 미점검은
    # 누적 기록이 남아 있어 다음 순번에서 이어서 볼 수 있다.
    positions_by_id = {p["id"]: p for p in positions}
    selected_themes, unchecked_themes = select_themes(themes, theme_state, upcoming, today_str)
    theme_results = []
    for cand in selected_themes:
        theme = cand["theme"]
        logger.info(f"선별(테마): {theme['id']} — {'; '.join(cand['reasons'])}")

        if usage_total["searches"] >= DAILY_SEARCH_BUDGET:
            logger.warning(
                f"일일 검색 예산 {DAILY_SEARCH_BUDGET}회 소진 — 테마 {theme['id']} 생략"
            )
            theme_results.append({**cand, "result": None, "skipped": "일일 검색 예산 소진"})
            continue

        entry = theme_state["themes"].setdefault(
            theme["id"], {"last_checked": None, "observations": {}, "shifts": {}}
        )
        result, u = search_theme(theme, positions_by_id, entry, now_str)
        merge_usage(usage_total, u)

        incomplete = is_search_incomplete(result, u["searches"], THEME_MAX_USES)
        if result:
            findings = result.get("findings") or []
            theme_state["themes"][theme["id"]] = update_theme_entry(
                entry, result, today_str,
                mark_checked=(incomplete is None) or bool(findings),
            )
            promoted = sum(
                1 for rec in theme_state["themes"][theme["id"]].get("shifts", {}).values()
                if rec.get("thesis_review") and rec.get("last_seen") == today_str
            )
            logger.info(
                f"테마 {theme['id']} 완료: findings {len(findings)}건 "
                f"(thesis 갱신 후보 {promoted})"
            )
        else:
            logger.warning(f"테마 {theme['id']} 결과 없음 ({incomplete})")

        theme_results.append({**cand, "result": result, "incomplete": incomplete})

    if unchecked_themes:
        logger.info(f"오늘 미점검 테마: {', '.join(t['id'] for t in unchecked_themes)}")

    # 6. 상태 저장 (종합 호출 실패해도 검색 결과는 남도록 먼저 저장)
    if dry_run:
        DRY_RUN_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        save_position_state(state, today_str, DRY_RUN_OUTPUT_DIR / f"{stamp}_position_state.json")
        save_theme_state(theme_state, today_str, DRY_RUN_OUTPUT_DIR / f"{stamp}_theme_state.json")
        logger.info("dry-run: 실제 상태 파일은 건드리지 않음")
    else:
        save_position_state(state, today_str)
        save_theme_state(theme_state, today_str)

    # 7. 종합 호출 (검색 없음)
    logger.info("종합 다이제스트 생성 중...")
    registry = SourceRegistry()
    prompt = build_prompt(
        us_prices=us_prices,
        kr_prices=kr_prices,
        now_str=now_str,
        positions_doc=positions_doc,
        layer0_result=layer0_result,
        news_sweep=news_sweep,
        position_results=position_results,
        unchecked=unchecked,
        upcoming=upcoming,
        state=state,
        theme_results=theme_results,
        theme_state=theme_state,
        registry=registry,
    )
    logger.info(f"각주 출처 {len(registry)}건 등록")

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
    file_md += build_thesis_appendix(
        positions_doc, position_results, news_sweep, state, today_str,
        theme_results=theme_results,
    )
    file_md += build_theme_appendix(positions_doc, theme_state, today_str)
    # 📎 출처는 모델이 아니라 코드가 붙인다 — 번호와 목록이 어긋나지 않게 하기 위함.
    # 본문에서는 각주 마커만 읽고, 필요할 때만 맨 아래를 본다.
    # 인용되지 않은 출처는 목록에서 뺀다 (본문에 없는 번호가 남지 않게).
    for label, text in (("파일", file_md), ("텔레그램", telegram_summary)):
        bogus = registry.unknown_markers(text)
        if bogus:
            logger.warning(f"{label}: 등록되지 않은 각주 마커 인용 — {', '.join(bogus)}")
    file_md += registry.render_file(file_md)
    file_md += build_cost_footer(usage_total, cost, now_str)
    telegram_summary += registry.render_telegram(telegram_summary)

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
            "news_sweep": news_sweep,
            "sources": registry.items(),
            "themes": {
                "selected": [
                    {
                        "id": r["theme"]["id"],
                        "reasons": r.get("reasons", []),
                        "skipped": r.get("skipped"),
                        "incomplete": r.get("incomplete"),
                        "result": r.get("result"),
                    }
                    for r in theme_results
                ],
                "unchecked": [t["id"] for t in unchecked_themes],
            },
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
    await send_telegram(telegram_summary, output_path, cost, usage_total)
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

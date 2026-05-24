"""
Daily Digest Generator
======================
매일 새벽 06:30 KST 자동 실행 (cron).

작동 순서:
1. 워치리스트·캘린더·dashboard 로드
2. yfinance·pykrx 로 시장 데이터 수집
3. Claude Sonnet 4.5 로 일간 다이제스트 생성
4. 파일 저장 (digests/sent/YYYY-MM-DD.md)
5. 텔레그램 푸시 (요약 + 파일 첨부 + GitHub URL)
"""

import os
import json
import logging
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

import pytz
import requests
import yfinance as yf
from dotenv import load_dotenv
from anthropic import Anthropic
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
DIGEST_OUTPUT_DIR = PROJECT_ROOT / "digests" / "sent"

KST = pytz.timezone("Asia/Seoul")

# 모델 (비용 통제 위해 Sonnet)
MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 3000

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
    "GEV", "ETN", "VRT", "PWR",                    # AI DC 전력
    "LLY", "NVO", "HIMS", "VKTX",                  # GLP-1 (BANB.SW 제외 — yfinance 안 됨)
    "CCJ", "CEG", "VST", "LEU", "BWXT", "SMR", "OKLO",  # 원자력
    "MSFT", "META", "GOOGL", "AMZN", "CRM", "NOW", "ADBE",  # AI App Foundation/Horizontal
    "PLTR", "TEM", "VEEV", "TRI", "INTU",          # AI App Vertical
]

KR_TICKERS = [
    "298040", "267260", "010120", "062040",  # AI DC 전력
    "128940", "207940", "196170",            # GLP-1
    "034020", "052690",                       # 원자력
    "328130",                                 # AI App Vertical
]

KR_NAMES = {
    "298040": "효성중공업", "267260": "HD현대일렉트릭", "010120": "LS일렉트릭",
    "062040": "산일전기", "128940": "한미약품", "207940": "삼성바이오로직스",
    "196170": "알테오젠", "034020": "두산에너빌리티", "052690": "한전기술",
    "328130": "루닛",
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
) -> str:
    """Claude 에 보낼 프롬프트."""

    # 가격 변동 큰 종목만 추출 (±3% 이상)
    sig_us = [p for p in us_prices if abs(p["change_pct"]) >= 3]
    sig_kr = [p for p in kr_prices if abs(p["change_pct"]) >= 3]

    us_lines = [
        f"- {p['ticker']}: ${p['price']} ({'+' if p['change_pct'] >= 0 else ''}{p['change_pct']}%) "
        f"vol×{p['volume_ratio']}"
        for p in sig_us
    ]
    kr_lines = [
        f"- {p['ticker']} ({p['name']}): {p['price']:,}원 "
        f"({'+' if p['change_pct'] >= 0 else ''}{p['change_pct']}%) vol×{p['volume_ratio']}"
        for p in sig_kr
    ]

    all_us_summary = (
        f"전체 미국 {len(us_prices)}종목 중 ±3% 이상 {len(sig_us)}종목:\n"
        + ("\n".join(us_lines) if us_lines else "(변동 큰 종목 없음)")
    )
    all_kr_summary = (
        f"전체 한국 {len(kr_prices)}종목 중 ±3% 이상 {len(sig_kr)}종목:\n"
        + ("\n".join(kr_lines) if kr_lines else "(변동 큰 종목 없음)")
    )

    # Track 4 종목 정보
    tracked_lines = []
    for t in tracked:
        ticker = t["ticker"]
        # 가격 정보 찾기
        price_info = next((p for p in us_prices + kr_prices if p["ticker"] == ticker), None)
        if price_info:
            change = price_info["change_pct"]
            change_str = f"{'+' if change >= 0 else ''}{change}%"
        else:
            change_str = "데이터 없음"
        tracked_lines.append(
            f"- {ticker} ({t.get('name', '')}, {t.get('area', '')}): {change_str}\n"
            f"  매수 deadline: {t.get('buy_deadline', '미정')}\n"
            f"  메모: {t.get('note', '')}"
        )
    tracked_section = "\n".join(tracked_lines) if tracked_lines else "(Track 4 등재 종목 없음)"

    prompt = f"""당신은 본인의 산업 분석·투자 시스템의 분석가. 오늘의 일간 다이제스트 작성.

# 현재 시점
{now_str}

# 작업
다음 데이터를 종합하여 일간 다이제스트 markdown 작성. 본인은 한국 VC 심사역으로 직설적·존대말 선호.

# 가격 변동 데이터 (어제 시장 기준)

## 미국 시장
{all_us_summary}

## 한국 시장
{all_kr_summary}

# Track 4 등재 종목 (본인 매수 검토 중)
{tracked_section}

# 시스템 파일 (참고)

## Mega Change Map dashboard (참고)
{dashboard[:3000]}

## 이벤트 캘린더 (향후 1주만 추출해 사용)
{calendar[:5000]}

## 다이제스트 템플릿 (이 형식 그대로 따름)
{template[:3000]}

# 출력 요구사항

다음 두 가지를 **반드시** 모두 작성:

1. **텔레그램 요약** (먼저 출력) — plain text, 표·복잡한 markdown 없이, 1500자 이내. 모바일에서 보기 좋게.
2. **전체 파일** (다음 출력) — markdown 표·헤더 등 풍부하게. 본인이 GitHub·VS Code 에서 봄.

## 출력 형식 (★ 정확히 이대로)

===TELEGRAM===
(여기에 텔레그램용 짧은 요약. plain text. 표 X. 줄바꿈 명확히. 1500자 이내.

형식:
📊 일간 다이제스트 — YYYY-MM-DD

🚨 P1 이벤트
- (없으면 "없음")

📈 큰 변동 (Top 5, ±3% 이상)
- 종목명: 가격 변동% (간단 사유)
- ...

🎯 영역 변화
- Tier 1: (한 줄)
- Tier 2: (한 줄)

📅 향후 7일 P1·P2
- MM-DD 이벤트명

💡 검토 제안
- (1개만)
)

===FILE===
(여기에 전체 markdown 파일. 헤더 ##, 표, 풍부한 정보. 텔레그램용 요약과 *별개*로 작성.)

## 본인 톤
직설·존대말·짧음. AI 특유의 모호함·"~할 수 있습니다" X. "~다" 또는 "~함" 위주.

## 노이즈 제거
- 변동 ±3% 미만 종목 생략
- P1 이벤트 없으면 "없음"
- 검토 제안 1개만 (가장 중요한 것)

## 캘린더 추출
오늘부터 향후 7일 (~2026-05-31) 안의 P1·P2만.

## 출력 형식
markdown 형식. 헤더는 ## 사용. 앞뒤 설명·코드블록 마커 없이 다이제스트만 출력.
"""
    return prompt


def call_claude(prompt: str) -> tuple[str, float, int, int]:
    """Claude 호출. 결과·비용·input/output tokens 리턴."""
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text
    usage = response.usage
    cost = (
        usage.input_tokens / 1_000_000 * 3.0
        + usage.output_tokens / 1_000_000 * 15.0
    )
    return text, cost, usage.input_tokens, usage.output_tokens

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

async def main():
    now = datetime.now(KST)
    now_str = now.strftime("%Y-%m-%d %H:%M KST")
    today_str = now.strftime("%Y-%m-%d")

    logger.info(f"=== Daily Digest {today_str} 시작 ===")

    # 1. 시장 데이터
    logger.info("미국 종목 수집...")
    us_prices = fetch_us_prices()
    logger.info(f"미국 {len(us_prices)}종목 수집 완료")

    logger.info("한국 종목 수집...")
    kr_prices = fetch_kr_prices()
    logger.info(f"한국 {len(kr_prices)}종목 수집 완료")

    # 2. 시스템 파일 로딩
    dashboard = load_text_file(DASHBOARD_PATH)
    calendar = load_text_file(CALENDAR_PATH)
    template = load_text_file(TEMPLATE_PATH)
    tracked = load_tracked_stocks()

    logger.info(f"Track 4 등재 종목: {len(tracked)}개")

    # 3. Claude 호출
    logger.info("Claude Sonnet 호출 중...")
    prompt = build_prompt(
        us_prices=us_prices,
        kr_prices=kr_prices,
        tracked=tracked,
        dashboard=dashboard,
        calendar=calendar,
        template=template,
        now_str=now_str,
    )

    response_text, cost, in_tok, out_tok = call_claude(prompt)
    logger.info(f"Claude 응답 완료. Tokens: {in_tok:,} in / {out_tok:,} out. 비용 ${cost:.4f}")

    # 텔레그램용 요약 + 파일용 markdown 분리
    telegram_summary, file_md = parse_claude_response(response_text)

    # 4. 파일 저장 (markdown 전체)
    DIGEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DIGEST_OUTPUT_DIR / f"{today_str}.md"
    output_path.write_text(file_md, encoding="utf-8")
    logger.info(f"파일 저장: {output_path}")

    # 5. 텔레그램 전송 (요약 + 파일 첨부)
    logger.info("텔레그램 전송 중...")
    await send_telegram(telegram_summary, output_path, cost)
    logger.info("텔레그램 전송 완료")
    # 6. Git commit
    git_commit_and_push(output_path)

    logger.info(f"=== Daily Digest {today_str} 완료 ===")


if __name__ == "__main__":
    asyncio.run(main())

"""Claude 호출 최소 래퍼 (봇용).

daily_digest.py 에도 같은 기능이 있지만 그쪽을 import 하면 yfinance·pykrx·
anthropic 이 전부 딸려온다. 24/7 폴링하는 봇에 얹을 이유가 없어 따로 둔다.
검색은 쓰지 않는다 — 봇 대화는 사실 수집이 아니라 초안 작성용이다.
"""

import json
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5")
CLAUDE_CLI_BIN = os.getenv("CLAUDE_CLI_BIN", "claude")
CLI_TIMEOUT = 300


def _env_value(key: str) -> Optional[str]:
    """.env 에서 값 하나 읽기. 봇은 systemd 로 뜨므로 환경변수가 없을 수 있다."""
    v = os.getenv(key)
    if v:
        return v.strip().strip("'\"")
    if not ENV_PATH.exists():
        return None
    try:
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            if line.startswith(f"{key}="):
                return line.split("=", 1)[1].strip().strip("'\"")
    except Exception as e:
        logger.warning(f".env 읽기 실패: {e}")
    return None


def call_claude(prompt: str) -> tuple[str, float]:
    """Claude CLI 호출. (응답 텍스트, 비용 USD) 리턴.

    ★ 블로킹 호출이다. 봇에서는 반드시 asyncio.to_thread 로 감싸 쓸 것 —
    그냥 부르면 응답이 올 때까지 봇 전체가 멈춘다.
    """
    # 구독으로만 인증한다. ANTHROPIC_API_KEY 가 환경에 남아 있으면 CLI 가
    # 그쪽을 집어 종량과금이 될 수 있으므로 빼고 넘긴다.
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    token = _env_value("CLAUDE_CODE_OAUTH_TOKEN")
    if token:
        env["CLAUDE_CODE_OAUTH_TOKEN"] = token

    proc = subprocess.run(
        [CLAUDE_CLI_BIN, "-p", prompt, "--model", MODEL, "--output-format", "json"],
        cwd=PROJECT_ROOT, capture_output=True, timeout=CLI_TIMEOUT, env=env,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"claude CLI 실패 (exit {proc.returncode}): "
            f"{proc.stderr.decode(errors='replace')[:300]}"
        )

    payload = json.loads(proc.stdout.decode(errors="replace"))
    if payload.get("is_error"):
        raise RuntimeError(f"claude CLI 오류: {str(payload.get('result'))[:300]}")
    return str(payload.get("result") or ""), float(payload.get("total_cost_usd") or 0.0)


def extract_json(text: str) -> Optional[dict]:
    """응답에서 JSON 객체 추출 (코드블록·앞뒤 설명 허용)."""
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

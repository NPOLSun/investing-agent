"""포지션 조회 — 텔레그램 표시용 순수 함수 모음.

daily_digest.py 를 import 하지 않는다. 그쪽은 모듈 로드 시점에 yfinance·pykrx·
anthropic 을 끌어오고 TELEGRAM_CHAT_ID 를 강제로 int 변환하는데, 봇이 그걸
전부 짊어질 이유가 없다. display_name·days_since 정도의 중복은 감수한다.
(공통 모듈로 합치는 정리는 다이제스트 쪽이 안정된 뒤에)
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
POSITIONS_PATH = PROJECT_ROOT / "data" / "positions.json"
POSITION_STATE_PATH = PROJECT_ROOT / "data" / "position_state.json"
THEME_STATE_PATH = PROJECT_ROOT / "data" / "theme_state.json"
AREA_ALIASES_PATH = PROJECT_ROOT / "data" / "area_aliases.json"
MARKET_PATH = PROJECT_ROOT / "data" / "market.json"

MONITORED_STATUSES = ("holding", "watching")
STATUS_LABEL = {
    "holding": "보유",
    "watching": "관심",
    "exited": "매도완료",
    "paused": "중단",
}
TELEGRAM_LIMIT = 4096


def _load(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def load_market() -> dict:
    """다이제스트가 남긴 시세 스냅샷. 없으면 빈 dict."""
    return _load(MARKET_PATH, {"prices": {}}).get("prices", {})


def load_all() -> tuple[dict, dict, dict, dict]:
    """(positions_doc, position_state, theme_state, area_aliases)"""
    return (
        _load(POSITIONS_PATH, {}),
        _load(POSITION_STATE_PATH, {"positions": {}}),
        _load(THEME_STATE_PATH, {"themes": {}}),
        _load(AREA_ALIASES_PATH, {"aliases": {}}),
    )


def label_base(label: str) -> str:
    return re.sub(r"\s*\([^()]*\)\s*$", "", label or "").strip() or label


def display_name(pos: dict) -> str:
    """출력용 표시명. 회사명이 앞, 포지션명이 뒤.

    그룹으로 쪼갠 뒤로는 label 이 형제 종목과 겹치므로(둘 다 "미국 변압기")
    회사명이 없으면 구분이 안 된다.
    """
    tickers = pos.get("tickers", [])
    companies = pos.get("companies") or {}
    base = label_base(pos.get("label", ""))
    if companies:
        return " · ".join(f"{companies.get(t, t)} ({base} {t})" for t in tickers)
    if not tickers:
        return pos.get("label", "")
    joined = ", ".join(tickers)
    label = pos.get("label", "")
    return f"{label[:-1]} {joined})" if label.endswith(")") else f"{label} ({joined})"


def days_since(date_str: Optional[str], today: str) -> Optional[int]:
    if not date_str:
        return None
    try:
        d0 = datetime.strptime(date_str, "%Y-%m-%d")
        d1 = datetime.strptime(today, "%Y-%m-%d")
        return (d1 - d0).days
    except Exception:
        return None


def _checked_phrase(entry: dict, today: str) -> str:
    last = entry.get("last_checked")
    if not last:
        return "점검 기록 없음"
    n = days_since(last, today)
    if n is None:
        return f"점검 {last}"
    if n == 0:
        return f"점검 {last} (오늘)"
    return f"점검 {last} ({n}일 전)"


def _flag_counts(entry: dict) -> str:
    flags = entry.get("open_flags", []) or []
    red = sum(1 for f in flags if f.get("level") == "RED")
    yellow = sum(1 for f in flags if f.get("level") == "YELLOW")
    bits = []
    if red:
        bits.append(f"🔴{red}")
    if yellow:
        bits.append(f"🟡{yellow}")
    return " · ".join(bits)


def monitored(doc: dict) -> list[dict]:
    return [p for p in doc.get("positions", []) if p.get("status") in MONITORED_STATUSES]


def themes_for(doc: dict, position_id: str) -> list[dict]:
    return [t for t in doc.get("themes", []) if position_id in (t.get("affects") or [])]


def format_list(doc: dict, state: dict, today: str) -> str:
    """/포지션 — 목록."""
    positions = doc.get("positions", [])
    if not positions:
        return "positions.json 을 읽지 못했거나 등록된 포지션이 없습니다."

    holding = [p for p in positions if p.get("status") == "holding"]
    watching = [p for p in positions if p.get("status") == "watching"]
    others = [p for p in positions if p.get("status") not in MONITORED_STATUSES]

    out = [f"📋 포지션 — 보유 {len(holding)} · 관심 {len(watching)}", ""]
    for i, pos in enumerate(monitored(doc), 1):
        entry = (state.get("positions") or {}).get(pos["id"], {})
        line = f"{i}. {display_name(pos)}"
        if pos.get("status") == "watching":
            line += "  [관심]"
        out.append(line)
        sub = _checked_phrase(entry, today)
        flags = _flag_counts(entry)
        if flags:
            sub += f" · {flags}"
        if not themes_for(doc, pos["id"]):
            sub += " · ⚠ 테마 미연결"
        out.append(f"   {sub}")
        out.append("")

    if others:
        out.append("— 모니터링 제외 —")
        for pos in others:
            out.append(f"· {display_name(pos)} [{STATUS_LABEL.get(pos.get('status'), pos.get('status'))}]")
        out.append("")

    out.append("상세: /포지션 1  또는  /포지션 파두")
    return "\n".join(out)


def find_position(doc: dict, query: str) -> tuple[Optional[dict], list[dict]]:
    """번호 또는 이름 조각으로 포지션 찾기. (단일 결과, 후보들)"""
    mon = monitored(doc)
    q = (query or "").strip()
    if not q:
        return None, []

    # 목록 번호로 해석. 단 한국 티커가 6자리 숫자라 그대로 두면 충돌한다
    # (/포지션 440110 이 "440110번 포지션" 으로 읽혀 아무것도 못 찾음).
    # 두 자리 이하일 때만 번호로 보고, 나머지는 티커 조회로 넘긴다.
    if q.isdigit() and len(q) <= 2:
        idx = int(q)
        if 1 <= idx <= len(mon):
            return mon[idx - 1], []
        return None, []

    ql = q.lower()
    hits = [
        p for p in doc.get("positions", [])
        if ql in p.get("label", "").lower()
        or ql in p.get("id", "").lower()
        or any(ql == t.lower() for t in p.get("tickers", []))
    ]
    if len(hits) == 1:
        return hits[0], []
    return None, hits


def format_detail(doc: dict, state: dict, area_aliases: dict, pos: dict, today: str) -> str:
    """/포지션 <n> — 상세. thesis·조건 원문을 그대로 보여준다 (요약하지 않는다)."""
    entry = (state.get("positions") or {}).get(pos["id"], {})
    aliases = area_aliases.get("aliases", {})

    out = [display_name(pos), ""]
    out.append(f"상태: {STATUS_LABEL.get(pos.get('status'), pos.get('status'))} · "
               f"{_checked_phrase(entry, today)}")

    areas = [aliases.get(a, {}).get("title", a) for a in (pos.get("areas") or [])]
    out.append(f"영역: {', '.join(areas) if areas else '미지정 ⚠'}")

    th = themes_for(doc, pos["id"])
    out.append(f"테마: {', '.join(t.get('label', t['id']) for t in th) if th else '미연결 ⚠'}")

    def block(title, items, empty="(없음)"):
        out.append("")
        out.append(title)
        if not items:
            out.append(f"  {empty}")
            return
        for i, it in enumerate(items, 1):
            out.append(f"  {i}. {it}")

    group = next((g for g in doc.get("groups", []) if g.get("id") == pos.get("group")), None)
    if group:
        out.append("")
        out.append(f"[그룹] {group.get('label')} — 아래 G 조건은 형제 종목과 공유")
        block("  공통 보유 근거", group.get("thesis"))
        block("  공통 매도 조건", group.get("kill_signals"))

    block("보유 근거", pos.get("thesis"), "(미작성 ⚠ — 이게 없으면 왜 들고 있는지 기록이 없습니다)")
    block("매도 검토 조건", pos.get("kill_signals"),
          "(미작성 ⚠ — 이게 없으면 이 포지션은 영원히 🔴 가 뜨지 않습니다)")
    block("추가 검토 조건", pos.get("add_signals"))

    watch = pos.get("watch", {}) or {}
    out.append("")
    out.append("감시")
    out.append(f"  경쟁사: {', '.join(watch.get('peers', [])) or '(없음)'}")
    inds = watch.get("indicators") or []
    names = [i.get("name", i.get("key", "")) if isinstance(i, dict) else str(i) for i in inds]
    out.append(f"  지표: {', '.join(n for n in names if n) or '(없음)'}")

    if pos.get("ignore"):
        out.append("")
        out.append("무시 (보고 안 함)")
        for it in pos["ignore"]:
            out.append(f"  · {it}")

    flags = [f for f in (entry.get("open_flags") or []) if f.get("count", 1) >= 2]
    if flags:
        out.append("")
        out.append("반복 관측 (누적)")
        for f in flags:
            out.append(f"  · [{f.get('level')}] {f.get('signal')} — "
                       f"{f.get('count')}회 (최초 {f.get('first_seen')})")

    obs = entry.get("observations") or {}
    if obs:
        out.append("")
        out.append("최근 관측값")
        for k, series in list(obs.items())[:8]:
            if series:
                out.append(f"  · {k} = {series[-1].get('value')} ({series[-1].get('date')})")

    if pos.get("note"):
        out.append("")
        out.append("메모")
        out.append(f"  {pos['note']}")

    return "\n".join(out)


def split_message(text: str, limit: int = TELEGRAM_LIMIT) -> list[str]:
    """텔레그램 길이 제한에 맞춰 자른다. 줄 중간에서 끊지 않는다.

    포지션 상세는 thesis 7개 + kill 9개짜리도 있어(발전 종합) 한 통에 안 들어간다.
    잘라 보내되 문장이 갈라지지는 않게 한다.
    """
    if len(text) <= limit:
        return [text]
    chunks, cur = [], ""
    for line in text.split("\n"):
        piece = (line[:limit - 1] if len(line) >= limit else line)
        if len(cur) + len(piece) + 1 > limit:
            if cur:
                chunks.append(cur)
            cur = piece
        else:
            cur = f"{cur}\n{piece}" if cur else piece
    if cur:
        chunks.append(cur)
    return chunks

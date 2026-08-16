"""포지션별 이벤트 로그 — 매일 찾은 finding 을 종목 파일에 누적한다.

지금까지 파이프라인은 매일 finding 을 수십 건 만들어 다이제스트에 한 번 렌더하고
버렸다. 남는 건 open_flags 카운터와 observations 숫자뿐이라 "지난 3개월간
이 종목에 무슨 일이 있었나" 에 답할 수 없었다. 그 원문을 여기 쌓는다.

유입 경로 네 가지를 모두 받는다:
  position — 개별 점검 (하루 3종목, 깊음)
  sweep    — 전 종목 소식 스윕 (매일, 얕음)
  theme    — 테마 흐름 팬아웃 (오늘 점검 안 한 종목에도 꽂힘)
  layer0   — 포트폴리오 상위 변수 (_portfolio 로 따로 보관)

같은 사실이 며칠 연속 잡히면 새 항목을 만들지 않고 last_seen 과 count 만 올린다.
안 그러면 타임라인이 같은 뉴스로 도배된다.
"""

import json
import logging
import re
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVENTS_DIRNAME = Path("data") / "events"
PORTFOLIO_ID = "_portfolio"

# 종목당 보관 상한. 하루 최대 몇 건씩 들어오므로 300 이면 1년 이상 버틴다.
MAX_EVENTS = 300
_SLUG_OK = re.compile(r"^[A-Za-z0-9._-]+$")


def events_dir(base: Optional[Path] = None) -> Path:
    return (base or PROJECT_ROOT) / EVENTS_DIRNAME


def _path(position_id: str, base: Optional[Path] = None) -> Optional[Path]:
    # id 는 positions.json 에서 오지만 파일명으로 쓰므로 경로 조작을 막는다
    if not position_id or not _SLUG_OK.match(position_id):
        logger.warning(f"이벤트 로그: 부적절한 id 무시 — {position_id!r}")
        return None
    return events_dir(base) / f"{position_id}.jsonl"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def event_key(ev: dict) -> str:
    """같은 사실인지 판정하는 키.

    표현이 조금 달라져도 같은 신호를 가리키면 한 항목으로 묶는다.
    signal/shift 원문이 있으면 그걸 우선 쓰고, 없으면 요약 앞부분으로 대체한다.
    """
    anchor = ev.get("signal") or ev.get("shift") or ev.get("headline") or ev.get("summary") or ""
    refs = ",".join(sorted(ev.get("refs") or []))
    return f"{ev.get('layer')}|{refs}|{_norm(anchor)[:90]}"


def load_events(position_id: str, base: Optional[Path] = None) -> list[dict]:
    p = _path(position_id, base)
    if not p or not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue  # 한 줄 깨져도 나머지는 살린다
    return out


def _merge(old: dict, new: dict, today: str) -> dict:
    """같은 키의 기존 항목에 새 관측을 합친다. 원문은 최신으로 갱신."""
    merged = dict(old)
    merged.update({k: v for k, v in new.items() if v not in (None, "", [], {})})
    merged["first_seen"] = old.get("first_seen") or old.get("date") or today
    merged["last_seen"] = today
    merged["count"] = old.get("count", 1) + (0 if old.get("last_seen") == today else 1)
    # 출처는 합집합 (URL 기준)
    seen, srcs = set(), []
    for s in (old.get("sources") or []) + (new.get("sources") or []):
        k = (s.get("url") or s.get("outlet") or "").strip().rstrip("/").lower()
        if k and k not in seen:
            seen.add(k)
            srcs.append(s)
    merged["sources"] = srcs[:6]
    return merged


def append_events(
    position_id: str, new_events: list[dict], today: str, base: Optional[Path] = None
) -> int:
    """한 종목의 이벤트를 병합 저장. 새로 추가된 건수 리턴."""
    p = _path(position_id, base)
    if not p or not new_events:
        return 0

    existing = load_events(position_id, base)
    index = {event_key(e): i for i, e in enumerate(existing)}
    added = 0

    for ev in new_events:
        ev = dict(ev)
        ev.setdefault("date", today)
        ev["last_seen"] = today
        k = event_key(ev)
        if k in index:
            i = index[k]
            existing[i] = _merge(existing[i], ev, today)
        else:
            ev["first_seen"] = today
            ev["count"] = 1
            existing.append(ev)
            index[k] = len(existing) - 1
            added += 1

    # 최근 관측이 위로. 같은 날이면 원래 순서 유지 (안정 정렬)
    existing.sort(key=lambda e: e.get("last_seen") or e.get("date") or "", reverse=True)
    existing = existing[:MAX_EVENTS]

    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        "\n".join(json.dumps(e, ensure_ascii=False) for e in existing) + "\n",
        encoding="utf-8",
    )
    return added


# ============================================================
# 하루치 실행 결과 → 이벤트로 변환
# ============================================================

def _from_finding(f: dict, layer: str, extra: dict) -> dict:
    """finding → 이벤트. 빈 값은 빼서 파일이 불필요하게 커지지 않게 한다."""
    ev = {
        "level": f.get("level"),
        "refs": f.get("refs") or [],
        "signal": f.get("signal"),
        "quant": f.get("quant") or {},
        "qual": f.get("qual") or [],
        "reported_at": f.get("reported_at"),
        **extra,
    }
    ev = {k: v for k, v in ev.items() if v or v == 0}
    # layer 와 summary 는 비어 있어도 항상 남긴다 — 키 계산과 표시의 기준이다
    ev["layer"] = layer
    ev["summary"] = f.get("summary", "")
    return ev


def build_events(
    today: str,
    positions_doc: dict,
    layer0_result: Optional[dict],
    news_sweep: Optional[dict],
    position_results: list[dict],
    theme_results: list[dict],
    normalize_sources=None,
) -> dict[str, list[dict]]:
    """실행 결과를 {position_id: [event, ...]} 로 정리."""
    ns = normalize_sources or (lambda f: f.get("sources") or [])
    out: dict[str, list[dict]] = {}

    def add(pid, ev):
        out.setdefault(pid, []).append(ev)

    # Layer 0 — 포트폴리오 전체
    for f in ((layer0_result or {}).get("findings") or []):
        ev = _from_finding(f, "layer0", {})
        ev["sources"] = ns(f)
        add(PORTFOLIO_ID, ev)

    # 개별 점검
    for item in (position_results or []):
        pid = item.get("position", {}).get("id")
        if not pid:
            continue
        for f in ((item.get("result") or {}).get("findings") or []):
            ev = _from_finding(f, "position", {"kind": f.get("kind")})
            ev["sources"] = ns(f)
            add(pid, ev)

    # 전 종목 소식 스윕 — position_label 로 역매핑
    by_label = {p.get("label"): p["id"] for p in positions_doc.get("positions", [])}
    for it in ((news_sweep or {}).get("items") or []):
        pid = by_label.get(it.get("position_label"))
        if not pid:
            continue
        ev = _from_finding(it, "sweep", {})
        ev["sources"] = ns(it)
        add(pid, ev)

    # 테마 흐름 — affects 로 팬아웃. 오늘 개별 점검 안 한 종목에도 들어간다
    live = {p["id"] for p in positions_doc.get("positions", [])}
    for item in (theme_results or []):
        theme = item.get("theme") or {}
        allowed = [p for p in (theme.get("affects") or []) if p in live]
        for f in ((item.get("result") or {}).get("findings") or []):
            hits = [p for p in (f.get("affects") or []) if p in allowed] or allowed
            for pid in hits:
                ev = _from_finding(f, "theme", {
                    "theme_id": theme.get("id"),
                    "theme_label": theme.get("label"),
                    "direction": f.get("direction"),
                    "headline": f.get("headline"),
                    "shift": f.get("shift"),
                })
                ev["sources"] = ns(f)
                add(pid, ev)

    return out


def record_run(
    today: str,
    positions_doc: dict,
    layer0_result: Optional[dict],
    news_sweep: Optional[dict],
    position_results: list[dict],
    theme_results: list[dict],
    normalize_sources=None,
    base: Optional[Path] = None,
) -> tuple[int, int]:
    """하루치 실행을 종목별 로그에 기록. (신규 건수, 대상 종목 수) 리턴."""
    grouped = build_events(
        today, positions_doc, layer0_result, news_sweep,
        position_results, theme_results, normalize_sources,
    )
    total = 0
    for pid, evs in grouped.items():
        total += append_events(pid, evs, today, base)
    return total, len(grouped)

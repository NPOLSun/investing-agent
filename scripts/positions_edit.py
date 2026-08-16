"""포지션 추가 — 초안 작성 · 검증 · 저장.

positions.json 은 전체 시스템의 단일 진실이다. 이 파일이 깨지면 다음날
다이제스트가 통째로 죽는다. 그래서 저장 경로는 세 겹으로 막는다.
  1. 스키마·참조 검증 (validate_draft) — 통과 못 하면 쓰지 않는다
  2. 원자적 쓰기 (temp → os.replace) — 도중에 죽어도 반쪽 파일이 남지 않는다
  3. 쓴 뒤 재파싱 확인, 실패하면 원본 복구
"""

import json
import logging
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import positions_view as pv

logger = logging.getLogger(__name__)

PROJECT_ROOT = pv.PROJECT_ROOT
POSITIONS_PATH = pv.POSITIONS_PATH

REQUIRED_FIELDS = ("id", "label", "status", "tickers", "thesis", "kill_signals")
VALID_STATUS = ("holding", "watching", "exited", "paused")
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


# ============================================================
# 초안 작성
# ============================================================

def build_draft_prompt(
    ticker: str, reason: str, doc: dict, revision: Optional[str] = None,
    previous: Optional[dict] = None,
) -> str:
    """포지션 초안 작성 프롬프트.

    기존 포지션들을 문체·구체성의 본보기로 함께 넘긴다. 새 포지션의 조건만
    추상적이면 다이제스트가 그 종목에 대해서만 판정을 못 한다.
    """
    samples = []
    for p in doc.get("positions", [])[:3]:
        samples.append(json.dumps({
            "id": p.get("id"), "label": p.get("label"), "areas": p.get("areas"),
            "thesis": p.get("thesis"), "kill_signals": p.get("kill_signals"),
            "add_signals": p.get("add_signals"), "watch": p.get("watch"),
            "ignore": p.get("ignore"),
        }, ensure_ascii=False, indent=1))

    themes = [{
        "id": t["id"], "label": t.get("label"), "areas": t.get("areas"),
        "watch_shifts": t.get("watch_shifts"), "affects": t.get("affects"),
    } for t in doc.get("themes", [])]

    aliases = pv._load(pv.AREA_ALIASES_PATH, {"aliases": {}}).get("aliases", {})
    area_keys = sorted({k for k in aliases})

    revision_block = ""
    if revision and previous:
        revision_block = f"""
# 직전 초안
{json.dumps(previous, ensure_ascii=False, indent=1)}

# 사용자의 수정 요청
{revision}

위 초안을 요청대로 고쳐서 다시 출력할 것. 요청하지 않은 부분은 그대로 둘 것.
"""

    return f"""당신은 투자 포지션 모니터링 설정을 작성하는 조수.

# 추가할 종목
{ticker}

# 사용자가 밝힌 보유 이유
{reason}

# 기존 포지션 예시 (문체·구체성의 기준으로 삼을 것)
{chr(10).join(samples)}

# 기존 테마 목록
{json.dumps(themes, ensure_ascii=False, indent=1)}

# 사용 가능한 영역 키 (areas 에는 이 중에서만 쓸 것)
{', '.join(area_keys)}
{revision_block}
# 작업
아래 JSON 만 출력. 웹 검색은 하지 말 것 — 아는 범위에서 초안을 잡고,
불확실한 것은 notes_for_user 에 확인이 필요하다고 적을 것.

★ 작성 원칙
- kill_signals 는 **관측 가능한 사실**로 쓸 것. "성장이 둔화되면" 같은 모호한
  표현 금지. "분기 매출 성장률이 2개 분기 연속 X% 미만" 처럼 판정 가능하게.
- thesis 는 사용자가 밝힌 이유를 근거로 하되, 무너지면 보유 이유가 사라지는
  문장으로 쪼갤 것.
- ignore 에는 이 종목에서 나올 노이즈(테마 급등락, 목표주가 조정 등)를 적을 것.
- 사용자가 말하지 않은 판단을 지어내지 말 것. 애매하면 notes_for_user 로 물을 것.
- id 는 소문자 영문·하이픈만. 기존 id 와 겹치지 말 것.
- label 은 한글로. 회사명을 괄호에 넣을 것 (예: "GPU 전력공급 (Vicor)").

★ 테마 배치
- 이 포지션이 기존 테마의 affects 에 들어가야 하면 theme_assignment.existing 에 id 를 적을 것.
- 기존 테마 중 결이 맞는 게 없으면 new_theme 을 제안할 것. 억지로 끼워넣지 말 것.
  예: 기존 테마가 전부 "AI capex 를 받는 쪽"인데 새 종목이 "capex 를 쓰는 쪽"이면
  방향이 반대이므로 새 테마가 맞다.
- 어느 쪽도 아니면 둘 다 비우고 notes_for_user 에 이유를 쓸 것.

{{
  "position": {{
    "id": "소문자-하이픈",
    "label": "한글 이름 (회사명)",
    "status": "holding",
    "tickers": ["티커"],
    "areas": ["영역 키"],
    "thesis": ["...", "..."],
    "kill_signals": ["...", "..."],
    "add_signals": ["..."],
    "watch": {{"peers": ["..."], "indicators": ["..."], "queries": ["..."]}},
    "ignore": ["..."],
    "note": "한 문단. 주의할 점·함정"
  }},
  "theme_assignment": {{
    "existing": ["테마 id"],
    "new_theme": null
  }},
  "notes_for_user": ["사용자에게 확인받아야 할 점"]
}}

JSON 외 다른 텍스트 출력 금지."""


# ============================================================
# 검증
# ============================================================

def validate_draft(draft: dict, doc: dict) -> tuple[list[str], list[str]]:
    """(치명적 오류, 경고) 리턴. 오류가 하나라도 있으면 저장하지 않는다."""
    errors, warns = [], []
    pos = (draft or {}).get("position") or {}

    for f in REQUIRED_FIELDS:
        if not pos.get(f):
            errors.append(f"{f} 가 비어 있음")

    pid = pos.get("id", "")
    if pid and not ID_RE.match(pid):
        errors.append(f"id '{pid}' 형식 오류 (소문자 영문·숫자·하이픈만)")
    if pid and any(p.get("id") == pid for p in doc.get("positions", [])):
        errors.append(f"id '{pid}' 가 이미 있음")

    if pos.get("status") not in VALID_STATUS:
        errors.append(f"status '{pos.get('status')}' 는 허용값이 아님 ({', '.join(VALID_STATUS)})")

    tickers = pos.get("tickers") or []
    if not isinstance(tickers, list) or not all(isinstance(t, str) and t for t in tickers):
        errors.append("tickers 는 비어있지 않은 문자열 배열이어야 함")
    else:
        existing = {t: p.get("label") for p in doc.get("positions", []) for t in p.get("tickers", [])}
        for t in tickers:
            if t in existing:
                warns.append(f"티커 {t} 는 이미 '{existing[t]}' 에 등록돼 있음")

    for f in ("thesis", "kill_signals", "add_signals", "ignore"):
        v = pos.get(f)
        if v is not None and not (isinstance(v, list) and all(isinstance(x, str) for x in v)):
            errors.append(f"{f} 는 문자열 배열이어야 함")

    watch = pos.get("watch")
    if watch is not None and not isinstance(watch, dict):
        errors.append("watch 는 객체여야 함")

    aliases = pv._load(pv.AREA_ALIASES_PATH, {"aliases": {}}).get("aliases", {})
    bad_areas = [a for a in (pos.get("areas") or []) if a not in aliases]
    if bad_areas:
        errors.append(f"areas 에 등록되지 않은 키: {', '.join(bad_areas)}")
    if not pos.get("areas"):
        warns.append("areas 미지정 — mega-change-map 영역과 연결되지 않음")

    ta = (draft or {}).get("theme_assignment") or {}
    existing_ids = {t["id"] for t in doc.get("themes", [])}
    for tid in (ta.get("existing") or []):
        if tid not in existing_ids:
            errors.append(f"존재하지 않는 테마 id: {tid}")

    nt = ta.get("new_theme")
    if nt:
        if not nt.get("id") or not ID_RE.match(nt.get("id", "")):
            errors.append("새 테마 id 형식 오류")
        elif nt["id"] in existing_ids:
            errors.append(f"새 테마 id '{nt['id']}' 가 이미 있음")
        for f in ("label", "watch_shifts", "queries"):
            if not nt.get(f):
                errors.append(f"새 테마의 {f} 가 비어 있음")

    if not (ta.get("existing") or nt):
        warns.append("어느 테마에도 연결되지 않음 — 🔷 AI 인프라 흐름 섹션에 나오지 않음")

    if not pos.get("kill_signals"):
        warns.append("매도 검토 조건 없음 — 이 포지션은 영원히 🔴 가 뜨지 않음")

    return errors, warns


# ============================================================
# 표시
# ============================================================

def format_draft(draft: dict, doc: dict) -> str:
    pos = draft.get("position") or {}
    ta = draft.get("theme_assignment") or {}
    themes_by_id = {t["id"]: t for t in doc.get("themes", [])}
    aliases = pv._load(pv.AREA_ALIASES_PATH, {"aliases": {}}).get("aliases", {})

    out = [f"📝 초안 — {pos.get('label')} ({', '.join(pos.get('tickers', []))})", ""]

    def block(title, items):
        out.append(title)
        for i, it in enumerate(items or [], 1):
            out.append(f"  {i}. {it}")
        if not items:
            out.append("  (없음)")
        out.append("")

    block("보유 근거", pos.get("thesis"))
    block("매도 검토 조건", pos.get("kill_signals"))
    block("추가 검토 조건", pos.get("add_signals"))

    watch = pos.get("watch") or {}
    out.append("감시")
    out.append(f"  경쟁사: {', '.join(watch.get('peers', [])) or '(없음)'}")
    out.append(f"  지표: {', '.join(watch.get('indicators', [])) or '(없음)'}")
    out.append(f"  검색어: {', '.join(watch.get('queries', [])) or '(없음)'}")
    out.append("")

    if pos.get("ignore"):
        out.append("무시")
        for it in pos["ignore"]:
            out.append(f"  · {it}")
        out.append("")

    areas = [aliases.get(a, {}).get("title", a) for a in (pos.get("areas") or [])]
    out.append(f"영역: {', '.join(areas) or '미지정'}")

    exist = [themes_by_id.get(t, {}).get("label", t) for t in (ta.get("existing") or [])]
    nt = ta.get("new_theme")
    if exist:
        out.append(f"테마: {', '.join(exist)} 에 연결")
    if nt:
        out.append(f"테마: 🆕 '{nt.get('label')}' 새로 만들기 제안")
        for w in (nt.get("watch_shifts") or [])[:4]:
            out.append(f"     · {w}")
    if not exist and not nt:
        out.append("테마: 없음")

    if pos.get("note"):
        out.append("")
        out.append(f"메모: {pos['note']}")

    notes = draft.get("notes_for_user") or []
    if notes:
        out.append("")
        out.append("❓ 확인이 필요합니다")
        for n in notes:
            out.append(f"  · {n}")

    return "\n".join(out)


# ============================================================
# 저장
# ============================================================

def _git(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=PROJECT_ROOT,
                          capture_output=True, timeout=timeout)


def save_draft(draft: dict) -> tuple[bool, str]:
    """검증 → 원자적 쓰기 → git 커밋·푸시. (성공여부, 메시지)

    쓰기 직전에 파일을 다시 읽는다. 대화하는 동안 다른 곳에서 파일이
    바뀌었을 수 있고(다이제스트의 상태 커밋, PC 에서의 편집), 대화 시작
    시점의 사본에 덮어쓰면 그 변경이 사라진다.
    """
    pull = _git(["pull", "--ff-only", "origin", "main"], timeout=120)
    if pull.returncode != 0:
        logger.warning(f"git pull 실패 (계속 진행): {pull.stderr.decode(errors='replace')[:200]}")

    doc = pv._load(POSITIONS_PATH, {})
    if not doc.get("positions"):
        return False, "positions.json 을 읽지 못했습니다. 저장을 중단합니다."

    errors, _warns = validate_draft(draft, doc)
    if errors:
        return False, "검증 실패로 저장하지 않았습니다:\n" + "\n".join(f"· {e}" for e in errors)

    pos = draft["position"]
    ta = draft.get("theme_assignment") or {}

    doc["positions"].append(pos)
    doc.setdefault("themes", [])
    for tid in (ta.get("existing") or []):
        for t in doc["themes"]:
            if t["id"] == tid and pos["id"] not in (t.get("affects") or []):
                t.setdefault("affects", []).append(pos["id"])
    nt = ta.get("new_theme")
    if nt:
        nt.setdefault("affects", [])
        if pos["id"] not in nt["affects"]:
            nt["affects"].append(pos["id"])
        nt.setdefault("core", False)
        doc["themes"].append(nt)

    meta = doc.setdefault("meta", {})
    meta["last_updated"] = __import__("datetime").date.today().isoformat()

    original = POSITIONS_PATH.read_bytes()
    payload = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"

    try:
        fd, tmp = tempfile.mkstemp(dir=str(POSITIONS_PATH.parent), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
        os.replace(tmp, POSITIONS_PATH)
        # 쓴 결과가 실제로 파싱되는지 확인 — 안 되면 즉시 되돌린다
        check = json.loads(POSITIONS_PATH.read_text(encoding="utf-8"))
        assert any(p["id"] == pos["id"] for p in check["positions"])
    except Exception as e:
        POSITIONS_PATH.write_bytes(original)
        logger.exception("positions.json 쓰기 실패 — 원본 복구")
        return False, f"저장 실패, 원본을 복구했습니다: {e}"

    add = _git(["add", str(POSITIONS_PATH)])
    if add.returncode != 0:
        return True, f"파일은 저장했으나 git add 실패: {add.stderr.decode(errors='replace')[:150]}"
    msg = f"Add position {pos['id']} via bot"
    commit = _git(["commit", "-m", msg])
    if commit.returncode != 0:
        return True, f"파일은 저장했으나 커밋 실패: {commit.stderr.decode(errors='replace')[:150]}"
    push = _git(["push", "origin", "main"], timeout=120)
    if push.returncode != 0:
        return True, ("파일 저장·커밋은 됐으나 푸시 실패 (나중에 수동 푸시 필요): "
                      f"{push.stderr.decode(errors='replace')[:150]}")

    extra = f" · 테마 '{nt['label']}' 신설" if nt else ""
    return True, f"✅ 저장·커밋·푸시 완료{extra}\n내일 아침 다이제스트부터 반영됩니다."

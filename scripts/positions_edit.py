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
    "existing": ["기존 테마 id (없으면 빈 배열)"],
    "new_theme": null
  }},
  "notes_for_user": ["사용자에게 확인받아야 할 점"]
}}

new_theme 을 제안할 때는 null 대신 아래를 **모든 필드 채워서** 넣을 것:

{{
  "id": "소문자-하이픈",
  "label": "한글 테마명",
  "areas": ["영역 키 (없으면 빈 배열)"],
  "core": false,
  "watch_shifts": ["추적할 '변화'. kill 조건이 아니라 방향·속도를 묻는 문장. 3~5개"],
  "queries": ["검색 키워드 3~5개"],
  "key_vendors": ["회사 — 제품/브랜드명 (3~6개)"]
}}

★ key_vendors 를 반드시 채울 것. 업계 뉴스는 기술 일반명이 아니라 **제품 브랜드명**
으로 보도된다. 여기가 비면 그 테마는 큰 발표를 통째로 놓친다 (실측 사례 있음).
회사명만 쓰지 말고 제품 라인까지 적을 것 — 예: "NVIDIA — Spectrum-X Photonics(이더넷 CPO)".

JSON 외 다른 텍스트 출력 금지."""


# ============================================================
# 검증
# ============================================================

def validate_draft(draft: dict, doc: dict, editing_id: Optional[str] = None) -> tuple[list[str], list[str]]:
    """(치명적 오류, 경고) 리턴. 오류가 하나라도 있으면 저장하지 않는다.

    editing_id 가 주어지면 기존 포지션 수정으로 본다 — id 중복은 자기 자신이면
    정상이고, 오히려 id 가 바뀌면 다른 포지션을 덮어쓰는 셈이라 막는다.
    """
    errors, warns = [], []
    pos = (draft or {}).get("position") or {}

    for f in REQUIRED_FIELDS:
        if not pos.get(f):
            errors.append(f"{f} 가 비어 있음")

    pid = pos.get("id", "")
    if pid and not ID_RE.match(pid):
        errors.append(f"id '{pid}' 형식 오류 (소문자 영문·숫자·하이픈만)")
    if editing_id:
        if pid != editing_id:
            errors.append(f"수정 중에는 id 를 바꿀 수 없음 ({editing_id} → {pid})")
    elif pid and any(p.get("id") == pid for p in doc.get("positions", [])):
        errors.append(f"id '{pid}' 가 이미 있음")

    if pos.get("status") not in VALID_STATUS:
        errors.append(f"status '{pos.get('status')}' 는 허용값이 아님 ({', '.join(VALID_STATUS)})")

    tickers = pos.get("tickers") or []
    if not isinstance(tickers, list) or not all(isinstance(t, str) and t for t in tickers):
        errors.append("tickers 는 비어있지 않은 문자열 배열이어야 함")
    else:
        existing = {
            t: p.get("label") for p in doc.get("positions", [])
            if p.get("id") != editing_id
            for t in p.get("tickers", [])
        }
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
        # key_vendors 를 필수로 두는 이유: 벤더·제품명 없이 기술 일반명으로만
        # 검색하면 브랜드명으로 보도되는 발표를 통째로 놓친다 (2026-08-16 실측).
        for f in ("label", "watch_shifts", "queries", "key_vendors"):
            if not nt.get(f):
                errors.append(f"새 테마의 {f} 가 비어 있음")
        bad_theme_areas = [a for a in (nt.get("areas") or []) if a not in aliases]
        if bad_theme_areas:
            errors.append(f"새 테마 areas 에 등록되지 않은 키: {', '.join(bad_theme_areas)}")

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

    extra = f" · 테마 '{nt['label']}' 신설" if nt else ""
    return _write_and_push(
        doc, f"Add position {pos['id']} via bot",
        f"✅ 저장·커밋·푸시 완료{extra}\n내일 아침 다이제스트부터 반영됩니다.",
    )


# ============================================================
# 수정
# ============================================================

_EDITABLE = ("label", "status", "tickers", "areas", "thesis", "kill_signals",
             "add_signals", "watch", "ignore", "note")


def build_edit_prompt(pos: dict, request: str, doc: dict) -> str:
    """기존 포지션 수정 프롬프트. 요청한 곳만 고치게 강하게 못박는다."""
    aliases = pv._load(pv.AREA_ALIASES_PATH, {"aliases": {}}).get("aliases", {})
    themes = [{"id": t["id"], "label": t.get("label"), "affects": t.get("affects")}
              for t in doc.get("themes", [])]

    return f"""당신은 투자 포지션 모니터링 설정을 수정하는 조수.

# 현재 설정 (원문)
{json.dumps(pos, ensure_ascii=False, indent=1)}

# 기존 테마 목록
{json.dumps(themes, ensure_ascii=False, indent=1)}

# 사용 가능한 영역 키
{', '.join(sorted(aliases))}

# 사용자의 수정 요청
{request}

# 작업
수정된 포지션 전체를 아래 JSON 으로 출력. 웹 검색 금지.

★★ 가장 중요한 규칙
- **요청한 부분만 고칠 것.** 나머지 항목은 글자 하나 바꾸지 말고 그대로 옮길 것.
  문장을 다듬거나 더 매끄럽게 고치지 말 것. 이건 사용자가 직접 쓴 판단 근거이고,
  다이제스트가 이 문장을 그대로 인용한다. 임의로 바꾸면 판정 기준이 조용히 달라진다.
- id 는 절대 바꾸지 말 것 ("{pos.get('id')}" 유지).
- 항목을 지우라고 하면 지우고, 추가하라고 하면 추가할 것. 번호는 배열 순서다.
- 요청이 모호하면 추측하지 말고 notes_for_user 에 무엇이 불분명한지 적고,
  해당 부분은 원문 그대로 둘 것.

{{
  "position": {{ 수정된 포지션 전체 — 위 현재 설정과 같은 키 구성 }},
  "theme_assignment": {{ "existing": ["연결할 테마 id — 변경 요청이 없으면 빈 배열"], "new_theme": null }},
  "notes_for_user": ["불분명해서 손대지 않은 부분"]
}}

JSON 외 다른 텍스트 출력 금지."""


def diff_position(old: dict, new: dict) -> str:
    """변경 전후 비교. 모델이 요청하지 않은 문장을 손댔는지 눈으로 잡기 위한 것."""
    lines = []
    for f in _EDITABLE:
        o, n = old.get(f), new.get(f)
        if o == n:
            continue
        if isinstance(o, list) and isinstance(n, list):
            lines.append(f"[{f}]")
            for item in o:
                if item not in n:
                    lines.append(f"  − {item}")
            for item in n:
                if item not in o:
                    lines.append(f"  + {item}")
        else:
            lines.append(f"[{f}]")
            lines.append(f"  − {o}")
            lines.append(f"  + {n}")
    return "\n".join(lines) if lines else "(변경 없음)"


def save_position_update(new_pos: dict, theme_assignment: Optional[dict] = None) -> tuple[bool, str]:
    """기존 포지션 교체 저장. save_draft 와 같은 3중 안전장치를 탄다."""
    pull = _git(["pull", "--ff-only", "origin", "main"], timeout=120)
    if pull.returncode != 0:
        logger.warning(f"git pull 실패 (계속): {pull.stderr.decode(errors='replace')[:200]}")

    doc = pv._load(POSITIONS_PATH, {})
    if not doc.get("positions"):
        return False, "positions.json 을 읽지 못했습니다. 저장을 중단합니다."

    pid = new_pos.get("id")
    idx = next((i for i, p in enumerate(doc["positions"]) if p.get("id") == pid), None)
    if idx is None:
        return False, f"'{pid}' 포지션을 찾을 수 없습니다."

    errors, _ = validate_draft({"position": new_pos,
                                "theme_assignment": theme_assignment or {}},
                               doc, editing_id=pid)
    if errors:
        return False, "검증 실패로 저장하지 않았습니다:\n" + "\n".join(f"· {e}" for e in errors)

    doc["positions"][idx] = new_pos
    for tid in ((theme_assignment or {}).get("existing") or []):
        for t in doc.get("themes", []):
            if t["id"] == tid and pid not in (t.get("affects") or []):
                t.setdefault("affects", []).append(pid)

    doc.setdefault("meta", {})["last_updated"] = __import__("datetime").date.today().isoformat()
    return _write_and_push(doc, f"Update position {pid} via bot",
                           f"✅ '{new_pos.get('label')}' 수정 완료")


def exit_position(pos_id: str, reason: str) -> tuple[bool, str]:
    """매도 처리 — status 를 exited 로. 기록은 지우지 않고 남긴다.

    positions.json 의 status_values 가 exited 를 "기록 보존용 (판단 복기 재료)"
    로 정의한다. 삭제하면 나중에 왜 그렇게 판단했는지 복기할 수 없다.
    테마 affects 에서는 뺀다 — 안 그러면 판 종목이 계속 '닿는 포지션' 으로 나온다.
    """
    pull = _git(["pull", "--ff-only", "origin", "main"], timeout=120)
    if pull.returncode != 0:
        logger.warning(f"git pull 실패 (계속): {pull.stderr.decode(errors='replace')[:200]}")

    doc = pv._load(POSITIONS_PATH, {})
    if not doc.get("positions"):
        return False, "positions.json 을 읽지 못했습니다."

    pos = next((p for p in doc["positions"] if p.get("id") == pos_id), None)
    if pos is None:
        return False, f"'{pos_id}' 포지션을 찾을 수 없습니다."
    if pos.get("status") == "exited":
        return False, f"'{pos.get('label')}' 는 이미 매도 완료 상태입니다."

    today = __import__("datetime").date.today().isoformat()
    pos["status"] = "exited"
    tail = f"[{today} 매도] {reason}".strip()
    pos["note"] = f"{pos.get('note', '').strip()}\n{tail}".strip()

    removed = []
    for t in doc.get("themes", []):
        if pos_id in (t.get("affects") or []):
            t["affects"].remove(pos_id)
            removed.append(t.get("label", t["id"]))

    doc.setdefault("meta", {})["last_updated"] = today
    extra = f"\n테마 연결 해제: {', '.join(removed)}" if removed else ""
    return _write_and_push(
        doc, f"Exit position {pos_id} via bot",
        f"✅ '{pos.get('label')}' 매도 처리 완료 (기록은 보존){extra}\n"
        f"내일 아침 다이제스트부터 모니터링 대상에서 빠집니다.",
    )


def _write_and_push(doc: dict, commit_msg: str, ok_msg: str) -> tuple[bool, str]:
    """원자적 쓰기 + 검증 + git. save_draft 와 공유하는 마지막 단계."""
    original = POSITIONS_PATH.read_bytes()
    payload = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    try:
        fd, tmp = tempfile.mkstemp(dir=str(POSITIONS_PATH.parent), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
        os.replace(tmp, POSITIONS_PATH)
        json.loads(POSITIONS_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        POSITIONS_PATH.write_bytes(original)
        logger.exception("positions.json 쓰기 실패 — 원본 복구")
        return False, f"저장 실패, 원본을 복구했습니다: {e}"

    if _git(["add", str(POSITIONS_PATH)]).returncode != 0:
        return True, ok_msg + "\n(git add 실패 — 수동 커밋 필요)"
    if _git(["commit", "-m", commit_msg]).returncode != 0:
        return True, ok_msg + "\n(커밋 실패 — 수동 커밋 필요)"
    push = _git(["push", "origin", "main"], timeout=120)
    if push.returncode != 0:
        return True, ok_msg + "\n(푸시 실패 — 나중에 수동 푸시 필요)"
    return True, ok_msg

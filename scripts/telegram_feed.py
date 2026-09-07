"""텔레그램 구독 채널 수집기 (Layer -1 · 원문 피드).

web_search 로 뉴스를 '발굴'하려던 기존 방식은 실패했다. 실측 결과 이벤트의 45%가
보고 시점보다 15일 이상 오래된 기사를 재확인한 것이었다. 검색 엔진은 오늘 뭐가
새로 터졌는지를 모른다 — 이미 색인된 것 중 질의어에 맞는 걸 줄 뿐이다.

대신 사용자가 직접 골라 구독 중인 텔레그램 채널을 원천으로 삼는다. 사람이 이미
큐레이션한 피드이므로 신선도와 관련성이 검색보다 압도적으로 낫고, 여러 채널이
같은 건을 동시에 다루면 그 자체가 중요도 신호가 된다 (dupe_count).

★ Bot API 로는 불가능하다. 봇은 자신이 멤버인 방만 읽는다. 사용자가 구독한
  채널을 읽으려면 MTProto 사용자 세션이 필요하다 → Telethon.
  .env 에 TELEGRAM_API_ID / TELEGRAM_API_HASH (my.telegram.org 발급) 필요.

사용법:
  python scripts/telegram_feed.py --login          최초 1회. 전화번호 + 인증코드
  python scripts/telegram_feed.py --list           구독 채널 목록 (번호 확인용)
  python scripts/telegram_feed.py --enable 1,4,9   수집 대상 지정
  python scripts/telegram_feed.py --fetch          새 글 수집 → data/feed/
  python scripts/telegram_feed.py --show           오늘 수집분 미리보기
  python scripts/telegram_feed.py --stats          튜닝용 실측 (물량·길이·중복·표본)

채널별 설정 (data/feed_channels.json 을 직접 고치지 않아도 된다):
  --set-note '시그널랩' '증권사 리포트 요약. 밀도 최고'
  --set-drop '특파원' '비트코인|암호화폐'      무엇이 걸리는지 바로 보여준다
  --unset-drop '특파원'                        현재 패턴 목록
  --set-docs '시그널랩' on                     첨부 PDF 리포트까지 읽는다
"""

import argparse
import asyncio
import hashlib
import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pytz
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

KST = pytz.timezone("Asia/Seoul")

SESSION_PATH = PROJECT_ROOT / ".telegram_user"      # Telethon 이 .session 을 붙인다
CHANNELS_PATH = PROJECT_ROOT / "data" / "feed_channels.json"
FEED_DIR = PROJECT_ROOT / "data" / "feed"

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

# 최초 수집 시 얼마나 거슬러 올라갈지. 이후로는 채널별 last_id 부터만 읽는다.
FIRST_RUN_HOURS = 24
# 채널 하나당 한 번에 가져올 상한. 폭주 채널이 하루치를 다 먹는 걸 막는다.
# 실측(2026-09-07): 가장 폭주하는 채널이 24시간에 109건. 평일은 더 늘 수 있어
# 여유를 둔다 — 여기서 잘리면 오래된 쪽이 아니라 **최신 쪽이 남고 옛것이 잘린다**.
MAX_PER_CHANNEL = 200
# 이보다 짧은 글은 버린다 (이모지 한 줄, "ㅋㅋ" 같은 잡음)
MIN_TEXT_LEN = 25

# 첨부 리포트(PDF) 처리. 증권사 리포트를 옮기는 채널은 본문이 "[SK증권 반도체
# 한동희]" 한 줄이고 알맹이는 전부 첨부에 있다. 그걸 안 열면 그 채널을 구독한
# 의미가 없다.
#
# ★ 채널별로 켠다 (feed_channels.json 의 "fetch_docs": true). 전 채널에 켜면
#   짤·이미지까지 받느라 디스크와 시간을 태운다.
DOCS_DIR = FEED_DIR / "docs"
# 이보다 큰 첨부는 건너뛴다. EC2 디스크가 6.8GB 뿐이다.
MAX_DOC_MB = 25
# 추출 텍스트 보관 기간. 원본 PDF 는 추출 직후 지우고 텍스트만 남긴다.
DOC_RETENTION_DAYS = 30

# 매일 같은 모양으로 반복되는 정기 잡음. 실측(2026-09-07) 204건 중 20건 이상이
# 이것이었다. 채널 공지·기상통보·2시간마다 올라오는 리포트 목차 같은 것들.
#
# ★ 수집 때가 아니라 **읽을 때** 거른다. 원문은 그대로 저장해 둔다 —
#   패턴을 잘못 잡아 알짜를 버려도 되돌릴 수 있어야 하기 때문이다.
#   수집 단계에서 버리면 워터마크가 이미 지나가 복구가 불가능하다.
# 채널별 잡음 패턴을 걸 범위. 제목 줄 앞부분만 본다 (headline 주석 참고).
DROP_HEADLINE_CHARS = 160

DROP_PATTERNS = [
    r"현재 채널은.*딜레이가 있는",          # 채널 자체 공지
    r"^\s*\[단기예보\]\s*기상청 통보문",     # 기상청 자동 포스팅
    r"^\s*\*{0,2}\d+\.\s*📚.*리포트\*{0,2}\s*\(\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}\s*기준\)",
                                            # 2시간마다 올라오는 리포트 목차
]


# ============================================================
# 설정 파일
# ============================================================

def load_channels() -> dict:
    if not CHANNELS_PATH.exists():
        return {"channels": []}
    try:
        return json.loads(CHANNELS_PATH.read_text(encoding="utf-8")) or {"channels": []}
    except Exception as e:
        logger.error(f"feed_channels.json 읽기 실패: {e}")
        return {"channels": []}


def save_channels(doc: dict):
    CHANNELS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHANNELS_PATH.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ============================================================
# 중복 판정
# ============================================================

_URL_RE = re.compile(r"https?://\S+")
_NOISE_RE = re.compile(r"[^\w가-힣]+")

# 4-gram 이 이 비율 이상 겹치면 같은 건으로 본다. 채널마다 "[속보]" 같은
# 머리말과 자기 코멘트를 덧붙이므로 완전 일치로는 절대 안 잡힌다.
DUPE_SIMILARITY = 0.55
# 유사도 비교에 쓸 본문 길이. 뒤에 붙는 채널 홍보 문구를 잘라내는 효과도 있다.
DUPE_PREFIX_LEN = 200


def text_shingles(text: str) -> set:
    """유사도 비교용 문자 4-gram 집합. URL·기호·공백은 털어낸다."""
    t = _URL_RE.sub("", text or "")
    t = _NOISE_RE.sub("", t).lower()[:DUPE_PREFIX_LEN]
    return {t[i:i + 4] for i in range(max(0, len(t) - 3))}


def similarity(a: set, b: set) -> float:
    """자카드가 아니라 포함률(작은 쪽 기준)을 쓴다.

    한 채널은 헤드라인만, 다른 채널은 기사 본문까지 붙이는 일이 흔하다.
    자카드로 재면 길이 차 때문에 같은 건인데도 점수가 주저앉는다.
    """
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def group_duplicates(items: list[dict]) -> None:
    """같은 뉴스를 옮긴 항목끼리 dupe_group 을 공유하도록 제자리에서 표시.

    여러 채널이 동시에 다룬다는 것 자체가 중요도 신호다 (dupe_count).
    항목 수가 하루 수백 건 수준이라 단순 O(n²) 비교로 충분하다.
    """
    sigs = [text_shingles(x["text"]) for x in items]
    parent = list(range(len(items)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if similarity(sigs[i], sigs[j]) >= DUPE_SIMILARITY:
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[rj] = ri

    groups: dict[int, list[int]] = {}
    for i in range(len(items)):
        groups.setdefault(find(i), []).append(i)

    for root, members in groups.items():
        # 그룹 id 는 대표 항목 본문으로 고정한다 — 실행이 갈려도 같은 값이 나온다.
        gid = hashlib.sha1(
            "".join(sorted(text_shingles(items[root]["text"]))).encode("utf-8")
        ).hexdigest()[:16]
        names = sorted({items[m]["channel"] for m in members})
        for m in members:
            items[m]["dupe_group"] = gid
            items[m]["dupe_count"] = len(names)
            items[m]["also_in"] = [n for n in names if n != items[m]["channel"]]


# ============================================================
# 수집
# ============================================================

def _require_creds():
    if not API_ID or not API_HASH:
        sys.exit(
            "TELEGRAM_API_ID / TELEGRAM_API_HASH 가 .env 에 없습니다.\n"
            "  1) https://my.telegram.org -> API development tools 에서 앱 생성\n"
            "  2) .env 에 아래 두 줄 추가\n"
            "       TELEGRAM_API_ID=12345678\n"
            "       TELEGRAM_API_HASH=0123456789abcdef...\n"
            "  3) python scripts/telegram_feed.py --login"
        )


def _client():
    from telethon import TelegramClient
    return TelegramClient(str(SESSION_PATH), int(API_ID), API_HASH)


async def cmd_login():
    """최초 1회. 전화번호와 인증코드를 물어보고 세션 파일을 만든다."""
    _require_creds()
    client = _client()
    await client.start()                    # 대화형 — 전화번호·코드·2FA 프롬프트
    me = await client.get_me()
    print(f"로그인 완료: {me.first_name} (@{me.username or '-'})")
    print(f"세션 파일: {SESSION_PATH}.session  <- .gitignore 대상, EC2 로 따로 복사할 것")
    await client.disconnect()


async def cmd_list():
    """구독 중인 채널·그룹을 번호와 함께 출력. --enable 에 쓸 번호를 여기서 고른다."""
    _require_creds()
    from telethon.tl.types import Channel
    client = _client()
    await client.start()
    enabled = {c["id"] for c in load_channels()["channels"] if c.get("enabled")}
    rows = []
    async for d in client.iter_dialogs():
        ent = d.entity
        if not isinstance(ent, Channel):
            continue                        # 개인 대화·소규모 그룹은 제외
        rows.append({
            "id": ent.id,
            "title": d.name,
            "username": getattr(ent, "username", None),
            "broadcast": bool(getattr(ent, "broadcast", False)),
        })
    await client.disconnect()

    print(f"\n채널 {len(rows)}개\n")
    for i, r in enumerate(rows, 1):
        mark = "*" if r["id"] in enabled else " "
        kind = "채널" if r["broadcast"] else "그룹"
        uname = f"@{r['username']}" if r["username"] else f"id:{r['id']}"
        print(f" {mark} {i:>3}. [{kind}] {r['title'][:42]:<44} {uname}")
    print("\n수집할 번호 지정:  python scripts/telegram_feed.py --enable 1,4,9")

    # 번호 -> id 매핑을 남겨야 --enable 이 번호로 동작한다
    doc = load_channels()
    doc["last_listing"] = rows
    save_channels(doc)


def cmd_enable(spec: str):
    """--list 가 남긴 번호 매핑을 보고 수집 대상을 켠다. 기존 선택은 대체된다."""
    doc = load_channels()
    listing = doc.get("last_listing") or []
    if not listing:
        sys.exit("먼저 --list 를 실행해 채널 목록을 받아야 합니다.")

    try:
        picks = [int(x) for x in re.split(r"[,\s]+", spec.strip()) if x]
    except ValueError:
        sys.exit("번호는 쉼표로 구분한 정수여야 합니다 (예: 1,4,9)")

    prev = {c["id"]: c for c in doc.get("channels", [])}
    chosen = []
    for n in picks:
        if not (1 <= n <= len(listing)):
            sys.exit(f"{n} 번은 목록(1~{len(listing)}) 범위 밖입니다.")
        r = listing[n - 1]
        old = prev.get(r["id"], {})
        chosen.append({
            "id": r["id"],
            "title": r["title"],
            "username": r["username"],
            "enabled": True,
            "last_id": old.get("last_id", 0),   # 워터마크는 보존
        })
    doc["channels"] = chosen
    save_channels(doc)
    print(f"수집 대상 {len(chosen)}개 저장:")
    for c in chosen:
        print(f"  - {c['title']}")


def doc_text_path(doc_id: int) -> Path:
    return DOCS_DIR / f"{doc_id}.txt"


def read_doc_text(doc_id: int, limit: Optional[int] = None) -> str:
    p = doc_text_path(doc_id)
    if not p.exists():
        return ""
    try:
        t = p.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning(f"첨부 텍스트 읽기 실패 ({doc_id}): {e}")
        return ""
    return t[:limit] if limit else t


def _pdf_to_text(path: Path) -> tuple[str, int]:
    """PDF 에서 본문 텍스트를 뽑는다. (텍스트, 페이지수).

    스캔 이미지로만 된 리포트는 빈 문자열이 나온다 — OCR 은 하지 않는다.
    그런 경우 호출자가 '본문 추출 실패' 로 남겨 사람이 알 수 있게 한다.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        logger.error("pypdf 가 없어 첨부를 못 읽는다 — pip install pypdf")
        return "", 0
    try:
        reader = PdfReader(str(path))
        pages = [(p.extract_text() or "") for p in reader.pages]
        return "\n".join(pages).strip(), len(pages)
    except Exception as e:
        msg = str(e)
        if "cryptography" in msg or "AES" in msg:
            # 암호화된 PDF. pip install cryptography 로 풀리는 문제라
            # '스캔본' 으로 뭉뚱그리면 고칠 수 있는 걸 못 고친다.
            logger.error(f"PDF 가 암호화돼 있다 — pip install cryptography ({path.name})")
        else:
            logger.warning(f"PDF 파싱 실패 ({path.name}): {e}")
        return "", 0


async def _grab_document(client, msg, ch: dict) -> Optional[dict]:
    """메시지에 붙은 PDF 를 받아 텍스트만 남긴다.

    같은 파일이 여러 채널에 돌면 document.id 가 같으므로 한 번만 받는다.
    원본 PDF 는 추출 직후 삭제한다 — 디스크가 6.8GB 뿐이고, 다시 필요하면
    텔레그램 원문 링크로 돌아갈 수 있다.
    """
    doc = getattr(msg, "document", None)
    if doc is None:
        return None

    name = ""
    for attr in (getattr(doc, "attributes", None) or []):
        name = getattr(attr, "file_name", "") or name
    mime = (getattr(doc, "mime_type", "") or "").lower()
    if "pdf" not in mime and not name.lower().endswith(".pdf"):
        return None

    size_mb = (getattr(doc, "size", 0) or 0) / (1024 * 1024)
    if size_mb > MAX_DOC_MB:
        logger.info(f"[{ch['title']}] 첨부 건너뜀 ({size_mb:.1f}MB > {MAX_DOC_MB}MB): {name}")
        return None

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    out = doc_text_path(doc.id)
    if out.exists():                       # 이미 받아 뽑아둔 파일
        return {"id": doc.id, "name": name, "chars": len(out.read_text(encoding="utf-8"))}

    pdf_path = DOCS_DIR / f"{doc.id}.pdf"
    try:
        await client.download_media(msg, file=str(pdf_path))
    except Exception as e:
        logger.warning(f"[{ch['title']}] 첨부 다운로드 실패 ({name}): {e}")
        return None

    text, pages = _pdf_to_text(pdf_path)
    try:
        pdf_path.unlink()                  # 텍스트만 남기고 원본은 버린다
    except Exception:
        pass

    if not text:
        logger.info(f"[{ch['title']}] 본문 추출 실패 (스캔본으로 보임): {name}")
        return {"id": doc.id, "name": name, "chars": 0, "pages": pages}

    out.write_text(text, encoding="utf-8")
    logger.info(f"[{ch['title']}] 첨부 {name} — {pages}쪽 {len(text):,}자 추출")
    return {"id": doc.id, "name": name, "chars": len(text), "pages": pages}


def prune_docs(days: int = DOC_RETENTION_DAYS):
    """오래된 추출 텍스트 정리. 디스크가 6.8GB 뿐이라 무한 적재 금지."""
    if not DOCS_DIR.exists():
        return
    cutoff = datetime.now().timestamp() - days * 86400
    for p in DOCS_DIR.iterdir():
        try:
            if p.stat().st_mtime < cutoff:
                p.unlink()
        except Exception:
            continue


def _find_channel(doc: dict, needle: str) -> dict:
    """제목 일부로 수집 대상 채널 하나를 찾는다.

    번호로 지정하게 하면 --list 를 다시 돌려야 하고, 목록 순서는 대화 활동에
    따라 바뀐다. 제목 일부가 사람이 쓰기에도 안전하다.
    """
    hits = [c for c in doc.get("channels", []) if needle.lower() in c["title"].lower()]
    if not hits:
        names = "\n".join(f"  - {c['title']}" for c in doc.get("channels", []))
        sys.exit(f"'{needle}' 와 맞는 채널이 없습니다. 현재 수집 대상:\n{names}")
    if len(hits) > 1:
        names = "\n".join(f"  - {c['title']}" for c in hits)
        sys.exit(f"'{needle}' 가 여러 채널과 맞습니다. 더 길게 지정하세요:\n{names}")
    return hits[0]


def cmd_set_note(needle: str, note: str):
    """채널 성격 메모. 분류 프롬프트에 그대로 들어간다."""
    doc = load_channels()
    ch = _find_channel(doc, needle)
    ch["note"] = note
    save_channels(doc)
    print(f"[{ch['title']}] 메모 설정:\n  {note}")


def cmd_set_drop(needle: str, pattern: str):
    """채널별 잡음 패턴(정규식). 읽을 때만 적용되고 원문은 그대로 남는다."""
    doc = load_channels()
    ch = _find_channel(doc, needle)
    try:
        rx = re.compile(pattern)
    except re.error as e:
        sys.exit(f"정규식이 잘못됐습니다: {e}")

    ch.setdefault("drop", [])
    if pattern in ch["drop"]:
        sys.exit(f"[{ch['title']}] 에 이미 있는 패턴입니다.")
    ch["drop"].append(pattern)
    save_channels(doc)

    # 저장한 패턴이 실제로 뭘 얼마나 거르는지 바로 보여준다. 정규식을
    # 눈으로만 확인하면 너무 넓게 잡아 알짜까지 날리는 걸 알 수 없다.
    recent = [r for r in load_feed(48, drop_noise=False)
              if r.get("channel_id") == ch["id"]]
    hits = [r for r in recent if rx.search(headline(r.get("text", "")))]
    print(f"[{ch['title']}] 패턴 추가: {pattern}")
    print(f"최근 48시간 {len(recent)}건 중 {len(hits)}건이 걸립니다. (제목 줄 기준)")
    for r in hits[:8]:
        print(f"  - {r['text'].splitlines()[0][:64]}")
    if len(hits) > 8:
        print(f"  ... 외 {len(hits) - 8}건")
    print("\n너무 많이 걸리면 --unset-drop 으로 되돌리세요 (원문은 안 지워집니다).")


def cmd_set_docs(needle: str, onoff: str):
    """첨부 PDF 수집 on/off. 리포트 채널에만 켠다."""
    doc = load_channels()
    ch = _find_channel(doc, needle)
    if onoff.lower() not in ("on", "off"):
        sys.exit("on 또는 off 로 지정하세요.")
    ch["fetch_docs"] = onoff.lower() == "on"
    save_channels(doc)
    state = "받는다" if ch["fetch_docs"] else "안 받는다"
    print(f"[{ch['title']}] 첨부 PDF 리포트를 {state}.")
    if ch["fetch_docs"]:
        print("다음 --fetch 부터 적용됩니다. 이미 지나간 글의 첨부는 안 받습니다\n"
              "(워터마크가 지나갔기 때문). 과거분이 필요하면 last_id 를 낮추세요.")


def cmd_unset_drop(needle: str, pattern: Optional[str]):
    doc = load_channels()
    ch = _find_channel(doc, needle)
    if not ch.get("drop"):
        sys.exit(f"[{ch['title']}] 에 설정된 패턴이 없습니다.")
    if pattern is None:
        print(f"[{ch['title']}] 패턴 목록:")
        for p in ch["drop"]:
            print(f"  {p}")
        return
    if pattern not in ch["drop"]:
        sys.exit(f"그런 패턴이 없습니다. --unset-drop '{needle}' 만 쳐서 목록을 보세요.")
    ch["drop"].remove(pattern)
    save_channels(doc)
    print(f"[{ch['title']}] 패턴 제거: {pattern}")


def _msg_url(ch: dict, msg_id: int) -> str:
    if ch.get("username"):
        return f"https://t.me/{ch['username']}/{msg_id}"
    return f"https://t.me/c/{ch['id']}/{msg_id}"


async def cmd_fetch(dry_run: bool = False) -> list[dict]:
    """켜둔 채널의 새 메시지를 읽어 data/feed/YYYY-MM-DD.jsonl 에 적재."""
    _require_creds()
    doc = load_channels()
    channels = [c for c in doc.get("channels", []) if c.get("enabled")]
    if not channels:
        sys.exit("수집 대상 채널이 없습니다. --list 후 --enable 로 지정하세요.")

    now = datetime.now(KST)
    cutoff = now - timedelta(hours=FIRST_RUN_HOURS)

    client = _client()
    await client.start()

    collected: list[dict] = []
    for ch in channels:
        last_id = int(ch.get("last_id") or 0)
        got, newest, docs_got = 0, last_id, 0
        try:
            # min_id 를 쓰면 그 이후만 온다. 최초 실행(last_id=0)은 시간으로 자른다.
            kwargs = {"limit": MAX_PER_CHANNEL}
            if last_id:
                kwargs["min_id"] = last_id
            async for m in client.iter_messages(ch["id"], **kwargs):
                if not last_id and m.date and m.date.astimezone(KST) < cutoff:
                    break
                text = (m.text or "").strip()

                # 첨부는 본문 길이 검사보다 먼저 본다. 리포트 채널은 본문이
                # "[SK증권 반도체 한동희]" 한 줄이라 길이로 자르면 알맹이째 버린다.
                doc_info = None
                if ch.get("fetch_docs") and not dry_run:
                    doc_info = await _grab_document(client, m, ch)

                if len(text) < MIN_TEXT_LEN and not doc_info:
                    continue
                item = {
                    "channel_id": ch["id"],
                    "channel": ch["title"],
                    "msg_id": m.id,
                    "date": m.date.astimezone(KST).isoformat(timespec="minutes"),
                    "text": text,
                    "url": _msg_url(ch, m.id),
                    "views": getattr(m, "views", None) or 0,
                    "forwards": getattr(m, "forwards", None) or 0,
                }
                if doc_info:
                    item["doc"] = doc_info
                    docs_got += 1
                collected.append(item)
                got += 1
                newest = max(newest, m.id)
        except Exception as e:
            logger.error(f"[{ch['title']}] 수집 실패 — 건너뜀: {e}")
            continue
        logger.info(f"[{ch['title']}] {got}건"
                    + (f" (첨부 리포트 {docs_got}건)" if docs_got else ""))
        if not dry_run:
            ch["last_id"] = newest

    await client.disconnect()
    prune_docs()

    # 여러 채널이 같은 건을 옮겼는지 묶는다. 반복 횟수 자체가 중요도 신호다.
    group_duplicates(collected)
    collected.sort(key=lambda x: x["date"])

    if dry_run:
        print(f"[dry-run] {len(collected)}건 수집 (저장 안 함)")
        return collected

    FEED_DIR.mkdir(parents=True, exist_ok=True)
    out = FEED_DIR / f"{now:%Y-%m-%d}.jsonl"
    seen = set()
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                seen.add((r["channel_id"], r["msg_id"]))
            except Exception:
                continue
    fresh = [x for x in collected if (x["channel_id"], x["msg_id"]) not in seen]
    with out.open("a", encoding="utf-8") as f:
        for x in fresh:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")

    save_channels(doc)          # 워터마크 갱신
    logger.info(f"총 {len(fresh)}건 신규 -> {out.name}")
    print(f"{len(fresh)}건 저장 -> {out}")
    return fresh


# ============================================================
# 다이제스트에서 쓰는 읽기 API
# ============================================================

def headline(text: str) -> str:
    """메시지의 제목 줄. 채널별 잡음 패턴은 여기에만 걸린다.

    ★ 본문 전체에 걸면 주제가 섞인 긴 글이 통째로 날아간다. 실측(2026-09-07):
      암호화폐 패턴을 본문 전체에 걸었더니 "9월 6일 시장 아침 브리핑" 이
      함께 걸렸다 — 브리핑이 여러 시장을 훑다가 코인을 한 줄 언급했기 때문이다.
      속보 채널은 한 건에 헤드라인 하나라 제목 줄만 보면 정확히 갈린다.
    """
    for line in (text or "").splitlines():
        s = line.strip()
        if s:
            return s[:DROP_HEADLINE_CHARS]
    return ""


def _compiled_filters() -> tuple[list, dict]:
    """전역 잡음 패턴 + 채널별 추가 패턴을 컴파일해 돌려준다.

    채널별 패턴은 feed_channels.json 의 각 채널에 "drop": ["정규식", ...] 로 둔다.
    폭주 채널 하나 때문에 전역 패턴을 넓히면 다른 채널의 알짜까지 날아간다.
    """
    glob = [re.compile(p) for p in DROP_PATTERNS]
    per_channel = {}
    for c in load_channels().get("channels", []):
        pats = c.get("drop") or []
        if pats:
            per_channel[c["id"]] = [re.compile(p) for p in pats]
    return glob, per_channel


def is_noise(item: dict, glob: list, per_channel: dict) -> bool:
    text = item.get("text", "")
    for rx in glob:                       # 전역 패턴은 이미 ^ 로 묶여 있다
        if rx.search(text):
            return True
    head = headline(text)                 # 채널별 패턴은 제목 줄에만 건다
    for rx in per_channel.get(item.get("channel_id"), []):
        if rx.search(head):
            return True
    return False


def load_feed(hours: int = 24, now: Optional[datetime] = None,
              drop_noise: bool = True) -> list[dict]:
    """최근 N시간 피드를 시간순으로 반환. daily_digest 가 이걸 물어 쓴다.

    저장된 원문은 손대지 않고 여기서만 거른다 (DROP_PATTERNS 주석 참고).
    """
    now = now or datetime.now(KST)
    cutoff = now - timedelta(hours=hours)
    glob, per_channel = _compiled_filters() if drop_noise else ([], {})
    dropped = 0
    rows = []
    # 자정을 걸치면 어제 파일에도 걸리므로 이틀치를 훑는다
    for d in sorted({(now - timedelta(days=i)).strftime("%Y-%m-%d") for i in (0, 1)}):
        p = FEED_DIR / f"{d}.jsonl"
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                if datetime.fromisoformat(r["date"]) < cutoff:
                    continue
                if drop_noise and is_noise(r, glob, per_channel):
                    dropped += 1
                    continue
                # 첨부가 있으면 앞부분을 실어 보낸다. 리포트 채널은 본문이
                # 한 줄이라 이게 없으면 분류기가 판단할 근거가 없다.
                #
                # ★ 저장된 chars 를 믿지 말고 추출 파일을 직접 본다. 추출이
                #   나중에 고쳐지는 일이 있다 — 암호화 PDF 를 cryptography 설치
                #   후 다시 뽑은 경우, jsonl 의 항목은 chars=0 으로 굳어 있어
                #   멀쩡한 리포트를 영영 안 읽게 된다 (msg_id 중복이라 재저장도 안 된다).
                doc = r.get("doc") or {}
                if doc.get("id"):
                    head = read_doc_text(doc["id"], limit=1200)
                    if head:
                        r["doc_head"] = head
                        doc["chars"] = doc.get("chars") or len(head)
                rows.append(r)
            except Exception:
                continue
    rows.sort(key=lambda x: x["date"])
    if dropped:
        logger.info(f"정기 잡음 {dropped}건 제외 — 남은 {len(rows)}건")
    return rows


def cmd_stats(hours: int):
    """튜닝용 실측. 채널별 물량·길이·중복 묶임 상태와 표본을 뽑는다.

    상수(배치 크기·중복 임계값·잡음 패턴)를 감으로 정하면 반드시 틀린다.
    실제 채널이 어떤 문체로 무엇을 얼마나 쏟아내는지 보고 정하기 위한 출력이다.
    """
    raw = load_feed(hours, drop_noise=False)
    kept = load_feed(hours, drop_noise=True)
    kept_keys = {(r["channel_id"], r["msg_id"]) for r in kept}

    print(f"\n최근 {hours}시간 — 원문 {len(raw)}건, 잡음 제외 후 {len(kept)}건 "
          f"({len(raw) - len(kept)}건 걸러짐)\n")

    by_ch: dict = {}
    for r in raw:
        b = by_ch.setdefault(r["channel"], {"n": 0, "kept": 0, "lens": []})
        b["n"] += 1
        b["lens"].append(len(r.get("text", "")))
        if (r["channel_id"], r["msg_id"]) in kept_keys:
            b["kept"] += 1

    print(f"{'채널':<26} {'전체':>5} {'유효':>5} {'평균길이':>7} {'중간길이':>7}")
    for name, b in sorted(by_ch.items(), key=lambda x: -x[1]["n"]):
        lens = sorted(b["lens"])
        avg = sum(lens) // len(lens)
        med = lens[len(lens) // 2]
        print(f"{name[:24]:<26} {b['n']:>5} {b['kept']:>5} {avg:>7} {med:>7}")

    groups: dict = {}
    for r in kept:
        groups.setdefault(r.get("dupe_group") or r["msg_id"], []).append(r)
    multi = {k: v for k, v in groups.items()
             if len({x["channel"] for x in v}) > 1}
    print(f"\n여러 채널이 동시에 다룬 건: {len(multi)}묶음")
    for v in list(multi.values())[:5]:
        chans = ", ".join(sorted({x["channel"][:12] for x in v}))
        print(f"  [{chans}] {v[0]['text'].splitlines()[0][:60]}")

    print("\n=== 채널별 본문 표본 (긴 글 2개씩, 400자까지) ===")
    for name in by_ch:
        samples = sorted((r for r in kept if r["channel"] == name),
                         key=lambda x: -len(x.get("text", "")))[:2]
        for s in samples:
            body = re.sub(r"\s+", " ", s["text"])[:400]
            print(f"\n--- [{name[:20]}] {s['date'][5:16].replace('T', ' ')} "
                  f"({len(s['text'])}자)\n{body}")


def cmd_show(hours: int):
    rows = load_feed(hours)
    print(f"\n최근 {hours}시간 · {len(rows)}건\n")
    for r in rows:
        dupe = f"  [{r.get('dupe_count', 1)}개 채널]" if r.get("dupe_count", 1) > 1 else ""
        head = r["text"].splitlines()[0][:70]
        print(f"{r['date'][5:16]}  {r['channel'][:16]:<18} {head}{dupe}")


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description="텔레그램 구독 채널 수집기")
    ap.add_argument("--login", action="store_true", help="최초 1회 사용자 인증")
    ap.add_argument("--list", action="store_true", help="구독 채널 목록")
    ap.add_argument("--enable", metavar="N,N", help="수집할 채널 번호")
    ap.add_argument("--fetch", action="store_true", help="새 글 수집")
    ap.add_argument("--show", action="store_true", help="수집분 미리보기")
    ap.add_argument("--stats", action="store_true", help="튜닝용 실측 (채널별 물량·길이·중복·표본)")
    ap.add_argument("--set-note", nargs=2, metavar=("채널", "메모"),
                    help="채널 성격 메모 (분류 프롬프트에 들어간다)")
    ap.add_argument("--set-drop", nargs=2, metavar=("채널", "정규식"),
                    help="채널별 잡음 패턴 추가. 무엇이 걸리는지 바로 보여준다")
    ap.add_argument("--unset-drop", nargs="+", metavar="채널 [정규식]",
                    help="패턴 제거. 정규식을 빼면 현재 목록을 출력한다")
    ap.add_argument("--set-docs", nargs=2, metavar=("채널", "on|off"),
                    help="첨부 PDF 리포트 수집 여부")
    ap.add_argument("--hours", type=int, default=24, help="--show 조회 범위")
    ap.add_argument("--dry-run", action="store_true", help="--fetch 시 저장하지 않음")
    a = ap.parse_args()

    if a.login:
        asyncio.run(cmd_login())
    elif a.list:
        asyncio.run(cmd_list())
    elif a.enable:
        cmd_enable(a.enable)
    elif a.fetch:
        asyncio.run(cmd_fetch(dry_run=a.dry_run))
    elif a.show:
        cmd_show(a.hours)
    elif a.stats:
        cmd_stats(a.hours)
    elif a.set_note:
        cmd_set_note(*a.set_note)
    elif a.set_drop:
        cmd_set_drop(*a.set_drop)
    elif a.unset_drop:
        cmd_unset_drop(a.unset_drop[0],
                       a.unset_drop[1] if len(a.unset_drop) > 1 else None)
    elif a.set_docs:
        cmd_set_docs(*a.set_docs)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()

"""피드 라우터 — 텔레그램 원문을 포지션·테마별로 가른다.

telegram_feed 가 긁어온 하루치 원문은 수백 건이고 대부분은 내 포지션과 무관하다.
그걸 통째로 포지션 프롬프트마다 붙이면 토큰만 태우고 모델의 주의도 흩어진다.
그래서 검색 이전에 값싼 분류 호출을 한 번 넣어, 각 원문이 어느 포지션·테마에
걸리는지만 먼저 정한다. 여기서는 판정하지 않는다 — 판정은 뒤의 검색 단계 몫이다.

이 단계의 유일한 실패 모드는 '관련 있는 걸 버리는 것' 이다. 애매하면 남기게
지시한다. 반대로 과하게 남는 건 다음 단계가 걸러주므로 손해가 적다.
"""

import json
import logging
import re
from typing import Callable, Optional

logger = logging.getLogger(__name__)

# 한 번의 분류 호출에 넣을 원문 수. 너무 크게 잡으면 뒤쪽 항목을 대충 본다.
ROUTE_BATCH = 50
# 분류에 넘길 원문 길이. 첫 문단이면 무엇에 관한 글인지는 거의 다 드러난다.
SNIPPET_LEN = 400
# 포지션 하나에 붙일 원문 상한. 같은 뉴스가 채널마다 도배되는 걸 막는다.
MAX_ITEMS_PER_TARGET = 12
# 그 중 low(시황 코멘트·주가 이야기)로 채울 수 있는 몫. 사실 옆에 잡담이
# 나란히 놓이면 판정 프롬프트에서 주의가 그만큼 흩어진다.
MAX_LOW_PER_TARGET = 2
# 감시 목록 밖 '그래도 중요한 것' 상한. 여기가 넓어지면 다이제스트가 뉴스 요약이 된다.
MAX_NOTABLE = 6
# 하루에 다룰 '큰 건' 상한. 건당 영향 분석 호출이 하나씩 붙는다.
MAX_EVENTS = 3
# 분류 단계에서 첨부 리포트 본문을 얼마나 보여줄지. 여기서는 '어디로 보낼지' 만
# 정하면 되므로 앞부분(표지·요약)이면 충분하다. 정독은 뒤의 정리 단계 몫이다.
DOC_SNIPPET_LEN = 700
# 한 번 실행에서 정독할 리포트 수 상한. 리포트당 호출이 하나씩 붙는다.
MAX_DOC_DIGESTS = 8
# 정독 호출에 넣을 리포트 본문 길이. 실측(2026-09-07): DELL 실적발표 49쪽이
# 50,703자, HPE 34쪽이 48,355자였다. 4만자로 자르면 뒤쪽 가이던스가 날아간다.
DOC_READ_CHARS = 60000


def compact(item: dict, idx: int) -> str:
    """분류 프롬프트에 넣을 한 건의 압축 표현."""
    text = re.sub(r"\s+", " ", item.get("text", ""))[:SNIPPET_LEN]
    dupe = ""
    if item.get("dupe_count", 1) > 1:
        dupe = f" [{item['dupe_count']}개 채널 동시보도]"
    when = item["date"][5:16].replace("T", " ")
    line = f"[{idx}] ({when} · {item['channel']}){dupe} {text}"

    # 증권사 리포트 채널은 본문이 "[SK증권 반도체 한동희]" 한 줄이라 이것만 보면
    # 분류가 불가능하다. 첨부에서 뽑은 앞부분을 같이 줘야 어디로 보낼지 정해진다.
    doc = item.get("doc") or {}
    if doc.get("name"):
        head = re.sub(r"\s+", " ", item.get("doc_head", ""))[:DOC_SNIPPET_LEN]
        line += f"\n     [첨부: {doc['name']}] {head}" if head else \
                f"\n     [첨부: {doc['name']} — 본문 추출 실패]"
    return line


def build_prompt(batch: list[tuple[int, dict]], targets: list[dict],
                 channel_notes: Optional[dict] = None) -> str:
    target_lines = "\n".join(
        f"- {t['id']} · {t['label']} — {t['hint']}" for t in targets
    )
    items = "\n\n".join(compact(item, idx) for idx, item in batch)

    # 채널마다 성격이 완전히 다르다. 같은 헤드라인이라도 증권사 리포트를 옮기는
    # 채널에서 온 것과 지정학 속보 firehose 에서 온 것은 무게가 다르다.
    notes = channel_notes or {}
    seen = [item["channel"] for _, item in batch]
    note_lines = "\n".join(
        f"- {name}: {notes[name]}" for name in dict.fromkeys(seen) if notes.get(name)
    )
    channel_block = f"\n# 채널 성격 (분류 판단에 참고)\n{note_lines}\n" if note_lines else ""

    return f"""당신은 뉴스 원문을 감시 대상별로 분류하는 사서. 판정도 요약도 하지 않는다.
{channel_block}
# 감시 대상
{target_lines}
- portfolio — 개별 종목이 아니라 포트폴리오 전체에 걸리는 상위 변수
  (하이퍼스케일러 capex, 금리·환율, 전력·원자재 가격, 미국 통상·관세 정책 등)

# 분류할 원문
{items}

# 작업
각 원문이 위 대상 중 무엇에 관련되는지 판단해 JSON 만 출력.

판단 기준:
- 회사명이 직접 나오지 않아도 된다. 그 대상의 전방 수요·후방 공급·경쟁사·
  규제·전방산업 투자에 관한 것이면 관련 있는 것으로 본다.
- 하나의 원문이 여러 대상에 걸릴 수 있다. 걸리는 것을 모두 적는다.
- 애매하면 **남긴다**. 여기서 버린 건 뒤 단계에서 되살릴 수 없다.
- 어느 대상에도 안 걸리면 targets 를 빈 배열로 둔다 (그게 대부분이다).

- weight 는 이 원문이 얼마나 실질적인지다. 사실이 담긴 것일수록 높다.
  "high"  실적·수주·계약·증설·인허가·규제·소송·가격/물량 수치·경영권 변동
          **그리고 수요를 바꾸는 대형 사건** — 주요 AI 모델·제품 출시, 성능 도약,
          표준 채택, 대형 고객사의 도입 결정. 계약금액이 안 붙어도 high 다.
  "mid"   업계 동향·전방 투자계획·경쟁사 움직임·정책 논의
  "low"   시황 코멘트·주가 등락·수급 이야기·목표주가·추측성 전망·홍보

★ 사건 자체와 그 사건에 대한 코멘트를 구분할 것. 큰 사건을 다룬 글이면
  글쓴이가 개인 감상으로 썼더라도 사건의 무게로 매긴다. 실측 사례: GPT-6 출시를
  다룬 글이 "계약금액이 없다" 는 이유로 전부 low 로 떨어져, 메모리 수요를 뒤흔드는
  사건이 시황 잡담과 같은 칸에 묶였다.

그리고 **어느 대상에도 안 걸리지만 그 자체로 중요한 것**은 notable 에 따로 담는다.
지금 감시 목록에 없다는 이유로 큰 변화를 통째로 놓치는 걸 막는 통로다.
해당하는 것: 새로 형성되는 산업 흐름, 대형 정책·규제 변화, 거시 충격,
감시 목록 밖 기업의 판을 바꾸는 발표. 시황·수급·주가 이야기는 여기 담지 않는다.
대부분의 날은 비어 있는 게 정상이다. 최대 5건.

{{
  "routed": [
    {{"idx": 0, "targets": ["ess-foil"], "weight": "high", "why": "관련 이유 한 줄"}}
  ],
  "notable": [
    {{"idx": 7, "why": "감시 목록 밖이지만 중요한 이유 한 줄"}}
  ]
}}

JSON 외 다른 텍스트 출력 금지."""


def _targets_from(positions_doc: dict) -> list[dict]:
    """positions.json 에서 분류 대상 목록을 만든다.

    hint 는 모델이 '이 원문이 여기 걸리나' 를 판단할 근거다. 라벨만 주면
    회사명이 직접 안 나온 산업 뉴스를 통째로 놓치므로 티커·키워드·경쟁사까지 붙인다.
    """
    targets = []
    for p in positions_doc.get("positions", []):
        if p.get("status") not in ("holding", "watching"):
            continue
        w = p.get("watch", {})
        bits = [
            ", ".join(p.get("tickers", [])),
            ", ".join(w.get("queries", [])[:8]),
            "경쟁사: " + ", ".join(w.get("peers", [])[:6]) if w.get("peers") else "",
        ]
        targets.append({
            "id": p["id"],
            "label": p.get("label", p["id"]),
            "hint": " / ".join(b for b in bits if b) or "(키워드 없음)",
        })
    for t in positions_doc.get("themes", []):
        w = t.get("watch", {}) if isinstance(t, dict) else {}
        targets.append({
            "id": t.get("id"),
            "label": t.get("label", t.get("id")),
            "hint": " / ".join(w.get("queries", [])[:8]) or "(테마)",
        })
    return [t for t in targets if t.get("id")]


def route(
    feed: list[dict],
    positions_doc: dict,
    call: Callable[[str], str],
    channel_notes: Optional[dict] = None,
) -> dict:
    """피드를 대상별로 가른다.

    call 은 프롬프트를 받아 응답 텍스트를 돌려주는 함수 (검색 없이 호출할 것).
    실패한 배치는 통째로 버리지 않고 '분류 실패' 로 남겨 호출자가 알 수 있게 한다.

    반환: {"by_target": {id: [item,...]}, "unrouted": n, "failed_batches": n}
    """
    if not feed:
        return {"by_target": {}, "notable": [], "unrouted": 0, "failed_batches": 0}

    targets = _targets_from(positions_doc)
    if not targets:
        logger.warning("분류 대상이 없다 — positions.json 확인 필요")
        return {"by_target": {}, "notable": [], "unrouted": len(feed), "failed_batches": 0}

    valid = {t["id"] for t in targets} | {"portfolio"}
    by_target: dict[str, list[dict]] = {}
    routed_idx: set[int] = set()
    notable: list[dict] = []
    failed = 0

    indexed = list(enumerate(feed))
    for start in range(0, len(indexed), ROUTE_BATCH):
        batch = indexed[start:start + ROUTE_BATCH]
        try:
            text = call(build_prompt(batch, targets, channel_notes))
            data = _extract_json(text)
            if data is None:
                raise ValueError("JSON 파싱 실패")
        except Exception as e:
            failed += 1
            logger.error(f"피드 분류 배치 {start // ROUTE_BATCH + 1} 실패: {e}")
            continue

        for r in data.get("routed") or []:
            try:
                idx = int(r.get("idx"))
            except (TypeError, ValueError):
                continue
            if not (0 <= idx < len(feed)):
                continue
            tids = [t for t in (r.get("targets") or []) if t in valid]
            if not tids:
                continue
            routed_idx.add(idx)
            for tid in tids:
                item = dict(feed[idx])
                item["route_weight"] = r.get("weight", "mid")
                item["route_why"] = r.get("why", "")
                by_target.setdefault(tid, []).append(item)

        for r in data.get("notable") or []:
            try:
                idx = int(r.get("idx"))
            except (TypeError, ValueError):
                continue
            if not (0 <= idx < len(feed)):
                continue
            item = dict(feed[idx])
            item["route_why"] = r.get("why", "")
            notable.append(item)

    # 대상별로 자른다. 같은 뉴스가 채널마다 도배되면 위쪽만 남는다.
    #
    # ★ low 는 따로 상한을 둔다. 실측(2026-09-07): memory-storage 에 12건이
    #   붙었는데 그 중 6건이 low 였다 — "이거의 80-90% 성능을 1/3가격에 제공해줄
    #   업체만 기다리는 중" 같은 한 줄 채팅이 SK증권 리포트와 나란히 판정
    #   프롬프트에 들어간다. 분류는 옳았는데 상한이 안 걸러줬다.
    #   시황 코멘트가 사실 옆에 놓이면 모델의 주의가 그만큼 흩어진다.
    order = {"high": 0, "mid": 1, "low": 2}
    for tid, items in by_target.items():
        seen_groups: set = set()
        picked, lows = [], 0
        for it in sorted(items, key=lambda x: (order.get(x.get("route_weight"), 1),
                                               x["date"])):
            g = it.get("dupe_group")
            if g and g in seen_groups:
                continue
            if it.get("route_weight") == "low":
                if lows >= MAX_LOW_PER_TARGET:
                    continue
                lows += 1
            if g:
                seen_groups.add(g)
            picked.append(it)
            if len(picked) >= MAX_ITEMS_PER_TARGET:
                break
        by_target[tid] = picked

    # notable 도 채널 도배분을 접는다. 배치가 갈리면 같은 건이 여러 번 올라온다.
    seen_groups = set()
    deduped_notable = []
    for it in notable:
        g = it.get("dupe_group")
        if g and g in seen_groups:
            continue
        if g:
            seen_groups.add(g)
        deduped_notable.append(it)

    return {
        "by_target": by_target,
        "notable": deduped_notable[:MAX_NOTABLE],
        "unrouted": len(feed) - len(routed_idx),
        "failed_batches": failed,
    }


def build_event_prompt(feed: list[dict]) -> str:
    """오늘 피드에서 '큰 건' 을 찾는 프롬프트. 제목 줄만 훑는다.

    분류(route)와 따로 도는 이유: 분류는 50건씩 배치로 쪼개는데, 큰 사건은
    여러 배치에 흩어져 나타난다. 배치 안에서만 보면 "여러 글이 같은 걸 말하고
    있다" 는 신호 자체가 안 보인다. 여기서는 전체를 한 번에 훑는다.
    """
    lines = []
    for i, it in enumerate(feed):
        head = re.sub(r"\s+", " ", it.get("text", ""))[:110]
        lines.append(f"[{i}] ({it['channel'][:12]}) {head}")
    body = "\n".join(lines)

    return f"""당신은 하루치 뉴스 피드에서 **오늘의 큰 건**을 골라내는 분석가.

# 오늘 들어온 글 (제목 줄)
{body}

# 작업
여러 글이 반복해서 다루고 있는 사건, 또는 한 건뿐이어도 산업의 수요·공급·경쟁
구도를 바꿀 사건을 골라 JSON 만 출력.

무엇이 '큰 건' 인가:
- 주요 AI 모델·제품의 출시나 성능 도약 (수요를 통째로 움직인다)
- 대형 정책·규제 확정, 관세·수출통제 변경
- 주요 기업의 대규모 투자·증설·인수 발표
- 공급망 충격 (사고·분쟁·제재·병목)
- 가격의 추세 전환 (원자재·메모리·운임 등)

무엇이 아닌가:
- 시황·수급·주가 등락, 목표주가, 개인 감상만 있고 사건이 없는 글
- 이미 몇 주 전에 알려져 오늘 새로울 게 없는 사안

★ 여러 글이 같은 사건을 다루면 **하나의 event 로 묶고** idxs 에 전부 넣을 것.
   글쓴이가 개인 코멘트로 썼더라도 다루는 사건이 크면 큰 건이다.
★ 최대 3건. 오늘 큰 건이 없으면 빈 배열이 정상이다. 억지로 채우지 말 것.

{{
  "events": [
    {{
      "label": "사건을 한 줄로 (예: OpenAI GPT-6 Astra 공개)",
      "idxs": [12, 45, 78],
      "what": "무슨 일이 있었는지 2~3문장. 확인된 사실만",
      "why_big": "왜 큰 건인지 한 줄"
    }}
  ]
}}

JSON 외 다른 텍스트 출력 금지."""


def detect_events(feed: list[dict], call: Callable[[str], str]) -> list[dict]:
    """오늘의 큰 건을 찾는다. 실패하면 빈 목록 (다이제스트는 계속 돈다)."""
    if not feed:
        return []
    try:
        data = _extract_json(call(build_event_prompt(feed)))
        if data is None:
            raise ValueError("JSON 파싱 실패")
    except Exception as e:
        logger.error(f"큰 건 탐지 실패: {e}")
        return []

    events = []
    for e in (data.get("events") or [])[:MAX_EVENTS]:
        idxs = [i for i in (e.get("idxs") or []) if isinstance(i, int) and 0 <= i < len(feed)]
        if not e.get("label"):
            continue
        events.append({
            "label": e["label"],
            "what": e.get("what", ""),
            "why_big": e.get("why_big", ""),
            "sources": [{"channel": feed[i]["channel"], "url": feed[i].get("url", ""),
                         "date": feed[i]["date"]} for i in idxs[:6]],
            "mentions": len(idxs),
        })
    return events


def build_impact_prompt(event: dict, positions_doc: dict) -> str:
    """사건 하나가 보유 포지션 각각에 어떻게 닿는지 묻는 프롬프트.

    기존 레이어들은 "내 kill_signal 에 걸리나" 만 묻는다. 큰 사건이 터졌을 때
    "11개 포지션 각각에 어떤 경로로 얼마나 닿나" 를 묻는 자리가 없었다.
    그래서 GPT-6 출시 같은 건이 주가 설명 각주로만 남았다.
    """
    blocks = []
    for p in positions_doc.get("positions", []):
        if p.get("status") not in ("holding", "watching"):
            continue
        thesis = (p.get("thesis") or ["(thesis 미작성)"])[0]
        blocks.append(
            f"- {p['id']} · {p.get('label')} ({', '.join(p.get('tickers', []))})\n"
            f"  보유 근거: {thesis}"
        )
    positions = "\n".join(blocks)
    srcs = "\n".join(f"  - {s['channel']} {s['date'][:16].replace('T', ' ')} {s['url']}"
                     for s in event.get("sources", []))

    return f"""당신은 하나의 사건이 특정 포트폴리오에 어떻게 닿는지 따지는 분석가.

# 사건
{event['label']}
{event.get('what', '')}
(구독 채널에서 {event.get('mentions', 0)}건 언급)
{srcs}

# 내 보유 포지션
{positions}

# 작업
web_search 로 이 사건의 사실관계를 먼저 확인한 뒤, 아래 JSON 만 출력.

★ 먼저 사실을 확인할 것. 채널 글은 전언이라 과장·오보가 섞인다. 발표 주체의
  공식 자료나 1차 보도로 무엇이 실제로 발표됐는지 확인하고, 확인된 것만 쓴다.
  확인이 안 되면 confirmed=false 로 두고 impacts 를 비울 것.

★ 전달 경로를 구체적으로 쓸 것. "AI 수요 증가로 수혜" 같은 문장은 쓸모가 없다.
  무엇이 늘어서 → 어디를 거쳐 → 이 회사의 무엇이 바뀌는지를 쓴다.
  예: "추론 토큰 수요 증가 → 하이퍼스케일러 eSSD 발주 증가 → 컨트롤러 물량 증가"

★ 강도는 정직하게 매길 것. 대부분의 포지션에는 '없음' 이거나 '간접' 이 정상이다.
  전부 수혜라고 쓰면 아무 정보도 주지 못한다.
  "직접"  이 회사의 매출·원가·수주에 이번 분기 안에 반영될 경로가 있다
  "간접"  전방 수요를 거쳐 몇 분기 뒤에 닿는다
  "없음"  연결 경로가 없다 (이렇게 쓰는 걸 두려워하지 말 것)

★ 반대 방향도 볼 것. 같은 사건이 어떤 포지션에는 역풍일 수 있다
  (예: 자체 칩 내재화 가속 → 외부 컨트롤러 벤더에 역풍).

★ 시차와 확인 지표를 쓸 것. 언제쯤 숫자로 나타나는지, 무엇을 보면 확인되는지.

{{
  "confirmed": true,
  "fact_check": "1차 확인 결과 실제로 무엇이 발표됐는지 2~3문장",
  "impacts": [
    {{
      "position_id": "ssd-controller",
      "direction": "순풍|역풍|중립",
      "strength": "직접|간접|없음",
      "path": "전달 경로를 화살표로",
      "lag": "언제쯤 숫자로 나타나는지",
      "watch": "무엇을 보면 확인되는지"
    }}
  ],
  "sources": [
    {{"url": "출처 URL", "outlet": "매체명", "date": "YYYY-MM-DD", "tier": "S1|S2|S3"}}
  ]
}}

JSON 외 다른 텍스트 출력 금지."""


def build_doc_prompt(item: dict, targets: list[dict], body: str) -> str:
    """첨부 리포트 정독 프롬프트.

    범용 요약을 시키면 안 된다 — "반도체 업황이 좋다" 같은 글이 나오고 그건
    이미 아는 얘기다. 내 포지션에 닿는 대목만, 숫자와 함께 뽑아내게 한다.
    """
    target_lines = "\n".join(
        f"- {t['id']} · {t['label']} — {t['hint']}" for t in targets
    )
    doc = item.get("doc") or {}
    return f"""당신은 증권사 리포트에서 **특정 포지션에 닿는 대목만** 뽑아내는 분석가.

# 리포트
{doc.get('name', '(파일명 없음)')} — {item['channel']} {item['date'][:16].replace('T', ' ')}
원문 링크: {item.get('url', '-')}

# 내가 보유·감시 중인 대상
{target_lines}

# 리포트 본문 (PDF 추출본. 표·그림은 깨져 있을 수 있다)
{body}

# 작업
아래 JSON 만 출력.

★ 범용 요약을 하지 말 것. "업황이 개선되고 있다" 같은 문장은 쓸모가 없다.
   위 감시 대상에 닿는 대목만, **숫자와 근거를 붙여** 뽑는다.
★ 리포트에 그 대상 얘기가 없으면 findings 를 빈 배열로 둔다. 그게 정상이다.
   억지로 연결하지 말 것 — 없는 연결을 만들면 판정 전체가 오염된다.
★ 목표주가·투자의견·투자의견 변경은 담지 말 것. 사실이 아니라 남의 의견이다.
   단, 그 근거로 제시된 **실적 추정치·출하량·가격·capex 숫자**는 담을 것.
★ 추출본이 깨져 읽을 수 없으면 readable=false 로 정직하게 보고할 것.
   내용 없이 지어내지 말 것.

{{
  "readable": true,
  "findings": [
    {{
      "target": "위 목록의 id 중 하나",
      "point": "이 리포트가 그 대상에 대해 말하는 것 2~3문장. 숫자 포함",
      "numbers": {{"지표명": "값"}},
      "page_hint": "본문 어디쯤인지 (알 수 있으면)"
    }}
  ],
  "one_line": "이 리포트 전체를 한 줄로 (감시 대상과 무관해도 무슨 리포트인지)"
}}

JSON 외 다른 텍스트 출력 금지."""


def read_documents(
    routed: dict,
    positions_doc: dict,
    call: Callable[[str], str],
    load_text: Callable[[int], str],
) -> int:
    """분류 결과에서 첨부 리포트를 골라 정독하고 결과를 항목에 붙인다.

    분류 **뒤에** 도는 이유: 어느 포지션에도 안 걸린 리포트를 정독하는 건 낭비다.
    이미 대상에 배정된 것만 편다. 정독 결과는 같은 doc id 를 가진 모든 사본에
    붙여 같은 리포트를 두 번 읽지 않는다.

    반환: 정독한 리포트 수.
    """
    targets = _targets_from(positions_doc)

    # doc id -> 그 리포트를 물고 있는 모든 항목 (여러 대상에 배정됐을 수 있다)
    by_doc: dict[int, list[dict]] = {}
    for items in routed.get("by_target", {}).values():
        for it in items:
            doc = it.get("doc") or {}
            if doc.get("id") and doc.get("chars"):
                by_doc.setdefault(doc["id"], []).append(it)
    for it in routed.get("notable", []):
        doc = it.get("doc") or {}
        if doc.get("id") and doc.get("chars"):
            by_doc.setdefault(doc["id"], []).append(it)

    if not by_doc:
        return 0

    # 여러 대상에 걸린 리포트가 더 중요하다고 보고 먼저 읽는다.
    order = sorted(by_doc.items(), key=lambda kv: -len(kv[1]))
    done = 0
    for doc_id, copies in order[:MAX_DOC_DIGESTS]:
        body = (load_text(doc_id) or "")[:DOC_READ_CHARS]
        if not body.strip():
            continue
        try:
            data = _extract_json(call(build_doc_prompt(copies[0], targets, body)))
            if data is None:
                raise ValueError("JSON 파싱 실패")
        except Exception as e:
            logger.error(f"리포트 정독 실패 (doc {doc_id}): {e}")
            continue

        if not data.get("readable", True):
            logger.info(f"리포트 추출본을 못 읽음 (doc {doc_id}) — 건너뜀")
            continue
        for it in copies:
            it["doc_digest"] = data
        done += 1

    if len(by_doc) > MAX_DOC_DIGESTS:
        logger.warning(
            f"첨부 리포트 {len(by_doc)}건 중 {MAX_DOC_DIGESTS}건만 정독 "
            f"(상한). 나머지는 첨부 앞부분만 쓴다"
        )
    return done


def _extract_json(text: str) -> Optional[dict]:
    if not text:
        return None
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    candidate = fence.group(1) if fence else text
    start, end = candidate.find("{"), candidate.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        return json.loads(candidate[start:end + 1])
    except Exception:
        return None


def format_block(items: list[dict], target_id: Optional[str] = None) -> str:
    """검색 프롬프트에 붙일 원문 블록.

    출처 URL(t.me 링크)까지 같이 준다. 모델이 '이 건의 1차 출처를 찾아라' 를
    수행하려면 원문 그대로가 필요하고, 다이제스트에서 역추적도 가능해야 한다.
    """
    if not items:
        return "(오늘 피드에 관련 원문 없음)"
    out = []
    for i, it in enumerate(items, 1):
        text = re.sub(r"\s+", " ", it.get("text", ""))[:700]
        dupe = (f" · {it['dupe_count']}개 채널 동시보도"
                if it.get("dupe_count", 1) > 1 else "")
        when = it["date"][5:16].replace("T", " ")
        block = [
            f"F{i}. [{when} · {it['channel']}{dupe}] {text}",
            f"    원문: {it.get('url', '-')}",
        ]

        # 첨부 리포트를 정독했으면 그 결과를 붙인다. 리포트는 채널 글보다
        # 근거가 두껍다 — 증권사가 이름을 걸고 낸 추정치와 숫자다.
        digest = it.get("doc_digest") or {}
        doc = it.get("doc") or {}
        if digest:
            # 한 리포트가 여러 대상을 다루므로 이 대상 얘기만 남긴다. 변압기
            # 프롬프트에 eSSD 대목이 섞이면 그만큼 모델의 주의가 흩어진다.
            found = digest.get("findings") or []
            if target_id:
                mine = [f for f in found if f.get("target") == target_id]
                found = mine or found
            out_lines = [f"    ▣ 첨부 리포트: {doc.get('name', '')}"]
            if digest.get("one_line"):
                out_lines.append(f"      개요: {digest['one_line']}")
            for f in found[:4]:
                out_lines.append(f"      · {f.get('point', '')}")
                nums = f.get("numbers") or {}
                if isinstance(nums, dict) and nums:
                    out_lines.append(
                        "        수치: " + " · ".join(f"{k} = {v}" for k, v in nums.items()))
            block += out_lines
        elif doc.get("name"):
            block.append(f"    ▣ 첨부 리포트: {doc['name']} (정독하지 않음 — 제목만)")

        out.append("\n".join(block))
    return "\n".join(out)

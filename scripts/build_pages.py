"""포지션·테마 페이지 생성기.

positions.json + position_state.json + theme_state.json + events/ + market.json
을 읽어 markdown 을 찍는다. 검색도 LLM 호출도 네트워크도 없다 — 순수 렌더링.

★ 생성물은 손으로 고치지 말 것. 진실은 data/ 에 있고 페이지는 그 투영이다.
   thesis 수정은 봇의 /수정 으로만.

신선도를 1급 정보로 취급한다. 대시보드는 그냥 보면 현재 상태처럼 읽히는데
로테이션 때문에 대부분의 페이지는 며칠 묵어 있다. 10일 전 정보를 최신인 양
보여주는 페이지는 "오늘 점검 안 함"이라고 말해주는 다이제스트보다 나쁘다.

실행: python3 scripts/build_pages.py [--out pages]
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import events_log
import positions_view as pv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DEFAULT = PROJECT_ROOT / "pages"
MARKET_PATH = PROJECT_ROOT / "data" / "market.json"

LEVEL_MARK = {"RED": "🔴", "YELLOW": "🟡", "WHITE": "⚪"}
DIR_MARK = {"순풍": "↗", "역풍": "↘", "중립": "→", "불명": "?"}
STALE_WARN_DAYS = 7
TIMELINE_LIMIT = 40


# ============================================================
# 로딩 · 포맷 헬퍼
# ============================================================

def load_market() -> dict:
    return pv._load(MARKET_PATH, {"prices": {}}).get("prices", {})


def fresh(last: Optional[str], today: str) -> str:
    """신선도 문구. 오래되면 눈에 띄게."""
    if not last:
        return "점검 기록 없음"
    n = pv.days_since(last, today)
    if n is None:
        return f"확인 {last}"
    if n == 0:
        return f"확인 {last} (오늘)"
    tag = f"확인 {last} ({n}일 전)"
    return f"**{tag}**" if n >= STALE_WARN_DAYS else tag


def money(ticker: str, v) -> str:
    if v in (None, ""):
        return "—"
    krw = ticker.isdigit() and len(ticker) == 6
    try:
        v = float(v)
    except Exception:
        return str(v)
    return f"{v:,.0f}원" if krw else f"${v:,.2f}"


def pct(v: Optional[float], sign=True) -> str:
    if v is None:
        return "—"
    s = "+" if (sign and v >= 0) else ""
    return f"{s}{v:.1f}%"


def cap(ticker: str, v) -> str:
    """시가총액 축약. 한국은 조/억, 미국은 B/M."""
    if not v:
        return "—"
    try:
        v = float(v)
    except Exception:
        return "—"
    if ticker.isdigit() and len(ticker) == 6:
        if v >= 1e12:
            return f"{v/1e12:.1f}조"
        return f"{v/1e8:,.0f}억"
    if v >= 1e9:
        return f"${v/1e9:.1f}B"
    return f"${v/1e6:,.0f}M"


def ret_pct(price, avg) -> Optional[float]:
    try:
        price, avg = float(price), float(avg)
        if avg <= 0:
            return None
        return (price - avg) / avg * 100
    except Exception:
        return None


def company_of(pos: dict, ticker: str) -> str:
    return (pos.get("companies") or {}).get(ticker, ticker)


def label_base(label: str) -> str:
    """포지션명에서 회사명 괄호를 뗀다.

    label 이 "SSD 컨트롤러 (파두)" 처럼 회사명을 이미 품고 있어서, 그대로 쓰면
    "파두 (SSD 컨트롤러 (파두))" 가 된다. 회사명은 앞에서 이미 말했으므로 뗀다.
    """
    return re.sub(r"\s*\([^()]*\)\s*$", "", label or "").strip() or label


def title_of(pos: dict) -> str:
    """회사명이 주체, 포지션명은 부제."""
    names = [company_of(pos, t) for t in pos.get("tickers", [])]
    base = label_base(pos.get("label", ""))
    head = " · ".join(names) if names else base
    return f"{head} ({base})" if base and head != base else head


def slug(pid: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "-", pid)


# ============================================================
# 포지션 페이지
# ============================================================

def render_position(pos, state, theme_state, doc, market, today) -> str:
    pid = pos["id"]
    entry = (state.get("positions") or {}).get(pid, {})
    events = events_log.load_events(pid)
    aliases = pv._load(pv.AREA_ALIASES_PATH, {"aliases": {}}).get("aliases", {})
    themes = pv.themes_for(doc, pid)

    L = [f"# {title_of(pos)}", ""]

    areas = ", ".join(aliases.get(a, {}).get("title", a) for a in (pos.get("areas") or [])) or "미지정"
    tl = ", ".join(t.get("label", t["id"]) for t in themes) or "미연결"
    L += [
        f"**{pv.STATUS_LABEL.get(pos.get('status'), pos.get('status'))}** · "
        f"{fresh(entry.get('last_checked'), today)}",
        "",
        f"영역 {areas} · 테마 {tl}",
        "",
    ]

    # ---- 시세 ----
    L += ["## 시세", "", "| 종목 | 종가 | 등락 | 시가총액 | 평단 | 평단 대비 |",
          "|---|---:|---:|---:|---:|---:|"]
    for t in pos.get("tickers", []):
        m = market.get(t, {})
        avg = (pos.get("avg_cost") or {}).get(t)
        r = ret_pct(m.get("price"), avg)
        L.append(
            f"| {company_of(pos, t)} <br><small>`{t}`</small> "
            f"| {money(t, m.get('price'))} "
            f"| {pct(m.get('change_pct'))} "
            f"| {cap(t, m.get('market_cap'))} "
            f"| {money(t, avg) if avg else '_미입력_'} "
            f"| {'**'+pct(r)+'**' if r is not None else '—'} |"
        )
    L += ["", "<small>평단은 선택 입력 — 봇에서 `/평단 <종목> <가격>`</small>", ""]

    # ---- 보유 근거 / 조건 ----
    def block(title, items, prefix, extra=""):
        L.append(f"## {title}")
        L.append("")
        if not items:
            L.append(f"_미작성_{extra}")
        else:
            for i, it in enumerate(items, 1):
                L.append(f"{i}. `{prefix}{i}` {it}")
        L.append("")

    block("보유 근거", pos.get("thesis"), "T")
    block("매도 검토 조건", pos.get("kill_signals"), "K",
          " — 이게 없으면 이 포지션은 영원히 🔴 가 뜨지 않습니다")
    block("추가 검토 조건", pos.get("add_signals"), "A")

    # ---- 반복 관측 ----
    flags = [f for f in (entry.get("open_flags") or []) if f.get("count", 1) >= 2]
    if flags:
        L += ["## 반복 관측", "", "| 신호 | 등급 | 누적 | 최초 | 최근 |", "|---|---|---:|---|---|"]
        for f in flags:
            L.append(f"| {f.get('signal','')} | {LEVEL_MARK.get(f.get('level'),'')} "
                     f"{f.get('level','')} | {f.get('count')}회 | "
                     f"{f.get('first_seen','-')} | {f.get('last_seen','-')} |")
        L.append("")

    # ---- 타임라인 ----
    L += ["## 최근 신호 · 뉴스", ""]
    if not events:
        L += ["_아직 기록이 없습니다. 이벤트 로그는 2026-08-17 실행부터 쌓입니다._", ""]
    else:
        for ev in events[:TIMELINE_LIMIT]:
            L.append(render_event(ev))
        if len(events) > TIMELINE_LIMIT:
            L.append(f"<small>… 외 {len(events)-TIMELINE_LIMIT}건</small>")
        L.append("")

    # ---- 추적 지표 ----
    obs = entry.get("observations") or {}
    L += ["## 추적 지표", ""]
    if not obs:
        L += ["_관측값 없음_", ""]
    else:
        L += ["| 지표 | 최근 | 관측일 | 직전 |", "|---|---|---|---|"]
        for k, series in obs.items():
            if not series:
                continue
            cur = series[-1]
            prev = series[-2]["value"] if len(series) > 1 else "—"
            L.append(f"| {k} | **{cur.get('value')}** | {cur.get('date')} | {prev} |")
        L.append("")

    # ---- 공시 · 재무 (미연결) ----
    L += ["## 공시 · 재무", "",
          "!!! note \"아직 연결되지 않았습니다\"",
          "    DART·SEC 수집기를 붙이면 공시와 분기 실적이 여기 쌓입니다.",
          ""]

    # ---- 감시 / 무시 / 메모 ----
    watch = pos.get("watch") or {}
    L += ["## 감시", "",
          f"- **경쟁사** {', '.join(watch.get('peers', [])) or '(없음)'}",
          f"- **지표** {', '.join(watch.get('indicators', [])) or '(없음)'}", ""]
    if pos.get("ignore"):
        L += ["## 무시 (보고 안 함)", ""] + [f"- {x}" for x in pos["ignore"]] + [""]
    if pos.get("note"):
        L += ["## 메모", "", pos["note"], ""]

    L += ["---", "",
          f"<small>이 페이지는 생성물입니다. 직접 고치지 마세요 — "
          f"판정 기준 변경은 봇의 `/수정`. 마지막 생성 {today}</small>", ""]
    return "\n".join(L)


def render_event(ev: dict) -> str:
    layer = ev.get("layer")
    date = ev.get("last_seen") or ev.get("date", "")
    bits = []
    if layer == "theme":
        d = ev.get("direction", "")
        bits.append(f"🔷 흐름 {DIR_MARK.get(d,'')} {d}")
        if ev.get("theme_label"):
            bits.append(ev["theme_label"])
    elif layer == "sweep":
        bits.append("📰 소식")
    elif layer == "layer0":
        bits.append("Layer 0")
    else:
        lv = ev.get("level", "")
        bits.append(f"{LEVEL_MARK.get(lv,'')} {lv}".strip())
    if ev.get("refs"):
        bits.append(" ".join(f"`{r}`" for r in ev["refs"]))
    if ev.get("count", 1) >= 2:
        bits.append(f"{ev['count']}회째 (최초 {ev.get('first_seen')})")

    head = f"**{date}** · " + " · ".join(b for b in bits if b)
    body = [head, ""]
    if ev.get("headline"):
        body.append(f"**{ev['headline']}** — {ev.get('summary','')}")
    else:
        body.append(ev.get("summary", ""))
    if ev.get("quant"):
        body.append("")
        body.append("　정량 " + " · ".join(f"{k} = {v}" for k, v in ev["quant"].items()))
    for q in (ev.get("qual") or [])[:2]:
        body.append("")
        body.append(f"　맥락 {q}")
    if ev.get("signal"):
        body.append("")
        body.append(f"　↳ 해당 조건 「{ev['signal']}」")
    srcs = ev.get("sources") or []
    if srcs:
        links = ", ".join(
            f"[{s.get('outlet') or '출처'}]({s['url']})" if s.get("url")
            else (s.get("outlet") or "출처")
            for s in srcs[:4]
        )
        body.append("")
        body.append(f"　<small>근거 {links}</small>")
    return "\n".join(body) + "\n"


# ============================================================
# 테마 페이지
# ============================================================

def render_theme(theme, theme_state, doc, state, today) -> str:
    tid = theme["id"]
    entry = (theme_state.get("themes") or {}).get(tid, {})
    by_id = {p["id"]: p for p in doc.get("positions", [])}
    aliases = pv._load(pv.AREA_ALIASES_PATH, {"aliases": {}}).get("aliases", {})

    L = [f"# {theme.get('label', tid)}", "",
         f"{'핵심 테마 · 3일 주기' if theme.get('core') else '7일 주기'} · "
         f"{fresh(entry.get('last_checked'), today)}", "",
         "!!! info \"판정하지 않는 레이어\"",
         "    포지션은 \"내 근거가 깨졌나\"를 묻고, 테마는 \"상위 변화가 어디로 얼마나 "
         "움직이나\"를 묻습니다. 개별 점검은 하루 3종목뿐이라 여러 포지션을 동시에 "
         "흔드는 변화가 새어나가는데, 이 레이어가 그 구멍을 메웁니다.", ""]

    L += ["## 추적 대상 변화", ""]
    for i, w in enumerate(theme.get("watch_shifts", []), 1):
        L.append(f"{i}. `W{i}` {w}")
    L.append("")

    shifts = sorted((entry.get("shifts") or {}).values(),
                    key=lambda r: (0 if r.get("thesis_review") else 1,
                                   -r.get("count", 1), r.get("last_seen", "")))
    L += ["## 흐름", ""]
    if not shifts:
        L += ["_아직 관측이 없습니다._", ""]
    else:
        for r in shifts:
            star = " ★ **thesis 갱신 후보**" if r.get("thesis_review") else ""
            d = r.get("direction", "불명")
            names = ", ".join(
                title_of(by_id[p]) for p in (r.get("affects") or []) if p in by_id) or "—"
            L += [f"**{r.get('headline') or r.get('shift','')}** "
                  f"{DIR_MARK.get(d,'')} {d} · {r.get('count',1)}회"
                  f" (최초 {r.get('first_seen','-')}, 최근 {r.get('last_seen','-')}){star}",
                  "", r.get("summary", ""), "", f"　↳ 닿는 포지션 {names}", ""]

    L += ["## 닿는 포지션", ""]
    for pidx in theme.get("affects", []):
        p = by_id.get(pidx)
        if not p:
            continue
        e = (state.get("positions") or {}).get(pidx, {})
        L.append(f"- [{title_of(p)}](../positions/{slug(pidx)}.md) — "
                 f"{fresh(e.get('last_checked'), today)}")
    L.append("")

    if theme.get("key_vendors"):
        L += ["## 핵심 벤더 · 제품", "",
              "<small>기술 일반명으로만 검색하면 브랜드명으로 보도되는 발표를 놓칩니다.</small>", ""]
        L += [f"- {v}" for v in theme["key_vendors"]] + [""]

    deep = [aliases[a] for a in (theme.get("areas") or []) if a in aliases]
    if deep:
        L += ["## 심층 자료", ""]
        for d in deep:
            L.append(f"- [{d.get('title')}](../../{d.get('path')}) "
                     f"<small>Tier {d.get('tier')}</small>")
        L.append("")
    elif theme.get("map_gap"):
        L += ["## 심층 자료", "", f"_{theme['map_gap']}_", ""]

    L += ["---", "", f"<small>생성물 · 마지막 생성 {today}</small>", ""]
    return "\n".join(L)


# ============================================================
# 홈 · 보유 현황
# ============================================================

def render_home(doc, state, theme_state, market, today) -> str:
    mon = pv.monitored(doc)
    reds = yellows = 0
    for p in mon:
        for f in ((state.get("positions") or {}).get(p["id"], {}).get("open_flags") or []):
            if f.get("level") == "RED":
                reds += 1
            elif f.get("level") == "YELLOW":
                yellows += 1
    flows = [r for e in (theme_state.get("themes") or {}).values()
             for r in (e.get("shifts") or {}).values()]
    promoted = sum(1 for r in flows if r.get("thesis_review"))
    stale = sum(1 for p in mon
                if (pv.days_since((state.get("positions") or {}).get(p["id"], {}).get("last_checked"),
                                  today) or 999) >= STALE_WARN_DAYS)

    L = ["# 오늘 한눈에", "", f"<small>{today} 기준</small>", "",
         "| 판단 필요 | 확인 필요 | 흐름 | thesis 갱신 후보 | 7일+ 미점검 |",
         "|---:|---:|---:|---:|---:|",
         f"| **{reds}** 🔴 | **{yellows}** 🟡 | {len(flows)} | {promoted} | {stale} |", "",
         "## 포지션", "",
         "| 종목 | 포지션 | 종가 | 등락 | 평단 대비 | 신호 | 마지막 점검 |",
         "|---|---|---:|---:|---:|---|---|"]
    for p in mon:
        e = (state.get("positions") or {}).get(p["id"], {})
        n = pv.days_since(e.get("last_checked"), today)
        fr = "기록 없음" if n is None else ("오늘" if n == 0 else f"{n}일 전")
        if n is not None and n >= STALE_WARN_DAYS:
            fr = f"**{fr}**"
        flg = pv._flag_counts(e) or "—"
        for t in p.get("tickers", []):
            m = market.get(t, {})
            r = ret_pct(m.get("price"), (p.get("avg_cost") or {}).get(t))
            L.append(f"| [{company_of(p, t)}](positions/{slug(p['id'])}.md) "
                     f"| <small>{label_base(p.get('label',''))}</small> "
                     f"| {money(t, m.get('price'))} | {pct(m.get('change_pct'))} "
                     f"| {pct(r) if r is not None else '—'} | {flg} | {fr} |")
    L += ["", "<small>**굵은 경과일** = 7일 이상 미점검. 확인 안 한 것이지 이상 없음이 아닙니다.</small>", "",
          "## 테마", "", "| 테마 | 주기 | 마지막 점검 | 흐름 | 닿는 포지션 |", "|---|---|---|---:|---:|"]
    for t in doc.get("themes", []):
        e = (theme_state.get("themes") or {}).get(t["id"], {})
        L.append(f"| [{t.get('label')}](themes/{slug(t['id'])}.md) "
                 f"| {'3일' if t.get('core') else '7일'} "
                 f"| {fresh(e.get('last_checked'), today).replace('확인 ', '')} "
                 f"| {len(e.get('shifts') or {})} | {len(t.get('affects') or [])} |")
    L += ["", "---", "", f"<small>생성물 · 마지막 생성 {today}</small>", ""]
    return "\n".join(L)


def render_holdings(doc, market, today) -> str:
    rows = []
    for p in pv.monitored(doc):
        for t in p.get("tickers", []):
            m = market.get(t, {})
            avg = (p.get("avg_cost") or {}).get(t)
            rows.append({
                "co": company_of(p, t), "label": label_base(p.get("label", "")), "pid": p["id"], "t": t,
                "price": m.get("price"), "chg": m.get("change_pct"),
                "cap": m.get("market_cap"), "avg": avg,
                "ret": ret_pct(m.get("price"), avg),
            })
    have = [r for r in rows if r["ret"] is not None]
    have.sort(key=lambda r: r["ret"], reverse=True)
    none = [r for r in rows if r["ret"] is None]

    L = ["# 보유 현황", "", f"<small>{today} 종가 기준 · 평단 입력분만 계산</small>", "",
         f"종목 **{len(rows)}** · 평단 입력 **{len(have)}** · "
         f"플러스 **{sum(1 for r in have if r['ret'] > 0)}** · "
         f"마이너스 **{sum(1 for r in have if r['ret'] <= 0)}**", "",
         "| 종목 | 포지션 | 종가 | 등락 | 시가총액 | 평단 | 수익률 |",
         "|---|---|---:|---:|---:|---:|---:|"]
    for r in have + none:
        L.append(f"| [{r['co']}](positions/{slug(r['pid'])}.md) "
                 f"| <small>{r['label']}</small> "
                 f"| {money(r['t'], r['price'])} | {pct(r['chg'])} "
                 f"| {cap(r['t'], r['cap'])} "
                 f"| {money(r['t'], r['avg']) if r['avg'] else '_미입력_'} "
                 f"| {'**'+pct(r['ret'])+'**' if r['ret'] is not None else '—'} |")
    L += ["", "<small>수익률순 · 평단 미입력 종목은 아래로. 입력은 봇에서 "
          "`/평단 <종목> <가격>`</small>", "",
          "<small>수량을 받지 않으므로 비중과 포트폴리오 총수익률은 계산하지 않습니다. "
          "조망용입니다.</small>", ""]
    return "\n".join(L)


# ============================================================
# 실행
# ============================================================

def build(out_dir: Path, today: str) -> dict:
    doc, state, theme_state, _aliases = pv.load_all()
    if not doc.get("positions"):
        raise SystemExit("positions.json 을 읽지 못했습니다.")
    market = load_market()

    (out_dir / "positions").mkdir(parents=True, exist_ok=True)
    (out_dir / "themes").mkdir(parents=True, exist_ok=True)

    counts = {"positions": 0, "themes": 0}
    for pos in doc["positions"]:
        if pos.get("status") not in pv.MONITORED_STATUSES:
            continue
        (out_dir / "positions" / f"{slug(pos['id'])}.md").write_text(
            render_position(pos, state, theme_state, doc, market, today), encoding="utf-8")
        counts["positions"] += 1
    for theme in doc.get("themes", []):
        (out_dir / "themes" / f"{slug(theme['id'])}.md").write_text(
            render_theme(theme, theme_state, doc, state, today), encoding="utf-8")
        counts["themes"] += 1

    (out_dir / "index.md").write_text(
        render_home(doc, state, theme_state, market, today), encoding="utf-8")
    (out_dir / "holdings.md").write_text(
        render_holdings(doc, market, today), encoding="utf-8")
    return counts


def nav_yaml(doc: dict) -> str:
    """mkdocs.yml 의 생성 구간에 넣을 nav 조각."""
    L = ["  - 현황:",
         "    - 오늘 한눈에: pages/index.md",
         "    - 보유 현황: pages/holdings.md",
         "  - 포지션:"]
    for p in doc.get("positions", []):
        if p.get("status") not in pv.MONITORED_STATUSES:
            continue
        L.append(f"    - {title_of(p)}: pages/positions/{slug(p['id'])}.md")
    L.append("  - 테마:")
    for t in doc.get("themes", []):
        L.append(f"    - {t.get('label')}: pages/themes/{slug(t['id'])}.md")
    return "\n".join(L)


BEGIN = "  # BEGIN:generated-nav"
END = "  # END:generated-nav"


def update_mkdocs(doc: dict, path: Path) -> bool:
    """mkdocs.yml 의 마커 사이만 갈아끼운다. 나머지 설정은 건드리지 않는다."""
    text = path.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(f"  ⚠ {path.name} 에 생성 마커가 없어 nav 갱신 생략")
        return False
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    path.write_text(f"{head}{BEGIN}\n{nav_yaml(doc)}\n{END}{tail}", encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser(description="포지션·테마 페이지 생성")
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--date", default=None, help="기준일 (기본: 오늘)")
    ap.add_argument("--no-nav", action="store_true", help="mkdocs.yml nav 갱신 생략")
    a = ap.parse_args()

    today = a.date or datetime.now().strftime("%Y-%m-%d")
    out = Path(a.out)
    counts = build(out, today)
    print(f"생성: 포지션 {counts['positions']} · 테마 {counts['themes']} · 홈 1 · 보유현황 1 → {out}")

    if not a.no_nav:
        doc, *_ = pv.load_all()
        if update_mkdocs(doc, PROJECT_ROOT / "mkdocs.yml"):
            print("mkdocs.yml nav 갱신")


if __name__ == "__main__":
    main()

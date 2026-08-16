"""포지션·테마 페이지 생성기.

positions.json + position_state.json + theme_state.json + events/ + market.json
을 읽어 markdown(+HTML 컴포넌트)을 찍는다. 검색도 LLM 호출도 네트워크도 없다.

★ 생성물은 손으로 고치지 말 것. 진실은 data/ 에 있고 페이지는 그 투영이다.
   thesis 수정은 봇의 /수정 으로만.

레이아웃은 2026-08-16 확정 목업을 따른다. Material 기본 마크다운으로는
카드·시세 스트립·타임라인이 안 나오므로 HTML 을 직접 찍고 assets/pages.css 가
받는다. 생성기가 출력을 100% 통제하므로 이쪽이 오히려 안전하다.

신선도를 1급 정보로 취급한다. 로테이션 때문에 대부분의 페이지는 며칠 묵어 있는데,
10일 전 정보를 최신인 양 보여주는 페이지는 "오늘 점검 안 함" 이라고 말해주는
다이제스트보다 나쁘다.

실행: python scripts/build_pages.py
"""

import argparse
import html
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
LEVEL_WORD = {"RED": "판단 필요", "YELLOW": "확인 필요", "WHITE": "참고"}
LEVEL_CLS = {"RED": "ia-red", "YELLOW": "ia-amber", "WHITE": "ia-grey"}
DIR_MARK = {"순풍": "↗", "역풍": "↘", "중립": "→", "불명": "?"}
DIR_CLS = {"순풍": "ia-teal", "역풍": "ia-red", "중립": "ia-grey", "불명": "ia-grey"}
STALE_DAYS = 7
TIMELINE_LIMIT = 40


# ============================================================
# 포맷 헬퍼
# ============================================================

def esc(s) -> str:
    return html.escape(str(s if s is not None else ""), quote=True)


def load_market() -> dict:
    return pv._load(MARKET_PATH, {"prices": {}}).get("prices", {})


def days(last: Optional[str], today: str) -> Optional[int]:
    return pv.days_since(last, today) if last else None


def fresh_text(last: Optional[str], today: str) -> str:
    n = days(last, today)
    if last is None:
        return "점검 기록 없음"
    if n is None:
        return f"확인 {last}"
    return f"확인 {last} (오늘)" if n == 0 else f"확인 {last} · {n}일 전"


def fresh_stamp(last: Optional[str], today: str) -> str:
    n = days(last, today)
    warn = " warn" if (n is not None and n >= STALE_DAYS) or last is None else ""
    return f'<span class="ia-stamp{warn}">{esc(fresh_text(last, today))}</span>'


def is_krw(ticker: str) -> bool:
    return ticker.isdigit() and len(ticker) == 6


def money(ticker: str, v) -> str:
    if v in (None, ""):
        return "—"
    try:
        v = float(v)
    except Exception:
        return esc(v)
    return f"{v:,.0f}원" if is_krw(ticker) else f"${v:,.2f}"


def pct(v) -> str:
    if v is None:
        return "—"
    try:
        v = float(v)
    except Exception:
        return "—"
    return f"{'+' if v >= 0 else ''}{v:.1f}%"


def pct_html(v, bold=False) -> str:
    if v is None:
        return '<span class="ia-num">—</span>'
    cls = "ia-up" if float(v) >= 0 else "ia-down"
    weight = ' style="font-weight:650"' if bold else ""
    return f'<span class="ia-num {cls}"{weight}>{pct(v)}</span>'


def cap(ticker: str, v) -> str:
    if not v:
        return "—"
    try:
        v = float(v)
    except Exception:
        return "—"
    if is_krw(ticker):
        return f"{v/1e12:.1f}조" if v >= 1e12 else f"{v/1e8:,.0f}억"
    return f"${v/1e9:.1f}B" if v >= 1e9 else f"${v/1e6:,.0f}M"


def ret_pct(price, avg) -> Optional[float]:
    try:
        price, avg = float(price), float(avg)
        return (price - avg) / avg * 100 if avg > 0 else None
    except Exception:
        return None


def pill(text, cls="ia-grey") -> str:
    return f'<span class="ia-pill {cls}">{esc(text)}</span>'


def company_of(pos: dict, ticker: str) -> str:
    return (pos.get("companies") or {}).get(ticker, ticker)


def label_base(label: str) -> str:
    """포지션명에서 회사명 괄호를 뗀다 — "SSD 컨트롤러 (파두)" → "SSD 컨트롤러"."""
    return re.sub(r"\s*\([^()]*\)\s*$", "", label or "").strip() or label


def title_of(pos: dict) -> str:
    """회사명이 주체, 포지션명은 부제."""
    names = [company_of(pos, t) for t in pos.get("tickers", [])]
    base = label_base(pos.get("label", ""))
    head = " · ".join(names) if names else base
    return f"{head} ({base})" if base and head != base else head


def slug(pid: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "-", pid)


def flag_pills(entry: dict) -> str:
    flags = entry.get("open_flags") or []
    out = []
    for lv in ("RED", "YELLOW"):
        n = sum(1 for f in flags if f.get("level") == lv)
        if n:
            out.append(pill(f"{LEVEL_MARK[lv]} {n}", LEVEL_CLS[lv]))
    return "".join(out) or '<span class="ia-stamp">신호 없음</span>'


# ============================================================
# 컴포넌트
# ============================================================

def kpis(items) -> str:
    cells = "".join(
        f'<div class="ia-kpi"><div class="k">{esc(k)}</div>'
        f'<div class="v" style="color:{c}">{esc(v)}</div>'
        f'<div class="n">{esc(n)}</div></div>'
        for k, v, n, c in items
    )
    return f'<div class="ia-kpis">{cells}</div>'


def quote_strip(pos, ticker, market) -> str:
    m = market.get(ticker, {})
    avg = (pos.get("avg_cost") or {}).get(ticker)
    r = ret_pct(m.get("price"), avg)
    price = m.get("price")
    chg = m.get("change_pct")

    cells = [
        f'<div class="main"><div class="k">종가</div>'
        f'<div class="v">{esc(money(ticker, price))}</div>'
        f'{pct_html(chg)}</div>',
        f'<div><div class="k">시가총액</div>'
        f'<div class="v">{esc(cap(ticker, m.get("market_cap")))}</div>'
        f'<div class="ia-stamp">{esc(m.get("market") or "")}</div></div>',
        f'<div><div class="k">내 평단</div>'
        f'<div class="v sm">{esc(money(ticker, avg)) if avg else "미입력"}</div>'
        f'<div class="ia-stamp">{"" if avg else "/평단 으로 입력"}</div></div>',
        f'<div class="{"hl" if r is not None else ""}"><div class="k">평단 대비</div>'
        f'<div class="v">{pct_html(r, bold=True) if r is not None else "—"}</div></div>',
        f'<div><div class="k">거래량</div>'
        f'<div class="v sm">×{esc(m.get("volume_ratio") or "—")}</div>'
        f'<div class="ia-stamp">5일 평균 대비</div></div>',
    ]
    return f'<div class="ia-quote">{"".join(cells)}</div>'


def cond_list(groups) -> str:
    """groups: [(소제목 or None, [(번호, 본문, 부연, 배지html)])]"""
    out = ['<div class="ia-conds">']
    for i, (sub, rows) in enumerate(groups):
        if sub:
            out.append(f'<div class="ia-subhd{" sep" if i else ""}">{sub}</div>')
        if not rows:
            out.append('<div class="ia-cond"><span class="tx" '
                       'style="color:var(--ia-faint)">(없음)</span></div>')
        for ix, tx, note, badge in rows:
            q = f'<span class="q">{esc(note)}</span>' if note else ""
            out.append(f'<div class="ia-cond"><span class="ix">{esc(ix)}</span>'
                       f'<span class="tx">{esc(tx)}{q}</span>{badge}</div>')
    out.append("</div>")
    return "\n".join(out)


def event_html(ev: dict) -> str:
    layer = ev.get("layer")
    date = ev.get("last_seen") or ev.get("date", "")
    cls = "ia-ev"
    meta = [f'<span class="d">{esc(date)}</span>']

    if layer == "theme":
        cls += " theme"
        d = ev.get("direction", "불명")
        meta.append(pill(f"🔷 흐름 {DIR_MARK.get(d,'')} {d}", DIR_CLS.get(d, "ia-grey")))
        if ev.get("theme_label"):
            meta.append(pill(ev["theme_label"], "ia-blue"))
    elif layer == "sweep":
        meta.append(pill("📰 소식", "ia-grey"))
    elif layer == "layer0":
        meta.append(pill("Layer 0", "ia-blue"))
    else:
        lv = ev.get("level") or "WHITE"
        cls += f" lv-{lv}"
        meta.append(pill(f"{LEVEL_MARK.get(lv,'')} {LEVEL_WORD.get(lv, lv)}",
                         LEVEL_CLS.get(lv, "ia-grey")))
    for r in (ev.get("refs") or []):
        meta.append(f"<code>{esc(r)}</code>")
    if ev.get("count", 1) >= 2:
        meta.append(f'<span class="ia-stamp">{ev["count"]}회째 · 최초 '
                    f'{esc(ev.get("first_seen",""))}</span>')

    head = ev.get("headline")
    body = (f"<b>{esc(head)}</b> — {esc(ev.get('summary',''))}"
            if head else esc(ev.get("summary", "")))

    parts = [f'<div class="{cls}">', f'<div class="meta">{"".join(meta)}</div>',
             f'<div class="body">{body}</div>']
    if ev.get("quant"):
        parts.append('<div class="sub">정량 · ' +
                     esc(" · ".join(f"{k} = {v}" for k, v in ev["quant"].items())) + "</div>")
    for q in (ev.get("qual") or [])[:2]:
        parts.append(f'<div class="sub">맥락 · {esc(q)}</div>')
    if ev.get("signal"):
        parts.append(f'<div class="lk">↳ 해당 조건 「{esc(ev["signal"])}」</div>')
    srcs = ev.get("sources") or []
    if srcs:
        links = ", ".join(
            f'<a href="{esc(s["url"])}" rel="noopener">{esc(s.get("outlet") or "출처")}</a>'
            if s.get("url") else esc(s.get("outlet") or "출처")
            for s in srcs[:4])
        parts.append(f'<div class="lk">근거 · {links}</div>')
    parts.append("</div>")
    return "\n".join(parts)


def table(headers, rows, cls="") -> str:
    th = "".join(f"<th{' class=\"r\"' if h.startswith('>') else ''}>"
                 f"{esc(h.lstrip('>'))}</th>" for h in headers)
    body = "".join(f'<tr class="{r[0]}">' + "".join(r[1]) + "</tr>" for r in rows)
    return (f'<div class="ia-tablewrap"><table class="ia-table {cls}">'
            f"<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>")


def obs_value(v) -> tuple[str, str, str]:
    """관측값 → (표시값, 기간, 부연). 구형 문자열과 신형 객체를 모두 받는다."""
    if isinstance(v, dict):
        val = v.get("value")
        unit = v.get("unit") or ""
        shown = f"{val:,}{unit}" if isinstance(val, (int, float)) else f"{val}{unit}"
        return shown, v.get("period") or "", v.get("note") or ""
    return str(v), "", ""


def render_indicators(pos: dict, entry: dict) -> str:
    """선언된 지표를 기준으로 렌더. 관측이 없어도 '무엇을 왜 보는지' 는 보여준다.

    값만 나열하면 이게 좋은 건지 나쁜 건지, 뭘 넘으면 문제인지 알 수 없다.
    판단 기준(why·judge·refs)은 positions.json 에 선언돼 있고 여기서 붙인다.
    """
    inds = (pos.get("watch") or {}).get("indicators") or []
    obs = entry.get("observations") or {}
    if not inds:
        return '<div class="ia-empty">추적 지표가 선언되지 않았습니다</div>'

    rows = []
    for it in inds:
        if isinstance(it, str):
            rows.append(f'<div class="ia-cond"><span class="tx">{esc(it)}</span></div>')
            continue
        series = obs.get(it.get("key")) or obs.get(it.get("name")) or []
        arrow = "↗ 증가가 좋음" if it.get("good") == "up" else (
                "↘ 감소가 좋음" if it.get("good") == "down" else "")

        if series:
            cur, per, note = obs_value(series[-1].get("value"))
            when = per or series[-1].get("date", "")
            prev = ""
            if len(series) > 1:
                pv_, pper, _ = obs_value(series[-2].get("value"))
                prev = f'<span class="ia-stamp">직전 {esc(pv_)}' +                        (f' ({esc(pper)})' if pper else "") + "</span>"
            head = (f'<span class="ia-num" style="font-size:.95rem;font-weight:650">{esc(cur)}</span>'
                    f'<span class="ia-stamp">{esc(when)}</span>'
                    + (f'<span class="ia-stamp">{esc(note)}</span>' if note else "")
                    + prev)
        else:
            head = '<span class="ia-stamp">아직 관측 없음</span>'

        refs = "".join(f"<code>{esc(r)}</code>" for r in (it.get("refs") or []))
        body = [f'<div class="ia-cond"><span class="ix">{esc(arrow.split()[0] if arrow else "·")}</span>',
                '<span class="tx">',
                f'<b>{esc(it.get("name"))}</b> '
                f'<span class="ia-stamp">{esc(it.get("unit") or "")}</span> {refs}',
                f'<span style="display:block;margin:.25rem 0">{head}</span>']
        if it.get("why"):
            body.append(f'<span class="q">왜 보나 · {esc(it["why"])}</span>')
        if it.get("judge"):
            body.append(f'<span class="q" style="color:var(--ia-amber)">판정 · {esc(it["judge"])}</span>')
        if arrow:
            body.append(f'<span class="q">{esc(arrow)}</span>')
        body += ["</span></div>"]
        rows.append("".join(body))

    # 선언되지 않은 관측도 버리지 않는다. 지금까지 모델이 즉석 key 로 쌓아온
    # 값들이 실제 숫자라서, 숨기면 페이지가 오히려 빈약해진다.
    # 내일부터는 선언 key 로 쌓이므로 이 목록은 자연히 줄어든다.
    extra = [k for k in obs if not any(
        (isinstance(i, dict) and (i.get("key") == k or i.get("name") == k)) for i in inds)]
    tail = ""
    if extra:
        er = []
        for k in extra:
            series = obs.get(k) or []
            if not series:
                continue
            cur, per, note = obs_value(series[-1].get("value"))
            er.append(("", [f'<td class="co"><b>{esc(k)}</b></td>',
                            f'<td>{esc(cur)}</td>',
                            f'<td class="r"><span class="sm">'
                            f'{esc(per or series[-1].get("date",""))}</span></td>']))
        tail = ('<div class="ia-subhd sep" style="margin-top:1rem">선언 외 관측</div>'
                + table(["관측", "값", ">시점"], er)
                + '<div class="ia-legend"><span>검색이 즉석 key 로 남긴 것들입니다. '
                  '추이 비교가 안 되므로, 계속 볼 값이면 <code>/수정</code> 으로 '
                  '추적 지표에 올리세요.</span></div>')
    return f'<div class="ia-conds">{"".join(rows)}</div>{tail}'


# ============================================================
# 포지션 페이지
# ============================================================

def render_position(pos, state, theme_state, doc, market, today) -> str:
    pid = pos["id"]
    entry = (state.get("positions") or {}).get(pid, {})
    events = events_log.load_events(pid)
    aliases = pv._load(pv.AREA_ALIASES_PATH, {"aliases": {}}).get("aliases", {})
    themes = pv.themes_for(doc, pid)
    tickers = pos.get("tickers", [])

    areas = ", ".join(aliases.get(a, {}).get("title", a)
                      for a in (pos.get("areas") or [])) or "미지정"
    tl = ", ".join(t.get("label", t["id"]) for t in themes) or "미연결 ⚠"

    L = [f'<p class="ia-eyebrow">포지션 · {esc(areas)}</p>',
         "", f"# {title_of(pos)}", "",
         f'<p class="ia-sub">'
         f'{esc(", ".join(f"{company_of(pos,t)} {t}" for t in tickers))}'
         f'<span class="ia-sep">·</span>'
         f'{esc(pv.STATUS_LABEL.get(pos.get("status"), pos.get("status")))}'
         f'<span class="ia-sep">·</span>테마 {esc(tl)}'
         f'<span class="ia-sep">·</span>{fresh_text(entry.get("last_checked"), today)}'
         f' {flag_pills(entry)}</p>', ""]

    # 시세
    L += ["## 시세", ""]
    for t in tickers:
        if len(tickers) > 1:
            L.append(f'<p class="ia-eyebrow">{esc(company_of(pos, t))} · {esc(t)}</p>')
        L.append(quote_strip(pos, t, market))
    if not market:
        L.append('<div class="ia-legend"><span>시세는 매일 06:30 실행이 갱신합니다. '
                 '평단은 봇에서 <code>/평단</code>.</span></div>')
    L.append("")

    # 보유 근거 · 조건
    def numbered(items, prefix, empty_note=""):
        return [(f"{prefix}{i}", it, "", "") for i, it in enumerate(items or [], 1)] or \
               ([("", empty_note or "미작성", "", pill("확인 필요", "ia-amber"))] if empty_note
                else [])

    L += ["## 보유 근거", "", cond_list([(None, numbered(pos.get("thesis"), "T",
          "미작성 — 왜 들고 있는지 기록이 없습니다"))]), ""]
    L += ["## 매도 검토 조건", "", cond_list([(None, numbered(pos.get("kill_signals"), "K",
          "미작성 — 이 포지션은 영원히 🔴 가 뜨지 않습니다"))]), ""]
    if pos.get("add_signals"):
        L += ["## 추가 검토 조건", "",
              cond_list([(None, numbered(pos.get("add_signals"), "A"))]), ""]

    # 반복 관측
    flags = [f for f in (entry.get("open_flags") or []) if f.get("count", 1) >= 2]
    if flags:
        rows = [("", [f'<td class="co"><b>{esc(f.get("signal",""))}</b></td>',
                      f'<td>{pill(f"{LEVEL_MARK.get(f.get("level"),"")} {f.get("level","")}", LEVEL_CLS.get(f.get("level"),"ia-grey"))}</td>',
                      f'<td class="r">{f.get("count")}회</td>',
                      f'<td class="r">{esc(f.get("first_seen","-"))}</td>',
                      f'<td class="r">{esc(f.get("last_seen","-"))}</td>'])
                for f in flags]
        L += ["## 반복 관측", "",
              table(["신호", "등급", ">누적", ">최초", ">최근"], rows), ""]

    # 타임라인
    L += ["## 최근 신호 · 뉴스", ""]
    if not events:
        L += ['<div class="ia-empty">아직 기록이 없습니다 — 이벤트 로그는 '
              '2026-08-17 실행부터 쌓입니다</div>', ""]
    else:
        L.append('<div class="ia-tl">')
        L += [event_html(e) for e in events[:TIMELINE_LIMIT]]
        L.append("</div>")
        if len(events) > TIMELINE_LIMIT:
            L.append(f'<div class="ia-legend"><span>외 {len(events)-TIMELINE_LIMIT}건</span></div>')
        L.append("")

    # 추적 지표 — 값만 던지지 말고 왜 보는지·어디에 걸리는지까지
    L += ["## 추적 지표", "", render_indicators(pos, entry), ""]

    # 공시·재무
    L += ["## 공시 · 재무", "",
          '<div class="ia-empty">DART·SEC 수집기 미연결 — 붙이면 공시와 분기 실적이 여기 쌓입니다</div>', ""]

    # 감시 / 무시 / 메모
    watch = pos.get("watch") or {}
    L += ["## 감시", "",
          cond_list([(None, [
              ("경쟁사", ", ".join(watch.get("peers", [])) or "(없음)", "", ""),
              ("검색어", ", ".join(watch.get("queries", [])) or "(없음)", "", ""),
          ])]), ""]
    if pos.get("ignore"):
        L += ["## 무시 (보고 안 함)", "",
              cond_list([(None, [("·", x, "", "") for x in pos["ignore"]])]), ""]
    if pos.get("note"):
        L += ["## 메모", "", f'<div class="ia-note">{esc(pos["note"])}</div>', ""]

    L.append(foot(today))
    return "\n".join(L)


def foot(today: str) -> str:
    return ('<div class="ia-foot">생성물입니다 — 직접 고치지 마세요. '
            '판정 기준 변경은 봇의 <code>/수정</code>. '
            f'마지막 생성 {esc(today)}</div>')


# ============================================================
# 테마 페이지
# ============================================================

def render_theme(theme, theme_state, doc, state, today) -> str:
    tid = theme["id"]
    entry = (theme_state.get("themes") or {}).get(tid, {})
    by_id = {p["id"]: p for p in doc.get("positions", [])}
    aliases = pv._load(pv.AREA_ALIASES_PATH, {"aliases": {}}).get("aliases", {})

    L = ['<p class="ia-eyebrow">테마 · Layer 0.5</p>', "",
         f"# {theme.get('label', tid)}", "",
         f'<p class="ia-sub">{"핵심 · 3일 주기" if theme.get("core") else "7일 주기"}'
         f'<span class="ia-sep">·</span>{fresh_text(entry.get("last_checked"), today)}'
         f'<span class="ia-sep">·</span>닿는 포지션 {len(theme.get("affects") or [])}개</p>', "",
         '<div class="ia-note">포지션은 “내 근거가 깨졌나”를 묻고, 테마는 “상위 변화가 '
         '어디로 얼마나 움직이나”를 묻습니다. 개별 점검은 하루 3종목뿐이라 여러 포지션을 '
         '동시에 흔드는 변화가 새어나가는데, 이 레이어가 그 구멍을 메웁니다. '
         '<b>여기서는 등급을 매기지 않습니다.</b></div>', ""]

    # 흐름
    shifts = sorted((entry.get("shifts") or {}).values(),
                    key=lambda r: (0 if r.get("thesis_review") else 1,
                                   -r.get("count", 1), r.get("last_seen", "")))
    L += ["## 흐름", ""]
    if not shifts:
        L += ['<div class="ia-empty">아직 관측이 없습니다</div>', ""]
    else:
        L.append('<div class="ia-tl">')
        for r in shifts:
            d = r.get("direction", "불명")
            meta = [f'<span class="d">{esc(r.get("last_seen",""))}</span>',
                    pill(f"{DIR_MARK.get(d,'')} {d}", DIR_CLS.get(d, "ia-grey"))]
            for x in (r.get("refs") or []):
                meta.append(f"<code>{esc(x)}</code>")
            meta.append(f'<span class="ia-stamp">{r.get("count",1)}회 · 최초 '
                        f'{esc(r.get("first_seen","-"))}</span>')
            if r.get("thesis_review"):
                meta.append(pill("★ thesis 갱신 후보", "ia-amber"))
            names = ", ".join(title_of(by_id[p]) for p in (r.get("affects") or [])
                              if p in by_id) or "—"
            L.append(f'<div class="ia-ev theme"><div class="meta">{"".join(meta)}</div>'
                     f'<div class="body"><b>{esc(r.get("headline") or r.get("shift",""))}</b>'
                     f' — {esc(r.get("summary",""))}</div>'
                     f'<div class="lk">↳ 닿는 포지션 · {esc(names)}</div></div>')
        L += ["</div>", ""]

    # 추적 대상 변화
    L += ["## 추적 대상 변화", "",
          '<div class="ia-legend"><span>kill 조건이 아니라 방향과 속도를 묻는 항목입니다</span></div>',
          cond_list([(None, [(f"W{i}", w, "", "")
                             for i, w in enumerate(theme.get("watch_shifts", []), 1)])]), ""]

    # 닿는 포지션
    L += ["## 닿는 포지션", "", '<div class="ia-grid">']
    for pidx in theme.get("affects", []):
        p = by_id.get(pidx)
        if not p:
            continue
        e = (state.get("positions") or {}).get(pidx, {})
        n = days(e.get("last_checked"), today)
        L.append(f'<a class="ia-card{" dim" if (n is None or n >= STALE_DAYS) else ""}" '
                 f'href="../../positions/{slug(pidx)}/">'
                 f'<div class="top"><div><div class="nm">{esc(title_of(p))}</div>'
                 f'<div class="tk">{esc(", ".join(p.get("tickers", [])))}</div></div>'
                 f'{flag_pills(e)}</div>'
                 f'<div class="foot"><span class="ia-stamp">'
                 f'{esc(fresh_text(e.get("last_checked"), today))}</span></div></a>')
    L += ["</div>", ""]

    if theme.get("key_vendors"):
        L += ["## 핵심 벤더 · 제품", "",
              '<div class="ia-legend"><span>기술 일반명으로만 검색하면 브랜드명으로 '
              '보도되는 발표를 놓칩니다</span></div>',
              cond_list([(None, [("·", v, "", "") for v in theme["key_vendors"]])]), ""]

    deep = [aliases[a] for a in (theme.get("areas") or []) if a in aliases]
    if deep:
        L += ["## 심층 자료", ""]
        for d in deep:
            L.append(f'- [{d.get("title")}](../../{d.get("path")}) '
                     f'<span class="ia-stamp">Tier {d.get("tier")}</span>')
        L.append("")
    elif theme.get("map_gap"):
        L += ["## 심층 자료", "", f'<div class="ia-empty">{esc(theme["map_gap"])}</div>', ""]

    L.append(foot(today))
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
                if (days((state.get("positions") or {}).get(p["id"], {}).get("last_checked"),
                         today) or 999) >= STALE_DAYS)

    L = ['<p class="ia-eyebrow">현황판</p>', "", "# 오늘 한눈에", "",
         f'<p class="ia-sub">{esc(today)}<span class="ia-sep">·</span>'
         f'포지션 {len(mon)}개<span class="ia-sep">·</span>'
         f'다이제스트는 평일 06:30 KST 자동</p>',
         kpis([
             ("판단 필요", f"{reds}", "🔴 kill 조건 해당", "var(--ia-red)" if reds else "var(--ia-ink)"),
             ("확인 필요", f"{yellows}", "🟡 열린 신호", "var(--ia-amber)" if yellows else "var(--ia-ink)"),
             ("인프라 흐름", f"{len(flows)}", "테마 누적", "var(--ia-ink)"),
             ("thesis 갱신 후보", f"{promoted}", "3회 반복 시 승격", "var(--ia-ink)"),
             ("7일+ 미점검", f"{stale}", "로테이션 대기", "var(--ia-amber)" if stale else "var(--ia-ink)"),
         ]), ""]

    # 포지션 카드
    L += ["## 포지션", "", '<div class="ia-grid">']
    for p in mon:
        e = (state.get("positions") or {}).get(p["id"], {})
        n = days(e.get("last_checked"), today)
        dim = " dim" if (n is None or n >= STALE_DAYS) else ""
        t0 = (p.get("tickers") or [""])[0]
        m = market.get(t0, {})
        r = ret_pct(m.get("price"), (p.get("avg_cost") or {}).get(t0))
        evs = events_log.load_events(p["id"])
        last = evs[0].get("summary", "") if evs else ""
        last = (last[:78] + "…") if len(last) > 78 else last
        L.append(
            f'<a class="ia-card{dim}" href="positions/{slug(p["id"])}/">'
            f'<div class="top"><div>'
            f'<div class="nm">{esc(" · ".join(company_of(p, t) for t in p.get("tickers", [])))}</div>'
            f'<div class="tk">{esc(", ".join(p.get("tickers", [])))} · {esc(label_base(p.get("label","")))}</div>'
            f'</div>{flag_pills(e)}</div>'
            f'<div class="row"><span class="ia-num big">{esc(money(t0, m.get("price")))}</span>'
            f'{pct_html(m.get("change_pct"))}'
            f'<span class="ia-stamp">시총 {esc(cap(t0, m.get("market_cap")))}</span></div>'
            + (f'<div class="last">{esc(last)}</div>' if last else
               '<div class="last" style="color:var(--ia-faint)">기록 없음</div>')
            + f'<div class="foot">'
            f'{(pill(f"평단 대비 {pct(r)}", "ia-teal" if r >= 0 else "ia-red") if r is not None else pill("평단 미입력", "ia-grey"))}'
            f'<span class="ia-stamp">{esc(fresh_text(e.get("last_checked"), today))}</span>'
            f'</div></a>')
    L += ["</div>",
          '<div class="ia-legend"><span>흐린 카드 = 7일 이상 미점검. '
          '<b>확인 안 한 것이지 이상 없음이 아닙니다.</b></span></div>', ""]

    # 테마
    rows = []
    for t in doc.get("themes", []):
        e = (theme_state.get("themes") or {}).get(t["id"], {})
        n = days(e.get("last_checked"), today)
        rows.append(("", [
            f'<td class="co"><a href="themes/{slug(t["id"])}/"><b>{esc(t.get("label"))}</b></a>'
            f'<span class="sm">{esc("핵심 · 3일" if t.get("core") else "7일")}</span></td>',
            f'<td>{fresh_stamp(e.get("last_checked"), today)}</td>',
            f'<td class="r">{len(e.get("shifts") or {})}</td>',
            f'<td class="r">{len(t.get("affects") or [])}</td>']))
    L += ["## 테마", "", table(["테마", "마지막 점검", ">흐름", ">닿는 포지션"], rows), ""]
    L.append(foot(today))
    return "\n".join(L)


def render_holdings(doc, market, today) -> str:
    rows_data = []
    for p in pv.monitored(doc):
        for t in p.get("tickers", []):
            m = market.get(t, {})
            avg = (p.get("avg_cost") or {}).get(t)
            rows_data.append({
                "co": company_of(p, t), "label": label_base(p.get("label", "")),
                "pid": p["id"], "t": t, "price": m.get("price"),
                "chg": m.get("change_pct"), "cap": m.get("market_cap"),
                "avg": avg, "ret": ret_pct(m.get("price"), avg),
            })
    have = sorted([r for r in rows_data if r["ret"] is not None],
                  key=lambda r: r["ret"], reverse=True)
    none = [r for r in rows_data if r["ret"] is None]
    peak = max((abs(r["ret"]) for r in have), default=1) or 1

    rows = []
    for r in have + none:
        if r["ret"] is None:
            bar = ""
        else:
            w = min(100, abs(r["ret"]) / peak * 100)
            side = "pos" if r["ret"] >= 0 else "neg"
            bar = f'<span class="ia-bar"><b class="{side}" style="width:{w:.0f}%"></b></span>'
        rows.append(("none" if r["ret"] is None else "", [
            f'<td class="co"><a href="positions/{slug(r["pid"])}/"><b>{esc(r["co"])}</b></a>'
            f'<span class="sm">{esc(r["t"])} · {esc(r["label"])}</span></td>',
            f'<td class="r">{esc(money(r["t"], r["price"]))}</td>',
            f'<td class="r">{pct_html(r["chg"])}</td>',
            f'<td class="r">{esc(cap(r["t"], r["cap"]))}</td>',
            f'<td class="r">{esc(money(r["t"], r["avg"])) if r["avg"] else "<i>미입력</i>"}</td>',
            f'<td class="r">{pct_html(r["ret"], bold=True) if r["ret"] is not None else "—"}</td>',
            f"<td>{bar}</td>"]))

    L = ['<p class="ia-eyebrow">보유 현황</p>', "", "# 수익률", "",
         f'<p class="ia-sub">{esc(today)} 종가 기준<span class="ia-sep">·</span>'
         f'평단 입력분만 계산</p>',
         kpis([
             ("종목", f"{len(rows_data)}", f"{len(pv.monitored(doc))} 포지션", "var(--ia-ink)"),
             ("평단 입력", f"{len(have)}", f"{len(none)}종목 미입력", "var(--ia-ink)"),
             ("플러스", f"{sum(1 for r in have if r['ret'] > 0)}", "", "var(--ia-teal)"),
             ("마이너스", f"{sum(1 for r in have if r['ret'] <= 0)}", "", "var(--ia-red)"),
         ]),
         table(["종목", ">종가", ">등락", ">시가총액", ">평단", ">수익률", ""], rows), "",
         '<div class="ia-legend">'
         '<span>수익률순 · 평단 미입력은 아래로</span>'
         '<span>입력: 봇에서 <code>/평단 &lt;종목&gt; &lt;가격&gt;</code></span>'
         '<span>수량을 받지 않으므로 비중·총수익률은 계산하지 않습니다 (조망용)</span>'
         "</div>", "", foot(today)]
    return "\n".join(L)


# ============================================================
# 실행
# ============================================================

def build(out_dir: Path, today: str) -> dict:
    doc, state, theme_state, _ = pv.load_all()
    if not doc.get("positions"):
        raise SystemExit("positions.json 을 읽지 못했습니다.")
    market = load_market()

    (out_dir / "positions").mkdir(parents=True, exist_ok=True)
    (out_dir / "themes").mkdir(parents=True, exist_ok=True)

    n_pos = 0
    for pos in doc["positions"]:
        if pos.get("status") not in pv.MONITORED_STATUSES:
            continue
        (out_dir / "positions" / f"{slug(pos['id'])}.md").write_text(
            render_position(pos, state, theme_state, doc, market, today), encoding="utf-8")
        n_pos += 1
    for theme in doc.get("themes", []):
        (out_dir / "themes" / f"{slug(theme['id'])}.md").write_text(
            render_theme(theme, theme_state, doc, state, today), encoding="utf-8")

    (out_dir / "index.md").write_text(
        render_home(doc, state, theme_state, market, today), encoding="utf-8")
    (out_dir / "holdings.md").write_text(
        render_holdings(doc, market, today), encoding="utf-8")
    return {"positions": n_pos, "themes": len(doc.get("themes", []))}


def nav_yaml(doc: dict) -> str:
    """생성 구간에 넣을 nav 조각. 첫 항목이 사이트 첫 페이지가 된다."""
    L = ["  - 오늘 한눈에: index.md",
         "  - 보유 현황: pages/holdings.md",
         "  - 포지션:"]
    for p in doc.get("positions", []):
        if p.get("status") not in pv.MONITORED_STATUSES:
            continue
        L.append(f"    - {title_of(p)}: pages/positions/{slug(p['id'])}.md")
    L.append("  - 테마:")
    for t in doc.get("themes", []):
        L.append(f"    - {t.get('label')}: pages/themes/{slug(t['id'])}.md")
    return "\n".join(L)


BEGIN, END = "  # BEGIN:generated-nav", "  # END:generated-nav"


def update_mkdocs(doc: dict, path: Path) -> bool:
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
    ap.add_argument("--date", default=None)
    ap.add_argument("--no-nav", action="store_true")
    a = ap.parse_args()

    today = a.date or datetime.now().strftime("%Y-%m-%d")
    c = build(Path(a.out), today)
    print(f"생성: 포지션 {c['positions']} · 테마 {c['themes']} · 홈 1 · 보유현황 1")
    if not a.no_nav:
        doc, *_ = pv.load_all()
        if update_mkdocs(doc, PROJECT_ROOT / "mkdocs.yml"):
            print("mkdocs.yml nav 갱신")


if __name__ == "__main__":
    main()

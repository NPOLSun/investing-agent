# 광인터커넥트 / CPO — Tier 1 Deep Dive

> **Trigger**: NVIDIA $2B씩 Coherent·Lumentum 동시 지분 투자 (2026-03-02), Marvell-Celestial AI $5.5B 인수 (2025-12), Lumentum 1년 +966%. AI 시대 *데이터센터 plumbing* 으로 광인터커넥트 자리잡음. Coherent Q3 FY26 DC&Comm 매출 +41% yoy, book-to-bill > 4×.
> **Linked methodology**: methodology_v2.1.md

---

## 0. 메타 정보

| 항목 | 값 |
|------|----|
| 작성일 | 2026-05-24 |
| 최근 갱신 | 2026-05-24 |
| 다음 정기 갱신 | 2026-07-01 |
| 시계 분류 | Core (1.5~2.5년) |
| Tier | 1 (Deep) |
| Confidence | High |
| 트랙 | L1A (Global) + KR transmission 부분 |

---

## 1. 한 줄 요약 + 핵심 가설

### 한 줄 요약

> AI 클러스터의 *대역폭·전력·열* 한계가 800G·1.6T 세대에서 폭발. 2026~2028 광인터커넥트가 데이터센터 *표준 plumbing* 으로 전환. 알파는 **3개 층** 분화 — 상층 광원 (Coherent·Lumentum 의 EML·InP 과점), 중층 CPO·실리콘 포토닉스 (Marvell·NVDA·AVGO), 하층 모듈 (commoditization 진행, 한국 오이솔루션 부분 노출). 본인 진입 우선순위: **광원 > 실리콘 포토닉스 > 모듈**.

### 핵심 가설

**가설 A — 광원 (EML·InP) 이 진정한 병목, 과점 강화 중**
- 800G·1.6T 트랜시버는 *EML (Externally Modulated Laser)* 필수. 200G/lane EML 이 1.6T 의 핵심.
- Lumentum 글로벌 EML **50~60%** 점유, Coherent ~25% 트랜시버 점유. 나머지 MACOM·Sumitomo.
- NVIDIA가 2026-03-02 Coherent·Lumentum 각 $2B 씩 지분 투자 + 다년 구매 약정 = *광원이 GPU 만큼 strategic bottleneck* 이라는 공식 인정.
- InP wafer fab 이 진짜 capa 제약. Lumentum 자체 InP 확장, Coherent 6-inch InP 80% 진행 (Q4 cal 2026 doubling 목표).

**가설 B — CPO 본격 양산은 2027~2028, 그 전까지 800G·1.6T pluggable 이 본체**
- NVIDIA Spectrum-X·Quantum-X (CPO 본격 적용) 발표 (2025 GTC).
- Broadcom Tomahawk 5-Bailly: 2025년 5만+ unit 출하 = *CPO 이미 양산 진입*.
- TSMC COUPE platform: 2H 2026 high-volume risk production (AMD lead).
- 그러나 Coherent Q3 FY26 commentary: "calendar 2026 거의 다 예약, 2027 빠르게 채워짐". 800G·1.6T pluggable 이 2026~2027 매출의 본체.
- → CPO 가 *주류* 되는 시점 = 2027 후반~2028. 그 전까지 Coherent·Lumentum *기존 EML·트랜시버 매출이 폭증*.

**가설 C — Marvell-Celestial AI 인수가 시장 표준화 시그널**
- 2025-12-03 Marvell $5.5B (초기 $3.25B = 현금 $1B + 주식 2,720만주 $2.25B) 로 Celestial AI 인수, 2026 Q1 closing.
- Celestial *Photonic Fabric* = chip-to-chip 광 인터커넥트. CPO 보다 낮은 power, ns latency, thermal 강건. AWS 지원 성명 + $90M warrant.
- Marvell 매출 가이던스: FY2028 2H 부터, FY2028 Q4 $500M run-rate, FY2029 Q4 $1B. CEO Murphy 명시 $10B TAM.
- → 시장이 "광 인터커넥트 = 표준" 이라는 *상장사 verification* 받음. Marvell 이 photonics pure-play 에 가까워짐.

**가설 D — Marvell 이 valuation 매력 최대 (저평가 alpha)**
- YTD -18% (인수 부담 일시 압축)
- Q3 FY26 매출 $2.1B (+37% yoy), Data center $1.5B (+38% yoy)
- 자동차 Ethernet 매각 Infineon $2.5B (2025) = Celestial 자금
- Custom XPU (AWS Trainium·Microsoft Maia) 다중 노출 + Photonic Fabric

**가설 E — Lumentum 1년 +966% = 과열 부담, 분할 진입 필요**
- EML 50~60% 점유 + NVIDIA $2B + OCS pure-play
- 그러나 *valuation 상당 반영*. 10~15% 조정 wait 권장.

**가설 F — 한국 transmission 약함, 모듈 commoditization 직격탄**
- 오이솔루션 (138080) = 광 트랜시버 KR 1위지만 *글로벌 EML 광원 공급망 종속*.
- 라이팩 (비상장), 광림 (비상장) 등 모듈 일부.
- 한국 비중 위성 수준. 본인 미국 종목 중심.

### 기각 조건

- 빅테크 AI CapEx 분기 -20%+ 둔화 (가능성 매우 낮음)
- CPO 양산 6개월+ 지연 (TSMC COUPE 일정 흔들리면)
- VCSEL 200G+ 본격 양산이 EML 잠식 (자기 잠식 가능성)
- 중국 자체 InP·EML 양산 가속 (DeepSeek 식 시그널)
- Marvell-Celestial 통합 실패 또는 Photonic Fabric 양산 지연

---

## 2. 4가지 잣대 채점

### 잣대 1: TAM

**점수: 4 / 5** (Major expansion, ×3~5 + 100B$+ 도달)

- 광 트랜시버: 2025 ~$15B → 2030 ~$50B+ (LightCounting, Yole)
- 실리콘 포토닉스: 2026 ~$4B → 2030 ~$15B (IDTechEx 2026 보고서)
- CPO 단독: 2025 $95M → 2026 $124M → 2034 $1,055M (CAGR 30.7%, Precedence)
- Optical Circuit Switch: Lumentum 자체 목표 $100M/q (2026 EOY), 18개월 전 거의 0
- 합산 광인터커넥트 5년 후 ~$80~120B
- Marvell scale-up TAM 별도 $10B (Murphy CEO 인용)

**Confidence**: High

### 잣대 2: Moat (해자 재편 + 비가역성)

**점수: 4 / 5** (Major reshuffle + 비가역 강)

- **광원 (EML/InP) 과점 매우 강**: Lumentum 50~60% + Coherent 25% + MACOM·Sumitomo. InP wafer fab 신규 진입 불가 (자본·공정·인허가·고객 lock-in).
- **NVIDIA $2B 직접 투자 + 다년 구매 약정** = 새 진입자 진입로 봉쇄.
- **실리콘 포토닉스 시스템 재편**: 기존 NVDA·AVGO·MRVL + 신규 Ayar·Lightmatter·Celestial (Marvell 인수). Marvell-Celestial 로 상장사 photonics pure-play 자리매김.
- **CPO 패키징** = TSMC COUPE 사실상 독점 (AMD 2H 2026 lead).
- **모듈 단계는 commoditization 강** (중국 InnoLight·Eoptolink·HG Genuine, 한국 오이솔루션) — Moat 약.
- **비가역성**: NVIDIA·Coherent·Lumentum 다년 합의 = 3~5년 lock-in. InP fab 확장 = 8년+ 회수 sunk cost.

**Confidence**: High

### 잣대 3: Capital

**점수: 4 / 5** (Major capital 10~100B$/년)

- 빅테크 AI CapEx 중 광인터커넥트: 추정 $30~50B/년 (전체 $500B+ 의 5~8%)
- M&A: Marvell-Celestial $5.5B (2025-12), Coherent-InnoLight (2024)
- 빅테크 직접 지분: NVIDIA → Coherent + Lumentum 각 $2B (2026-03-02) 합산 $4B
- VC 펀딩: Ayar Labs $300M+, Lightmatter $600M+, Celestial $500M+ (인수 전) 누적 ~$3B
- 합산 직접 자본 ~$40~60B/년

**Confidence**: Medium-High

### ~~잣대 4: Tech~~ (폐기)

### 합산

| 트랙 | 점수 | 임계 |
|------|------|------|
| L1A | **12 / 15** | Tier 1 ≥ 12 ✅ |

→ **Tier 1 확정**

---

## 3. A·B·C 시차 평가

### A 지표 (자본 유입) — **5 / 5**

- NVIDIA → Coherent·Lumentum $4B 직접 지분 + 다년 구매
- Marvell-Celestial $5.5B 인수
- Lumentum·Coherent S&P 500 동시 편입 (2026-03)
- AWS·MS·Google·Meta 2026~2027 본격 배치 공표
- 빅테크 AI CapEx 분기 신기록 갱신

### B 지표 (실물 변화) — **4 / 5**

- Coherent Q3 FY26 DC&Comm 매출 $1,362M (+41% yoy, +13% qoq), book-to-bill > 4×
- 2026 calendar 거의 다 예약, 2027 빠르게 채워짐
- Lumentum FY26 Q3 가이던스 $780~830M (+65% yoy). 200G/lane EML 출하 ramping (5% unit → 25% by EOY 2026)
- Broadcom Tomahawk 5-Bailly 2025 5만+ CPO switch shipped
- TSMC COUPE 2H 2026 high-volume risk production
- Marvell Q3 FY26 매출 $2.1B (+37% yoy), Data center $1.5B (+38% yoy)
- CPO 본격 주류화는 2027~ → B 만점 아님

### C 지표 (가격 반영) — **4 / 5**

- Lumentum 1년 +966% (2025-08 ~ 2026-03)
- Coherent S&P 500 편입 후 추가 상승
- MACOM·AAOI 동반 상승
- 광원 종목 *과열 신호* (P/S 7~12x)
- **단 Marvell 만 상대적 저평가** (YTD -18%, 인수 가격 부담 일시 압축)

### 시차 매력도 = A + B − C = **5 + 4 − 4 = +5 (Strong entry)**

→ 시차 매력 매우 큼. 단 *광원 종목 과열 부담, Marvell 이 상대적 저평가*. 분할 매수 권장.

---

## 4. 산업 메가트렌드 (Step 1)

### 4.1 수요 측

**단기 (12~18개월)**
- 800G 트랜시버 양산 정점: NVIDIA H100·H200·Blackwell GB200 모두 800G. 2026 출하 수천만 unit.
- 1.6T 트랜시버 본격 ramp: 2026 후반~2027 주류화. 200G/lane EML 핵심. 1.6T module GM > 800G (early-cycle ASP 효과).
- 광 회로 스위치 (OCS) 등장: Google 자체 OCS 사용, Lumentum 외부 공급 pure-play. 18개월 전 거의 0 → 2026 EOY $100M/q 목표.
- AI 클러스터당 광 인터커넥트 폭증: GPU N개 클러스터의 인터커넥트는 N² 비례. NVIDIA NVL72 (72 GPU) rack 당 트랜시버 수천 개.

**중기 (2~4년)**
- CPO 본격 표준화 (2027~2028): NVIDIA Spectrum-X·Quantum-X 양산 본격. Broadcom Tomahawk 5/6 모두 CPO. AMD·Intel 추격.
- Scale-up vs Scale-out 양분화: Scale-up (GPU↔GPU within node) = CPO + Celestial Photonic Fabric. Scale-out (rack↔rack) = 기존 pluggable 800G·1.6T·3.2T.
- 3.2T 출시 (2027 후반~2028): 400G/lane EML 필요. Coherent *400G differential-EML* 이미 ECOC 2025 award 수상.

**장기 (5~10년)**
- 광 컴퓨팅 (Lightmatter·Lightelligence·Q.ant): 2030+
- 양자 인터커넥트: 매우 장기

### 4.2 공급 측

**현재 병목 — 광원 (EML, InP) capa**
- Lumentum InP fab 확장: San Jose + 신규 capa, 2026 내내.
- Coherent 6-inch InP: Sherman TX + Tarfala 스웨덴. 현재 80%, Q4 cal 2026 doubling.
- 3-inch → 6-inch 전환 = 단위면적당 칩 수 4×.
- 수요가 capa 추월. Lumentum CEO: "narrow-line laser shipments 6 consecutive quarters 증가, demand outpacing supply through rest of fiscal 2026"

**다음 병목 — CPO 패키징 capa**
- TSMC COUPE: AMD lead customer, 2H 2026 risk production.
- OSAT (ASE, Amkor) 진입 시도 — TSMC 정밀도 따라잡기 어려움.
- 2027~2028 CPO 주류화 시 패키징이 새 병목.

**추가 병목 — 실리콘 포토닉스 fab capa**
- Intel Foundry photonics 일부, GlobalFoundries (FAMA), Tower Semiconductor.

### 4.3 정책·지정학 변수

- **미국 photonics 자국 capa**: CHIPS Act 자금 일부 photonics fab. AAOI 미국 자국 제조 정책 수혜.
- **미·중 광인터커넥트 견제**: 트랜시버 수출 통제. 중국 자체 EML 개발 가속 (Hisense·HG Genuine).
- **유럽 photonics sovereignty 약함**: Ranovus 등 일부.
- **한국 photonics 정책 미미**.

---

## 5. 밸류체인 매핑 (Step 2)

### 5.1 다이어그램

```
[L1 Substrate]
  ├ InP wafer (EML용): Sumitomo Electric, IQE (IQE.L)
  ├ GaAs wafer (VCSEL용): Sumitomo, AXT, IQE
  └ Si wafer (실리콘 포토닉스): Soitec (SOI.PA), Shin-Etsu, SUMCO
       ↓
[L2 Epitaxy 장비]
  ├ Aixtron (AIXA.DE) — MOCVD 1위
  ├ Veeco (VECO)
  └ 각 fab 자체 epi (Coherent·Lumentum 내재화)
       ↓
[L3 광원 (Laser Source)] ★★★ 가장 안전한 알파
  ├ EML: Lumentum (LITE 50~60%), Coherent (COHR), MACOM (MTSI), Sumitomo (5802.T)
  ├ VCSEL: Coherent (II-VI 인수, leader), Lumentum
  ├ Quantum-Dot Lasers (next-gen): Ranovus (비상장)
  └ 고출력 CW Laser (CPO 외부 광원): Coherent 400mW, Lumentum ultra-high-power
       ↓
[L4 실리콘 포토닉스 IC / 광 IC] ★★ 핵심 시스템
  ├ Marvell (MRVL) — Celestial AI 인수 (Photonic Fabric), Rockley IP, COLORZ ZR/ZR+
  ├ Broadcom (AVGO) — Tomahawk 5/6 CPO switch
  ├ NVIDIA (NVDA) — Spectrum-X / Quantum-X Photonics
  ├ Cisco (CSCO) — Acacia 인수
  ├ POET Technologies (POET) — Optical Interposer, 시총 ~$400M
  └ Ayar Labs, Lightmatter, Celestial (Marvell 인수) — 비상장
       ↓
[L5 CPO 패키징] ★★ 다음 병목
  ├ TSMC COUPE — 사실상 독점
  ├ Intel Foveros, Samsung X-Cube — 추격
  └ ASE, Amkor — OSAT 진입 시도
       ↓
[L6 Pluggable Modules 800G/1.6T] (commoditization)
  ├ Coherent (COHR) — InnoLight 인수로 모듈 1위
  ├ Lumentum (LITE) — 모듈 + 광원 통합
  ├ Applied Optoelectronics (AAOI) — 미국 자국 제조 ★ 정책 수혜
  ├ Eoptolink (300502.SZ), HG Genuine — 중국 강
  └ 오이솔루션 (138080) — 한국 1위 (commoditization 압박)
       ↓
[L7 OCS Optical Circuit Switch] ★ 신규 카테고리
  ├ Lumentum (LITE) — 외부 공급 pure-play, $100M/q 목표 2026 EOY
  └ Google 자체 OCS (외부 미공급), Calient (비상장)
       ↓
[L8 Switch / 시스템]
  ├ NVIDIA (Spectrum-4, Quantum-2/3)
  ├ Broadcom (Tomahawk 5/6)
  └ Marvell (Teralynx), Cisco (Silicon One)
       ↓
[L9 Hyperscaler]
  AWS, Microsoft, Google, Meta, Oracle, xAI
```

### 5.2 레이어별 분석

| 레이어 | GM | 경쟁구도 | 중국 침투 | 진입장벽 | 본인 매력도 |
|--------|-----|---------|---------|---------|----------|
| L1 InP Substrate | 매우 높음 (50%+) | Sumitomo·IQE·AXT 과점 | 거의 없음 | 매우 높음 | 중간 (간접) |
| L3 광원 (EML/InP) | 매우 높음 (40~50%) | 강한 과점 | 거의 없음 | 매우 높음 | **★★★** |
| L4 SiP IC | 매우 높음 (50%+) | NVDA·AVGO·MRVL 과점 | 일부 | IP + 기술 | **★★** |
| L5 CPO 패키징 | 매우 높음 | TSMC 독점 | 거의 없음 | 매우 높음 | 간접 (TSM) |
| L6 모듈 800G/1.6T | 25~40% | 다수, 중국 강 | 큼 | 낮음 | **★ 위성** |
| L7 OCS | 매우 높음 (early) | Lumentum + 비상장 | 거의 없음 | 기술 | **★★ 신생** |
| L8 Switch | 매우 높음 | NVDA·AVGO·MRVL·Cisco | 일부 | 매우 높음 | 중복 |

### 5.3 하위 세분화 (Sub-areas)

#### Sub-area 1: 광원 (EML/InP) ★★★ 본인 매수 1순위
- **Lumentum (LITE)**: EML 50~60%. NVIDIA $2B + ultra-high-power CW. OCS pure-play. 1년 +966% (과열).
- **Coherent (COHR)**: 트랜시버 25%, EML 자체. NVIDIA $2B. 6-inch InP 80%. S&P 500. DC&Comm +41% yoy.
- **MACOM (MTSI)**: 광원 + RF, 시총 ~$10B, EML pure-play 비중 적음.
- **Sumitomo (5802.T)**: 일본, ADR 약함.

#### Sub-area 2: 실리콘 포토닉스 시스템 ★★ 본인 매수 2순위
- **Marvell (MRVL)**: Celestial AI 인수 $5.5B. Rockley IP. Q3 FY26 +37% yoy. YTD -18% (저평가). Photonic Fabric 매출 FY2028 2H~.
- **NVIDIA (NVDA)**, **Broadcom (AVGO)**: AI Foundation 영역 중복.
- **POET (POET)**: 시총 ~$400M, 변동성 매우 큼.

#### Sub-area 3: 외부 CPO 광원 (CW Laser)
- Coherent 400mW CW Laser (2025 발표, 다수 고객 샘플링)
- Lumentum ultra-high-power lasers (largest order in history)
- 양강. 기존 광원 강자 그대로 진입.

#### Sub-area 4: Optical Circuit Switch (OCS) ★★ 신생
- Lumentum 외부 공급 pure-play, $400M+ backlog, $100M/q 목표 (2026 EOY).
- Google 자체 (외부 미공급), Calient 비상장.
- → 상장사 alpha 는 사실상 Lumentum 만.

#### Sub-area 5: 모듈 (commoditization)
- Coherent (InnoLight 통합 후 모듈 1위), Lumentum 자체 모듈
- AAOI (미국 자국 정책 수혜, 시총 ~$2B, 변동성 큼)
- 중국 Eoptolink·HG Genuine·Hisense
- 오이솔루션 (KR) — commoditization 압박 직격탄

#### Sub-area 6: 한국 transmission (매우 약함)
- 오이솔루션 (138080): KR 1위지만 *글로벌 EML 광원 공급망 종속*
- 라이팩 (비상장) — 모듈 소형
- 인텔리안테크 (189300) — 위성 안테나 (광인터커넥트 아님, 별도 영역)
- → 본인 매수 권장 안함

---

## 6. 병목 식별 (Step 3)

### 6.1 현재 병목

| 병목 | 영향 | 수혜자 |
|------|-----|------|
| InP wafer capa | 광원 lead time 6+ 개월 | Lumentum, Coherent, IQE, Sumitomo |
| 6-inch InP 양산 | 효율 4× → margin expansion | Lumentum (San Jose), Coherent (Sherman+Tarfala) |
| 200G/lane EML | 1.6T 트랜시버 본격 ramp | Lumentum (50~60%) |
| CPO 검증·인증 시간 | hyperscaler 채택 지연 | NVIDIA·Broadcom·Marvell |

### 6.2 다음 병목 ★ 투자 핵심

| 병목 | 등장 시점 | 수혜자 |
|------|---------|------|
| TSMC COUPE 패키징 capa | 2027~2028 본격 | TSMC, ASE·Amkor (간접) |
| 400G/lane EML (3.2T 용) | 2027 후반~ | Coherent (이미 award), Lumentum |
| CW Laser for CPO 양산 | 2026 후반~ | Coherent 400mW, Lumentum ultra-high-power |
| Scale-up chip-to-chip 광 인터커넥트 | 2027~2028 | Marvell (Celestial), 비상장 |
| OCS hyperscale 확산 | 2026~2027 | Lumentum (외부 공급 유일) |

### 6.3 컨센서스 vs 본인 뷰의 갭

**컨센서스**: "CPO 가 모든 걸 바꾼다" → 2026 CPO 종목 다 매수. Lumentum 1년 +966% = 다 반영.

**본인 뷰**:
- CPO 본격 양산은 2027~2028. 그 전까지 800G·1.6T pluggable 이 매출의 본체.
- 광원 (EML/InP) 이 진짜 알파. CPO 든 pluggable 이든 광원은 필요. capa 2026~2027 supply-constrained.
- Marvell 이 valuation 측면에서 가장 매력 (YTD -18%, Celestial 통합 부담 일시 압축).
- OCS 가 hidden alpha — Lumentum 만 외부 공급. $400M backlog, 18개월 전 거의 0.

### 6.4 Next Wave Deep Analysis ★★★ 본인 진짜 알파

> **본인 메모**: "next-bottleneck identification, not current bottleneck confirmation". 광원 (COHR·LITE) 은 *over-known + 과열 valuation*. 진짜 alpha 는 **병목이 옮겨가는 자리**. 3개 선정 — FAU 패키징, DCI Coherent, AOS.

---

#### Next Wave 1: FAU (Fiber Array Unit) 패키징 ★★★ 가장 가까운 next wave

**왜 next wave 인가**
- CPO·NPO (Near-Packaged Optics) 가 본격화되면 *광 fiber 를 chip 에 정렬·접속하는 단계* 가 새 병목.
- FAU = N개 광섬유를 sub-micron 정밀도로 PIC chip 의 grating coupler 에 정합 + 영구 접착하는 부품.
- 800G·1.6T pluggable 도 FAU 필요하지만, **CPO 는 channel 수 폭증 (32~64 fiber/engine)** 으로 FAU 수요가 *수십 배* 증가.
- 단가 $200~500/FAU, CPO module 당 8~16개. 광원 (EML) 보다 *단위 매출 비중이 작지만 양은 폭증*.
- *광원 capa 풀린 후 (2027~) 다음 capa 제약은 FAU 다*.

**병목 메커니즘**
- 정렬 정밀도 ±0.5 μm 이하 (sub-micron) — *수작업 비중 여전히 높음*. 자동화 ramp 진행 중.
- 접착제 (epoxy) 신뢰성 — 고온 (CPO 환경 100℃+) 장기 안정성 critical.
- *수동 정렬 → 능동 정렬 (active alignment) → 패시브 정렬* 자동화 step-by-step.

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Furukawa Electric (5801.T)** | 일본 | 광 부품 종합 (FAU·CW Laser·fiber). 데이터센터 비중 증가 | A — 일본 대형, 안정 |
| **AFL (Fujikura 자회사, 5803.T)** | 일본 | FAU·fiber·접속 부품 | A — Fujikura 통해 진입 |
| Browave (3494.TW) | 대만 | FAU·optical sub-assembly, 시총 작음 | B — 변동성 |
| **POET Technologies (POET)** | US/CA | Optical Interposer 가 *FAU 우회* 시도 (chip 내 통합) | C — 시총 $400M, 매우 변동 |
| Coherent (COHR) | US | FAU 자체 일부 (수직통합) | 이미 광원 영역 매수 |
| Lumentum (LITE) | US | FAU 자체 일부 (수직통합) | 이미 광원 영역 매수 |
| **Senko (비상장 일본)** | 일본 | 광 connector·FAU 1위, 비상장 | n/a — IPO 시그널 모니터링 |

**한국**
- 라이팩 (비상장) — 광 connector·FAU 일부
- 광림 (비상장) — photonics device
- 한국정보통신 (025770) — 다중 (FAU 가 본업 아님)
- → **상장 알파 약함**. 본인은 *Furukawa·Fujikura 등 일본 종목 진입 검토*.

**Timing & Catalyst**
- 2026 후반: TSMC COUPE AMD 양산 진입 → FAU 수요 본격 시그널
- 2027: NVIDIA Spectrum-X·Quantum-X 본격화 → FAU capa 부족 노출
- 2027~2028: FAU pure-play 가격·매출 가속

**모니터링**
- TSMC COUPE AMD launch 일정 → 직접 trigger
- Furukawa·Fujikura·Browave 분기 매출 데이터센터 segment
- FAU 자동화 progress (active → passive alignment 전환)
- Senko IPO 시그널

**리스크**
- POET Optical Interposer 가 *FAU 우회* 성공 → FAU pure-play 약화 (단 가능성 낮음, POET 양산 진척 더딤)
- 광원 (EML) capa 빨리 풀리면 FAU 병목 부각 늦춰짐

---

#### Next Wave 2: DCI Coherent (800ZR·1.6T ZR+) ★★ 매출 가속 직진

**왜 next wave 인가**
- **DCI (Data Center Interconnect) = 데이터센터들 *간* 광 연결** (10~600+ km). 동일 데이터센터 *내부* 인터커넥트와 다른 시장.
- AI 가속으로 *멀티-DC 분산 학습* 폭증 → DCI 트래픽 폭증.
- 기존 ZR (80km) → ZR+ (400~600km) → 800ZR (800G, 코히어런트 광) 가속.
- **1.6T ZR+** 가 2026~2027 본격 ramp. 800G ZR 보다 GM 높음 (early-cycle ASP).
- 코히어런트 광 = DSP + 변조기 (Modulator) + 광원 + receiver 통합 모듈. **DSP·Modulator 가 핵심 가치**.
- *광원 자체보다 시스템 통합·DSP 가 진짜 알파* 자리.

**병목 메커니즘**
- Coherent DSP = 매우 복잡한 ASIC (TSMC 7nm 이하). 신규 진입 어려움.
- 변조기 (Mach-Zehnder Modulator) 대형화·통합 — 실리콘 포토닉스 통합 가속.
- TBN (Tunable Laser) — 일부만 공급 (Lumentum + 일부).

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Marvell (MRVL)** | US | **COLORZ ZR/ZR+** 시리즈, Rockley IP, Coherent DSP | **A — 이미 1순위 (Celestial 도 동일 종목 노출)** |
| **Cisco (CSCO)** | US | Acacia 인수 후 DSP·코히어런트 module 다중 | B — DCI 비중 적지만 안정 |
| **Coherent (COHR)** | US | DCI 모듈 (InnoLight 통합) | 이미 광원 영역 매수 |
| **Lumentum (LITE)** | US | narrow-line laser (DCI ZR+ 핵심), 6 분기 연속 증가 | 이미 광원 영역 매수 |
| **Ciena (CIEN)** | US | DCI 시스템·DSP, 시총 ~$10B | **A — pure-play 가까움** |
| NeoPhotonics (Coherent 인수됨) | - | - | n/a |
| InPhi (Marvell 인수됨) | - | - | n/a (MRVL 통해) |

**한국**
- 직접 노출 거의 없음. *글로벌 종목 중심*.

**Timing & Catalyst**
- 2026: 800ZR 본격 양산, 1.6T ZR+ 샘플링
- 2027: 1.6T ZR+ 본격 ramp
- 빅테크 멀티-DC 분산 학습 가속이 직접 trigger

**모니터링**
- Marvell COLORZ 매출 (Q-by-Q) → P1
- Ciena 분기 DCI segment → P1
- Lumentum narrow-line laser 매출 → P1
- 빅테크 (Microsoft·Google·Meta) 멀티-DC 학습 발표 → P2

**숨겨진 매력 — Ciena (CIEN)**
- 시총 ~$10B (Marvell·Coherent 보다 작음)
- DCI pure-play 에 가장 가까움. WaveLogic DSP 자체 (Coherent DSP 시장 점유 상위)
- AI 가속 DCI 수요 직접 노출
- valuation 상대적 저평가 (P/E ~25x)
- **본인 매수 우선순위 4~5순위로 추가 검토**

**리스크**
- DCI 양산이 빅테크 자체 fiber 부설 (dark fiber lease)로 *우회* 가능성
- 1.6T ZR+ 양산 지연 (TSMC 7nm capa 경쟁)

---

#### Next Wave 3: All-Optical Switch (AOS) ★ 임팩트 가장 크지만 timing 더 멀음

**왜 next wave 인가**
- **AOS = 광 → 전기 → 광 변환 *없이* 광 자체로 routing**. OCS (Optical Circuit Switch) 보다 *더 깊은 layer*.
- OCS = MEMS mirror 기반, **mm-second 단위 reconfig**. AOS = ns 단위 *packet-level* 광 switching.
- NVIDIA Spectrum-X·Quantum-X Photonics 가 2025 GTC 에서 *photonic switch* 발표 = AOS catalyst.
- AOS 가 본격화되면 **scale-up (rack 내)** 인터커넥트가 *근본 재편*. 기존 electrical switch 까지 광으로 대체.
- Scale-out (rack↔rack) 도 결국 AOS 로 전환 가능성.

**병목 메커니즘**
- Photonic IC + 외부 광원 + control electronics 통합 — *완전 새로운 칩 카테고리*
- TSMC COUPE 또는 자체 fab 필요
- 검증·인증 시간 매우 김 (3~5년+)

**상장 alpha (매우 약함)**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **NVIDIA (NVDA)** | US | Spectrum-X·Quantum-X Photonic Switch — 자체 통합 | AI Foundation 중복 |
| **Marvell (MRVL)** | US | Celestial Photonic Fabric 일부 노출 | 이미 매수 |
| **Coherent (COHR)** | US | photonic switch 부품 일부 | 이미 매수 |
| Lumentum (LITE) | US | OCS 는 있으나 AOS 직접 노출 약함 | 이미 매수 |
| Calient (비상장) | US | OCS pure-play, AOS 진입 시도 | n/a |
| **Ayar Labs (비상장)** | US | TeraPHY chiplet optics — *간접 AOS 토대* | IPO 2026~2027 모니터링 |
| **Lightmatter (비상장)** | US | Passage photonic fabric — *AOS 가까운 비상장* | IPO 2026~2027 모니터링 |
| Lightelligence (비상장) | US | photonic AI computing — AOS 인접 | IPO 시그널 |
| Q.ant (비상장 독일) | EU | photonic computing | 비상장 |

**한국**
- 직접 노출 없음

**Timing & Catalyst**
- 2026~2027: NVIDIA photonic switch 양산 진입 신호
- 2027~2028: AOS 본격 catalyst
- Lightmatter·Ayar Labs IPO 가 *AOS 영역 자금 본격 유입* trigger

**모니터링**
- NVIDIA Spectrum-X·Quantum-X Photonic Switch 양산 일정 → P1
- Lightmatter·Ayar Labs IPO 발표 → P1 (catalyst)
- Celestial Photonic Fabric 매출 시작 (FY28 2H) → P1
- 빅테크 (Microsoft·Google·Meta) photonic switch 채택 발표 → P2

**진입 전략**
- 직접 alpha 매우 약함 → **현재 단계 추가 매수 종목 없음**
- Lightmatter·Ayar Labs IPO 시 *상장 즉시 매수 검토 후보*
- NVIDIA·Marvell 이 *간접 노출* 이지만 이미 다른 thesis 로 보유

**리스크**
- AOS 양산 일정이 5년+ 지연될 가능성 (전통적으로 photonic 기술 양산 어려움)
- NVIDIA 자체 통합으로 *상장 supplier alpha 약화* 가능성

---

### 6.5 Next Wave 종합 — 본인 진입 전략

**우선순위 (Timing + 상장 alpha 양쪽 고려)**

| 순위 | Next Wave | Timing | 핵심 종목 | 비중 |
|-----|---------|--------|---------|-----|
| 1 | **DCI Coherent (Ciena)** | 2026~ 본격 | **Ciena (CIEN)** | 1~2% (4순위 신규) |
| 2 | **FAU 패키징** | 2026 후반~2027 | **Furukawa (5801.T)** | 1~2% (위성 일본) |
| 3 | **AOS** | 2027~2028 | Lightmatter·Ayar Labs IPO wait | 0% (catalyst wait) |

**광인터커넥트 영역 종합 매수 우선순위 업데이트**

1. **Coherent (COHR)** — 광원 1위, 즉시 분할 매수
2. **Marvell (MRVL)** — 저평가 + DCI + Celestial, 즉시 분할 매수
3. **Lumentum (LITE)** — 광원 EML 50~60%, *조정 wait*
4. **Ciena (CIEN)** ← **Next wave 신규 추가, DCI pure-play 저평가**
5. **Furukawa Electric (5801.T)** ← **Next wave 신규 추가, FAU 일본 노출**
6. MACOM (MTSI) — 위성
7. AAOI — 위성 (미국 정책)

**모니터링 watchlist (현재 매수 X, 추후 catalyst 발생 시 진입)**
- Lightmatter (비상장 IPO 모니터링)
- Ayar Labs (비상장 IPO 모니터링)
- POET Technologies (FAU 우회 시도, 양산 시그널)
- Senko (비상장 일본, FAU 1위)
- Fujikura (5803.T), Browave (3494.TW)
- GlobalFoundries (GFS) — PIC foundry (next-next wave, 보류)

---

## 7. 자금 흐름 시그널 (Step 4)

### 7.1 관련 ETF

| 티커 | 시장 | 비중 |
|------|------|----|
| SOXX | US | iShares Semi (NVDA·AVGO·MRVL·LITE·COHR 포함) — 중간 |
| SMH | US | VanEck Semi — 중간 |
| KODEX 미국반도체 | KR | SOXX 추종 — 중간 |
| TIGER 미국나스닥100 | KR | 간접 — 약함 |

→ ETF 노출 약함. **직접 종목 매수** 가 합리적.

### 7.2 추적 지표 (대시보드)

**P1 (분기 필수)**
- NVIDIA·Broadcom·Marvell 분기 매출 + CPO 가이던스
- Coherent·Lumentum 분기 매출 + EML segment + book-to-bill
- Lumentum InP fab 확장 진척, Coherent 6-inch InP 진척
- Marvell-Celestial 통합 + Photonic Fabric 매출 시작 (FY2028 2H~)
- 800G·1.6T 트랜시버 가격 트렌드 (LightCounting reports)

**P2 (분기 모니터링)**
- TSMC COUPE 양산 진척 + AMD CPO product launch
- AAOI 매출·정책 수혜
- OCS 매출 (Lumentum)
- 200G/lane EML 가격·점유
- 빅테크 CapEx 분기 가이던스

**P3 (지속)**
- 중국 자체 InP·EML 개발 시그널
- 오이솔루션 매출 (commoditization 진척 확인)
- Ayar Labs·Lightmatter IPO 신호
- photonic computing (Lightmatter·Q.ant) 진척

### 7.3 Startup Landscape (L2 신호)

| 스타트업 | 영역 | 누적 펀딩 | IPO 가능성 |
|---------|------|---------|---------|
| Ayar Labs | TeraPHY chiplet optics | $300M+ | 2026~2027 |
| Lightmatter | Passage photonic fabric | $600M+ | 2026~2027 |
| Celestial AI | Photonic Fabric | $500M (Marvell 인수됨) | N/A |
| Calient | OCS | 비공개 | 낮음 |

→ Ayar Labs·Lightmatter IPO 가 다음 catalyst.

---

## 8. 종목 매핑 (Step 5)

### 8.1 글로벌 종목

| 티커 | 기업 | 영역 | 시총 | P/S (대략) | Tier |
|------|------|-----|-----|---------|------|
| **COHR** | Coherent | L3+L4+L6 | ~$25B | ~3x (FY26) | **A 1순위** |
| **LITE** | Lumentum | L3+L6+L7 | ~$18B | ~7x | **A 2순위 (조정 wait)** |
| **MRVL** | Marvell | L4+L8 (Celestial) | ~$70B | ~7x | **A 3순위 (저평가)** |
| MTSI | MACOM | L3 (RF+photonics) | ~$11B | ~12x | B |
| NVDA | NVIDIA | L4+L8 | $4T+ | ~25x | AI Foundation 중복 |
| AVGO | Broadcom | L4+L8 | $1.5T+ | ~20x | AI Foundation 중복 |
| **CIEN** | **Ciena** | **DCI Coherent DSP·WaveLogic** | **~$10B** | **P/E ~25x** | **A 4순위 (next wave)** |
| **5801.T** | **Furukawa Electric** | **FAU + 광 부품 종합 (일본)** | **~¥1T** | **P/E ~15x** | **A 5순위 (next wave 위성)** |
| AAOI | Applied Optoelectronics | L6 (US 정책) | ~$2B | ~6x | B (위성) |
| POET | POET Technologies | L4 (소형, FAU 우회 시도) | ~$400M | n/a | C (변동성) |
| 5803.T | Fujikura (AFL) | FAU·fiber | ~¥800B | ~12x | C (위성, 일본) |
| 3494.TW | Browave | FAU optical sub-assembly | 소형 | n/a | C (변동성) |
| IQE.L | IQE plc | L1 InP wafer | ~£300M | 변동 | C |
| AIXA.DE | Aixtron | L2 MOCVD | ~€2B | ~6x | C |

### 8.2 한국 종목 (Korea transmission)

| 티커 | 기업 | 영역 | 시총 | Tier |
|------|------|-----|-----|------|
| 138080 | 오이솔루션 | L6 모듈 KR 1위 | ~3,000~5,000억원 | C (매수 권장 안함) |

→ 한국 직접 노출 약함. 본인 미국 종목 중심.

### 8.3 각 종목의 Valuation Gate

**Coherent (COHR) — 1순위**
- 광원 + 모듈 + InP fab 수직통합 1위
- DC&Comm +41% yoy, $1,362M Q3 FY26
- 6-inch InP 80% → 2H 2026 doubling
- NVIDIA $2B 지분 + 다년 합의
- 1.6T module GM > 800G
- Book-to-bill > 4× (이례적 visibility)
- **진입 전략**: 분할 매수 3~6개월 (현재가 → -10% → -20% 단계별)

**Marvell (MRVL) — 3순위 (저평가 우선 검토)**
- Celestial AI 인수 $5.5B (2025-12)
- Photonic Fabric 매출 FY2028 2H~, $500M run-rate (FY28 Q4), $1B (FY29 Q4)
- Photonics + Custom XPU (AWS·MS) 다중
- Q3 FY26 +37% yoy
- **YTD -18% = 진입 매력 가장 큼**
- **진입 전략**: 즉시 분할 매수 1~3개월

**Lumentum (LITE) — 2순위 (조정 wait)**
- EML 50~60%
- NVIDIA $2B + ultra-high-power CW order
- OCS pure-play
- FY26 Q3 가이던스 $780~830M (+65% yoy)
- **1년 +966% = 과열**
- **진입 전략**: 10~15% 조정 시 진입

**Ciena (CIEN) — 4순위 신규 (Next Wave: DCI Coherent)**
- WaveLogic DSP 자체 — Coherent DSP 시장 점유 상위
- DCI pure-play 에 가장 가까움 (시스템·DSP·코히어런트 module)
- AI 가속 멀티-DC 분산 학습 직접 노출
- 시총 ~$10B (Marvell·Coherent 보다 작음)
- 1.6T ZR+ 본격 ramp 시 매출 가속 예상
- **valuation 저평가 (P/E ~25x)** — Coherent·Lumentum 대비 *덜 알려짐*
- **진입 전략**: 분할 매수 2~4개월, 1.6T ZR+ 양산 시그널 시 가속

**Furukawa Electric (5801.T) — 5순위 신규 (Next Wave: FAU)**
- 일본 광 부품 종합 (FAU·CW Laser·fiber)
- 데이터센터 비중 점진 증가
- 시총 ~¥1T (안정 대형주)
- TSMC COUPE AMD 양산 → FAU 수요 시그널 시 매출 가속
- **진입 전략**: 위성 자산 (1~2% 비중), TSMC COUPE 일정 trigger 시 진입
- *환율 hedge*: 엔화 노출

**MACOM (MTSI) — 6순위 위성**
- 광원 + RF 다중, Coherent·Lumentum 보다 덜 pure-play
- 시장 조정 시 진입

**AAOI — 7순위 위성**
- 미국 자국 제조, CHIPS Act 수혜
- 시총 ~$2B, 변동성 큼
- 3~5% 비중

---

## 9. 모니터링 트리거

**즉시 (분기 실적)**
- Coherent 분기 (DC&Comm 매출, book-to-bill, InP) → P1
- Lumentum 분기 (EML, OCS backlog, narrow-line laser) → P1
- Marvell 분기 + Celestial 통합 + Photonic Fabric 매출 시작 → P1
- NVIDIA·Broadcom 분기 + CPO 가이던스 → P1

**정책·M&A**
- Marvell-Celestial closing (2026 Q1) → P1
- 미국 photonics CHIPS Act 자금 → P2
- 미·중 광인터커넥트 수출 통제 → P2
- 빅테크 자체 photonics 시그널 → P3

**기술**
- AMD CPO product launch (TSMC COUPE) → P1
- NVIDIA Spectrum-X·Quantum-X 양산 → P1
- 3.2T 트랜시버 샘플링 → P2
- LPO (Linear Pluggable Optics) 양산 → P2 (CPO 우회 가능성)
- VCSEL 1.6T 양산 (Coherent 2H 2026) → P2

**IPO·신규**
- Ayar Labs IPO 발표 → P1
- Lightmatter IPO 발표 → P1
- POET 양산·매출 시작 → P2

---

## 10. 리스크

**기술**
- LPO 양산 — CPO 우회. 광원 수요 유지되나 CPO 시스템 종목 영향.
- VCSEL 1.6T+ 양산 — EML 잠식. 단 Coherent·Lumentum 모두 VCSEL 보유.
- NVIDIA 자체 광원 개발 — 가능성 매우 낮음.

**시장**
- 빅테크 AI CapEx 둔화 (-20%+) — 직격탄
- 광원 종목 과열 조정 — Lumentum -10~30% 가능
- Marvell-Celestial 통합 지연 — Photonic Fabric 매출 지연
- CPO 표준화 지연 — pluggable 더 길게 유지 (광원 수요는 유지)

**지정학**
- 중국 자체 InP·EML 가속 — DeepSeek 식 시그널 시 일시 압박
- 미국 자국 photonics 정책 강화 — AAOI 수혜, 한국 transmission 약화

**수급**
- InP wafer 차질 (Sumitomo·IQE 사고) — 광원 lead time 폭증
- TSMC COUPE 일정 지연 — CPO 양산 6개월+ 지연

**본인 포트폴리오 — AI 인프라 중복 노출**
- 광인터커넥트 + AI DC 전력 + AI Foundation + 원자력 + 냉각 + 전력반도체 등이 *빅테크 CapEx 단일 변수* 노출 중첩
- → 광인터커넥트 + AI DC 전력 + AI Foundation 합산 *25~35% 상한*

---

## 11. 매크로 변수 민감도

| 변수 | 영향 | 메커니즘 |
|------|------|--------|
| Fed 금리 인하 | ++ | 성장주 멀티플 expansion (P/S 7~25x 직접) |
| 미중 갈등 강화 | + | 미국 자국 photonics fab 정책 (AAOI·Coherent·Lumentum) |
| 달러 강세 | − | 해외 매출 환산 감소 (COHR·LITE 약 40% 해외) |
| 빅테크 AI CapEx 둔화 | −− | 직접 |
| AI 규제 (EU AI Act) | 중립 | 인프라보다 application 영향 |
| 한국 원화 강세 | − | 미국 종목 매수 환차익 감소 |
| Treasury 금리 상승 | − | 성장주 멀티플 압축 |

---

## 12. 본인 의사결정 메모

### 최종 매수 우선순위 (Next Wave 반영)
1. **Coherent (COHR)** — 가장 안정적, 즉시 분할 매수
2. **Marvell (MRVL)** — 상대적 저평가, 즉시 분할 매수
3. **Lumentum (LITE)** — 과열 부담, 10~15% 조정 wait
4. **Ciena (CIEN)** ← **Next wave: DCI Coherent 저평가 신규**
5. **Furukawa Electric (5801.T)** ← **Next wave: FAU 일본 위성**

### 비중 가이드 (AI 인프라 중복 고려)
- 본 영역 전체: **포트폴리오의 5~10%**
- 본 영역 + AI DC 전력 + AI Foundation 합산: **25~35% 상한**
- 종목별: COHR + MRVL 각 2~3%, LITE 1~2%, **CIEN 1~2% (신규)**, **Furukawa 1% (위성 신규)**

### 진입 timing
- 즉시: COHR (분할), MRVL (분할), **CIEN (분할 next wave)**
- 조정 wait: LITE (10~15% 조정 시)
- Catalyst wait: Furukawa (TSMC COUPE AMD launch 시그널), Lightmatter·Ayar Labs IPO
- 위성: MACOM, AAOI — 시장 조정 시

### 핵심 trade-off
- 광원 (안전·over-known) vs Next wave (덜 알려짐·진짜 alpha)
- 과열 (LITE) vs 저평가 (MRVL·CIEN)
- 상장 (COHR·LITE·MRVL·CIEN) vs 비상장 catalyst wait (Lightmatter·Ayar·Senko)
- AI 인프라 중복 노출 인지

### Next Wave 모니터링 watchlist
- Lightmatter (비상장 IPO 모니터링)
- Ayar Labs (비상장 IPO 모니터링)
- POET Technologies (FAU 우회 시도, 양산 시그널)
- Senko (비상장 일본 FAU 1위, IPO 시그널)
- Fujikura (5803.T), Browave (3494.TW)
- GlobalFoundries (GFS) — PIC foundry (next-next wave 보류)

### Track 4 등재 후보
- Coherent (COHR) — 1순위 등재
- Marvell (MRVL) — 2순위 등재
- **Ciena (CIEN) — 3순위 등재 (next wave)**
- Lumentum (LITE) — 조정 후 등재
- **Furukawa Electric (5801.T) — 위성 등재 (next wave)**

---

## 13. 업데이트 로그

| 날짜 | 변경 |
|------|------|
| 2026-05-24 | 최초 작성 (Tier 1 깊이). TAM 4 + Moat 4 + Capital 4 = 12/15. 시차 A5 B4 C4 = +5 (Strong entry). Tier 1 확정. 매수 우선순위: COHR > MRVL > LITE. Coherent Q3 FY26 DC&Comm $1,362M (+41% yoy, book-to-bill >4×), Lumentum FY26 Q3 가이던스 $780-830M (+65% yoy, EML 50-60% 점유), Marvell Q3 FY26 $2.1B (+37%, Celestial $5.5B 인수 2026 Q1 closing), NVIDIA $2B 각 COHR+LITE (2026-03-02), S&P 500 편입 반영. |
| 2026-05-24 | **Next Wave Deep Analysis 추가 (6.4·6.5)**. 광원 over-known·과열 인식, 진짜 alpha 는 *병목 이동*. 3개 next wave 선정: (1) FAU 패키징 (2026~2027, Furukawa·Fujikura·Senko·POET), (2) DCI Coherent 800ZR·1.6T ZR+ (2026~, Ciena·Marvell COLORZ·Coherent), (3) AOS (2027~2028, Lightmatter·Ayar Labs IPO wait). 매수 우선순위 업데이트: COHR > MRVL > LITE > **CIEN (신규 4순위 next wave)** > **Furukawa (신규 5순위 위성)**. Next wave 모니터링 watchlist: Lightmatter·Ayar·POET·Senko·GFS. |


---

# ═══════════════════════════════════════════════════
# KR Transmission Boost — KR pure-play thorough 보강
# ═══════════════════════════════════════════════════

# 광인터커넥트 (CPO) — KR Transmission Boost (v2.3 추가)

> **Base document**: optical-interconnect-cpo.md (2026-05-24, 40KB)
> **Boost 작성일**: 2026-05-24
> **변경 사항**: KR pure-play thorough 보강 (KR 광원·FAU·packaging 추가)

---

## 5.3 Sub-area X: 한국 — *KR pure-play thorough* (보강·교체)

> v2.3 KR transmission 강화. 기존 본문에 약했던 KR 광인터커넥트 종목 thorough 보강. **K-광 부품 (오이솔루션·라이파이텍·옵트론텍·옵티시스) + 광 산업 KR 정책**.

### KR 상장 pure-play

| 티커 | 기업 | 영역 | 시총 | 핵심 thesis | Tier |
|------|------|-----|-----|----------|------|
| **138080** | **오이솔루션** ★ | L3 광 transceiver·CWDM·DWDM | 3,000~5,000억원 | **K-광 transceiver 1위**, 800G·1.6T transceiver 진입. NVDA·Coherent 등 글로벌 공급 추진 | **A KR 1순위** |
| **425500** | **라이파이텍 (LiPath)** | L3 광부품·CPO 패키징·active optic | 1,500~3,000억원 | CPO 패키징 + active optic. 변동성 큼 | **B KR 2순위 (변동성)** |
| **082210** | **옵트론텍** | L3 광 sensor·iris·camera | 3,000~4,000억원 | 광 sensor + 자율 cross. 변동성 | **B KR 3순위** |
| **125210** | **옵티시스** | L3 광 케이블 (Active Optical Cable·AOC) | 1,500~2,500억원 | AOC + 데이터센터 광케이블 | **B KR 4순위** |
| **000990** | **DB하이텍** | L3 8-inch foundry (전력반도체·일부 광) | 3~4조원 | 전력반도체 cross | 전력반도체 중복 |
| **090460** | **비에이치** | L3 PCB·flex (AI 서버 cross) | 1조원+ | AI 서버 PCB | AI Foundation cross |
| **042700** | **한미반도체** | L3 HBM TC bonder + 일부 광 | 17~22조원 | HBM cross + 일부 광패키징 | 반도체 cross |
| **007660** | **이수페타시스** | L3 AI 서버 고밀도 PCB | 4~5조원 | AI 서버 PCB | AI Foundation cross |

### KR 비상장 / IPO 후보

- **에이디알 (ADR)** — 광인터커넥트 패키지 부품 (비상장)
- **포톤웨이브 (Photon Wave)** — 광 모듈 (비상장)
- **에프케이아이엠 (FKIM)** — 광 통신 부품 (비상장)
- 신광인터컨넥트·KOC·우리이앤엘 — 위성

### KR 정책 trigger

- **K-반도체·AI 인프라 자체 build-out 가속** → KR 광 부품 수요 증가
- **삼성·SK 데이터센터 + 미국 fab** → 광 인터커넥트 수요 직접

### 진입 전략 (KR 우선순위)

- **KR 1순위: 오이솔루션 (138080)** — K-광 transceiver 1위 + 800G/1.6T 진입
- **KR 2순위: 라이파이텍 (425500)** — CPO 패키징 변동성 (분할 매수)
- **KR 3순위 위성**: 옵트론텍·옵티시스
- 반도체·AI Foundation 영역 cross: 한미반도체·이수페타시스·비에이치

---

## 8.2 한국 종목 보강

| 티커 | 기업 | 영역 | 시총 | Tier | 매수 우선순위 |
|------|------|-----|-----|------|-----------|
| **138080** | **오이솔루션** ★ | L3 광 transceiver 1위 | 3,000~5,000억원 | **A** | **KR 1순위** |
| **425500** | **라이파이텍** | L3 CPO 패키징 변동성 | 1,500~3,000억원 | **B** | KR 2순위 변동성 |
| 082210 | 옵트론텍 | L3 광 sensor | 3,000~4,000억원 | **B** | KR 3순위 |
| 125210 | 옵티시스 | L3 AOC 광케이블 | 1,500~2,500억원 | **B** | KR 4순위 |
| 042700 | 한미반도체 | HBM TC bonder + 일부 광 | 17~22조원 | A | 반도체 cross |
| 007660 | 이수페타시스 | AI 서버 PCB | 4~5조원 | A | AI Foundation cross |

---

## 12 비중 분배 권장 (KR 보강 반영)

- **글로벌 80% : KR 20%** (기존 본문 유지)
- 종목별:
  - COHR·MRVL·LITE·CIEN·Furukawa = 글로벌 본문 매수
  - 오이솔루션 0.5~1%, 라이파이텍 0.3~0.5% (변동성)
  - 옵트론텍·옵티시스 위성 합산 0.3%

### Cross-area
- 한미반도체·이수페타시스 = 반도체 영역에서 매수
- DB하이텍·동운아나텍 = 전력반도체 cross

---

## 업데이트 로그 — KR Boost (v2.3)

| 날짜 | 변경 |
|------|------|
| 2026-05-24 | KR boost retrofit. **오이솔루션 (138080) KR 1위 광 transceiver, 라이파이텍 (425500) CPO 패키징, 옵트론텍 (082210), 옵티시스 (125210), 한미반도체·이수페타시스 반도체 cross** 추가. 비상장: 에이디알·포톤웨이브·FKIM 모니터링. KR 비중 분배 권장 20% 유지. |

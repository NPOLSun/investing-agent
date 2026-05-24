# 데이터센터 냉각 — Tier 2 Deep Dive (Tier 1 깊이)

> **Trigger**: Vertiv backlog $15B (+109% yoy, Q4 2025), Q1 2026 매출 $2.65B, EPS +83% yoy. Eaton 이 $9.5B 로 Boyd Thermal 인수 (2026-03), 2026 매출 $1.5~1.7B 기여 예상. Modine FY26 Q3 데이터센터 +78% yoy. **liquid cooling 이 데이터센터 표준 전환** — AI rack 100kW+ 시대의 *필수 인프라*. 본인 메모상 cross-sector bottleneck 으로 식별.
> **Linked methodology**: methodology_v2.1.md

---

## 0. 메타 정보

| 항목 | 값 |
|------|----|
| 작성일 | 2026-05-24 |
| 최근 갱신 | 2026-05-24 |
| 다음 정기 갱신 | 2026-07-01 |
| 시계 분류 | Core (1.5~2.5년) + 사이클 부분 |
| Tier | 2 (Tier 1 깊이) |
| Confidence | High |
| 트랙 | L1A + KR 일부 |

---

## 1. 한 줄 요약 + 핵심 가설

### 한 줄 요약

> AI rack power density 가 *50kW → 100kW → 200kW* 로 폭증. 공랭 (air cooling) 의 *물리적 한계 (~40~50kW/rack)* 초과. liquid cooling 가 데이터센터 *표준 전환*. 알파 4개 층 — **Pure-play (Vertiv)**, **Diversified Industrial (Eaton·Schneider·nVent)**, **Specialty (Modine)**, **Materials/TIM (Henkel·Honeywell·Parker)**. Vertiv 47x P/E 부담 → *Modine·Eaton 상대 매력*. **Next wave 는 Immersion + PFAS-free Fluid + TIM + AI Cooling SW**.

### 핵심 가설

**가설 A — Air cooling 의 물리적 한계가 liquid cooling 강제**
- AI rack power density: 일반 cloud ~10kW → 현재 AI (H100·H200) 30~50kW → Blackwell GB200 NVL72 120kW → Rubin 200kW+ (2027~2028)
- 공랭 물리적 한계 ~40~50kW/rack. 이상은 liquid cooling 필수.
- liquid cooling 25~40%/년 가속 (cooling 시장 평균의 2배+)
- *모든 신규 AI 데이터센터*: liquid cooling 기본 (NVIDIA Reference Architecture)

**가설 B — Liquid cooling 4가지 방식, D2C 가 표준**
1. **D2C (Direct-to-Chip, cold plate)**: GPU·CPU 직접 냉각. **현재 표준 (2026 55% 점유)**. Vertiv·CoolIT·Asetek·Boyd 강.
2. **Rear-Door Heat Exchanger (RDHx)**: rack 뒷면 액냉. 기존 공랭 retrofit.
3. **Single-phase immersion**: 전체 서버 액체 침지. Submer·GRC·Modine 일부.
4. **Two-phase immersion**: 끓는점 활용. 최고 효율, 그러나 *PFAS 규제 부담* (3M Novec 철수, Chemours·Solvay 대체 개발).
- 표준은 D2C. Immersion 은 *틈새 + 신규 hyperscaler 일부* + *중동 사막 시장 (Abu Dhabi 150MW 2026 후반)*.

**가설 C — 상장사 알파 4개 층**

| 층 | 종목 | 매수 우선순위 |
|----|------|-----------|
| Pure-play (D2C + power 통합) | **Vertiv (VRT)** | A (47x P/E 부담, 분할) |
| Diversified (전력 + 냉각 통합) | **Eaton (ETN), Schneider (SU.PA), nVent (NVT)** | A |
| Specialty Cooling | **Modine (MOD)** | A (저평가 specialty) |
| Materials / TIM | Henkel·Honeywell·Parker·DuPont·3M | B (간접, **next wave 에서 deep**) |
| 한국 | 코오롱·LG·일부 유틸 | C (간접) |

**가설 D — Vertiv leadership 확정, valuation 매력 약함**
- Q1 2026 매출 $2.65B, EPS +83% yoy
- Backlog $15B+ (+109% yoy), book-to-bill 2.9x
- NVIDIA reference architecture co-development
- 2026 가이던스: 매출 $13.5~14.0B, +30% organic growth, 2029 OM 25%
- **그러나** 47x forward P/E, 1년 +250%. *valuation 매력 약*
- 분할 매수 + 조정 wait

**가설 E — Eaton-Boyd Thermal 인수 ($9.5B, 2026-03) = 즉시 1.5~1.7B 매출 기여**
- 전력 + 냉각 통합 (cross-sell)
- Boyd Thermal = D2C·CDU·cold plate 자산 즉시 확보
- Eaton P/E ~25x — *상대적 valuation 매력*
- 본인 전력 영역과 *이중 노출* 인지

**가설 F — Modine 이 hidden specialty alpha**
- FY26 Q3 데이터센터 매출 +78% yoy
- FY2026 매출 성장 가이던스 15~20% (상향)
- 시총 ~$6~8B (Vertiv 대비 저평가)
- 자동차 cooling 노하우 + DC 진입
- 단상 immersion 부분 진입

**가설 G — 한국 transmission 약함**
- LG전자 (066570) — chiller·HVAC 일부 (DC 비중 매우 작음)
- 신성ENG (011930), 신성델타테크 (065350) — HVAC 부품
- 코오롱인더스트리 (120110) — TIM polymer 일부 (next wave 관련)
- *한국 글로벌 채택 거의 없음* — 본인 미국·유럽 중심

### 기각 조건
- AI rack power density 폭증 둔화 (가능성 매우 낮음)
- liquid cooling 표준 분기 (D2C vs Immersion 양분) → 단 Vertiv·Boyd 균등 노출이 hedge
- 빅테크 자체 cooling 개발 (가능성 매우 낮음)
- PFAS·GWP 규제로 specific fluid 금지 → two-phase immersion 약화 가능 (D2C 영향 없음)

---

## 2. 4가지 잣대 채점

### 잣대 1: TAM

**점수: 3 / 5** (Major expansion, ×3~5)

- DC cooling 전체: 2025 ~$18B → 2030 ~$45B (CAGR 20%)
- Liquid cooling 단독: 2025 ~$4B → 2030 ~$25B (CAGR 35~40%)
- AI rack 비율 증가 시 전체의 60~70% 가 liquid
- Vertiv 본 영역 노출 ~80%, 시총 $50B+ → 본 영역 alpha 시총 ~$40B
- 5년 후 50B$ 수준

**Confidence**: High

### 잣대 2: Moat

**점수: 3 / 5** (Moderate reshuffle + 비가역 큼)

- **Vertiv NVIDIA reference architecture co-development** — 비가역 강, 5+년 lock-in
- Eaton-Boyd $9.5B M&A = 시장 재편 가속
- 신규 진입 어려움: hyperscaler 인증 1~2년, R&D + 자본
- Diversified (Eaton·Schneider·nVent) cross-sell 강
- Modine specialty = automotive 노하우 차별화
- 중국 침투 상대적 약함 (현지 hyperscaler 만)
- 비가역성: 정부 platform install 시 5~10년 lock-in

**Confidence**: Medium-High

### 잣대 3: Capital

**점수: 4 / 5** (Major capital 10~100B$+/년)

- 빅테크 AI CapEx 중 냉각 비중: 추정 *전체 8~12%*. $500B+ CapEx 의 5~10% = $25~50B/년
- Vertiv backlog $15B+ (12~18개월 forward revenue)
- M&A: Eaton-Boyd $9.5B (2026-03)
- 데이터센터 자체 capex 폭증 → 냉각 직접

**Confidence**: High

### ~~잣대 4: Tech~~ (폐기)

### 합산

| 트랙 | 점수 | 임계 |
|------|------|------|
| L1A | **10 / 15** | Tier 2 ≥ 9 ✅ |

→ **Tier 2 확정**, Tier 1 깊이 분석

---

## 3. A·B·C 시차 평가

### A 지표 (자본 유입) — **5 / 5**
- 빅테크 AI CapEx 분기 신기록
- Vertiv backlog $15B+ (+109% yoy)
- Eaton-Boyd $9.5B M&A
- Modine FY26 Q3 +78% yoy
- NVIDIA-Vertiv reference arch co-development

### B 지표 (실물 변화) — **5 / 5**
- Vertiv Q1 2026 매출 $2.65B, EPS +83% yoy, OM 20.8% (+430bp)
- Backlog $15B → 2026~2027 visibility 명확
- Modine FY26 Q3 데이터센터 +78% yoy
- Eaton Boyd 2026 매출 $1.5~1.7B 기여 예상
- liquid cooling 25~40%/년 가속
- GB200 NVL72 120kW liquid 표준

### C 지표 (가격 반영) — **4 / 5**
- Vertiv 1년 +250%, 47x forward P/E
- Eaton 25x P/E (Boyd 부분 반영)
- nVent ~30% DC 노출 일부 반영
- **Modine ~$6~8B 상대적 저평가**

### 시차 매력도 = A + B − C = **5 + 5 − 4 = +6 (Very strong entry)**

→ Modine·Eaton 상대 매력, Vertiv 분할 wait

---

## 4. 산업 메가트렌드 (Step 1)

### 4.1 수요 측

**단기 (12~18개월)**
- Blackwell GB200 NVL72 본격 출하: 120kW/rack liquid 표준
- D2C 표준화: 모든 신규 AI DC. Vertiv·Boyd·CoolIT·Asetek 다중
- RDHx hybrid: 기존 DC retrofit 채택
- 자율 cooling 관리 SW: 빅테크 + Vertiv·Schneider 자체

**중기 (2~4년)**
- Rubin·Rubin Ultra 200kW+/rack: 2027~2028
- Single-phase immersion: 일부 hyperscaler (MS·Meta 실험), 본격 양산 미정
- 사막·중동 immersion: Abu Dhabi 150MW (2026 후반), 사우디·UAE
- Sustainability 요구: water-positive (MS 약속), PUE 1.1 이하

**장기 (5~10년)**
- 양자컴 cryogenic
- 우주·해저 데이터센터 (Microsoft Natick 후속)

### 4.2 공급 측

**현재 병목 — liquid cooling 시스템 capa**
- Vertiv capa 확장 진행 (Eaton-Boyd 도 추가)
- D2C cold plate 정밀 가공 — lead time 6+ 개월
- CDU (Coolant Distribution Unit) — Vertiv·Schneider·Boyd
- Liquid fittings (Stäubli) — 정밀도 critical

**다음 병목 — 200kW+ rack 액침 fluid + Manifold**
- Dielectric fluid (3M 철수, Chemours·Solvay 대체) — *PFAS 규제* 직격탄
- Manifold·piping 누설 방지
- 냉각수 재활용 (water-positive)

**추가 병목 — TIM (Thermal Interface Material) — next wave deep**
- chip-cold plate 열전도 재료
- Henkel·Honeywell·3M·Parker·DuPont 다중
- 고성능 TIM 이 200kW+ rack critical path

### 4.3 정책·지정학 변수
- **물 사용 규제**: 텍사스·아리조나 가뭄 시 water 수요 제약
- **에너지 효율**: EU·US PUE 1.3 → 1.1 가속
- **PFAS·GWP 규제**: two-phase immersion fluid 제한 가속 (3M Novec 철수)
- **미·중 DC 견제**: Vertiv·Schneider 중국 매출 일부 영향
- **한국 정책 미흡**

---

## 5. 밸류체인 매핑 (Step 2)

### 5.1 다이어그램

```
[L1 Materials (TIM, Fluid, Coolant)] ★ next wave deep
  ├ TIM: Henkel Bergquist, Honeywell, Parker, DuPont, 3M
  ├ Dielectric Fluid (Immersion): 3M Fluorinert (철수), Chemours Opteon, Solvay, Shell, Cargill (next wave deep)
  └ Coolant (Water+Glycol): Dow, BASF
       ↓
[L2 Components]
  ├ Cold Plates (D2C): Boyd (Eaton 인수), CoolIT, Asetek, Aavid
  ├ CDU: Vertiv, Schneider, nVent, Boyd (Eaton)
  ├ Pumps·Manifold·Fittings: Stäubli (비상장), Parker, CPC (Eaton 자회사)
  └ Heat Exchangers: Vertiv, Schneider, Modine
       ↓
[L3 System / Integrated]
  ├ D2C 통합: Vertiv (VRT, 1위), Schneider (SU.PA), Eaton (Boyd), nVent
  ├ RDHx: Vertiv, Schneider, Modine
  ├ Single-phase Immersion: Submer (비상장), GRC (비상장), Asperitas, Modine 일부
  └ Two-phase Immersion: LiquidStack, ZutaCore, Iceotope (비상장)
       ↓
[L4 Diversified Industrial]
  ├ Eaton (ETN) — 전력+냉각
  ├ Schneider (SU.PA) — 전력+냉각+SW 1위
  ├ nVent (NVT) — DC 비중 30%
  ├ Honeywell (HON) — building auto + DC
  ├ Johnson Controls (JCI) — HVAC + DC
  └ Carrier (CARR) — HVAC + DC (진입 3~5년)
       ↓
[L5 End Customer]
  AWS, MS, Google, Meta, Oracle | Equinix, Digital Realty | CoreWeave, Crusoe | NVIDIA reference arch
```

### 5.2 레이어별 분석

| 레이어 | GM | 경쟁구도 | 중국 침투 | 진입장벽 | 본인 매력도 |
|--------|-----|---------|---------|---------|----------|
| L1 TIM/Fluid | 매우 높음 (40%+) | Henkel·Honeywell·3M·DuPont | 일부 | 화학 IP | **★★ next wave deep** |
| L2 Cold Plate | 중상 (25~35%) | Boyd·CoolIT·Asetek | 일부 | 정밀 가공 | 간접 (Eaton) |
| L2 CDU·Pump | 중상 (25~35%) | Vertiv·Schneider·Eaton·nVent | 약함 | 시스템+인증 | **★★** |
| L3 Pure-play | 중상 (20~25%) | Vertiv 1위 | 약함 | 매우 높음 | **★★★ (Modine 저평가)** |
| L3 Immersion | 중간 (회복기) | 비상장+Modine | 일부 | 기술 | **★ next wave** |
| L4 Diversified | 중간 (15~25%) | Eaton·Schneider·nVent·Honeywell·JCI·Carrier | 약함 | 규모 + cross-sell | **★★** |

### 5.3 하위 세분화

#### Sub-area 1: Pure-play (Vertiv) ★ — 가격 조정 wait
- **Vertiv (VRT)**: D2C·CDU·Rear-Door 다중. NVIDIA reference arch. Q1 2026 매출 $2.65B, EPS +83% yoy. Backlog $15B+. 2026 가이던스 $13.5~14.0B. 1년 +250%, **47x forward P/E 부담**.
- 분할 매수 + 조정 wait (10~20% 조정 시 진입)

#### Sub-area 2: Diversified Industrial ★★ — 안정 alpha
- **Eaton (ETN)**: Boyd 인수 $9.5B (2026-03), 2026 매출 $1.5~1.7B 기여. DC 25~30%. P/E 25x. 전력 영역 중복.
- **Schneider Electric (SU.PA)**: 글로벌 1위 (전력+냉각+SW). DC 24%. P/E 25x. 유로 hedge.
- **nVent (NVT)**: DC 30% (diversified 中 최고). NVIDIA 파트너십. 시총 ~$15B, P/E 22x.

#### Sub-area 3: Specialty Cooling ★★★ — hidden alpha
- **Modine (MOD)**: FY26 Q3 데이터센터 +78% yoy. FY2026 가이던스 15~20%. 시총 ~$6~8B. **Vertiv 대비 저평가**. 자동차 cooling 노하우 + DC. **본인 매수 매력 큼**

#### Sub-area 4: Materials / TIM — 간접 (next wave deep)
- Henkel (HEN3.DE) — Bergquist TIM
- Honeywell (HON), 3M (MMM), Parker (PH), DuPont (DD)

#### Sub-area 5: Immersion 전문 — 변동성·소형
- Asetek (ASTK.OL) — 노르웨이 작음, 시총 ~$200M
- Iceotope, ZutaCore, Submer, GRC — 비상장

#### Sub-area 6: 한국 — 매수 권장 안함 또는 위성
- LG전자 (066570) — chiller·HVAC, DC 매우 작음
- 신성ENG (011930), 신성델타테크 (065350) — HVAC 부품
- 코오롱인더스트리 (120110) — TIM polymer 일부

---

## 6. 병목 식별 (Step 3)

### 6.1 현재 병목

| 병목 | 영향 | 수혜자 |
|------|-----|------|
| D2C cold plate capa | lead time 6+ 개월 | Boyd (Eaton), Vertiv, CoolIT |
| Vertiv capa 확장 | backlog 소화 1.5+년 | Vertiv |
| Eaton-Boyd 통합 | 2026 통합 진행 | Eaton |
| 정밀 fittings (Stäubli·CPC) | lead time 길어짐 | Stäubli, Eaton (CPC) |
| TIM 고성능 grade | 200kW+ rack 제약 | Henkel, Honeywell, 3M |

### 6.2 다음 병목 ★ 투자 핵심

| 병목 | 등장 시점 | 수혜자 |
|------|---------|------|
| 200kW+ rack liquid cooling | 2027~ | Vertiv, Eaton, Schneider |
| **Single-phase immersion 본격화** | 2027~2028 | **Modine·Submer·GRC·Schneider·Dell** (next wave deep) |
| **Dielectric fluid (PFAS-free)** | 2027~ | **Chemours Opteon·Solvay·Shell** (next wave deep) |
| **Water-positive cooling 시스템** | 2027~2028 | Vertiv·Schneider (recycle) |
| **자율 cooling 관리 SW** | 2026~2027 | Vertiv·Schneider·Honeywell |

### 6.3 컨센서스 vs 본인 뷰

**컨센서스**: "Vertiv 다 가져간다" — 풀 매수. liquid cooling = D2C 만 본다.

**본인 뷰**:
- Vertiv 47x P/E 부담 → 분할·조정 wait
- **Modine hidden specialty alpha** — Vertiv 대비 저평가 + DC +78% yoy
- Eaton-Boyd 통합 = 2026 매출 즉시 기여, 전력+냉각 시너지
- Diversified (Schneider·nVent) 진정한 안정 alpha
- liquid cooling 4가지 방식 다 진행 → Modine immersion 일부 노출이 *2027~2028 hedge*

### 6.4 Next Wave Deep Analysis ★★★ 본인 진짜 알파

> **본인 메모**: "next-bottleneck identification". 광원 (광인터커넥트) 처럼, 냉각도 *D2C 가 over-known·과열* 단계. 진짜 alpha 는 *병목 이동*. 3개 선정 — Immersion + PFAS-free Fluid, TIM, AI Cooling SW.

---

#### Next Wave 1: Single-phase Immersion + PFAS-free Dielectric Fluid ★★★ 2027~

**왜 next wave 인가**
- D2C cold plate 가 200kW+ rack 에서 *물리적 한계 근접*. Single-phase immersion 이 *진정한 200kW+ 솔루션*.
- 2025 single-phase D2C = 55% 시장 점유. 2027~2028 immersion 부분 잠식 시작.
- **PFAS 규제** 가 핵심 변수: 3M Novec 철수 (Belgium 공장 PFAS 누출, 2023). Two-phase immersion *위기*.
- **PFAS-free dielectric fluid** 시장 폭증: Chemours Opteon (HFO), Solvay, Shell, Cargill 모두 진입. 2025 patent +40%.
- 사막·중동 immersion: Abu Dhabi 150MW (2026 후반 완공), 사우디·UAE 가속 — *환경 (45℃ 사막) 에서 immersion 의 thermal edge*.
- Vertiv·Schneider·Dell 다 immersion 진입 (M&A·파트너십) — *single-vendor accountability* 매력.

**병목 메커니즘**
- Dielectric fluid PFAS 대체: HFO (hydrofluoroolefin) 기반 + 자연 ester. 양산 capa 부족.
- Immersion tank 설계·인증 — 안전성·재고관리
- 패시브 vs 액티브 immersion — 회로 정밀도
- 서버 OEM 도 immersion 호환 변경 (Dell·HPE·Supermicro)

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Modine (MOD)** | US | Single-phase immersion 부분 + D2C 통합 | 이미 본문 1순위 |
| **Chemours (CC)** | US | **Opteon HFO fluid (PFAS-free immersion 핵심)**, 시총 ~$2~3B | **A next wave** |
| **Solvay (SOLB.BR)** | EU | PFAS-free dielectric fluid 개발, 시총 ~€2.5B | **B (EU 위성)** |
| **Shell (SHEL)** | UK | E.S. (Electric Fluid) — synthetic ester 기반, 시총 ~$200B | C (대형, 비중 작음) |
| **Cargill (비상장)** | US | natural ester fluid (대두유 기반) | n/a |
| **Schneider Electric (SU.PA)** | EU | immersion 통합 진입 | 이미 본문 매수 |
| **Vertiv (VRT)** | US | immersion 부분 진입 (NVIDIA 협력) | 이미 본문 매수 |
| **Dell (DELL)** | US | immersion 호환 서버 + 파트너십 | C (별도 thesis) |
| 3M (MMM) | US | Novec 철수, *thesis 약화* | 진입 권장 안함 |

**한국**
- 코오롱인더스트리 (120110) — polymer·dielectric 일부, *간접 노출 가능*
- LG화학 (051910) — chemical 다중, *간접*
- 시총 큰 종목들이라 직접 alpha 약함

**Timing & Catalyst**
- 2026 후반: Chemours Opteon 양산 진입
- 2027: Abu Dhabi 150MW immersion 완공 + 사막 시장 폭증
- 2027~2028: 단상 immersion 본격 채택 (hyperscaler 일부)
- PFAS 규제 강화 (EU REACH·미국 EPA) 시 가속

**모니터링**
- Chemours Opteon 분기 매출 + Q-by-Q yoy → P1
- Modine 분기 immersion segment → P1
- Schneider·Vertiv 분기 immersion 사례 → P2
- 빅테크 immersion 채택 발표 (MS·Meta·AWS) → P1
- PFAS 규제 진척 (EU REACH·US EPA) → P1
- LiquidStack·ZutaCore·Submer·GRC IPO 시그널 → P2

**숨겨진 매력 — Chemours (CC)**
- *PFAS-free immersion fluid 의 sector leader*. Opteon HFO + 다중 라인
- 시총 ~$2~3B (작음)
- HFO 시장 자체가 *cooling 외에도 refrigeration·heat pump* 다중 노출
- 단점: 화학 종목 cyclical 변동성
- **본 deep dive 의 next wave hidden alpha 1위**

**리스크**
- D2C 가 200kW+ 까지 효율적 → immersion 본격화 늦춰질 가능성
- PFAS-free fluid 신뢰성 인증 추가 1~2년
- Chemours 화학 사업 전체 cyclical (HFO 외 사업 둔화)

---

#### Next Wave 2: TIM (Thermal Interface Material) ★★ 2026~ 진행

**왜 next wave 인가**
- TIM = chip 표면 - cold plate 사이 *열전도 재료* (그리스, 시트, phase-change material).
- AI rack 100kW+ → 200kW+ 전환 시 TIM 의 *열전도율 (W/m·K)* 이 critical path.
- 기존 TIM 5~10 W/m·K → 차세대 TIM 50~100 W/m·K (carbon·metal·hybrid) 필요.
- **본인 재료 background 친숙도 최고 영역** (메모: advantage filter 아니지만 자연스럽게 깊이 이해)
- 200kW+ rack 양산 진입 (2027~) 시 TIM 매출 폭증 가속

**병목 메커니즘**
- TIM 양산 grade 의 *낮은 열저항* + *기계적 신뢰성* (열 cycle 5+ 년)
- 자동 도포 (dispensing) 기술 + 균일도
- 신규 재료 (graphene·boron nitride·liquid metal) 양산 어려움

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Henkel (HEN3.DE)** | EU | **Bergquist 브랜드 TIM 1위** (그리스·시트·gap filler). 시총 ~€30B, P/E 12~15x **저평가** | **A 1순위 next wave** |
| **Honeywell (HON)** | US | TIM 일부 + electronic materials. 시총 ~$140B, P/E 20x | B (대형, 비중 작음) |
| **Parker Hannifin (PH)** | US | Thermal solution + fittings. 시총 ~$80B, P/E 25x | B (다중 노출) |
| **DuPont (DD)** | US | TIM·polymer + electronic materials. 시총 ~$30B, P/E 18x | B |
| **Shin-Etsu Chemical (4063.T)** | JP | TIM·silicone material 글로벌 강. 시총 ~¥10T | B (위성, 일본) |
| **Indium Corporation (비상장)** | US | liquid metal TIM, 비상장 | n/a |
| **MMM (3M)** | US | TIM 일부 (Novec 철수 후 다중 영향) | C |

**한국**
- **코오롱인더스트리 (120110)** — polymer·composite 다중. TIM 부분 일부. 시총 ~7,000억원
- **LG화학 (051910)** — chemical 다중 (간접)
- **삼성SDI (006400)** — 배터리 TIM 일부 (DC 영역 아님)
- 한국 *TIM 글로벌 alpha 약함*, 위성

**Timing & Catalyst**
- 2026 후반: Rubin 양산 진입 → 200kW+ 본격
- 2027: 차세대 TIM (carbon·hybrid) 양산 본격
- 2027~2028: liquid metal TIM 일부 hyperscaler 채택

**모니터링**
- Henkel 분기 (Bergquist segment, electronic materials yoy) → P1
- Shin-Etsu 분기 (silicone material) → P1
- 코오롱인더 분기 (composite·polymer) → P2
- 차세대 TIM 양산 신고 (graphene·BN·liquid metal) → P2

**숨겨진 매력 — Henkel (HEN3.DE)**
- **Bergquist TIM 사실상 글로벌 1위** (그리스·시트·gap filler)
- 시총 ~€30B, P/E 12~15x **저평가**
- 본업 (소비재·접착제) 안정 + electronic materials AI DC 성장
- 유로 거래 (Frankfurt, ADR HENKY 가능)
- 단점: 전체 매출 中 electronic materials 비중 ~10% 미만, *전체 매출은 소비재 cyclical*
- **본 deep dive next wave hidden alpha 2위**

**리스크**
- 차세대 TIM (liquid metal·graphene) 양산 정체
- 빅테크 자체 TIM 개발 가속

---

#### Next Wave 3: AI-driven Cooling Optimization SW ★ 2026~2027

**왜 next wave 인가**
- 데이터센터 cooling = *대규모 multi-variable 제어 문제* (수만 sensor, 수천 valve, 풍속·온도·습도·전력 동시 최적화)
- AI 가 적용되면 PUE 0.05~0.15 추가 개선 가능 (Google DeepMind 사례)
- **AI cooling 관리 SW 가 hardware 보다 *고 GM*** (SaaS 75%+, hardware 25%)
- 빅테크 (Google·Meta·MS) 자체 솔루션 vs Vertiv·Schneider·Honeywell 외부 솔루션 경쟁

**병목 메커니즘**
- Real-time multi-sensor data + AI inference (edge)
- Predictive maintenance (cooling unit 고장 예측)
- Digital twin (디지털 트윈 cooling 시뮬레이션)
- 빅테크 자체 platform vs vendor 솔루션

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Vertiv (VRT)** | US | Vertiv Liebert AI 관리 SW + edge analytics | 이미 본문 매수 |
| **Schneider Electric (SU.PA)** | EU | EcoStruxure IT (cooling SW), AI-driven | 이미 본문 매수 |
| **Honeywell (HON)** | US | Forge for Buildings + Forge for Industrial | B (대형 다중) |
| **Cadence (CDNS)** | US | Celsius EC (computational fluid dynamics for DC), 시총 ~$80B | C (별도 thesis, EDA 영역) |
| **Ansys (ANSS)** | US | Ansys Fluent (CFD for DC). Synopsys 인수 (2025), 시총 ~$30B | C (EDA·simulation 영역) |
| **Synopsys (SNPS)** | US | Ansys 인수 후 Cadence 와 함께 EDA·simulation 1·2위 | 별도 thesis (EDA 영역) |
| **Palantir (PLTR)** | US | Foundry for DC operations (일부) | AI Vertical 중복 |

**한국**
- 자체 DC 운영 SW 한국 직접 노출 작음
- 더존비즈온 (012510), 한글과컴퓨터 등 *DC 관리 SW 아님*

**Timing & Catalyst**
- 2026~2027: AI cooling SW 본격 채택 가속
- 2027: 빅테크 자체 platform vs vendor 솔루션 분기 명확화

**모니터링**
- Vertiv·Schneider AI cooling SW 사례 발표 → P2
- Cadence·Ansys CFD for DC 매출 시그널 → P3
- 빅테크 자체 cooling AI 발표 → P2

**진입 전략**
- 직접 alpha 약함 (Vertiv·Schneider 이미 본문 매수 통해 노출)
- Cadence·Ansys 는 *EDA 영역* 별도 thesis
- *추가 진입 종목 없음* — 본문 종목으로 충분 노출

**리스크**
- 빅테크 자체 platform 강화 시 vendor 솔루션 약화
- AI cooling SaaS GM 압박 (가격 경쟁)

---

### 6.5 Next Wave 종합 — 본인 진입 전략

**우선순위 (Timing + 상장 alpha)**

| 순위 | Next Wave | Timing | 핵심 종목 | 비중 |
|-----|---------|--------|---------|-----|
| 1 | **TIM (Thermal Interface Material)** | 2026~ 가속 | **Henkel (HEN3.DE)** — Bergquist 1위 | 1~2% (저평가 신규) |
| 2 | **Single-phase Immersion + PFAS-free Fluid** | 2027~ | **Chemours (CC)** + Modine (본문 중복) | 1~2% (Chemours 신규) |
| 3 | **AI Cooling SW** | 2026~2027 | Vertiv·Schneider (본문 중복) | 본문 종목으로 충분 |

**냉각 영역 종합 매수 우선순위 업데이트**

1. **Modine (MOD)** — hidden specialty alpha, immediate
2. **Eaton (ETN)** — Boyd 통합 + 전력 영역 중복
3. **Schneider Electric (SU.PA)** — 글로벌 1위 + 유로 hedge
4. **nVent (NVT)** — DC 비중 최고 (diversified)
5. **Vertiv (VRT)** — sector leader, 조정 wait
6. **Henkel (HEN3.DE)** ← **Next wave: TIM 1위 저평가 신규**
7. **Chemours (CC)** ← **Next wave: PFAS-free fluid 신규**
8. Honeywell (HON), JCI — 위성

**모니터링 watchlist**
- Asetek (ASTK.OL) — D2C 소형 변동성
- Submer·GRC·LiquidStack·ZutaCore·Iceotope (비상장) — IPO 시그널
- Shin-Etsu (4063.T) — TIM silicone (일본)
- Solvay (SOLB.BR), Shell (SHEL) — PFAS-free fluid 부분 노출
- 코오롱인더스트리 (120110) — polymer TIM 간접 (한국)
- Cadence (CDNS), Ansys (ANSS) — CFD for DC (별도 thesis)

---

## 7. 자금 흐름 시그널 (Step 4)

### 7.1 관련 ETF

| 티커 | 시장 | 비중 |
|------|------|----|
| XLI | US | Industrial Select (ETN·HON·JCI·PH·Carrier) — 약~중간 |
| DTCR | US | Global X DC & Digital Infra — 중간 |
| SRVR | US | Pacer DC & Tech REITs — 약함 |
| KODEX 미국S&P500 | KR | 간접 — 약함 |

→ ETF 노출 약함. **직접 종목 매수** 필수.

### 7.2 추적 지표

**P1 (분기 필수)**
- Vertiv 분기 (매출·backlog·OM)
- Eaton 분기 + Boyd 통합 진척 + 매출 기여
- Modine 분기 (DC 매출 yoy)
- Schneider 분기 (DC segment)
- nVent 분기 (DC 비중)
- **Henkel 분기 (Bergquist segment, electronic materials)** ← next wave
- **Chemours 분기 (Opteon fluid)** ← next wave
- NVIDIA Blackwell·Rubin 출하 + 800V DC

**P2 (분기 모니터링)**
- MS·Google·Meta·AWS CapEx 가이던스 (cooling 비중)
- Equinix·Digital Realty·CoreWeave liquid cooling 채택
- PFAS·GWP 규제 진척
- Water-positive 정책

**P3 (지속)**
- Submer·GRC·Iceotope·LiquidStack IPO 시그널
- 한국 LG·신성 DC 매출
- Carrier·JCI DC 진입

### 7.3 Startup Landscape

| 스타트업 | 영역 | 비고 |
|---------|------|----|
| CoolIT Systems | D2C cold plate | $200M+, IPO 2026~2027 |
| Submer | Single-phase immersion | $150M+ |
| LiquidStack | Two-phase immersion | PFAS 부담 |
| ZutaCore | Two-phase (D2C 유사) | PFAS 2026 phase-out 약속 |
| Iceotope | Two-phase | $80M+ |
| GRC (Green Revolution Cooling) | Single-phase immersion | $100M+ |

---

## 8. 종목 매핑 (Step 5)

### 8.1 글로벌 종목

| 티커 | 기업 | 영역 | 시총 | P/E | Tier |
|------|------|-----|-----|-----|------|
| **MOD** | Modine | L3 (specialty) | ~$6~8B | ~25x | **A 1순위** |
| **ETN** | Eaton | L4 (전력+냉각 Boyd) | ~$150B+ | ~25x | **A 2순위** |
| **SU.PA** | Schneider Electric | L4 (전력+냉각+SW 1위) | ~$154B | ~25x | **A 3순위** |
| **NVT** | nVent | L4 (전력+냉각 DC 30%) | ~$15B | ~22x | **A 4순위** |
| **VRT** | Vertiv | L3 (pure-play) | ~$50B+ | 47x fwd | **A 5순위 (조정 wait)** |
| **HEN3.DE** | Henkel ★ next wave | L1 TIM (Bergquist 1위) | ~€30B | 12~15x | **A 6순위 (신규 저평가)** |
| **CC** | Chemours ★ next wave | L1 PFAS-free fluid (Opteon) | ~$2~3B | n/a | **A 7순위 (신규 변동)** |
| HON | Honeywell | L4 (다중) | ~$140B | ~20x | B 위성 |
| JCI | Johnson Controls | L4 (HVAC + DC) | ~$60B | ~22x | B 위성 |
| CARR | Carrier | L4 (HVAC, DC 3~5년) | ~$60B | ~22x | C |
| PH | Parker Hannifin | L2 (fittings) + TIM 일부 | ~$80B | ~25x | C |
| DD | DuPont | L1 (일부 TIM) | ~$30B | ~18x | C |
| 4063.T | Shin-Etsu | TIM silicone (일본) | ~¥10T | ~20x | C 위성 JP |
| SOLB.BR | Solvay | PFAS-free fluid | ~€2.5B | ~10x | C 위성 EU |
| SHEL | Shell | E.S. dielectric fluid | ~$200B | ~12x | C |
| ASTK.OL | Asetek | D2C 소형 | ~$200M | n/a | C |

### 8.2 한국 종목

| 티커 | 기업 | 영역 | 시총 | Tier |
|------|------|-----|-----|------|
| 066570 | LG전자 | L4 (HVAC, DC 일부) | ~14조원 | C (위성) |
| 011930 | 신성ENG | L4 (HVAC) | ~3,000억원 | C |
| 065350 | 신성델타테크 | L2~L3 (냉각 부품) | ~1,500억원 | C |
| 120110 | 코오롱인더스트리 | L1 (polymer TIM 간접) | ~7,000억원 | C |
| 051910 | LG화학 | L1 (chemical 다중) | ~22조원 | 별도 thesis |

→ 한국 직접 alpha 약함

### 8.3 각 종목의 Valuation Gate

**Modine (MOD) — 1순위 (Hidden Specialty)**
- DC +78% yoy (FY26 Q3), FY2026 가이던스 15~20%
- 시총 ~$6~8B (Vertiv 대비 저평가)
- 자동차 cooling 노하우 + DC + single-phase immersion 부분
- **진입 전략**: 즉시 분할 매수, 1~3개월

**Eaton (ETN) — 2순위 (전력+냉각)**
- Boyd 2026 매출 $1.5~1.7B 기여
- DC 25~30% 성장, P/E 25x
- **진입 전략**: 즉시 분할 매수, *전력 영역과 통합 비중*

**Schneider Electric (SU.PA) — 3순위**
- 글로벌 1위 (전력+냉각+SW)
- DC 24%, P/E 25x
- 유로 거래 (ADR SBGSY)
- **진입 전략**: 분할 매수

**nVent (NVT) — 4순위**
- DC 30% (diversified 최고)
- NVIDIA 파트너십
- P/E 22x
- **진입 전략**: 분할 매수

**Vertiv (VRT) — 5순위 (조정 wait)**
- sector leader, Q1 2026 $2.65B, EPS +83% yoy
- 1년 +250%, **47x forward P/E 부담**
- **진입 전략**: 분할 매수 + 10~20% 조정 시 추가

**Henkel (HEN3.DE) — 6순위 신규 (Next Wave: TIM)**
- *Bergquist TIM 글로벌 1위*
- 시총 ~€30B, **P/E 12~15x 저평가**
- 본업 (소비재) 안정 + electronic materials 성장
- 유로 거래 (ADR HENKY 가능)
- **진입 전략**: 분할 매수, electronic materials 매출 비중 점검 (~10% 미만)

**Chemours (CC) — 7순위 신규 (Next Wave: PFAS-free Fluid)**
- *Opteon HFO fluid sector leader*
- 시총 ~$2~3B (작음, 변동성)
- HFO 시장 cooling 외에도 refrigeration·heat pump 다중
- **단점**: 화학 cyclical 변동성
- **진입 전략**: 위성 1~2% 비중, 변동성 인지

---

## 9. 모니터링 트리거

**즉시 (분기)**
- Vertiv 분기 (매출·backlog·book-to-bill·OM) → P1
- Eaton 분기 + Boyd 통합 → P1
- Modine 분기 (DC 매출 yoy) → P1
- Schneider 분기 (DC segment) → P1
- nVent 분기 (DC 비중) → P1
- **Henkel 분기 (Bergquist, electronic materials)** ← next wave → P1
- **Chemours 분기 (Opteon fluid)** ← next wave → P1

**정책·M&A**
- Eaton-Boyd Thermal 통합 완료 → P1
- **PFAS·GWP 규제 진척 (EU REACH·US EPA)** ← next wave → P1
- Water-positive 정책 (텍사스) → P2
- 미·중 DC 견제 → P2
- Carrier·JCI DC 추가 M&A → P3

**기술**
- Blackwell GB200 NVL72 출하 → P1
- Rubin·Rubin Ultra 200kW+/rack → P1
- **Single-phase immersion 본격 채택 (MS·Meta)** ← next wave → P1
- **PFAS-free dielectric fluid 양산** ← next wave → P1
- 차세대 TIM (carbon·BN·liquid metal) 양산 → P2
- Self-managed cooling SW → P3

**거시**
- 빅테크 AI CapEx 가이던스 → P1
- Fed 금리 → P2

---

## 10. 리스크

**기술**
- D2C vs Immersion 표준 분기 — Vertiv·Boyd 균등 노출이 hedge
- 빅테크 자체 cooling 개발 — 가능성 매우 낮음
- PFAS·GWP 규제 강화 — two-phase immersion fluid 제한 (D2C 영향 작음)
- 차세대 TIM 양산 지연

**시장**
- 빅테크 AI CapEx 둔화 (-20%+)
- Vertiv valuation 조정 (47x P/E 부담, -10~30% 가능)
- Eaton-Boyd 통합 지연
- liquid cooling 가격 압박 (CoolIT IPO 등)

**지정학**
- 미·중 DC 견제 강화 (Vertiv·Schneider 중국 매출 영향)
- 물 사용 규제 (텍사스·아리조나)

**본인 포트폴리오 — AI 인프라 중복**
- 본 영역 + Vertiv·Eaton 은 AI DC 전력 영역과 *완전 중복*
- 광인터커넥트 + 전력반도체 + AI Foundation 모두 빅테크 CapEx 단일 변수 노출
- → 총 비중 25~35% 상한, 중복 인지

---

## 11. 매크로 변수 민감도

| 변수 | 영향 | 메커니즘 |
|------|------|--------|
| 빅테크 AI CapEx 가속 | ++ | 직접 (모든 종목) |
| Fed 금리 인하 | + | 산업주 멀티플 |
| 물 사용 규제 | − | 텍사스·아리조나 DC 입지 제약 |
| **PFAS·GWP 규제** | + | Chemours·Solvay PFAS-free fluid 수혜, 3M Novec 약화 |
| 미중 갈등 | − | Vertiv·Schneider 중국 매출 영향 |
| 트럼프 인프라 정책 | + | 미국 DC capacity 강화 |
| 달러 강세 | − | Schneider·Henkel 유로 환산 |
| 한국 원화 강세 | − | 미국·유럽 종목 매수 환차익 |

---

## 12. 본인 의사결정 메모

### 최종 매수 우선순위 (Next Wave 반영)

**Tier A — 즉시 분할 매수**
1. **Modine (MOD)** — hidden specialty alpha
2. **Eaton (ETN)** — Boyd 통합 + 전력 영역 중복
3. **Schneider Electric (SU.PA)** — 글로벌 1위 + 유로 hedge
4. **nVent (NVT)** — DC 30% diversified
5. **Vertiv (VRT)** — sector leader, *조정 wait* (10~20% 조정 시)
6. **Henkel (HEN3.DE)** ← **Next wave: TIM 1위 저평가 (P/E 12~15x)**
7. **Chemours (CC)** ← **Next wave: PFAS-free fluid (변동성)**

**Tier B 위성**
8. Honeywell (HON), JCI

### 비중 가이드

- 본 영역 전체: **포트폴리오의 5~10%**
- 본 영역 + AI DC 전력 + AI Foundation 합산: **25~35% 상한**
- Eaton·Vertiv 는 *전력 영역과 이중 노출* — 전력 1.5x 로 카운트
- 종목별: Modine 1~2%, Eaton 2~3% (전력과 합산), Schneider 1~2%, nVent 1%, Vertiv 1~2% (조정 후), Henkel 1%, Chemours 1%

### 진입 timing

- 즉시: Modine, Eaton, Schneider, nVent, Henkel, Chemours
- 조정 wait: Vertiv (10~20% 조정 시)
- 위성: Honeywell, JCI — 시장 조정 시

### 핵심 trade-off

- Pure-play (Vertiv) vs Diversified (Eaton·Schneider): pure-play = 직접·과열, diversified = 안정+다중
- Specialty (Modine) vs Big Player (Vertiv·Eaton): Modine = 저평가+빠른 성장
- Materials (Henkel·Chemours) vs System (Vertiv·Modine): 재료 = 본인 background 친숙도 최고
- **AI 인프라 중복 노출 인지** — Eaton·Vertiv 전력 영역 이중 카운트

### 본인 친숙도 활용
- *재료 background* — TIM (Henkel Bergquist), dielectric fluid (Chemours) 깊이 이해 자연스러움
- 메모리 지침: advantage filter 아님. 그러나 *정보 비대칭* 측면에서 자연스럽게 진입 가능

### Next Wave 모니터링 watchlist
- Submer·GRC·LiquidStack·ZutaCore·Iceotope (비상장 IPO 모니터링)
- Shin-Etsu (4063.T) — TIM silicone JP
- Solvay (SOLB.BR), Shell (SHEL) — PFAS-free fluid
- 코오롱인더스트리 (120110) — polymer TIM 간접 KR
- Cadence (CDNS), Ansys (ANSS) — CFD for DC (별도 thesis)

### Track 4 등재 후보
- Modine (MOD) — 1순위 등재
- Eaton (ETN) — 2순위 등재 (전력 영역과 통합)
- Schneider Electric (SU.PA) — 3순위 등재
- nVent (NVT) — 4순위 등재
- **Henkel (HEN3.DE) — 5순위 등재 (next wave TIM)**
- **Chemours (CC) — 6순위 등재 (next wave PFAS-free)**
- Vertiv (VRT) — 7순위 등재 (조정 후)

---

## 13. 업데이트 로그

| 날짜 | 변경 |
|------|------|
| 2026-05-24 | 최초 작성 (Tier 1 깊이). TAM 3 + Moat 3 + Capital 4 = 10/15. 시차 A5 B5 C4 = +6 (Very strong entry). Tier 2 확정 (Tier 1 깊이 분석). 본문 매수 우선순위: MOD > ETN > SU.PA > NVT > VRT (조정 후). **Next Wave Deep (6.4·6.5) 추가**: (1) Single-phase Immersion + PFAS-free Fluid (2027~, **Chemours CC**, Modine 본문 중복), (2) **TIM (2026~, Henkel HEN3.DE Bergquist 1위 저평가 P/E 12~15x)**, (3) AI Cooling SW (Vertiv·Schneider 본문 중복). 매수 우선순위 업데이트: MOD > ETN > SU.PA > NVT > VRT > **Henkel (신규)** > **Chemours (신규)**. Vertiv Q1 2026 $2.65B (+30% organic, EPS +83% yoy, OM 20.8%) + backlog $15B (+109% yoy) + Eaton-Boyd $9.5B M&A (2026-03, 2026 매출 $1.5-1.7B 기여) + Modine FY26 Q3 +78% yoy 반영. 3M Novec PFAS 철수, Chemours Opteon HFO 대체 양산 진입. |


---

# ═══════════════════════════════════════════════════
# KR Transmission Boost — KR pure-play thorough 보강
# ═══════════════════════════════════════════════════

# 데이터센터 냉각 — KR Transmission Boost (v2.3 추가)

> **Base document**: data-center-cooling.md (2026-05-24, 36KB)
> **Boost 작성일**: 2026-05-24
> **변경 사항**: KR pure-play thorough 보강 (LG·신성·코오롱 polymer 등)

---

## 5.3 Sub-area X: 한국 — *KR pure-play thorough* (보강·교체)

> v2.3 KR boost. **KR 냉각 alpha 약하지만 LG전자 chiller, 신성ENG·신성델타테크 HVAC, 코오롱인더 polymer (TIM), 삼성SDI battery cooling 등 위성 보강**.

### KR 상장 pure-play

| 티커 | 기업 | 영역 | 시총 | 핵심 thesis | Tier |
|------|------|-----|-----|----------|------|
| **066570** | **LG전자** ★ | L3 데이터센터 chiller·HVAC | 12~17조원 | LG Chiller 사업부 데이터센터 진입. 가전 본업 + 데이터센터 cooling 신규 | **B KR 1순위 (다중)** |
| **011930** | **신성ENG** | L3 HVAC·냉각 부품 | 2,000~3,000억원 | HVAC + 클린룸 데이터센터 진입 | **B KR 2순위** |
| **065350** | **신성델타테크** | L3 냉각 부품 | 1,000~1,500억원 | 냉각 부품 변동성 | **C KR 3순위** |
| **120110** | **코오롱인더스트리** | L3 TIM polymer (간접) | 7,000억원~1조원 | polymer 소재 (TIM 일부 가능성). 간접 노출 | **C KR 위성 (간접)** |
| **006400** | **삼성SDI** | L3 battery thermal management | 20~22조원 | EV battery thermal (cooling 영역 일부 cross) | EV cross |
| **373220** | **LG에너지솔루션** | L3 battery cooling | 90~100조원 | EV battery thermal | EV cross |
| **078930** | **GS** | L4 utility + cooling 일부 | 2조원 | utility 다중 (간접) | C 위성 |
| **000080** | **하이트진로** | n/a | n/a | 영역 외 | - |
| **051915** | **LG화학 우선주** | L3 polymer·소재 | n/a | polymer 소재 | C 위성 |
| **267290** | **경동나비엔** | L3 HVAC·heat pump | 1조원 | 가정용 HVAC (데이터센터 X) | C 위성 변동성 |
| **003670** | **포스코퓨처엠** | L3 양극재·polymer (간접) | 5~7조원 | 양극재 + polymer 소재 (간접) | C 위성 |

### KR 비상장 / IPO 후보

- **TPMS Inc / KOREATEC** — 냉각 부품 (비상장 중소)
- **신성씨엔이엠** — 클린룸·냉각 (비상장)
- **LG화학 자회사 (LG MMA 등)** — polymer 소재

### KR 정책 trigger

- **삼성·SK·NAVER·카카오 데이터센터 자체 build-out** = KR 냉각 수요 증가
- **K-반도체 fab + 미국 fab 인근 데이터센터 cooling 인프라**

### 진입 전략 (KR 우선순위)

- **KR 1순위: LG전자 (066570)** — chiller + 가전 다중 (직접 alpha 약)
- **KR 2순위: 신성ENG (011930)** — HVAC 위성
- **KR 위성**: 신성델타테크·코오롱인더·경동나비엔
- **EV cross**: 삼성SDI·LG에너지 = EV 영역
- **KR 직접 alpha 매우 약함** → 글로벌 비중 강

---

## 8.2 한국 종목 보강

| 티커 | 기업 | 영역 | 시총 | Tier | 매수 우선순위 |
|------|------|-----|-----|------|-----------|
| 066570 | LG전자 | L3 chiller·HVAC | 12~17조원 | **B** | KR 1순위 (직접 alpha 약) |
| 011930 | 신성ENG | L3 HVAC 부품 | 2,000~3,000억원 | **B** | KR 2순위 |
| 065350 | 신성델타테크 | L3 냉각 부품 변동성 | 1,000~1,500억원 | C | KR 3순위 위성 |
| 120110 | 코오롱인더 | L3 polymer (간접 TIM) | 7,000억원~1조원 | C | KR 위성 간접 |
| 267290 | 경동나비엔 | L3 가정 HVAC | 1조원 | C | KR 위성 |

---

## 12 비중 분배 권장 (KR 보강 반영)

- **글로벌 80% : KR 20%** (KR 냉각 alpha 약함, 글로벌 dominant)
- KR 종목 비중 매우 작음 — 위성 합산 0.5% 이하 권장
- 본문 글로벌 매수 (Vertiv·Eaton·Schneider·Modine·nVent·Henkel·Chemours) 강화

### Cross-area
- **삼성SDI·LG에너지** = EV cross → EV 영역 매수
- **코오롱인더** = polymer 다중 → 일부 위성

---

## 업데이트 로그 — KR Boost (v2.3)

| 날짜 | 변경 |
|------|------|
| 2026-05-24 | KR boost retrofit. **LG전자 chiller, 신성ENG·신성델타테크 HVAC, 코오롱인더 polymer (간접), 경동나비엔** 보강. *KR 냉각 직접 alpha 매우 약함* — 글로벌 dominant 인지. KR 비중 20% 유지 (위성 0.5% 이하). |

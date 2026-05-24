# AI Application: Vertical / AI-native SaaS — Tier 1 Deep Dive

> **Trigger**: 사용자 요청. "Palantir 같은 영역이 빠졌다" 의 직접 응답. 시차 매력 + alpha 가능성 본 영역 핵심.
> **Linked methodology**: methodology.md v2.1
> **Note**: Foundation Models + Horizontal SaaS 는 별도 영역 (이미 작성). 본 문서는 industry-specific vertical AI + AI-native 신생 SaaS.

---

## 0. 메타 정보

| 항목 | 값 |
|------|----|
| 작성일 | 2026-05-23 |
| 최근 갱신 | 2026-05-23 |
| 다음 정기 갱신 | 2026-07-01 (Q3 첫 주) |
| 시계 분류 | Core (1.5~2.5년) |
| Tier | 1 (Deep) |
| Confidence (총점) | Medium (vertical 매출 가시화 vs valuation 비대칭, 상장사 적음) |
| 트랙 | L1A (Global) — 한국 transmission 약함 |

---

## 1. 한 줄 요약 + 핵심 가설

### 한 줄 요약
> Foundation model 의 commoditization → **distribution + 도메인 knowhow + 데이터 lock-in** 가진 vertical 회사가 진짜 alpha. Palantir (Q1 $1.6B 매출, +71% YoY 가이던스) 가 대표 상장 케이스. 비상장 vertical AI 폭증 — Harvey (legal, $11B), Hippocratic (의료), Sierra (CS agent, $10B). 상장사 직접 노출은 PLTR·TEM·VEEV·HIMS 등 한정.

### 핵심 가설

- **가설 A**: Foundation model commoditization 이 진행 (DeepSeek·Llama 사례). 모델 자체는 wrapping 위협에 노출. **distribution + domain expertise + 데이터 lock-in 가진 vertical AI 가 진짜 winner**.
- **가설 B**: **Palantir 가 vertical AI 의 상장 대표주**. 다만 PLTR 시총 ~$300B, Forward P/E 200x+ — 매수 매력은 약하나 *공매도도 어려운* 영역. 단, 2026 가이던스 $7.65B 매출 (전년 +71%) 이 진짜 입증. Anthropic ($44B ARR) 같은 빅테크 위협 인식 — PLTR YTD −18%.
- **가설 C**: **상장사 적고 비상장이 진짜 알파**. Harvey, Sierra, Cursor (Anysphere $29B), Glean ($7.2B), Hippocratic, Decagon, Abridge — 다 비상장. 상장사 노출은 PLTR + 일부 healthcare vertical (TEM·VEEV·HIMS·EXAS).
- **가설 D**: **2026이 vertical AI의 *real revenue* 검증 원년**. Sierra $150M ARR (7 분기), Glean $200M ARR (9개월에 ×2), Harvey 235 고객. ROI 입증되며 *AI 거품 vs 실재* 분기. 검증 통과 종목 폭발, 실패 종목 잠식.
- **가설 E**: **AI Code / Dev tools 가 가장 빠른 sub-area**. Anysphere(Cursor) $29B valuation, Replit ARR $2.8M → $150M (1년), Anthropic Claude Code $1B ARR. **이 영역 상장사 노출 거의 없음** — 빅테크 (MSFT-GitHub) 통한 간접만.

### 기각 조건
- Foundation model 자체 vertical layer 잠식 (Anthropic·OpenAI 가 directly vertical 진입)
- PLTR 분기 매출 가이던스 둔화 (qoq −5% 이상)
- Sierra·Harvey 등 비상장 IPO 시 가격 폭락 (벨류에이션 정점 시그널)
- AI Agent ROI 입증 실패 — 대기업 reference case 부재 2분기 연속
- Anthropic·OpenAI 가격 추가 인상 시 enterprise budget 위기 (vertical SaaS도 위협)

---

## 2. 잣대 채점

### 잣대 1: TAM

| 항목 | 값 |
|------|----|
| 점수 | 5 / 5 |
| 카테고리 | Mega-transformative |
| Confidence | Medium-High |

**근거**:
- Vertical AI 시장: 산업별 합산 시 $200B+ 시장 잠재
  - Legal AI: $5~10B (Harvey 단일 $1.3B 누적 펀딩)
  - Healthcare AI: $50B+ (Tempus, Veeva, Abridge, Hippocratic)
  - Customer support AI: $30B+ (Sierra, Decagon, Cresta)
  - Finance AI: $20B+ (Hebbia, Brex AI 등)
  - Code AI: $20B+ (Cursor, Cognition, Replit)
- 정부 & defense AI: PLTR 정부 매출 $687M 분기, 미국 정부 AI 시장 $50B+ 잠재
- 5년 후: vertical AI 전체 $500B+ 도달 가능 (consensus)
- **×10 + 100B$ 도달 가능. 5점.**

### 잣대 2: Moat (해자 재편 + 비가역성)

| 항목 | 값 |
|------|----|
| 점수 | 4 / 5 |
| Confidence | High |

**근거**:
- 기존 강자: 산업별 incumbent (legal: Thomson Reuters, Wolters Kluwer; healthcare: Epic, Cerner; CS: ServiceNow, Zendesk)
- **새 카테고리 신생**: AI-native 회사들이 incumbent 잠식 시작
  - Harvey 235 고객, AmLaw 100의 절반 도달
  - Tempus AI 2026 매출 $1.6B 가이던스 (전년 +83%)
  - Sierra $150M ARR (7분기 만에)
- **Moat 재편 강함**: 기존 SaaS 의 per-seat 모델이 agentic AI 로 잠식. 도메인 데이터 보유 회사 우위.

**비가역성 평가**:
- 도메인 데이터 lock-in: Tempus AI multimodal data 보유 → 빅테크가 따라잡기 어려움
- 정부 계약 lock-in: Palantir 정부 deal 20년 단위
- 산업 표준 lock-in: Harvey AmLaw 50%+ 침투 — 표준화 진입
- 단, foundation model 위협: Anthropic·OpenAI 가 vertical 직접 진입 시 잠식 가능 (PLTR 우려)
- **비가역성 부분적** — 도메인 lock-in 강하나 foundation model 위협 잔존

**해석**:
- 새 카테고리 형성 + 기존 강자 일부 도태
- 단, foundation model 으로부터 위협받는 layer 도 있음
- **4점** (Major reshuffle + 비가역 강), 5점 아님 (foundation 위협 인식)

### 잣대 3: Capital

| 항목 | 값 |
|------|----|
| 점수 | 4 / 5 |
| Confidence | High |

**근거** (출처 명시):
- VC 펀딩 vertical AI 2025: $15B+ (Sequoia·a16z·Benchmark 중심)
- Series A 규모 폭증: $50M~$100M (이전 $10M~$20M의 ×5)
- 주요 라운드 (2024~2026):
  - Harvey: $1.3B 누적 (Series F)
  - Sierra: $10B valuation 시리즈 진행
  - Anysphere (Cursor): $29B
  - Glean: $410M total, $200M ARR
  - Hippocratic: $126M Series C (NVIDIA NVentures 포함)
  - Legora (legal, EU): $550M Series D, $1B 누적
- 빅테크 CVC: NVIDIA NVentures, Google·Microsoft·Amazon VC arm 모두 vertical AI 투자
- 상장사: PLTR 시총 ~$300B, TEM 시총 ~$15B 등
- **합산 연간 자본 유입 ~$30~50B+** (VC + CVC + 상장사 시총 변화)

**해석**:
- 30~100B$ 구간 → 잣대 3점, 100~500B$ → 4점
- 본 영역 ~$30~50B 으로 4점 보더라인. 가속화 중. **4점**.

### 합산

| 트랙 | 합산 점수 | 통과 임계 | Tier 1 임계 |
|------|---------|---------|-----------|
| L1A | **13 / 15** | ≥ 9 ✅ | ≥ 12 ✅ |

**영역 전체 Confidence**: Medium-High (Moat·Tech 측 약간의 위협 인식)

→ **Tier 1 확정. AI Application: Foundation/Horizontal (14점) 다음 강력 영역.**

---

## 3. A·B·C 시차 평가

### A 지표 (자본 유입)
| 항목 | 값 |
|------|----|
| 점수 | **4 / 5** (강한 진행 중) |
| 갱신일 | 2026-05-23 |

**근거**:
- VC 펀딩 vertical AI 2024~2025 분기 강세
- Series 규모 폭증
- 빅테크 CVC 활발
- 단, foundation model layer 만큼의 mega 자본은 아님 (foundation 은 5점)
- **4점** (강한 진행, 정점은 아님)

### B 지표 (실물 변화)
| 항목 | 값 |
|------|----|
| 점수 | **3 / 5** (진행 중, 절반 못 미침) |
| 갱신일 | 2026-05-23 |

**근거**:
- Palantir Q1 2026 매출 $1.6B (+39% YoY), 2026 가이던스 $7.65B (+71%)
- Tempus AI Q1 매출 $348M (+36%), 2026 가이던스 $1.59~1.60B
- Sierra $150M ARR (7분기), Harvey 235 고객
- Glean $100M → $200M ARR (9개월)
- 단, **enterprise 도입은 아직 pilot 다수**. Production-grade (99%+ accuracy) 아직 어려움.
- **실물 변화 진행 중. 본격화 2027~** 3점.

### C 지표 (가격 반영)
| 항목 | 값 |
|------|----|
| 점수 | **3 / 5** (부분 반영) |
| 갱신일 | 2026-05-23 |

**근거**:
- Palantir: 시총 ~$300B, Forward P/E 200x+. **매우 비싸나 매출 가이던스 +71% 따라잡음**. YTD −18% (Anthropic 위협 인식 후).
- Tempus AI (TEM): 시총 ~$15B, P/E 변동 큼 (적자 → 흑자 전환). 매출 가이던스 강.
- Veeva (VEEV): 시총 ~$50B, P/E 50x. 안정적 vertical SaaS.
- Hims & Hers (HIMS): 시총 ~$15B, GLP-1 + AI telehealth 수혜.
- 비상장 vertical AI: 52x ARR 평균, 일부 127x ARR (CS agent) — **과열 시그널**
- **상장사 부분 반영, 비상장 과열**. 3점.

### 시차 매력도 = A + B − C

| 항목 | 값 |
|------|----|
| 계산 | 4 + 3 − 3 = **+4** |
| 카테고리 | **Good entry** |

**해석**:
- 자본·실물 진행 중, 가격 부분 반영. 진입 매력 양호.
- 단, **비상장 영역이 더 빠르게 성장**. 상장사 직접 노출은 한정적.
- 진입 전략:
  - Palantir: 가격 부담 vs 매출 모멘텀 binary. 분할 매수 또는 보류.
  - Healthcare vertical (Tempus, Veeva, HIMS): 합리적 valuation, 도메인 lock-in
  - Defense vertical: PLTR 외에는 상장사 적음 (Anduril, Shield AI 비상장)
  - 빅테크 통한 간접: Microsoft (GitHub Copilot), Google (Med-PaLM)

---

## 4. 산업 메가트렌드

### 4.1 수요 측
- **enterprise AI ROI 검증 단계**: 2025 pilot → 2026 production deployment
- 산업별 도입 가속: Legal (AmLaw 50%+ Harvey), Healthcare (Tempus 70+ 제약 고객), Finance, Customer Support
- 정부·국방 AI 도입: Trump 행정명령으로 가속
- **5년 성장률**: vertical 별 다름. Sierra 같은 CS는 연 ×3, Tempus 같은 healthcare 는 연 ×1.4

### 4.2 공급 측
- 비상장 vertical AI 회사 폭증 (2024~2025 펀딩 신기록)
- foundation model 가격 하락 → vertical 회사 마진 ↑
- 단, foundation model 회사 (Anthropic·OpenAI) 가 vertical 직접 진입 위협
- 빅테크 distribution 우위 (Microsoft·Google 산업별 솔루션 강화)

### 4.3 정책·지정학 변수
- **정부·국방 AI**: Trump 행정명령, Palantir 직접 수혜
- **헬스케어 AI 규제**: FDA AI/ML 가이던스, 일부 vertical (Tempus·Abridge) 인증 필수
- **EU AI Act**: 컴플라이언스 비용 (Harvey EU 시장 진입 변수)
- **개인정보·저작권**: vertical AI 가 산업 데이터 사용 → 소송 변수

---

## 5. 밸류체인 매핑

### 5.1 다이어그램
```
[Foundation Models]
   └─ OpenAI, Anthropic, Google, Meta (별도 영역)
        ↓ (model API + 데이터)
[Domain Data + Workflow Integration] ★ Vertical AI 핵심
   ├─ Healthcare:
   │  ├─ Tempus AI (TEM) — multimodal genomic + clinical
   │  ├─ Veeva (VEEV) — pharma data·CRM
   │  ├─ Abridge (비상장) — clinical scribe
   │  ├─ Hippocratic AI (비상장) — non-diagnostic agent
   │  ├─ Ambience Healthcare (비상장)
   │  └─ Exact Sciences (EXAS) — diagnostic AI
   ├─ Defense / Government:
   │  ├─ Palantir (PLTR) — gov + commercial
   │  ├─ Anduril (비상장)
   │  └─ Shield AI (비상장)
   ├─ Legal:
   │  ├─ Harvey (비상장, $11B)
   │  ├─ Legora (비상장, EU)
   │  └─ Thomson Reuters (TRI) — AI 통합 중
   ├─ Finance:
   │  ├─ Hebbia (비상장)
   │  ├─ Brex AI (비상장)
   │  └─ Intuit (INTU) — TurboTax·QuickBooks AI
   ├─ Customer Support:
   │  ├─ Sierra (비상장, $10B)
   │  ├─ Decagon (비상장, $4.5B)
   │  ├─ Cresta (비상장)
   │  └─ Zendesk (비상장, Permira 인수)
   ├─ Sales / Marketing:
   │  ├─ Writer (비상장)
   │  ├─ HubSpot (HUBS) — AI 통합
   │  └─ Sprout Social (SPT)
   ├─ Real Estate:
   │  ├─ Zillow (ZG), Compass (COMP)
   │  └─ EQRX, Cherre (비상장)
   └─ Manufacturing / Industrial:
      ├─ AutoStore (오슬로)
      └─ C3.ai (AI) — 산업 AI
        ↓
[AI-native Productivity Tools]
   ├─ Cursor (Anysphere, 비상장 $29B)
   ├─ Cognition AI (Devin, 비상장 $2B)
   ├─ Replit (비상장, $150M ARR)
   ├─ Glean (비상장, $7.2B, $200M ARR)
   ├─ Notion (비상장)
   └─ Linear (비상장)
        ↓
[Creative / Content AI]
   ├─ Runway (비상장, video)
   ├─ ElevenLabs (비상장, audio)
   ├─ Black Forest Labs (비상장, image)
   ├─ Adobe (별도 영역, Horizontal)
   └─ Canva (비상장)
```

### 5.2 레이어별 분석

| 레이어 | 마진 수준 | 경쟁 강도 | 중국 침투 | 진입장벽 |
|--------|---------|---------|---------|---------|
| Healthcare AI | 높음 | 중간 | 거의 없음 (규제) | 데이터+FDA 인증 |
| Defense / Gov AI | 매우 높음 | 매우 낮음 (보안 clearance 필요) | 거의 없음 | clearance+계약 |
| Legal AI | 높음 | 중간 (Harvey vs Legora) | 거의 없음 | 도메인 + 채택 |
| Finance AI | 중상 | 높음 (HUBS·INTU vs 신생) | 거의 없음 | 컴플라이언스 |
| Customer Support AI | 변동 (가격 압박) | 매우 높음 (Sierra·Decagon·Cresta) | 일부 진입 | 채널 |
| AI-native Code | 변동 (Cursor·Cognition 경쟁) | 매우 높음 | 약함 | 개발자 채택 |
| Creative AI | 변동 큼 (Sora 위협) | 매우 높음 | 큼 (중국 동영상 AI) | 모델+사용자 |

### 5.3 하위 세분화 (Sub-areas)

#### Sub-area 1: Healthcare Vertical ★ 매수 매력 큼
- 정의: AI 기반 진단·치료·신약·임상 시험
- 핵심 상장사: **Tempus AI (TEM)**, Veeva Systems (VEEV), Hims & Hers (HIMS), Exact Sciences (EXAS), Doximity (DOCS)
- 핵심 비상장: Hippocratic AI, Abridge, Ambience
- 매력도: **상장사 노출 가장 풍부**한 vertical. 데이터 lock-in 강. 규제로 진입장벽 高.
- Tempus AI: 70+ 제약 데이터 계약, multimodal data moat. 2026 가이던스 +25%.

#### Sub-area 2: Defense / Government Vertical ★ 정책 모멘텀
- 정의: 군·정부 AI (감시·정보·전장)
- 핵심 상장사: **Palantir (PLTR)** — 사실상 유일한 large-cap pure-play
- 핵심 비상장: Anduril ($30B+), Shield AI
- 매력도: Trump 행정명령 직접 수혜. Palantir 정부 매출 분기 +XX%
- **상장사 직접 노출 부족** — PLTR 외 한정 (RTX·LMT 부분)

#### Sub-area 3: Legal Vertical
- 정의: 법률 연구·계약·DD·컴플라이언스 AI
- 핵심 상장사: **Thomson Reuters (TRI)** (AI 통합 중), Wolters Kluwer
- 핵심 비상장: **Harvey** ($11B, 235 고객), Legora ($5.55B), Hebbia
- 매력도: 상장사 적음. Thomson Reuters 가 incumbent + AI 통합 유일 large-cap 매수처.

#### Sub-area 4: AI-native Productivity / Code Tools
- 정의: 차세대 개발자·지식 노동자용 도구
- 핵심 비상장: **Cursor (Anysphere, $29B)**, Cognition AI ($2B), Replit, Glean
- 매력도: 시장 폭발이지만 **상장사 직접 노출 거의 없음**. Microsoft (GitHub Copilot) 간접.
- IPO 가능성: Cursor·Glean 2026~2027

#### Sub-area 5: Customer Support / Sales AI
- 정의: B2B CS·sales agent
- 핵심 비상장: **Sierra ($10B)**, Decagon ($4.5B), Cresta
- 상장사: Salesforce·HubSpot·Zendesk (별도 Horizontal 영역과 겹침)
- 매력도: 비상장이 더 빠르게 성장. 상장사 (CRM·HUBS) 는 잠식 위험.

#### Sub-area 6: Creative AI
- 정의: 동영상·이미지·음성·3D AI
- 핵심 비상장: Runway, ElevenLabs, Black Forest Labs, Pika
- 핵심 상장사: Adobe (별도 영역)
- 매력도: **상장사 노출 약함**. Sora·OpenAI 위협으로 prod 위험.

#### Sub-area 7: 한국 Vertical AI
- 정의: 한국 도메인 vertical AI
- 핵심: 루닛 (의료 AI, 328130), 셀바스 AI (108860), 솔트룩스 (304100), 마음AI (377480)
- 매력도: 한국 시장 한정 약함. 단 일부 (루닛 의료 영상 AI) 는 글로벌 진출 진행.

---

## 6. 병목 식별

### 6.1 현재 병목
- **enterprise data integration**: vertical AI 가 작동하려면 사내 데이터 정리·통합 필요. SI·컨설팅 비용 큼.
- **"last mile" production-grade**: 99%+ accuracy 가 어려움. demo vs production 격차 큼.
- **AI agent security**: agent 실행 권한·감사 인프라 부족. 첫 보안 사고가 시장 재편 trigger.
- **인재**: vertical AI 도메인 전문가 + AI 엔지니어 hybrid 부족

### 6.2 다음 병목 ★ 투자 핵심
- **AI agent orchestration**: 여러 agent·tool·data system 통합 인프라
- **Vertical-specific compliance**: 의료 (FDA), legal (변호사회), defense (clearance) 인증 시스템
- **Foundation model 의존성 분산**: vertical 회사가 모델 lock-in 으로부터 자유로워지는 multi-model 아키텍처
- **Enterprise contract structure**: per-seat → consumption + outcome-based

→ 본인 선제 포지셔닝 후보: **healthcare vertical 의 데이터 보유 강자 (Tempus·Veeva) + Palantir + Thomson Reuters**

### 6.3 컨센서스 vs 본인 뷰의 갭
- 시장이 보는 것: AI = NVDA + 빅테크 + OpenAI hype
- 본인이 추가로 봐야 할 것:
  - **vertical 의 정직한 매출**: Tempus AI $1.6B, Palantir $7.65B 가이던스 — 빅테크 매출의 1~5%지만 성장률 +71~83%
  - **상장사 노출 부족 = 상대적 alpha**: 비상장 다수라 상장사로 자본 유입 집중 가능 (Palantir 폭등 사례)
  - **healthcare AI 의 도메인 lock-in**: foundation model 위협이 가장 약한 vertical
  - **Anthropic·OpenAI 의 vertical 직접 진입 시점**: PLTR YTD −18% 같은 사례. 모니터링 필수.

---

## 7. 자금 흐름 시그널

### 7.1 관련 ETF
| ETF 티커 | 시장 | 영역 노출도 | 비고 |
|---------|------|----------|------|
| AIQ | US | 부분 | AI 전반, vertical 일부 |
| IHF | US | Healthcare 부분 | TEM·VEEV·HIMS 포함 |
| ITA | US | Defense | PLTR 일부 포함 |
| ARKK | US | Disruptive innovation | PLTR·TEM 포함 |
| 한국 | KR | 약함 | TIGER AI 등 |

### 7.2 추적 지표 (대시보드)
- [ ] **Palantir 분기 매출·가이던스** → P1~P2 (특히 commercial 매출)
- [ ] **Tempus AI 분기 매출·data deal** → P2
- [ ] **Veeva 분기 매출** → P3
- [ ] **Hims & Hers 분기 매출·GLP-1 영향** → P3
- [ ] **비상장 vertical AI funding 라운드** (Harvey·Sierra·Cursor 등) → P3
- [ ] **Cursor·Harvey·Sierra IPO 신호** → P1
- [ ] **AI agent ROI case study** (대기업 reference) → P2
- [ ] **Anthropic·OpenAI vertical 직접 진입** → P1 (PLTR 위협)
- [ ] **AI agent 보안 사고** → P1 (시장 재편)
- [ ] **Trump AI/Defense 행정명령 후속** → P1~P2

### 7.3 Startup Landscape (L2 신호)

비상장 vertical AI 시총 / ARR / 핵심 산업:

| 회사 | Valuation | ARR | Vertical | 비고 |
|------|----------|-----|---------|------|
| Anysphere (Cursor) | $29B | n/a | Code AI | 5개월에 ×3 |
| Harvey | $11B | $75M+ | Legal | AmLaw 50%+ |
| Sierra | $10B | $150M | Customer Support | 7분기 만에 |
| Glean | $7.2B | $200M | Enterprise Search | 9개월 ×2 |
| Abridge | $5.3B | n/a | Healthcare scribe | |
| Legora | $5.55B | n/a | Legal (EU) | $550M Series D |
| Decagon | $4.5B | n/a | CS Agent | |
| Anduril | $30B+ | n/a | Defense | Lockheed 위협 |
| Cognition AI (Devin) | $2B | n/a | Code | |
| Hippocratic AI | n/a | n/a | Healthcare | $126M Series C, NVIDIA 투자 |

**시그널 해석**:
- 자본 유입 패턴: 같은 vertical 다수 회사 펀딩 → 시장 형성 단계 (Sierra/Decagon/Cresta CS 3강)
- 빅테크 CVC 참여: 시장 핵심 시그널 (NVIDIA → Hippocratic, MS·Google → 다수)
- IPO 신호 (2026~2027): Cursor·Glean·Harvey 가능성 큼

---

## 8. 종목 매핑

### 8.1 글로벌 종목

| 티커 | 기업명 | 밸류체인 위치 | Sub-area | 핵심 매수 논리 | 비고 |
|------|-------|------------|---------|-------------|------|
| PLTR | Palantir | Defense + Commercial AI | 2 | Q1 매출 $1.6B, 2026 가이던스 $7.65B (+71%). YTD −18%. 매수 시점 좋으나 P/E 200x+. | **★ Tier A but 가격 부담** |
| TEM | Tempus AI | Healthcare AI | 1 | 매출 +83% (2025), 가이던스 $1.59B. 70+ 제약 데이터 계약. multimodal moat. | **★ Tier A** |
| VEEV | Veeva Systems | Healthcare/Pharma SaaS | 1 | 안정 vertical SaaS. AI 통합 진행. 데이터 lock-in. | Tier B (안정) |
| HIMS | Hims & Hers | Healthcare telehealth + GLP-1 | 1 | GLP-1 telehealth + AI. 별도 GLP-1 영역과 중복. | Tier B |
| TRI | Thomson Reuters | Legal incumbent + AI | 3 | Westlaw + AI 통합. 안정. Harvey 위협 인식. | Tier B (안정 + AI 통합) |
| INTU | Intuit | Finance/Tax AI | 4 | TurboTax·QuickBooks AI 통합. 안정 + AI 신규 매출. | Tier B |
| EXAS | Exact Sciences | Cancer diagnostic AI | 1 | Cologuard + AI 진단. 회복 trajectory. | Tier C |
| DOCS | Doximity | Physician network AI | 1 | 의사 네트워크 + AI 도구. | Tier C |
| AI | C3.ai | 산업 AI | — | 매출 둔화·valuation 부담. | 후순위 |
| HUBS | HubSpot | Sales/Marketing AI | 5 | AI 통합. 별도 Horizontal과 중복. | Tier C |

### 8.2 한국 종목 (transmission 약함)

| 티커 | 기업명 | 밸류체인 위치 | Sub-area | 비고 |
|------|-------|------------|---------|------|
| 328130 | 루닛 | 의료 영상 AI | 1 (KR) | 한국 의료 AI 글로벌 진출 진행 |
| 108860 | 셀바스 AI | 음성·언어 AI | 7 | 한국 시장 한정 |
| 304100 | 솔트룩스 | 한국 LLM·검색 | 7 | 한국 시장 한정 |
| 377480 | 마음AI | 한국 vertical AI | 7 | 한국 시장 한정 |

→ **한국 transmission 약하나, 루닛만 글로벌 진입 가능성**.

### 8.3 매수 우선순위 (참고)

**Tier A (우선 검토)**:
1. **Tempus AI (TEM)** — Healthcare vertical 매출 가시 + 데이터 moat. 가격 합리적.
2. **Palantir (PLTR)** — Defense + Commercial. YTD −18% 매수 시점 좋으나 P/E 200x+ 부담. 분할 매수 권장.

**Tier B (보조·안정)**:
3. **Veeva (VEEV)** — Healthcare incumbent, 안정 SaaS
4. **Thomson Reuters (TRI)** — Legal incumbent + AI 통합
5. **Intuit (INTU)** — Finance/Tax AI 통합
6. **Hims & Hers (HIMS)** — Healthcare + GLP-1 중복 노출

**Tier C (위성·모니터링)**:
7. EXAS, DOCS, HUBS — 각자 한정 노출
8. 루닛 (328130) — 한국 의료 AI 글로벌 진출 모니터링

**비상장 IPO 대기**:
- Cursor (Anysphere) 2026~2027 가능성
- Harvey 2027~
- Sierra 2027~
- Glean 2026~2027
→ IPO 시 초기 모멘텀 모니터링

---

## 9. 모니터링 트리거

- [ ] **Palantir 분기 매출·commercial 가이던스** → P1
- [ ] **Tempus AI 분기 매출·data deal 추가** → P2
- [ ] **Veeva·Thomson Reuters 분기 실적** → P3
- [ ] **비상장 vertical AI IPO 발표** (Cursor·Harvey·Sierra·Glean) → P1
- [ ] **Anthropic·OpenAI vertical 직접 진입** (Palantir 위협) → P1
- [ ] **AI agent 보안 사고** (시장 재편 trigger) → P1
- [ ] **Trump AI/Defense 행정명령 후속** → P1
- [ ] **루닛 글로벌 진출 진척** → P2 (한국 종목)
- [ ] **빅테크 CVC vertical AI 투자** → P3
- [ ] **vertical AI ROI case study** (대기업 reference) → P2

---

## 10. 리스크

- **Foundation model 의 vertical 직접 진입** (가장 큰 리스크) — Anthropic·OpenAI 가 직접 vertical 진입 시 PLTR·Harvey 등 잠식
- **AI agent ROI 입증 실패** — 대기업 reference case 부재 시 시장 둔화
- **AI agent 보안 사고** — 첫 대형 사고 시 시장 재편
- **vertical 회사 valuation 거품** — 52x ARR 평균, 일부 127x ARR. 시장 조정 시 폭락 위험.
- **PLTR 단일 리스크**: 정부 의존도, 가격 200x+ 부담
- **healthcare 규제 강화** — FDA AI/ML 규제 변화 시 진입장벽 ↑
- **글로벌 경기 침체** — enterprise IT 예산 감축 시 vertical AI 지출 후순위로 밀림
- **상장사 적음** — 본 영역 자본이 비상장에 몰려 상장사 alpha 한정

---

## 11. 매크로 변수 민감도

| 매크로 변수 | 영역 영향 | 메모 |
|-----------|---------|------|
| Fed 금리 인하 | ++ (성장주 멀티플 ↑) | PLTR 같은 고멀티플 영향 큼 |
| 달러 강세 | − (해외 매출) | TEM·VEEV 영향 |
| 미중 갈등 | + (Defense AI 강세 — PLTR) | |
| 빅테크 CapEx 둔화 | − (간접 영향, foundation model 가격) | |
| AI 규제 강화 | − (단기), + (장기 진입장벽) | Healthcare 영향 큼 |
| 정권 교체 (2028) | PLTR Defense 매출 변수 | |
| 글로벌 경기 침체 | −− (enterprise IT 예산) | |

---

## 12. 본인 의사결정 메모

> 시스템은 매수 결정 안 함. 본인 참고용.

- 현재 보유 종목: (본인 입력)
- 추가 매수 검토 종목: Tempus AI, Palantir (분할), Veeva
- 청산 검토 종목: (없음)
- 다음 의사결정 시점:
  - PLTR Q2 실적 (8월)
  - TEM Q2 실적 (8월)
  - 비상장 IPO (Cursor·Glean 등) 신호
  - Anthropic·OpenAI vertical 진입 발표

### 본인이 인지해야 할 핵심 trade-off
- **Palantir = 가장 매력 vs 가장 비싸**. 매출 +71% 가이던스가 P/E 200x+ 정당화하는지 본인 판단.
- **Tempus AI = healthcare vertical 의 commitment play**. 데이터 moat 강력하나 적자 → 흑자 전환 단계. 변동성 큼.
- **상장사 적음 = 한계 + 기회**. 자본이 PLTR·TEM 같은 한정된 상장사에 몰림 — 단일 종목 변동성 큼.
- **비상장 IPO 모니터링**: Cursor·Harvey·Sierra·Glean IPO 시점이 본 영역의 큰 모멘텀 trigger.
- **한국 transmission 약함** — 본 영역은 미국 중심.
- **AI Application Foundation/Horizontal 영역과 중복**: 빅테크 비중 줄이고 vertical에 분산 시 alpha 가능성.

---

## 13. 업데이트 로그

| 날짜 | 변경 사항 | 점수 변화 |
|------|---------|---------|
| 2026-05-23 | 최초 작성 (v2.1 룰 적용) | TAM 5, Moat 4, Capital 4 → 합산 13/15. Conf. Medium-High. 시차 A4 B3 C3 = +4 (Good entry). Tier 1 확정. |


---

# ═══════════════════════════════════════════════════
# v2.3 UPGRADE — Next Wave Deep + KR Transmission
# ═══════════════════════════════════════════════════

> *아래 내용은 v2.3 retrofit 으로 위 v2.1 본문에 추가된 섹션입니다. 기존 본문은 그대로 유지하고 적용*

---

# AI Vertical (Application) — v2.3 Retrofit Delta

> **Base document**: 04_ai_application_vertical.md (v2.1, 25KB)
> **Retrofit 작성일**: 2026-05-24
> **변경 사항**: Next Wave Deep (6.4·6.5) + KR transmission 강화

---

## 본 문서 적용 가이드

- **6.4 Next Wave Deep Analysis** — *신규 추가*
- **6.5 Next Wave 종합** — *신규 추가*
- **5.3 Sub-area X: 한국** — *thorough 보강*
- **8.2 한국 종목** — *thorough 보강*
- **12 비중 분배 권장** — KR 강화
- **13 업데이트 로그** — v2.3 retrofit 진입

---

## 5.3 Sub-area X: 한국 — *KR pure-play thorough* (보강)

### KR 상장 AI Vertical pure-play

| 티커 | 기업 | 영역 | 시총 | 핵심 thesis | Tier |
|------|------|-----|-----|----------|------|
| **328130** | **루닛** ★ | L2 AI 의료영상 (oncology) | 5,000~7,000억원 | **K-AI 의료영상 1위**. INSIGHT CXR (폐결절·간질환·결핵), INSIGHT MMG (유방암). 글로벌 hospital 채택 가속. *정밀 종양학 영역 cross* | **A KR 1순위 (정밀 종양학 cross)** |
| **338220** | **뷰노** | L2 AI 의료 (다중 진단) | 2,000~4,000억원 | DeepCARS·DeepECG·DeepBrain, 한국 보험 인정 가속 | **A KR 2순위** |
| **060280** | **큐렉소** | L2 의료 로봇 (수술용 AI) | 3,000~5,000억원 | CUVIS-spine 수술 로봇, AI 영상 통합. 휴머노이드 영역 cross | **B KR 3순위 (휴머노이드 cross)** |
| **287410** | **제이엘케이** | L2 AI 의료 (뇌졸중·CT) | 1,500~3,000억원 | AI 뇌졸중 진단, 변동성 | **B KR (변동성)** |
| **131370** | **알서포트** | L2 enterprise AI (원격·support) | 1,500~2,500억원 | 한국 enterprise AI | **B KR 위성** |
| **402030** | **에이아이엠퓨처** | L2 산업 AI | 2,000~4,000억원 | 산업 AI, 변동성 | **C KR 변동성** |
| **042510** | **라온피플** | L2 산업 AI vision | 2,000~3,000억원 | 산업 검사 AI vision | **C KR 위성** |
| **376300** | **디어유** | L2 K-콘텐츠 AI (Bubble) | 4,000~6,000억원 | SM-NCSOFT AI fan platform | **C KR 변동성** |
| **293490** | **카카오게임즈** | L2 게임 AI | 3~4조원 | 게임 + AI integration | **C 위성** |

### KR Vertical 핵심 영역

- **AI Medical (Oncology·Cardiology·Radiology)**: 루닛·뷰노·제이엘케이·큐렉소 — *정밀 종양학 영역 cross*
- **AI Defense**: 한화시스템·LIG넥스원 — *K-방산 영역 cross*
- **AI Finance**: 신한·KB·하나·우리 자체 LLM 가속
- **AI Legal·HR**: 한국 startup 비상장
- **AI Industrial / Manufacturing**: 라온피플·에이아이엠퓨처
- **AI Mobility**: 자율주행 영역 cross
- **AI Bio Drug Discovery**: 정밀 종양학 영역 cross

### KR 비상장 / IPO 후보

- **업스테이지 (비상장)** — sovereign LLM (Solar)
- **포티투닷 (현대차 자회사)** — 자율 AI cross
- **마음AI (비상장)** — K-AI chatbot
- **스캐터랩 (비상장, 카카오)** — 페르소나 AI
- **노타 (비상장)** — AI 압축·on-device
- **인이지 (비상장)** — 산업 AI
- 코난테크놀로지·플리토 — IPO 시그널

### 진입 전략 (KR 우선순위)

- **KR 1순위: 루닛 (328130)** — *AI 의료영상 글로벌 가속*, 정밀 종양학 cross
- **KR 2순위: 뷰노 (338220)** — AI 의료 다중
- **KR 3순위: 큐렉소 (060280)** — 의료 로봇 AI (휴머노이드 cross)
- **KR 4순위 위성**: 제이엘케이·알서포트·라온피플
- **K-방산 AI (한화시스템·LIG)** — K-방산 영역 매수

---

## 6.4 Next Wave Deep Analysis ★★★ (신규 추가)

> v2.3 mandatory. Palantir·Cadence·Synopsys over-known. 다음 알파 3개.

---

### Next Wave 1: AI Medical (Oncology·Cardiology·Radiology) ★★★ 2026~2028

**왜 next wave 인가**
- 글로벌 AI medical 시장 2025 ~$3B → 2030 ~$15B (CAGR 35%)
- **루닛·뷰노 글로벌 hospital 채택 가속** (미국·EU·일본·동남아)
- FDA AI medical 승인 가속
- 한국 보험 인정 + 미국 Medicare reimbursement 가속
- *정밀 종양학 영역 cross*: ADC·Keytruda 진단·치료 통합

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Intuitive Surgical (ISRG)** ★ | US | 수술 로봇 + AI 통합 | **A 1순위 (안정)** |
| **Tempus AI (TEM)** | US | precision medicine AI | **B (신생 IPO 변동성)** |
| **Veeva Systems (VEEV)** | US | pharma cloud + AI | B 안정 |
| **루닛 (328130)** ★ | KR | AI 의료영상 글로벌 가속 | **A 1순위 KR** |
| **뷰노 (338220)** | KR | AI 의료 다중 | B KR 2순위 |
| 큐렉소 (060280) | KR | 의료 로봇 + AI | C 위성 (휴머노이드 cross) |

**Timing**: 2026~ 글로벌 hospital 채택 가속, FDA·CE 인증

---

### Next Wave 2: AI for Defense ★★★ 2026~2027

**왜 next wave 인가**
- **Palantir Foundry + Gotham + AIP** = Defense AI 1위
- **Anduril Lattice OS** = AI 자율 C2
- **C3.ai (AI)** = defense·federal
- *국방·드론 영역 cross*

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Palantir (PLTR)** ★ | US | Foundry·Gotham·AIP, $10B Army | **A 1순위 (가격 부담 분할)** |
| **Anduril (비상장)** | US | Lattice OS, $20B Army, $61B | n/a (IPO 2026~2027) |
| **Booz Allen (BAH)** | US | federal AI | B 안정 |
| **Leidos (LDOS)** | US | federal IT + AI | B 안정 |
| **한화시스템 (272210)** | KR | K-방산 AI (위성·전자전) | K-방산 영역 cross |
| **LIG넥스원 (079550)** | KR | K-방산 AI | K-방산 영역 cross |

**Timing**: 2026~ Defense AI 본격 가속, Anduril IPO catalyst

---

### Next Wave 3: AI Finance / Legal / HR ★★ 2026~2028

**왜 next wave 인가**
- **AI 금융 (rating·trading·compliance·fraud)** 가속
- **AI Legal (Harvey·Spellbook)** — 미국 변호사·금융업
- **AI HR (Workday·SAP)** — Enterprise HR 채택
- 글로벌 AI Enterprise 시장 2025 $20B → 2030 $100B+

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **MSCI (MSCI)** | US | finance index + AI analytics | A 안정 위성 |
| **Moody's (MCO)** | US | rating + AI | A 안정 위성 |
| **S&P Global (SPGI)** | US | rating + AI | A 안정 위성 |
| **Workday (WDAY)** | US | HR + AI | B 위성 |
| **SAP (SAP)** | DE | Enterprise + AI | B EU 안정 |
| **Salesforce (CRM)** | US | CRM + agents (AI Foundation cross) | AI Foundation 중복 |
| **신한·KB·하나·우리금융** | KR | 자체 LLM | C KR 금융 |
| **Harvey (비상장)** | US | AI legal | n/a (IPO 시그널) |

**한국**
- 신한금융 (055550), KB금융 (105560), 하나금융 (086790), 우리금융 (316140) — 자체 LLM 진입
- 신한 SOAR, KB Liiv, 하나 AI 어드바이저 — 위성

---

## 6.5 Next Wave 종합 — 본인 진입 전략

**우선순위 (Timing + 상장 alpha)**

| 순위 | Next Wave | Timing | 핵심 종목 | 비중 |
|-----|---------|--------|---------|-----|
| 1 | **AI Medical** | 2026~2028 | **ISRG (US), 루닛 (KR 1순위), Tempus (변동성)** | 1~2% |
| 2 | **AI for Defense** | 2026~2027 | **Palantir (본문 매수), Anduril IPO (catalyst)** | 본문 중복 |
| 3 | **AI Finance/Legal/HR** | 2026~2028 | **MSCI, MCO, SPGI (안정)** | 0.5~1% (위성) |

### AI Vertical 영역 종합 매수 우선순위

**Tier A — 즉시 분할 매수**

**글로벌**
1. **Palantir (PLTR)** — 본문 1순위 (가격 부담 분할)
2. **Intuitive Surgical (ISRG)** ← Next wave AI Medical 1순위
3. **Cadence (CDNS), Synopsys (SNPS)** — 본문 EDA AI (안정)
4. **MSCI (MSCI), Moody's (MCO), S&P (SPGI)** — Next wave AI Finance
5. **Tempus AI (TEM)** — AI Medical 신생 변동성

**KR (Tier A) — 본인 정보 비대칭 우위**
1. **루닛 (328130)** ★ **KR 1순위 next wave AI Medical** (정밀 종양학 cross)
2. **뷰노 (338220)** **KR 2순위 AI Medical**
3. **큐렉소 (060280)** — 의료 로봇 AI (휴머노이드 cross)
4. **NAVER (035420), 카카오 (035720)** — AI Foundation 영역에서 매수
5. **한화시스템 (272210), LIG (079550)** — K-방산 영역에서 매수
6. 신한·KB·하나·우리금융 — AI Finance KR 위성

**모니터링 watchlist (비상장 IPO)**
- **Anduril IPO** (2026~2027) ★ catalyst
- **Harvey IPO** (AI legal)
- **업스테이지·마음AI·노타 IPO** (KR)
- **포티투닷** (현대차 자회사, 자율 cross)

### 글로벌:KR 비중 분배 권장

- **글로벌 75~85% : KR 15~25%** (AI Vertical 글로벌 dominant, KR 의료영상·금융 부분)

---

## 12 본인 의사결정 메모 — 비중 분배 권장 (v2.3 추가)

### 비중 가이드

- 본 영역 전체: **포트폴리오의 5~8%** (AI Vertical 별도)
- *AI 인프라 합산 25~35% 상한* 인지
- **글로벌 75~85% : KR 15~25%**
- 종목별:
  - PLTR 1~2% (가격 부담 분할), ISRG 0.5~1%, CDNS 0.5%, SNPS 0.5%
  - MSCI·MCO·SPGI 합산 0.5~1%, Tempus 0.3% (변동성)
  - 루닛 0.5~1%, 뷰노 0.3~0.5%, 큐렉소 0.3% (휴머노이드 cross)
  - 한화시스템·LIG = K-방산 영역
  - NAVER·카카오 = AI Foundation 영역
  - 신한·KB·하나·우리금융 합산 0.3~0.5% (KR 금융 위성)

### Cross-area 중복 카운트
- **루닛** = 정밀 종양학 cross → 한쪽만 매수
- **큐렉소** = 휴머노이드 cross → 한쪽만 매수
- **NAVER·카카오** = AI Foundation cross → AI Foundation 영역에서 매수
- **한화시스템·LIG** = K-방산 cross → K-방산에서 매수
- **CRM·NOW·ADBE** = AI Foundation cross → AI Foundation 영역에서 매수

---

## 13 업데이트 로그 — v2.3 retrofit 진입

| 날짜 | 변경 |
|------|------|
| 2026-05-24 | **v2.1 → v2.3 retrofit**. Next Wave Deep (6.4·6.5) 신규 추가, KR transmission thorough 보강. 매수 우선순위 업데이트: **PLTR > ISRG (next wave AI Medical) > CDNS·SNPS > MSCI·MCO·SPGI (next wave Finance) > Tempus** + **KR: 루닛 (KR 1순위 next wave AI Medical 정밀 종양학 cross) > 뷰노 > 큐렉소 (휴머노이드 cross) > 한화시스템·LIG (K-방산 cross) > NAVER·카카오 (AI Foundation cross) > 신한·KB·하나·우리금융 (위성)**. **Next Wave Deep 3개**: (1) **AI Medical** (ISRG 안정, 루닛 KR 1위, Tempus 변동성, 뷰노), (2) **AI for Defense** (Palantir·Anduril IPO catalyst, BAH·LDOS, 한화시스템·LIG K-방산 cross), (3) **AI Finance/Legal/HR** (MSCI·MCO·SPGI 안정, Workday·SAP·CRM, Harvey IPO 시그널). **KR 비중 분배 권장 75~85% : 15~25%**. Cross-area 중복 카운트 인지 (루닛·큐렉소·NAVER·한화시스템 등). |
| (이전) | v2.1 본문 작성 |

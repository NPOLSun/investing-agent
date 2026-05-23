# AI Application: Foundation Models + Horizontal SaaS — Tier 1 Deep Dive

> **Trigger**: 빅테크 매수·매도 결정과 직접 관련. 사용자 요청으로 1차 배치 추가.
> **Linked methodology**: methodology.md v2.1
> **Note**: Vertical AI / AI-native SaaS (Palantir 등) 는 별도 영역으로 분리 — 다음 deep-dive 대상.

---

## 0. 메타 정보

| 항목 | 값 |
|------|----|
| 작성일 | 2026-05-23 |
| 최근 갱신 | 2026-05-23 |
| 다음 정기 갱신 | 2026-07-01 (Q3 첫 주) |
| 시계 분류 | Core (1.5~2.5년) — 단, layer별로 다름 |
| Tier | 1 (Deep) |
| Confidence (총점) | High (빅테크 데이터 풍부, foundation model 가치 산정만 Medium) |
| 트랙 | L1A (Global) — 한국 transmission 약함 |

---

## 1. 한 줄 요약 + 핵심 가설

### 한 줄 요약
> Foundation model 매출이 2026 폭증 (OpenAI $25B ARR, Anthropic $19B ARR, 둘 다 분기 ×2 페이스). 그러나 **상장사 직접 노출은 빅테크 (MSFT·GOOGL·AMZN·META) 와 Horizontal SaaS (CRM·NOW·ADBE) 한정**. Agentic AI 가 2026 키워드, Microsoft 15M paid Copilot seat. 가격은 빅테크별 격차 큼. Microsoft 가 가장 매출 가시화, Meta·Google이 가장 valuation 매력.

### 핵심 가설

- **가설 A**: Foundation model 시장은 **OpenAI·Anthropic·Google·Meta·xAI 5강 체제** 굳어짐. 빅테크 3사 (MSFT-OpenAI 제휴·GOOGL-자체·AMZN-Anthropic 제휴) 가 핵심 노출 채널. 비상장 (OpenAI·Anthropic·xAI) IPO는 2026 하반기~2027.
- **가설 B**: **Agentic AI 전환**이 2026 SaaS 재편 트리거. Microsoft Wave 3 agentic + Salesforce Agentforce + ServiceNow agentic 출시. Per-seat 모델 → consumption + agent 모델로. **기존 SaaS 강자가 농구공처럼 살아남거나 잠식당하는 binary 시점**.
- **가설 C**: Foundation model 가격 압박 시작. 중국 (DeepSeek·MiniMax·Knowledge Atlas IPO) + 오픈소스 (Meta Llama) → 가격 인하 압력. Anthropic 가격 인상 (Uber 사례 — €67 → €966) 같은 enterprise budget 문제 발생. **승자: 효율 좋은 inference (Anthropic Haiku·OpenAI 저비용 모델) + 자체 모델 보유 (Google·Meta)**.
- **가설 D**: **Microsoft 의 monetization 가시화 가장 빠름**. 15M paid Copilot seat → $5.4B ARR. 2026 Microsoft 365 + Copilot 번들링으로 추가 monetization. 단, Azure CapEx $190B 가이던스로 ROI 의문 지속.

### 기각 조건
- 빅테크 4사 합산 AI CapEx 가이던스 분기 −20% 이상 하향
- OpenAI·Anthropic 분기 매출 둔화 (둘 다 동시)
- Copilot paid seat 분기 신규 추가 둔화 (Microsoft IR 추적)
- Foundation model 가격 폭락 (token 가격 30%+ 하락) — 마진 자체 위협
- Agentic AI ROI 입증 실패 (대기업 reference case 부재)

---

## 2. 잣대 채점

### 잣대 1: TAM

| 항목 | 값 |
|------|----|
| 점수 | 5 / 5 |
| 카테고리 | Mega-transformative |
| Confidence | High |

**근거**:
- 전세계 enterprise SaaS 시장: 현재 ~$300B (Gartner). AI 통합 후 ×2~3 가능 (가격 인상 + 신규 카테고리)
- Foundation model 자체 매출: OpenAI 2026 Q1 ARR $25B+ (Sacra), Anthropic 19B → 26B 가이던스 (2026)
- 합산 foundation model 시장 ~$60~80B ARR (2026), 2030 $300B+ 가능 (consensus)
- **Agentic AI enterprise 시장**: $9B (2026, projected)
- Microsoft AI 매출 직접: $37B (2026 추정)
- 전 산업 AI 통합 시 영향 시장 $1T+ (10년 시계)
- **×10 + 100B$ 도달 확실. 5점.**

### 잣대 2: Moat (해자 재편 + 비가역성)

| 항목 | 값 |
|------|----|
| 점수 | 4 / 5 |
| Confidence | High |

**근거**:
- 기존 강자: Microsoft·Google·Amazon·Meta·Salesforce·ServiceNow·Oracle·Adobe·SAP
- **Moat 재편 양상**:
  - Foundation model layer: 5강 (OpenAI·Anthropic·Google·Meta·xAI) 형성, 중국 follow-up
  - Horizontal SaaS: 기존 강자 (CRM·NOW·ADBE) 가 Agentic AI 통합으로 *살아남거나* point-solution 스타트업에 잠식
  - Microsoft 가 일반 productivity layer 거의 독식 (15M Copilot seat)
  - Google·Meta는 자체 모델 보유로 유리, Apple은 자체 모델 약함
- **Moat 재편 강함**: 2025년 "Software Apocalypse" (밸류에이션 압축) 이후 Microsoft가 break-out → 기존 SaaS 회사 binary 갈림

**비가역성 평가**:
- Microsoft 365 user base 의 Copilot embed = 매우 강한 lock-in. 되돌리려면 거의 불가
- 빅테크 AI CapEx 누적 sunk cost ~$600B (2024~2026) — 되돌릴 수 없음
- OpenAI·Anthropic·Google·Meta·xAI 의 모델 weight + 사용자 base = 비가역
- 단, foundation model layer 는 **빠른 commoditization** 위험 — DeepSeek 사례
- **비가역성 양분**: Distribution layer (빅테크) 는 매우 강, foundation model layer 는 중간

**해석**:
- 새 카테고리 (Agentic AI) 형성 + 기존 강자 일부 도태 시작
- 마진 구조 재편 중 (per-seat → consumption + agent)
- **4점** (Major reshuffle + 비가역 강), 5점은 아님 (도태가 명확하지 않음)

### 잣대 3: Capital

| 항목 | 값 |
|------|----|
| 점수 | 5 / 5 |
| Confidence | High |

**근거** (출처 명시):
- 빅테크 4사 (MSFT·META·GOOGL·AMZN) 2026 AI CapEx: ~$650B
- 이 중 AI software·model 직접 투입 (chip CapEx 외): ~$200B+
- Microsoft 단독 2026 CapEx 가이던스: $190B
- VC 펀딩 AI startup (2024~2025): ~$50B
- OpenAI 추가 펀딩 (2025~2026): SoftBank $40B 펀딩, Anthropic $13B Series F
- Foundation model 5강 합산 valuation: OpenAI $782B + Anthropic $370B + xAI $244B + Google·Meta 내부 = $1.5T+
- **합산 직접 자본 ~$200~300B/년**

**해석**:
- 500B$+ 임계 충족. **5점** 확실.

### 합산

| 트랙 | 합산 점수 | 통과 임계 | Tier 1 임계 |
|------|---------|---------|-----------|
| L1A | **14 / 15** | ≥ 9 ✅ | ≥ 12 ✅ |

**영역 전체 Confidence**: High

→ **Tier 1 강력 확정. 백지 메가 체인지 맵에서 합산 최상위.**

---

## 3. A·B·C 시차 평가

### A 지표 (자본 유입)
| 항목 | 값 |
|------|----|
| 점수 | **5 / 5** (정점 진입 중) |
| 갱신일 | 2026-05-23 |

**근거**:
- 빅테크 CapEx 가속: 2025 $400B → 2026 $650B (75% 증가)
- OpenAI·Anthropic 매출 분기 ×2 페이스
- VC 펀딩 AI startup 분기 신기록
- **자본은 이미 정점 가까이.**

### B 지표 (실물 변화)
| 항목 | 값 |
|------|----|
| 점수 | **4 / 5** (강한 진행 중) |
| 갱신일 | 2026-05-23 |

**근거**:
- Microsoft 15M paid Copilot seat (2026 Q1), 분기 +160%
- OpenAI 50M+ paying subscriber, 900M+ weekly active
- Anthropic Q1 2026 매출 $4.8B → Q2 $10.9B 가이던스 (×2 분기)
- Enterprise 도입 폭증: 300,000+ firm Anthropic Claude 사용
- Salesforce Agentforce + ServiceNow agentic + Microsoft Wave 3 동시 출시
- **실물 변화 강. 단, ROI 입증은 진행 중.** 4점.

### C 지표 (가격 반영)
| 항목 | 값 |
|------|----|
| 점수 | **5 / 5** (완전 반영 또는 과열) |
| 갱신일 | 2026-05-23 |

**근거**:
- Microsoft: 시총 ~$4T, Forward P/E ~30x, 8.62x NTM EV/Revenue. 부분 반영.
- Alphabet: 시총 ~$2.5T, Forward P/E ~25x. 부분 반영 (Gemini 등 부족 인식).
- Meta: 시총 ~$1.5T, Forward P/E ~25x. **상대적 저평가** (CapEx 우려).
- Amazon: 시총 ~$2T, AWS AI 비중 부분 반영.
- **NVDA** (AI Compute 영역이지만 연관): 시총 ~$4T+, 완전 반영
- Foundation models 비상장: OpenAI $782B (12x revenue), Anthropic $370B (19x revenue) — **vc 시장 과열 수준**
- Salesforce: P/E 28x, 비교적 합리적이나 Agentic 전환 변수
- ServiceNow: P/E 60x, 프리미엄 (Agentic AI 수혜 기대)
- Adobe: P/E 22x, 상대적 매력
- **전체적으로 빅테크 상당 반영, 일부 (Meta·Google·Adobe) 매력 잔존, 비상장은 과열**. **5점** (완전 반영 또는 과열)

### 시차 매력도 = A + B − C

| 항목 | 값 |
|------|----|
| 계산 | 5 + 4 − 5 = **+4** |
| 카테고리 | **Good entry** |

**해석**:
- 자본·실물·가격 모두 강하나 **가격이 자본·실물 따라잡음**. 시차 매력 양호하나 GLP-1 (+5) 만큼은 아님.
- 진입 전략: **layer별 분화 필수**
  - 빅테크 직접: Microsoft (가장 안전), Meta·Google (valuation 매력)
  - Horizontal SaaS: Salesforce·ServiceNow 등 (Agentic 수혜 vs 잠식 binary)
  - Foundation models: 비상장 직접 매수 불가, 빅테크 통한 간접 노출
  - 한국: 거의 transmission 없음 — 본 영역은 미국 중심

---

## 4. 산업 메가트렌드

### 4.1 수요 측
- **Enterprise AI 도입 폭증**: 300,000+ firm Anthropic Claude 사용
- **Agentic AI**: Per-seat 모델 → 자동화·agent 모델로 전환
- **Consumer AI**: ChatGPT 900M+ WAU
- **5년 성장률**: enterprise SaaS 가격 인상 + AI agent 추가 매출로 연 30%+ 가능 (일부 영역)
- **구조적**. 사이클 아님. 단, ROI 입증 실패 시 단기 둔화 가능.

### 4.2 공급 측
- Foundation model 5강 경쟁 격화
- 중국 cheap model (DeepSeek·MiniMax·UBT 등) 진입
- Open source (Llama·Mistral) 가격 압박
- **공급 측 commoditization 진행 중** → foundation model layer 마진 압박, distribution layer 우위

### 4.3 정책·지정학 변수
- **AI 규제 (EU AI Act, 미국 행정명령)**: 컴플라이언스 비용 증가, 대기업 유리
- **미중 AI 경쟁**: 중국 cheap model 미국 진입 견제 (정책 변수)
- **개인정보·저작권 소송**: NYT vs OpenAI, 음악 산업 등 (변동성)
- **반독점 우려**: Microsoft-OpenAI, Google-Anthropic 등 빅테크-foundation model 제휴 견제 가능성

---

## 5. 밸류체인 매핑

### 5.1 다이어그램
```
[Foundation Models (대부분 비상장)]
   ├─ OpenAI (Microsoft 제휴) — 비상장
   ├─ Anthropic (Amazon·Google 제휴) — 비상장
   ├─ Google DeepMind / Gemini — Alphabet
   ├─ Meta AI / Llama — Meta
   ├─ xAI / Grok — Elon Musk, 비상장
   ├─ 중국: DeepSeek, Qwen (Alibaba), Knowledge Atlas (상장 2026)
        ↓
[Model Infrastructure / Cloud]
   ├─ Microsoft Azure (OpenAI 제휴)
   ├─ Amazon AWS (Anthropic 제휴 + Bedrock)
   ├─ Google Cloud (자체 + Anthropic 일부)
   ├─ NVIDIA (chip layer — 별도 영역 AI Compute)
   ├─ Databricks (비상장)
        ↓
[Horizontal AI Applications]
   ├─ Microsoft 365 Copilot (★ 가장 monetization 가시)
   ├─ Google Workspace + Gemini
   ├─ Apple Intelligence (자체 모델 + ChatGPT 통합)
   ├─ Adobe Firefly + AI (Photoshop·Acrobat)
   ├─ Notion AI, Asana AI 등 productivity SaaS
        ↓
[Enterprise SaaS w/ AI (Horizontal)]
   ├─ Salesforce (Agentforce) — CRM 1위
   ├─ ServiceNow (Now Assist + agentic) — ITSM 1위
   ├─ SAP (Joule AI) — ERP 1위
   ├─ Oracle (자체 AI + OpenAI 제휴)
   ├─ Workday (HCM AI)
   ├─ Atlassian (Rovo AI), HubSpot, Box, Slack 등
        ↓
[Dev Tools / Code AI]
   ├─ GitHub Copilot (Microsoft 산하)
   ├─ Cursor (비상장)
   ├─ Anthropic Claude Code ($1B ARR)
   ├─ Replit, Tabnine, Sourcegraph
        ↓
[Consumer AI]
   ├─ ChatGPT (OpenAI, 50M+ paying)
   ├─ Claude.ai (Anthropic)
   ├─ Gemini (Google)
   ├─ Perplexity (비상장)
   ├─ Character.AI (비상장)
```

### 5.2 레이어별 분석

| 레이어 | 마진 수준 | 경쟁 강도 | 중국 침투 | 진입장벽 |
|--------|---------|---------|---------|---------|
| Foundation Models | 변동 큼 (가격 압박) | 매우 높음 (5강 + 중국) | 큼 (DeepSeek 등) | 자본+데이터+인재 |
| Model Infrastructure (Cloud) | 매우 높음 | 낮음 (Azure·AWS·GCP 과점) | 거의 없음 (안보) | 자본 (수십B$) |
| Horizontal AI Apps (productivity) | 매우 높음 | 낮음 (Microsoft 독점) | 거의 없음 | distribution lock-in |
| Enterprise SaaS w/ AI | 높음 | 중간 | 거의 없음 | 채널·기존 deployment |
| Dev Tools / Code AI | 변동 (가격 압박) | 매우 높음 (스타트업+빅테크) | 약함 | 개발자 채택 |
| Consumer AI | 변동 큼 (모델 비용 ↑) | 매우 높음 | 큼 | 사용자 acquisition |

### 5.3 하위 세분화 (Sub-areas)

#### Sub-area 1: 빅테크 직접 (4사) ★ 매수 핵심
- 정의: Microsoft, Alphabet, Meta, Amazon
- 핵심 매력 차이:
  - **Microsoft**: AI monetization 가장 가시 (Copilot $5.4B ARR, 15M seat). Forward P/E 30x, 가격 부담 있으나 정당화.
  - **Meta**: CapEx 우려로 valuation 매력. 자체 Llama + 광고 시너지. **상대적 저평가**.
  - **Google (Alphabet)**: Gemini 자체 + AWS 의존 없음. 검색 변화 우려. Forward P/E 25x.
  - **Amazon**: AWS Bedrock + Anthropic 제휴. AWS AI 매출 비중 점증. Forward P/E 35x.

#### Sub-area 2: Foundation Models (간접 노출)
- 정의: 비상장 OpenAI·Anthropic·xAI + Google·Meta (내부)
- 핵심 노출 경로:
  - Microsoft → OpenAI (49% 지분)
  - Amazon → Anthropic ($8B 누적 투자)
  - Google → Anthropic ($3B+ 투자) + 자체 Gemini
  - SoftBank → OpenAI 11% (TYO 9984 통한 간접 노출)
- IPO 가능성: OpenAI 2026 하반기~2027, Anthropic 2026~2027
- 매력도: 직접 매수 불가, 빅테크 통한 간접만

#### Sub-area 3: Horizontal SaaS (CRM·NOW·SAP·Workday)
- 정의: 기존 SaaS 강자가 Agentic AI 통합
- 핵심 플레이어: Salesforce, ServiceNow, SAP, Workday, Adobe
- 매력도 분기:
  - **잠식 위험**: 기존 per-seat 모델이 Agentic으로 잠식
  - **수혜**: AI 통합 후 가격 인상·신규 카테고리 매출
  - **Binary 시점**: 2026 Q3~Q4 분기 실적이 결판
- ServiceNow Forward P/E 60x (프리미엄), Salesforce 28x (합리적)

#### Sub-area 4: Dev Tools / Code AI ★ 빠른 성장
- 정의: 개발자용 AI 도구
- 핵심: GitHub Copilot (MSFT 산하), Cursor (비상장), Claude Code, Replit
- 매력도: 시장 폭발 (Anthropic Claude Code 단일 제품 $1B ARR)
- 상장사 직접 노출 한정 — Microsoft 통한 GitHub Copilot
- **상장사 진입 어려움** — 비상장 다수

#### Sub-area 5: Adobe + Creative AI
- 정의: 콘텐츠 제작 AI
- 핵심: Adobe (Firefly), Canva (비상장)
- 매력도: Adobe 가격 매력 (P/E 22x), 단 OpenAI Sora·이미지 모델 직접 위협
- Binary 시점

#### Sub-area 6: 한국 (transmission 약함)
- 정의: 한국 horizontal AI SaaS
- 핵심: 카카오·네이버 (자체 AI 모델), 한컴 (Office AI)
- 매력도: 약함. 글로벌 시장 진입 어려움. 한국 시장 한정.

---

## 6. 병목 식별

### 6.1 현재 병목
- **GPU / 컴퓨트**: Anthropic Colossus 1 전체 인수 사례. 모델 학습·추론 GPU 부족.
- **인재**: AI 엔지니어 인건비 폭등 ($1M+/년 빈번)
- **enterprise 데이터 통합**: Agentic AI 작동 위한 사내 데이터 파이프라인
- **ROI 입증**: 대기업 reference case 부족 (특히 productivity layer)

### 6.2 다음 병목 ★ 투자 핵심
- **inference 비용**: 모델 학습보다 inference 가 더 큰 비용. **효율 (efficient inference) 이 차세대 경쟁**.
- **enterprise security·governance**: Agentic AI 가 실행하는 action 의 audit·permission
- **모델 차별화**: 5강 commoditization 진행 → 차별화 점차 어려움 → **distribution + integration 우위**
- **AI agent orchestration**: 여러 agent·도구·시스템 통합 인프라

→ 본인 선제 포지셔닝 후보: **distribution 강자 (Microsoft) + 효율 모델 (Anthropic via Amazon) + agent orchestration 인프라**

### 6.3 컨센서스 vs 본인 뷰의 갭
- 시장이 보는 것: AI = NVDA + Microsoft + OpenAI hype
- 본인이 추가로 봐야 할 것:
  - **layer별 마진 격차**: Foundation model layer 는 commoditization (-) / Distribution layer (Microsoft·Google·Meta) 는 lock-in (+)
  - **Meta·Google valuation 비대칭**: 자체 모델 + 데이터 + 광고 시너지에도 빅테크 중 가장 저평가
  - **Agentic AI ROI 입증 binary**: 2026 Q3~Q4 분기 실적이 SaaS 재편의 결정적 변수
  - **OpenAI cash burn 리스크**: $17B (2026) → $35B (2027) → $47B (2028) — Microsoft 위험 노출

---

## 7. 자금 흐름 시그널

### 7.1 관련 ETF
| ETF 티커 | 시장 | 영역 노출도 | 비고 |
|---------|------|----------|------|
| XLK | US | 빅테크 직접 | Tech sector ETF |
| QQQ | US | 빅테크 중심 | Nasdaq 100 |
| AIQ | US | AI 직접 노출 | Global X AI ETF |
| BOTZ | US | AI + 로봇 | |
| IGV | US | 소프트웨어 ETF | |
| 한국 | KR | 약함 | 한국 AI ETF 일부 (TIGER AI 등) |

### 7.2 추적 지표 (대시보드)
- [ ] **빅테크 4사 분기 실적·CapEx 가이던스** → P1~P2
- [ ] **Microsoft 365 Copilot paid seat 분기 추가** → P2
- [ ] **OpenAI·Anthropic 분기 매출 leak** (The Information 등) → P3
- [ ] **Foundation model 가격 변화** (token 가격) → P3
- [ ] **Agentic AI ROI case study** (대기업 reference) → P2
- [ ] **OpenAI·Anthropic IPO 신호** → P1
- [ ] **AI 규제 변화** (EU AI Act, 미국) → P2
- [ ] **빅테크-foundation model 제휴 변화** (Microsoft-OpenAI 재협상 등) → P1
- [ ] **Salesforce·ServiceNow·SAP Agentic AI 매출 segment** → P2~P3

### 7.3 Startup Landscape (L2 신호)
- **OpenAI**: 시총 $782B, ARR $25B, cash burn $17B (2026)
- **Anthropic**: 시총 $370B (~$1T 목표), ARR $19B, 2027 흑자 전망
- **xAI**: 시총 $244B, Colossus 1 매각 (Anthropic 이전)
- **소형**: Mistral $13B, Cohere $6B, Liquid AI $3B
- **중국**: DeepSeek·MiniMax 진입, Knowledge Atlas IPO (2026-01)

**시그널 해석**:
- 수혜 상장사: Microsoft (OpenAI 49%) > Amazon (Anthropic 투자자) > Google (Gemini 자체 + Anthropic 일부)
- 위협받는 상장사: Salesforce·ServiceNow (잠식 vs 수혜 binary), Apple (자체 모델 약함)

---

## 8. 종목 매핑

### 8.1 글로벌 종목

| 티커 | 기업명 | 밸류체인 위치 | Sub-area | 핵심 매수 논리 | 비고 |
|------|-------|------------|---------|-------------|------|
| MSFT | Microsoft | Cloud + Horizontal AI + OpenAI 49% | 1, 2, 3 | Copilot $5.4B ARR + 15M seat. 가장 monetization 가시. 다만 CapEx $190B 의문. | Forward P/E 30x, 가격 부담 |
| META | Meta Platforms | 자체 Llama + 광고 시너지 | 1, 2 | **빅테크 중 가장 저평가**. CapEx 우려 반영. 자체 모델 + 광고 데이터. | **★ Tier A 우선** |
| GOOGL | Alphabet | Gemini + Google Cloud | 1, 2, 3 | Forward P/E 25x. 검색 변화 우려로 약세. 자체 모델 강. | **★ Tier A 우선** |
| AMZN | Amazon | AWS + Anthropic 제휴 | 1, 2 | Bedrock + Claude. AWS AI 매출 비중 점증. | Tier B |
| ORCL | Oracle | DB + OpenAI 제휴 | 2, 3 | Stargate 데이터센터. AI Cloud 신생. | 변동성 큼 |
| AAPL | Apple | Apple Intelligence + ChatGPT 통합 | 3 | 자체 모델 약함, 후행 위험 | 우려 |
| CRM | Salesforce | CRM + Agentforce | 3 | P/E 28x 합리적. Agentic 잠식 vs 수혜 binary. | Tier B |
| NOW | ServiceNow | ITSM + Now Assist | 3 | P/E 60x 프리미엄. Agentic 수혜 기대 큼. | 가격 부담 |
| ADBE | Adobe | Firefly + Photoshop AI | 5 | P/E 22x 매력. Sora·이미지 위협 vs Lock-in | Tier B |
| SAP | SAP | ERP + Joule AI | 3 | 안정. Agentic 통합 진행. | 안정 |
| WDAY | Workday | HCM AI | 3 | 안정 SaaS. | 안정 |
| PLTR | Palantir | Vertical AI (별도 영역) | — | 다음 deep-dive 대상 | 본 영역 제외 |
| 9984.T | SoftBank | OpenAI 11% 간접 | 2 | OpenAI 노출 유일 상장 channel | 일본 종목 |

### 8.2 한국 종목 (transmission 약함)

| 티커 | 기업명 | 밸류체인 위치 | Sub-area | 비고 |
|------|-------|------------|---------|------|
| 035420 | 네이버 | 자체 AI (HyperCLOVA) | 6 | 한국 시장 한정. 글로벌 경쟁 약함. |
| 035720 | 카카오 | 자체 AI | 6 | 마찬가지 |
| 030520 | 한컴 | Office AI | 6 | 한국 시장 한정 |

→ **한국 종목 본 영역에서 매수 매력 약함**. 본 영역은 미국 빅테크 중심.

### 8.3 매수 우선순위 (참고)

**Tier A (우선 검토)**:
1. **Meta (META)** — 빅테크 중 valuation 매력 최상. 자체 모델 + 광고 시너지.
2. **Alphabet (GOOGL)** — 비슷한 valuation 매력. Gemini 자체 + AWS 비의존.
3. **Microsoft (MSFT)** — 가장 안전, Copilot monetization 가시. 가격 부담 인정 후 분할 매수.

**Tier B (보조)**:
4. **Amazon (AMZN)** — AWS Bedrock + Anthropic
5. **Salesforce (CRM)** — Agentic 수혜 binary, P/E 합리적
6. **Adobe (ADBE)** — 가격 매력, Sora 위협 모니터링

**Tier C (간접·위성)**:
7. SoftBank (9984.T) — OpenAI 노출 유일 상장 channel
8. ServiceNow (NOW) — Agentic 수혜 expected, 단 P/E 60x 프리미엄

---

## 9. 모니터링 트리거

- [ ] **빅테크 4사 분기 실적·CapEx 가이던스** → P1 (4분기 합산 모두)
- [ ] **Microsoft 365 Copilot paid seat 분기 데이터** → P2
- [ ] **OpenAI·Anthropic 분기 매출 leak** → P3
- [ ] **OpenAI·Anthropic IPO 발표** → P1
- [ ] **Foundation model 가격 폭락** (token 30%+ 하락) → P1
- [ ] **Agentic AI ROI case** (대기업 reference) → P2
- [ ] **AI 규제 변화** (EU AI Act 시행, 미국 행정명령) → P2
- [ ] **Microsoft-OpenAI 제휴 재협상** → P1
- [ ] **Salesforce·ServiceNow·SAP Agentic 매출 segment** → P2~P3
- [ ] **중국 cheap model 미국 시장 진입** → P2
- [ ] **OpenAI cash burn 가이던스 변화** → P1

---

## 10. 리스크

- **빅테크 CapEx ROI 입증 실패** (가장 큰 리스크) — $650B CapEx 매출 회수 의문
- **Foundation model commoditization** — DeepSeek·오픈소스 → 가격 폭락
- **OpenAI cash burn 위기** — Microsoft 위험 노출 확대
- **AI 규제** — EU AI Act, 미국 행정명령, 반독점
- **Agentic AI ROI 입증 실패** — SaaS 재편 자체가 늦어짐
- **AI 거품 시나리오** — "Software Apocalypse" 재발, 멀티플 압축
- **개인정보·저작권 소송** — 패소 시 학습 데이터·매출 영향
- **인재·GPU 비용** — 마진 압박 지속

---

## 11. 매크로 변수 민감도

| 매크로 변수 | 영역 영향 | 메모 |
|-----------|---------|------|
| Fed 금리 인하 | ++ (성장주 멀티플 ↑) | 본 영역 매우 민감 |
| 달러 강세 | − (해외 매출 비중 큰 빅테크) | |
| 미중 갈등 심화 | + (중국 model 미국 진입 견제) | 단, 빅테크 중국 매출 손실 |
| 빅테크 CapEx 둔화 | −− (직접 영향) | 본 영역 핵심 변수 |
| AI 규제 강화 | − (단기 컴플라이언스), + (장기 진입장벽) | |
| 반독점 강화 | −− (빅테크·foundation 제휴 견제) | |
| 글로벌 경기 침체 | −− (enterprise IT 예산 감축) | |

---

## 12. 본인 의사결정 메모

> 시스템은 매수 결정 안 함. 본인 참고용.

- 현재 보유 종목: (본인 입력)
- 추가 매수 검토 종목: Meta, Alphabet, Microsoft (분할)
- 청산 검토 종목: (Apple — AI 후행 위험 시)
- 다음 의사결정 시점:
  - 빅테크 Q2 실적 (7월 말~8월 초)
  - Salesforce·ServiceNow Q2 Agentic AI 매출 데이터
  - OpenAI·Anthropic 매출 leak·IPO 신호

### 본인이 인지해야 할 핵심 trade-off
- **Microsoft = 가장 안전하나 가격 부담**. CapEx $190B vs Copilot $5.4B ARR = ROI 의문이 valuation cap.
- **Meta·Google = valuation 매력**. 자체 모델 + 광고 시너지 + 빅테크 중 저평가. 단, AI 후행 우려 인식.
- **Foundation models = 직접 매수 불가**. OpenAI·Anthropic IPO 까지 빅테크 통한 간접 노출만.
- **Horizontal SaaS = binary**. Salesforce·ServiceNow 가 Agentic 수혜 vs 잠식 결정될 시점. 2026 Q3~Q4 분기 실적이 결정.
- **한국 transmission 약함** — 본 영역은 미국 중심, 한국 종목 우선순위 낮음.
- **AI Compute (NVDA·HBM) 영역과 중복 인지** — Tier 3 Thin tracking에서 가격 완전 반영. 본 영역과 동시 노출은 빅테크 CapEx 단일 변수 이중 베팅.

---

## 13. 업데이트 로그

| 날짜 | 변경 사항 | 점수 변화 |
|------|---------|---------|
| 2026-05-23 | 최초 작성 (v2.1 룰 적용) | TAM 5, Moat 4, Capital 5 → 합산 14/15. Conf. High. 시차 A5 B4 C5 = +4 (Good entry). Tier 1 확정. |

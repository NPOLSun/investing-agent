# 전력반도체 (GaN·SiC) — Tier 2 Deep Dive (Tier 1 깊이)

> **Trigger**: NVIDIA 800V DC 아키텍처를 차세대 AI Factory 표준으로 채택 (2026-03 GTC). **TI, STMicro, Navitas, Power Integrations 모두 800V-6V/12V GaN PDB 동시 발표** = 본 영역의 *진정한 변곡점*. EV 사이클 둔화 (2024~2025) 압축된 valuation + AI DC 새 driver. Wolfspeed Chapter 11 후 재무 정상화. 본인 재료·반도체 background 친숙도 최고.
> **Linked methodology**: methodology_v2.1.md

---

## 0. 메타 정보

| 항목 | 값 |
|------|----|
| 작성일 | 2026-05-24 |
| 최근 갱신 | 2026-05-24 |
| 다음 정기 갱신 | 2026-07-01 |
| 시계 분류 | Core (2~3년) |
| Tier | 2 (Tier 1 깊이) |
| Confidence | Medium-High |
| 트랙 | L1A + KR 부분 |

---

## 1. 한 줄 요약 + 핵심 가설

### 한 줄 요약

> EV 사이클 둔화 (2024~2025) → SiC 종목 valuation 압축. **NVIDIA 800V DC AI Factory 표준 채택 (2026-03 GTC) + 모든 주요 power semi 업체 800V-6V/12V GaN PDB 동시 발표** 이 *진정한 변곡점*. 알파 3개 층 — *Upstream (Wolfspeed turnaround)*, *Integrated EU 저평가 (STM·IFX)*, *AI DC GaN pure-play (Navitas·POWI·Vicor)*. **TI 도 NVIDIA 800VDC reference 공동 발표 — 새 진입자**. EV 압축 + AI DC 가속 = *진입 timing 매력 최대*.

### 핵심 가설

**가설 A — AI DC 가 EV 사이클 둔화를 대체할 새 driver**
- EV 사이클 둔화 (2024~2025) → SiC 종목 valuation 압축 (Wolfspeed Chapter 11, STM·IFX P/E 12~18x).
- AI DC 매출 가속: Wolfspeed AI DC +30% qoq, POWI 산업 +23% yoy, Navitas Q1 2026 +18% qoq (high-power 대다수).
- **800V DC 표준화**: NVIDIA Rubin AI Factory 표준. 기존 12V/48V → 800V (변환 stage 수 ↓, 효율 ↑, 밀도 ↑).
- 빅테크 1MW rack 본격 준비 (Microsoft·Google·Meta).

**가설 B — 모든 주요 power semi 업체가 800V-6V/12V GaN PDB 동시 발표 = 표준 확정**
- **TI**: 800V-6V DC/DC (integrated GaN, 97.6% efficiency, >2000W/in³), 30kW 800V AC/DC PSU (GTC 2026-03)
- **STMicro**: 6kW/12kW/20kW 800V GaN PDB (NVIDIA 공동 발표). 700V/120V GaN + STM32G4 MCU
- **Navitas**: 800V-6V PDB (20kW, 97.5% eff, 1MHz), 250kW SST EPFL 협력
- **Power Integrations**: 1250V/1700V PowiGaN — 800V→12V *단일 half-bridge* 변환 (>98% 효율)
- **Infineon**: GaN Systems 통합, 800V AI DC 타겟, AI DC FY2026 매출 €1.5B 가이던스
- 6개 업체 동시 진입 = **800V DC = AI 시대 표준** 확정

**가설 C — Wolfspeed turnaround 진행, GM 회복 1~2년**
- Chapter 11 완료, Renesas 자본·이사회 합류
- Q3 FY26 매출 $150M (Power $100M + Materials $50M), AI DC +30% qoq
- 10kV SiC MOSFET 양산 (그리드·산업·AI DC SST)
- 부채 1st lien -43%, 총 -$97M, 이자 -$62M, 유동성 $1.2B
- **GM 여전히 negative (Q4 가이던스 유지)** — 수익성 회복 1~2년 더
- 300mm SiC wafer 진행 중

**가설 D — EU Integrated (STM·IFX) 가 valuation 매력 최대**
- STM: SiC 1위 device (자동차 메인 인버터). Catania fab €3B+. P/E 12~15x 압축.
- IFX: SiC + GaN (GaN Systems 인수 통합). Marvell 자동차 Ethernet $2.5B 인수. AI DC €1.5B 가이던스. P/E 15~18x.
- **EV 회복 + AI DC re-rating** 시너지 가능.

**가설 E — AI DC GaN pure-play 3개 종목 다중 진입 가능**
- **Navitas (NVTS)**: NVIDIA 800V PDB 데모, EPFL 250kW SST, GeneSiC 1200V MOSFET. 시총 ~$1~2B, 변동성 매우 큼.
- **Power Integrations (POWI)**: 1250V/1700V PowiGaN — *유일한 직접 800V→12V*. 안정 dividend. 시총 ~$3~4B.
- **Vicor (VICR)** ← **hidden alpha (next wave 섹션 deep)**: FPA + Vertical Power Delivery. Q1 2026 backlog $300.6M (+70% QoQ).

**가설 F — 한국 transmission 부분 강, 그러나 글로벌 alpha 작음**
- DB하이텍 (000990) — foundry, GaN·SiC 일부 (비중 작음)
- 예스파워테크닉스 (비상장) — SiC 신생, IPO 모니터링
- KEC (092220) — 소형
- → **글로벌 종목 중심**, 한국은 위성

### 기각 조건

- EV 회복 지연 + AI DC 매출 둔화 동시
- 중국 SiC·GaN 가속 (BYD Semi, San'an) 으로 글로벌 가격 폭락 -20~30%/년
- Wolfspeed 재정 재발 (GM negative 지속)
- NVIDIA 800V DC 일정 1년+ 지연
- 빅테크 자체 PSU 개발 (가능성 매우 낮음)

---

## 2. 4가지 잣대 채점

### 잣대 1: TAM

**점수: 3 / 5** (Major expansion, ×3~5)

- GaN/SiC 합산: 2025 ~$5B → 2030 ~$15~20B (CAGR 25%)
- SiC ~80%, GaN ~20% (SiC 대형, GaN 빠른 성장)
- 800V DC 표준화 시 *시장 확장 가속*
- AI DC 인프라 전체 합산 5년 후 $200B+
- 합산 5년 후 $15~20B 수준

**Confidence**: Medium-High

### 잣대 2: Moat (해자 재편 + 비가역성)

**점수: 3 / 5** (Moderate reshuffle)

- 기존 강자 다수: STM·IFX·Wolfspeed·Rohm·Onsemi
- 중국 가속 (BYD Semi·San'an) 가격 압박 진행
- Wolfspeed Chapter 11 + Renesas 자본 = 시장 일시 재편
- AI DC pure-play (Navitas·POWI·Vicor) 신규 카테고리
- 재료·SiC substrate 만 강한 moat
- 비가역성 중간: EV·AI DC 인증 시간 lock-in 어느 정도

**Confidence**: Medium

### 잣대 3: Capital

**점수: 3 / 5** (Major capital 10~100B$/년)

- Wolfspeed CapEx 누적 $5B+ (CHIPS Act 일부)
- Infineon Kulim €8B+, STMicro Catania €3B
- Onsemi East Fishkill (전 GlobalFoundries fab 인수)
- 합산 산업 CapEx ~$15~20B/년
- M&A: Infineon-Marvell 자동차 Ethernet $2.5B (2025)
- VC: GaN·SiC ~$1B/년

**Confidence**: Medium

### ~~잣대 4: Tech~~ (폐기)

### 합산

| 트랙 | 점수 | 임계 |
|------|------|------|
| L1A | **9 / 15** | Tier 2 ≥ 9 ✅ |

→ **Tier 2 확정**, Tier 1 깊이로 분석

---

## 3. A·B·C 시차 평가

### A 지표 (자본 유입) — **4 / 5**

- NVIDIA 800V DC 표준 채택 (2026-03 GTC) — 빅테크 CapEx 가속 시그널
- Renesas-Wolfspeed 자본 진입
- Infineon-Marvell 자동차 Ethernet $2.5B (2025)
- TI·STM·Navitas·POWI·IFX 동시 800V GaN PDB 진입
- Vicor Q1 2026 backlog +70% QoQ ($300.6M)

### B 지표 (실물 변화) — **5 / 5**

- **NVIDIA 800V DC 채택 (2026-03 GTC)** — 결정적 변화
- TI·STM·Navitas·POWI 모두 800V-6V/12V PDB 동시 데모 (GTC 2026)
- Wolfspeed AI DC +30% qoq
- Navitas Q1 2026 +18% qoq, high-power 대다수
- POWI 산업 매출 +23% yoy
- 250kW SST 데모 (Navitas-EPFL)
- 10kV SiC MOSFET 양산 (Wolfspeed)
- Vicor backlog +70% QoQ

### C 지표 (가격 반영) — **2 / 5**

- EV 둔화로 valuation 크게 압축 (저평가)
- Wolfspeed 시총 $0.5~2B (Chapter 11 후 변동)
- STM·IFX P/E 12~18x 압축
- Onsemi P/E 압축
- Navitas·POWI 일부 반영, Vicor 부분 반영
- AI DC re-rating 아직 초기

### 시차 매력도 = A + B − C = **4 + 5 − 2 = +7 (Maximum entry)**

→ **시차 매력 최고 수준**. 가격 충분히 압축, 실물 변화 명확, 자본 가속. **본인 진입 적기**.

---

## 4. 산업 메가트렌드 (Step 1)

### 4.1 수요 측

**단기 (12~18개월)**
- EV 사이클 회복 진행: 2026 후반~2027 본격. BYD·Tesla·현대 신규 모델 SiC 채택 증가.
- AI DC 800V DC 전환: NVIDIA Rubin·Rubin Ultra 표준. PSU·전압 변환 SiC + GaN 직접 수혜.
- 그리드 modernization: 10kV SiC MOSFET 양산. 미국·EU·인도 그리드 업그레이드.
- Fast-charging GaN 보편화 (Navitas·POWI·Innoscience).

**중기 (2~4년)**
- 800V DC 표준화 완료: 모든 신규 데이터센터 기본. 기존 12V/48V → 800V 전환 가속.
- SST 본격화: MV→800V 변환. 3300V·2300V·1200V SiC 다중 등급.
- 300mm SiC wafer 양산: Wolfspeed lead. 단위 면적당 칩 수 ×1.7. 가격 폭락 시작.
- 데이터센터당 SiC·GaN 가치: 1MW 클러스터당 $50~100k 추정.

**장기 (5~10년)**
- 자율주행 전동화 + Robotaxi
- 우주·항공 SiC 채택 (Power-Density 우위)
- 양자 컴퓨터 cryogenic 전력 (매우 장기)

### 4.2 공급 측

**현재 병목 — SiC substrate 8-inch capa**
- Wolfspeed 8-inch 본격, 300mm 진행
- Coherent (전 II-VI) 일부, Resonac (4004.T) 일본
- 중국 (TankeBlue·SICC·Shanxi Shuoke) 가격 압박
- Wolfspeed Chapter 11 시기 capa 일시 위축, Renesas 후 정상화

**다음 병목 — 고전압 SiC (3300V·6500V·10kV) 양산**
- Wolfspeed 10kV MOSFET 양산 (Q3 FY26 시작)
- Navitas GeneSiC 3300V·2300V·1200V
- STM·IFX 고전압 SiC 진입 가속
- 2027~2028 본격 병목

**추가 병목 — GaN-on-Si + GaN IC 패키징**
- Navitas GaNFast (모바일 검증) → AI DC 진입
- Infineon GaN Systems 통합
- Power Integrations PowiGaN 자체
- EPC·Innoscience 가격 압박

### 4.3 정책·지정학 변수

- **CHIPS Act**: Wolfspeed·Onsemi·일부 fab 수혜
- **중국 자체 가속**: BYD Semi·San'an. 자동차 OEM 수직통합
- **EU 자체 capa**: Catania (STM+Mubadala), Kulim (IFX). EU Chips Act
- **한국 정책 미흡** — 글로벌 규모 대비 작음
- **일본**: Renesas-Wolfspeed 합의 — 정부 간접 backing

---

## 5. 밸류체인 매핑 (Step 2)

### 5.1 다이어그램

```
[L1 Substrate]
  ├ SiC: Wolfspeed (WOLF, 1위), Coherent (COHR 일부), Resonac (4004.T), SICC (중국)
  ├ GaN-on-Si: TSMC, UMC, STM 자체
  └ GaN-on-SiC: NXP·Macom 일부
       ↓
[L2 Epitaxy 장비]
  ├ Aixtron (AIXA.DE) — MOCVD 1위
  └ Veeco (VECO)
       ↓
[L3 Device 제조]
  ├ SiC MOSFET: STM (1위), Infineon, Wolfspeed, Rohm, Onsemi, Navitas GeneSiC, BYD Semi, San'an
  └ GaN HEMT/IC: Innoscience (CN), Infineon (GaN Systems), POWI (PowiGaN), Navitas (GaNFast), Renesas, EPC, TI
       ↓
[L4 Module/패키지]
  ├ Infineon TOLT (EV·산업)
  ├ Wolfspeed TOLT (자체)
  └ Navitas SiCPAK (산업)
       ↓
[L5 Application]
  ├ EV (메인 인버터·OBC·DC/DC)
  ├ AI DC (Server PSU·전압 변환·800V-6V·SST)
  ├ Grid (10kV SiC, 송배전, HVDC)
  ├ ESS·재생에너지
  ├ Industrial drive·motor
  └ Fast charging
       ↓
[L6 Customer]
  ├ EV: Tesla, BYD, Hyundai, VW, GM, Ford
  ├ AI DC: AWS, MS, Google, Meta, Oracle (via NVDA·서버 PSU OEM)
  ├ Grid: 전력 회사
  └ Server: Supermicro, Dell, HPE
```

### 5.2 레이어별 분석

| 레이어 | GM | 경쟁구도 | 중국 침투 | 진입장벽 | 본인 매력도 |
|--------|-----|---------|---------|---------|----------|
| L1 SiC Substrate | 매우 높음 (40%+) | Wolfspeed·Coherent·Resonac 과점 | 진행 중 | 매우 높음 | **★★★ (WOLF turnaround)** |
| L1 GaN-on-Si | 높음 (30~40%) | TSMC·STM 다중 | Innoscience 가속 | 기술 + 자본 | 중간 |
| L3 SiC MOSFET | 중상 (25~40%) | STM·IFX·WOLF·Rohm·ON·BYD·San'an | 큼 (가격 압박) | 인증·고객 lock-in | **★★ 매우 높음** |
| L3 GaN HEMT/IC | 중상 (25~35%) | IFX·NVTS·POWI·Innoscience·EPC·TI | 큼 | 기술 | **★★ AI DC 핵심** |
| L4 Module | 낮음~중간 (15~25%) | 다수 | 일부 | 패키징 | 중간 |

### 5.3 하위 세분화 (Sub-areas)

#### Sub-area 1: SiC Substrate (Wolfspeed turnaround) ★★★
- **Wolfspeed (WOLF)**: 글로벌 1위 (~40%), 8-inch + 300mm, Chapter 11 후 Renesas. AI DC +30% qoq, 10kV 양산.
  - **위성 자산 (3~5%)**, 분할 매수 6개월. 시장 조정 시 추가.
- Coherent (COHR) — 광인터커넥트 영역 중복
- Resonac (4004.T) — 일본 작음

#### Sub-area 2: Integrated SiC + GaN (EU 저평가) ★★
- **STM**: SiC 1위 device, Catania fab, P/E 12~15x **저평가**. EV + AI DC 다중.
- **IFX**: SiC + GaN (GaN Systems). Marvell 자동차 Ethernet $2.5B 인수. AI DC €1.5B 가이던스. P/E 15~18x.
- **Onsemi (ON)**: SiC 4위, EV 비중 매우 큼. *EV 둔화 직격탄 → 회복 시 re-rating*. P/E 압축.

#### Sub-area 3: AI DC GaN Pure-Play ★★
- **Navitas (NVTS)**: NVIDIA 800V PDB·EPFL 250kW SST. Q1 2026 +18% qoq. 시총 $1~2B, 변동성 매우 큼.
- **Power Integrations (POWI)**: *유일한 직접 800V→12V (1250V PowiGaN)*. 안정 dividend. 시총 $3~4B.

#### Sub-area 4: 일본
- Rohm (6963.T) — SiC, 환율 부담
- Renesas (6723.T) — Transphorm 인수, Wolfspeed 자본

#### Sub-area 5: 장비 — 간접
- Aixtron (AIXA.DE), Veeco (VECO)

#### Sub-area 6: 한국 — 위성
- DB하이텍 (000990) — foundry, GaN·SiC 일부
- 예스파워테크닉스 (비상장) — SiC 신생, IPO 모니터링
- KEC (092220) — 소형

---

## 6. 병목 식별 (Step 3)

### 6.1 현재 병목

| 병목 | 영향 | 수혜자 |
|------|-----|------|
| 8-inch SiC substrate capa | 가격 prem, lead time 길어짐 | Wolfspeed, Coherent |
| Wolfspeed 재무 정상화 | Q4 GM negative → 2026~2027 break-even | Wolfspeed |
| EV 수요 둔화 vs SiC 재고 | 자동차 OEM 주문 조정 | STM·IFX·Onsemi (EV 비중 큼) |
| 중국 SiC·GaN 가격 압박 | 글로벌 -10~20%/년 | 중국 BYD·San'an, 미국·EU 손해 |

### 6.2 다음 병목 ★ 투자 핵심

| 병목 | 등장 시점 | 수혜자 |
|------|---------|------|
| 300mm SiC wafer 양산 | 2027~ | Wolfspeed |
| AI DC 800V DC 표준화 GaN PSU | 2026~2027 | Navitas, POWI, IFX, TI, STM, **Vicor** |
| 10kV SiC MOSFET 그리드 본격 | 2026~2028 | Wolfspeed, Navitas (3300V) |
| SST 양산 | 2027~ | Navitas, Wolfspeed, IFX |
| GaN IC 통합 (driver·PMIC) | 2026~2027 | Navitas, POWI |

### 6.3 컨센서스 vs 본인 뷰

**컨센서스**: "EV 사이클 둔화 = SiC 회피". Wolfspeed = 위험. AI DC = NVDA·서버 종목만 본다.

**본인 뷰**:
- EV 둔화 충격 *대부분 가격 반영* — STM·IFX·ON 저평가 = 진입 기회
- AI DC 새 driver 확인 (NVIDIA 800V DC + Navitas·POWI·Vicor 실적)
- Wolfspeed turnaround 진행 — 위성 분할 매수 가능
- AI DC 진짜 GaN alpha 는 Navitas·POWI·Vicor — 빅테크 직접 노출

### 6.4 Next Wave Deep Analysis ★★★ 본인 진짜 알파

> **본인 메모**: "next-bottleneck identification". 광인터커넥트 광원 처럼, 전력반도체도 *진짜 next wave* 가 핵심. 3개 선정 — Vertical Power Delivery, SST, 10kV+ SiC Grid.

---

#### Next Wave 1: Vertical Power Delivery (VPD) + 800V Server PSU ★★★ 2026~ 진행 중

**왜 next wave 인가**
- AI rack 100kW → 200kW+ 로 폭증. 12V/48V → 800V DC 전환 필수.
- 기존 *수평 power delivery (rack 옆 PSU → motherboard → CPU)* 의 *I²R 손실* 이 KW 단위 낭비.
- **Vertical Power Delivery (VPD)**: GPU/CPU *직접 아래* 에 power 배치 → 전류 경로 최단화, 손실 90% 절감.
- Vicor 가 **FPA (Factorized Power Architecture)** + **VPD** 로 사실상 선점.
- TI·STM·Navitas·POWI·IFX 가 다 800V-6V/12V GaN PDB 발표 = *2026~2027 본격 양산*.

**병목 메커니즘**
- GaN HEMT 고전압 (1250V·1700V) 양산 — Power Integrations 만 1250V/1700V 양산 중
- 800V 회로 정밀 제어 — STM32G4 MCU 200ps 해상도 (STMicro)
- Multiphase buck converter (6V → <1V) 정밀 제어 — TI multiphase 솔루션
- *수동 부품 (MLCC)* — Murata·Samsung Electro-Mechanics·TDK 다중 노출 (AI 서버 *10~15× MLCC*)

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Vicor (VICR)** ★ | US | FPA + Vertical Power Delivery 사실상 선점. **Q1 2026 backlog $300.6M (+70% QoQ)**, 매출 가이던스 ~$570M | **A 1순위 next wave** |
| **Power Integrations (POWI)** | US | **1250V/1700V PowiGaN 유일 직접 800V→12V 변환** | 이미 본문 매수 (5순위 → 상위 조정) |
| **TI (Texas Instruments, TXN)** | US | NVIDIA GTC 2026 800VDC 전체 아키텍처 공동 발표. 800V-6V GaN integrated, 6V→<1V multiphase, 30kW 800V AC/DC PSU | **A 2순위 (다중 노출, 안정)** |
| **Monolithic Power (MPS)** | US | VRM (Voltage Regulator Module) 1위. 시총 $30~40B. AI 서버 multiphase buck 핵심 | **A 3순위 (밸류 매력)** |
| **STMicro (STM)** | EU | NVIDIA 800V GaN PDB 공동 발표 (6kW·12kW·20kW). 700V/120V GaN + STM32G4 MCU | 이미 본문 매수 |
| **Infineon (IFX)** | EU | AI DC FY2026 €1.5B 가이던스, GaN Systems 통합 | 이미 본문 매수 |
| **Navitas (NVTS)** | US | 800V-6V PDB 데모 | 이미 본문 매수 |
| Murata (6981.T) | JP | 고스펙 AI 서버 MLCC 1위, lead time 24주 | B (위성, 일본) |
| Samsung Electro-Mechanics (009150) | KR | AI 서버 MLCC 2위 | **A KR (위성)** |

**한국 — MLCC 노출**
- **삼성전기 (009150)** — AI 서버 MLCC 2위, 시총 ~10조원. **본 영역의 한국 직접 노출** ★
- **TDK 일부**, **TKC (KR 작음)**

**Timing & Catalyst**
- 2026 후반: NVIDIA Rubin 본격 ramp + 800V DC 양산 진입
- 2027: 1MW rack 본격 채택 (Microsoft·Google·Meta)
- 2027~2028: VPD 가 표준화

**모니터링**
- Vicor 분기 backlog·매출·VPD 채택 사례 → P1
- POWI 분기 PowiGaN 매출 → P1
- TI·MPS 분기 (AI server VRM segment) → P1
- 삼성전기 분기 MLCC·AI 서버 매출 → P1
- NVIDIA Rubin launch + 800V DC 표준 적용 시그널 → P1

**리스크**
- Si 기반 솔루션 (TI multiphase + 일반 MOSFET) 가속 — GaN 대비 비용 우위 시 GaN 잠식 가능
- NVIDIA 800V DC 표준 일정 1년+ 지연

**숨겨진 매력 — Vicor (VICR)**
- *AI DC VPD 의 사실상 선점*. Vertical Power Delivery 가 GPU 직접 아래 = NVIDIA·AMD·custom XPU 모두 채택
- Q1 2026 backlog $300.6M (+70% QoQ) — 매출 visibility 폭증
- 시총 ~$2~3B (Vertiv·Eaton·Modine 대비 작음)
- **본 deep dive 의 hidden alpha 1위**

---

#### Next Wave 2: Solid-State Transformer (SST) — MV→800V 변환 ★★ 2027~

**왜 next wave 인가**
- 1MW+ AI rack → 데이터센터 전체 *수십~수백 MW*. MV (중전압 10~33kV) → 800V DC 변환 필수.
- 기존 *철심 변압기* 너무 무겁고 효율 낮음 + 빠른 응답 어려움.
- **SST (Solid-State Transformer)** = SiC + GaN 으로 *고주파 변환* → 부피 1/10, 효율 +5%.
- Navitas-EPFL **250kW SST 데모** (APEC 2026) — 첫 양산급 시연.
- 2027~2028 본격 채택. 빅테크 hyperscaler 데이터센터 *전압 변환 layer 자체 재편*.

**병목 메커니즘**
- 고전압 SiC MOSFET (3300V·6500V·10kV) 양산 capa
- 변환 회로 정밀 제어 — multi-level converter 토폴로지
- 신뢰성·안전 인증 (Grid-tied 5~10년+)
- 정부 인허가 (전력 회사 표준)

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Navitas (NVTS)** | US | 250kW SST EPFL 협력, GeneSiC 3300V·1200V | 이미 본문 매수 |
| **Wolfspeed (WOLF)** | US | 10kV SiC MOSFET 양산 (그리드·SST 핵심) | 이미 본문 매수 |
| **Infineon (IFX)** | EU | 고전압 SiC + 그리드 솔루션 | 이미 본문 매수 |
| **GE Vernova (GEV)** | US | Grid solution + SST 가능성. AI DC 전력 영역 중복 (별도 deep dive 있음) | AI DC 전력 영역 중복 |
| **Hitachi Energy (6501.T 일부)** | JP | 그리드·SST, 일본 종합 | C (위성) |
| **ABB (ABBN.SW)** | EU | Grid + 800V DC, NVIDIA 협력 | B (EU 안정) |
| **Schneider Electric (SU.PA)** | EU | Power 통합 (냉각 영역 중복) | 냉각·전력 영역 중복 |
| **Hyundai Heavy Industries (267250)** | KR | 그리드·전력 변환 일부 | C (위성) |

**한국**
- **현대일렉트릭 (267260)** — 변압기·그리드, 미국 grid modernization 직접 수혜
- **효성중공업 (298040)** — 변압기·SST 일부 진입 시도. 미국 매출 가속
- **LS ELECTRIC (010120)** — 산업 전력
- → **K-그리드 (효성중·현대일렉) 가 K-방산 다음 핵심 K-수출**

**Timing & Catalyst**
- 2026~2027: SST 데모 가속 + 첫 데이터센터 채택
- 2027~2028: 본격 양산
- AI DC GW+ 캠퍼스 본격 가동 시 SST 표준화

**모니터링**
- Navitas-EPFL SST 진척 → P1
- Wolfspeed 10kV MOSFET 그리드 첫 채택 → P1
- 효성중공업·현대일렉트릭 분기 (미국 매출) → P1
- ABB-NVIDIA 800V DC 데이터센터 채택 사례 → P2

**리스크**
- 기존 철심 변압기 + 별도 DC 변환 솔루션 가성비 우위 지속 시 SST 지연
- 그리드 안전 인증 3~5년+ 소요

---

#### Next Wave 3: 10kV+ SiC for Grid Modernization ★★ 2026~2028

**왜 next wave 인가**
- 미국 그리드 노후화 + AI DC 폭증 + 재생에너지 전환 → *그리드 modernization $1T+ 시장*.
- 10kV SiC MOSFET = 기존 thyristor·IGBT 대비 효율 +5%, 부피 1/3
- Wolfspeed 10kV SiC MOSFET **양산 진입 (Q3 FY26)** — 첫 commercial
- HVDC (High-Voltage DC) 송전 + 마이크로그리드 + 재생에너지 인버터 다중 수요

**병목 메커니즘**
- 10kV+ SiC capa 매우 제한적 (Wolfspeed·Navitas·STM·IFX 만)
- 패키지 (SiCPAK press-fit) 정밀도
- 신뢰성 인증 (그리드 25년+ lifecycle)

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Wolfspeed (WOLF)** | US | 10kV SiC MOSFET 양산 첫 commercial | 이미 본문 매수 |
| **Navitas (NVTS)** | US | GeneSiC 3300V·6500V·15kV (DoE 자금) | 이미 본문 매수 |
| **GE Vernova (GEV)** | US | Grid + HVDC 통합 | AI DC 전력 영역 중복 |
| **Hitachi (6501.T)** | JP | HVDC·그리드 종합 | C (위성) |
| **Eaton (ETN)** | US | 전력 + 그리드, Boyd 통합 | 냉각·전력 영역 중복 |
| **Mitsubishi Electric (6503.T)** | JP | HVDC·전력 솔루션 | C (일본 환율) |

**한국**
- **현대일렉트릭 (267260)** — 미국 변압기·그리드 수출 가속. 시총 ~3~5조원
- **효성중공업 (298040)** — 미국 매출 폭증. 시총 ~3~4조원
- → AI DC 전력 영역 deep dive 와 중복. 종목 매수는 *AI DC 전력 영역에서 일괄 관리*

**Timing & Catalyst**
- 2026~2027: 10kV SiC 첫 그리드 채택
- 2027~2028: HVDC 본격 양산
- 미국·EU·인도 그리드 modernization 예산 가속

**모니터링**
- Wolfspeed 10kV SiC 매출 (Q-by-Q) → P1
- 미국 그리드 modernization 정책·자금 → P1
- 효성중공업·현대일렉트릭 미국 매출 → P1

**리스크**
- 그리드 채택 사이클 매우 길음 (5~10년)
- 기존 IGBT 가성비 우위 지속 가능성

---

### 6.5 Next Wave 종합 — 본인 진입 전략

**우선순위 (Timing + 상장 alpha)**

| 순위 | Next Wave | Timing | 핵심 종목 | 비중 |
|-----|---------|--------|---------|-----|
| 1 | **VPD + 800V Server PSU** | 2026~ 진행 중 | **Vicor (VICR)**, MPS, TI, 삼성전기 (KR) | 3~4% (신규 진입) |
| 2 | **SST (MV→800V)** | 2027~ | Navitas·Wolfspeed·IFX (본문 중복) + 효성중공업·현대일렉 (KR) | 2~3% (KR 신규) |
| 3 | **10kV+ SiC Grid** | 2026~2028 | Wolfspeed (본문 중복) + 효성중공업·현대일렉 (KR) | AI DC 전력 영역에서 카운트 |

**전력반도체 영역 종합 매수 우선순위 업데이트**

1. **STM** — Integrated 저평가, 즉시 분할
2. **Infineon (IFX)** — 다중 노출, 즉시 분할
3. **Vicor (VICR)** ← **Next wave 신규 1순위** (VPD 사실상 선점, backlog +70% QoQ)
4. **Power Integrations (POWI)** — 1250V PowiGaN, 안정 진입
5. **Monolithic Power (MPS)** ← **Next wave 신규** (VRM 1위, AI 서버 multiphase)
6. **TI (TXN)** ← **Next wave 신규** (NVIDIA 800VDC reference 공동, 안정 대형)
7. **Wolfspeed (WOLF)** — 위성 turnaround
8. **Navitas (NVTS)** — AI DC GaN 직접, 변동성
9. **삼성전기 (009150)** ← **Next wave 신규 KR** (AI 서버 MLCC)
10. **효성중공업 (298040)** ← **Next wave 신규 KR** (SST + 미국 그리드 수출)
11. **현대일렉트릭 (267260)** ← **Next wave 신규 KR** (그리드)
12. Onsemi (ON) — EV 회복 wait, B

**모니터링 watchlist (Catalyst wait)**
- 예스파워테크닉스 (비상장 SiC KR) — IPO 시그널
- ABB (ABBN.SW) — Grid + NVIDIA 800V DC
- Hitachi Energy (6501.T 일부)
- LS ELECTRIC (010120) — 산업 전력
- Mitsubishi Electric (6503.T)

---

## 7. 자금 흐름 시그널 (Step 4)

### 7.1 관련 ETF

| 티커 | 시장 | 비중 |
|------|------|----|
| SOXX | US | iShares Semi — 중간 (STM·IFX 미포함) |
| SMH | US | VanEck Semi — 중간 |
| TIGER 차이나전기차SOLACTIVE | KR | 중국 EV (간접) — 약함 |
| KODEX 미국반도체 | KR | SOXX 추종 — 중간 |

→ ETF 노출 약함. **직접 종목 매수** 필수.

### 7.2 추적 지표

**P1 (분기 필수)**
- Wolfspeed 분기 (AI DC 매출·GM·Materials)
- STM·IFX 분기 (SiC segment·EV vs AI DC 비중)
- Navitas·POWI 분기 (high-power markets 비중)
- **Vicor 분기 (backlog·VPD 채택)** ← next wave
- **MPS·TI 분기 (AI server VRM·800V PDB segment)** ← next wave
- **삼성전기 분기 (AI 서버 MLCC)** ← next wave KR
- **효성중공업·현대일렉트릭 분기 (미국 매출)** ← next wave KR
- NVIDIA Rubin 출시 + 800V DC 채택 진척

**P2 (분기 모니터링)**
- 중국 BYD Semi·San'an 가격
- 10kV SiC MOSFET 그리드 채택
- 300mm SiC wafer 진척
- EV 회복 (Tesla·BYD·VW 인버터 주문)
- Renesas-Wolfspeed 통합

**P3 (지속)**
- 예스파워테크닉스 IPO 시그널
- Innoscience 가격·점유
- Onsemi East Fishkill capa
- ABB·Hitachi 그리드 800V DC 채택

### 7.3 Startup Landscape

| 스타트업 | 영역 | 비고 |
|---------|------|----|
| 예스파워테크닉스 | SiC KR | IPO 시그널 모니터링 |
| EPC | GaN US | 소형 + 변동성 |
| Innoscience | GaN CN | 가격 압박 가속 |
| Transphorm | GaN US | Renesas 인수됨 |

---

## 8. 종목 매핑 (Step 5)

### 8.1 글로벌 종목

| 티커 | 기업 | 영역 | 시총 | P/E | Tier |
|------|------|-----|-----|-----|------|
| **STM** | STMicroelectronics | L3+L1 | ~$25B | 12~15x | **A 1순위** |
| **IFX** | Infineon | L3+L1+L4 | ~€45B | 15~18x | **A 2순위** |
| **VICR** | **Vicor** ★ next wave | **VPD pure-play** | **~$2~3B** | **~35x** | **A 3순위 (신규)** |
| **POWI** | Power Integrations | L3 (1250V PowiGaN) | ~$3~4B | 25~35x | **A 4순위** |
| **MPS** | Monolithic Power ★ next wave | **VRM 1위** | **~$30~40B** | **~30x** | **A 5순위 (신규)** |
| **TXN** | Texas Instruments ★ next wave | **800VDC 다중** | **~$170B** | **~25x** | **A 6순위 (안정 신규)** |
| **WOLF** | Wolfspeed | L1+L3 (재료 1위) | ~$1~2B | turnaround | **A 7순위 (위성)** |
| **NVTS** | Navitas | L3 (AI DC GaN/SiC) | ~$1~2B | P/S 5~8x | **A 8순위 (변동)** |
| ON | Onsemi | L3 (SiC EV) | ~$30B | 15~18x | B (EV 회복 wait) |
| 6963.T | Rohm | L3 (SiC JP) | ~¥800B | 18~22x | B |
| 6723.T | Renesas | L3 (GaN, Transphorm) | ~¥2.5T | 18~22x | B |
| 6981.T | Murata ★ next wave | **고스펙 MLCC 1위** | ~¥4T | 25x | B (위성 JP) |
| AIXA.DE | Aixtron | L2 MOCVD | ~€2B | 12~15x | C |
| VECO | Veeco | L2 MOCVD | ~$2B | 25~30x | C |
| ABBN.SW | ABB | Grid + 800V DC | ~CHF 110B | 22x | C (위성 EU) |

### 8.2 한국 종목 (Korea transmission)

| 티커 | 기업 | 영역 | 시총 | Tier |
|------|------|-----|-----|------|
| **009150** | **삼성전기** ★ next wave | AI 서버 MLCC 2위 | ~10조원 | **A 1순위 KR** |
| **298040** | **효성중공업** ★ next wave | SST·미국 그리드 변압기 | ~3~4조원 | **A 2순위 KR** |
| **267260** | **현대일렉트릭** ★ next wave | 미국 변압기·그리드 | ~3~5조원 | **A 3순위 KR** |
| 000990 | DB하이텍 | foundry (GaN/SiC 일부) | ~1.5~2.5조원 | C (위성) |
| 010120 | LS ELECTRIC | 산업 전력 | ~3조원 | C (위성) |
| 092220 | KEC | 전력반도체 KR | ~1,000억원 | C |
| - | 예스파워테크닉스 (비상장) | SiC KR 신생 | n/a | IPO 모니터링 |

### 8.3 각 종목의 Valuation Gate

**STM — 1순위 (Integrated 저평가)**
- SiC 1위 device, Catania €3B+ fab
- P/E 12~15x 상당히 압축
- EV 회복 + AI DC 다중
- **진입 전략**: 분할 매수 3개월, EV 회복 시그널 시 가속

**IFX — 2순위 (다중 노출)**
- SiC + GaN, Marvell 자동차 Ethernet 인수
- AI DC FY2026 €1.5B 가이던스
- **진입 전략**: 분할 매수 3개월

**Vicor (VICR) — 3순위 신규 (Next Wave: VPD)**
- *AI DC VPD 사실상 선점*. FPA + Vertical Power Delivery.
- Q1 2026 backlog $300.6M (+70% QoQ)
- 매출 가이던스 ~$570M
- 시총 ~$2~3B (Vertiv·Eaton·Modine 대비 작음)
- **본 영역 hidden alpha 1위**
- **진입 전략**: 즉시 분할 매수 1~3개월

**Power Integrations (POWI) — 4순위**
- *유일한 직접 800V→12V (1250V PowiGaN)*
- 안정 dividend, 시총 ~$3~4B
- **진입 전략**: 즉시 분할 매수

**Monolithic Power (MPS) — 5순위 신규 (Next Wave: VRM)**
- VRM 1위, AI 서버 multiphase
- 시총 ~$30~40B, P/E ~30x
- **진입 전략**: 분할 매수

**TI (TXN) — 6순위 신규 (Next Wave: 800VDC 다중)**
- NVIDIA GTC 2026 800VDC 전체 아키텍처 공동 발표
- 800V-6V GaN + 6V→<1V multiphase + 30kW 800V AC/DC PSU
- 시총 ~$170B (안정 대형)
- *P/E ~25x — 저평가 측면*
- **진입 전략**: 안정 분할 매수

**Wolfspeed (WOLF) — 7순위 (위성 turnaround)**
- 재료 1위, 300mm 진행, Renesas 자본
- AI DC +30% qoq, 10kV SiC 양산
- GM negative 지속, 변동성 매우 큼
- **진입 전략**: 위성 3~5% 비중, 분할 매수 6개월

**Navitas (NVTS) — 8순위 (변동성)**
- NVIDIA GTC 800V PDB·EPFL 250kW SST
- 시총 $1~2B
- **진입 전략**: 1~3% 비중, 분기 확인 후 증액

**삼성전기 (009150) — 1순위 KR**
- AI 서버 MLCC 2위 (Murata 다음)
- 시총 ~10조원, AI 서버 가격 prem
- **진입 전략**: 분할 매수

**효성중공업 (298040) — 2순위 KR**
- 미국 변압기 수출 폭증 (AI DC 전력 영역 직접 노출)
- SST 진입 시도
- **진입 전략**: 분할 매수, 미국 매출 시그널 시 가속

**현대일렉트릭 (267260) — 3순위 KR**
- 미국 변압기·그리드 수출
- 시총 ~3~5조원
- **진입 전략**: 분할 매수

---

## 9. 모니터링 트리거

**즉시 (분기)**
- Wolfspeed 분기 (AI DC·GM·Materials) → P1
- STM·IFX 분기 (SiC segment·EV vs AI DC) → P1
- Navitas·POWI 분기 (high-power 비중) → P1
- **Vicor 분기 (backlog, VPD 채택)** → P1
- **MPS·TI 분기 (AI VRM·800V PDB)** → P1
- **삼성전기 분기 (AI MLCC)** → P1
- **효성중공업·현대일렉 분기 (미국 매출)** → P1
- Onsemi 분기 (EV 회복) → P1

**정책·M&A**
- NVIDIA Rubin 출시 + 800V DC 채택 → P1
- Wolfspeed-Renesas 통합 → P2
- CHIPS Act 추가 자금 → P2
- 미·중 전력반도체 견제 강화 → P2

**기술**
- AMD·Intel 800V DC 채택 → P1
- 300mm SiC wafer 진척 → P2
- 10kV SiC 그리드 첫 채택 → P2
- SST (Navitas-EPFL) 상용화 → P2
- GaN IC 통합 (driver·PMIC) → P2

**거시**
- EV 사이클 회복 시그널 (Tesla·BYD·VW 주문) → P1
- 중국 SiC·GaN 가격 → P2
- Fed 금리 → P2

---

## 10. 리스크

**기술**
- GaN IC 통합 지연 — Navitas·POWI thesis 약화 가능
- 800V DC 표준 분기 (Open Compute Project vs NVIDIA)
- Si 기반 솔루션 가속 — GaN 잠식 가능
- 빅테크 자체 PSU 개발 — 가능성 매우 낮음

**시장**
- EV 회복 지연 + AI DC 둔화 동시 — worst case
- 중국 SiC·GaN 가속 — 가격 -20~30%/년 가속 시 GM 압박
- Wolfspeed 재정 재발
- NVIDIA 800V DC 1년+ 지연

**지정학**
- 트럼프 EV 보조금 폐지 — EV 수요 직격탄
- 미·중 전력반도체 견제 — 중국 BYD·San'an 가속
- 한국 정책 미흡 지속

**본인 포트폴리오 — AI 인프라 중복**
- 본 영역 + 광인터커넥트 + AI DC 전력 + AI Foundation + 냉각 + 원자력 = 빅테크 CapEx 단일 변수 중첩
- → 합산 25~35% 상한 인지

---

## 11. 매크로 변수 민감도

| 변수 | 영향 | 메커니즘 |
|------|------|--------|
| Fed 금리 인하 | + | 성장주 (NVTS·POWI·VICR·MPS) 멀티플 |
| 트럼프 EV 보조금 폐지 | −− | EV 수요 감소 → SiC 매출 |
| AI DC CapEx 가속 | ++ | Navitas·POWI·Vicor·MPS·TI·Wolfspeed 직접 |
| 그리드 정책 | ++ | 10kV SiC, 효성중공업·현대일렉 수요 |
| 미·중 갈등 | + | 중국 견제, 미국·EU 수혜 |
| 달러 강세 | − | 해외 매출 환산, STM·IFX 유로 hedge |
| 한국 원화 강세 | − | 미국 종목 매수 환차익 |

---

## 12. 본인 의사결정 메모

### 최종 매수 우선순위 (Next Wave 반영)

**Tier A — 즉시 분할 매수**
1. **STM** — Integrated 저평가
2. **Infineon (IFX)** — 다중 노출
3. **Vicor (VICR)** ← **Next wave 1순위 (VPD 사실상 선점)**
4. **Power Integrations (POWI)** — 1250V PowiGaN
5. **MPS** ← **Next wave (VRM 1위)**
6. **TI (TXN)** ← **Next wave (800VDC 다중)**
7. **삼성전기 (009150)** ← **Next wave KR (AI MLCC)**

**Tier A 위성 (변동성)**
8. **Wolfspeed (WOLF)** — turnaround
9. **Navitas (NVTS)** — AI DC GaN
10. **효성중공업 (298040)** ← **Next wave KR (SST·그리드)**
11. **현대일렉트릭 (267260)** ← **Next wave KR (그리드)**

**Tier B**
12. Onsemi (ON) — EV 회복 wait

### 비중 가이드

- 본 영역 전체: **포트폴리오의 5~10%**
- AI 인프라 합산 (광 + 전력반도체 + AI DC 전력 + AI Foundation + 냉각): **25~35% 상한**
- 종목별 (예): STM + IFX 각 2%, Vicor 2~3%, POWI 1~2%, MPS 1~2%, TI 1~2%, 삼성전기 1~2%, WOLF 1~2%, NVTS 1%, 효성중·현대일렉 1% 각

### 진입 timing

- 즉시: STM, IFX, Vicor, POWI, MPS, TI, 삼성전기
- 분할 매수 6개월: WOLF (변동성)
- 소액 진입: NVTS (분기 확인 후 증액)
- 시그널 wait: 효성중·현대일렉 (미국 매출 발표 시 가속)
- EV 회복 wait: Onsemi

### 핵심 trade-off

- Integrated (안정·EU) vs Pure-play (성장·US): STM·IFX = 안정, NVTS·POWI·Vicor = 직접 노출
- Upstream (Wolfspeed) vs Device (STM·IFX·Vicor·MPS·TI): 재료 turnaround vs device 안정
- EV (압축) vs AI DC (가속): 본인 *AI DC 가 primary driver* 인식
- US vs KR: 삼성전기·효성중·현대일렉 *한국 직접 alpha* 활용
- *Vicor 가 hidden alpha 1위* — VPD 사실상 선점, backlog +70% QoQ

### Next Wave 모니터링 watchlist

- 예스파워테크닉스 (비상장 SiC KR) — IPO
- ABB (ABBN.SW) — Grid + 800V DC
- Hitachi Energy (6501.T)
- LS ELECTRIC (010120)
- Mitsubishi Electric (6503.T)

### Track 4 등재 후보

- STM, IFX, Vicor, POWI, MPS, TI, 삼성전기, WOLF, NVTS, 효성중공업, 현대일렉트릭, Onsemi (EV 회복 wait)

---

## 13. 업데이트 로그

| 날짜 | 변경 |
|------|------|
| 2026-05-24 | 최초 작성 (Tier 1 깊이). TAM 3 + Moat 3 + Capital 3 = 9/15. 시차 A4 B5 C2 = +7 (Maximum entry). Tier 2 확정 (Tier 1 깊이 분석). 본문 매수 우선순위: STM > IFX > WOLF > NVTS > POWI. **Next Wave Deep (6.4·6.5) 추가**: (1) VPD + 800V Server PSU (2026~ 진행, **Vicor (VICR) hidden alpha 1위, backlog +70% QoQ**, TI·STM·Navitas·POWI·MPS 동시 진입), (2) SST MV→800V (2027~, Navitas-EPFL 250kW + 효성중공업·현대일렉트릭 KR), (3) 10kV+ SiC Grid (2026~2028, Wolfspeed). 매수 우선순위 업데이트: STM > IFX > **Vicor (신규)** > POWI > **MPS (신규)** > **TI (신규)** > **삼성전기 (신규 KR)** > WOLF > NVTS > **효성중공업·현대일렉트릭 (신규 KR)**. NVIDIA 800V DC GTC 2026 + TI·STM·Navitas·POWI 동시 800V GaN PDB 데모 반영. |


---

# ═══════════════════════════════════════════════════
# KR Transmission Boost — KR pure-play thorough 보강
# ═══════════════════════════════════════════════════

# 전력반도체 (GaN·SiC) — KR Transmission Boost (v2.3 추가)

> **Base document**: power-semi-gan-sic.md (2026-05-24, 36KB)
> **Boost 작성일**: 2026-05-24
> **변경 사항**: KR pure-play thorough 보강

---

## 5.3 Sub-area X: 한국 — *KR pure-play thorough* (보강·교체)

> v2.3 KR boost. 기존 본문에 약했던 KR 전력반도체 종목 thorough 보강.

### KR 상장 pure-play

| 티커 | 기업 | 영역 | 시총 | 핵심 thesis | Tier |
|------|------|-----|-----|----------|------|
| **009150** | **삼성전기** ★ | L3 AI 서버 MLCC + 고용량 pwr 모듈 | 12~15조원 | **AI 서버 MLCC 1위 (Murata 대비 lead 잠재)**. 자동차 MLCC + 전력 모듈 | **A KR 1순위** |
| **000990** | **DB하이텍** | L3 8-inch foundry (전력·analog) | 3~4조원 | 전력반도체 + analog 8-inch foundry KR 1위. 일부 SiC·GaN | **A KR 2순위** |
| **240810** | **원익IPS** | L3 반도체 장비 (SiC 부분) | 2~3조원 | SiC 장비 일부 | **B KR 3순위** |
| **123860** | **아나패스** | L3 전력반도체 IC 설계 | 1조원 | 전력반도체 IC | **B KR 4순위** |
| **064760** | **KEC** | L3 SiC 디바이스·power transistor | 2,000~4,000억원 | SiC power MOSFET 진입 시도 | **B KR 5순위** |
| **102710** | **SiCC (실리콘카바이드코리아)** | L3 SiC wafer·substrate | 비상장 / 일부 | SiC 웨이퍼 KR 자체 | **C KR (비상장)** |
| **037210** | **아이에이** | L3 전력반도체·자동차 | 1,500~2,500억원 | 자동차 power IC | **C KR 위성** |
| **131290** | **TES** | L3 반도체 장비 | 1조원 | SiC·power 장비 일부 | **C KR 위성** |
| **272290** | **이엠** | L3 전력 부품 | 1,000억원 | 변동성 | **C KR 위성** |
| **000660** | **SK하이닉스** | L1 반도체 (HBM 1위, 일부 power IC) | 100조원+ | HBM cross + 일부 power | A 메가 (반도체 영역 cross) |

### KR 비상장 / IPO 후보 ★

| 비상장 | 영역 | 펀딩·valuation | IPO 가능성 |
|---------|------|------------|---------|
| **예스파워테크닉스 (YESPowerTechnix)** ★ | L3 SiC power MOSFET·디바이스 | 다중 backed | **IPO 시그널 2026~2027** |
| **케이엘유 (KLU)** | L3 SiC wafer epi | 다중 | n/a |
| **유니드비티플러스 (Unid B Plus)** | L3 silicon carbide 가공 | 다중 | n/a |
| **NEPCS, SK실트론 CSS** | SiC wafer (비상장) | n/a | n/a (대기업 자회사) |

### KR 정책 trigger

- **K-반도체 K-칩스법 (2024~)** = 전력반도체 R&D 자금 가속
- **현대차·기아 EV + 자율 가속** = KR 전력반도체 수요 직접
- **삼성·SK 전력반도체 진입 검토** (HBM 외 신규 영역)

### 진입 전략 (KR 우선순위)

- **KR 1순위: 삼성전기 (009150)** — AI 서버 MLCC + 자동차 (반도체 영역 cross 메가)
- **KR 2순위: DB하이텍 (000990)** — 8-inch foundry 전력 1위 KR
- **KR 3순위 위성**: 원익IPS·아나패스·KEC
- **비상장 모니터링**: **예스파워테크닉스 IPO catalyst**
- **반도체 영역 cross**: SK하이닉스·삼성전자 = 반도체에서 매수

---

## 8.2 한국 종목 보강

| 티커 | 기업 | 영역 | 시총 | Tier | 매수 우선순위 |
|------|------|-----|-----|------|-----------|
| **009150** | **삼성전기** ★ | L3 AI 서버 MLCC | 12~15조원 | **A** | **KR 1순위 (반도체 cross)** |
| **000990** | **DB하이텍** | L3 8-inch foundry | 3~4조원 | **A** | **KR 2순위** |
| 240810 | 원익IPS | L3 SiC 장비 | 2~3조원 | **B** | KR 3순위 |
| 123860 | 아나패스 | L3 전력반도체 IC | 1조원 | **B** | KR 4순위 |
| 064760 | KEC | L3 SiC power | 2,000~4,000억원 | B | KR 5순위 |
| 037210 | 아이에이 | L3 전력 power IC | 1,500~2,500억원 | C | KR 위성 |
| 131290 | TES | L3 반도체 장비 | 1조원 | C | KR 위성 |
| 272290 | 이엠 | L3 전력 부품 | 1,000억원 | C | 변동성 위성 |

### 비상장 모니터링
- **예스파워테크닉스** — SiC power MOSFET, IPO 2026~2027 시그널 ★
- 케이엘유, 유니드비티플러스, NEPCS, SK실트론 CSS

---

## 12 비중 분배 권장 (KR 보강 반영)

- **글로벌 70% : KR 30%** (기존 본문 유지)
- KR 종목:
  - 삼성전기 1~1.5% (KR 1순위), DB하이텍 0.5~1%, 원익IPS 0.3%, 아나패스·KEC·아이에이 합산 0.5%
  - 비상장 예스파워 IPO catalyst wait

### Cross-area
- 삼성전기 = 반도체 영역 cross → 본 영역 매수
- SK하이닉스 = 반도체 영역 메가 카운트

---

## 업데이트 로그 — KR Boost (v2.3)

| 날짜 | 변경 |
|------|------|
| 2026-05-24 | KR boost retrofit. **삼성전기 (009150) AI 서버 MLCC 1위, DB하이텍 (000990) 8-inch foundry, 원익IPS·아나패스·KEC·아이에이·TES** 보강. 비상장: **예스파워테크닉스 SiC MOSFET IPO 2026~2027 시그널 catalyst** 추가. KR 비중 30% 유지. |

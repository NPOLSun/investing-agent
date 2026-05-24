# 자율주행 / Robotaxi — Tier 2 Deep Dive (Tier 1 깊이)

> **Trigger**: Waymo 10 도시 운영, 500k paid weekly rides (2025-12), 2026 EOY 1M/week 목표. Alphabet 이 Waymo $16B 추가 raise (valuation $126B). Tesla Cybercab Apr 2026 양산 진입 + Optimus Gen 3 Summer 2026 low-volume. Baidu Apollo Go 중국 250k+/week. **Aurora 자율 트럭 200대 EOY 2026 → $80M run-rate, Hirschbach 500대 deal ($수억) 2027 deliveries**. Humanoid robot (Apptronik $5B, Figure AI, Boston Dynamics Atlas) 양산 본격 진입. **2026 = Robotaxi + 자율 트럭 + Humanoid 가 commercial reality 로 진입한 원년**.
> **Linked methodology**: methodology_v2.1.md

---

## 0. 메타 정보

| 항목 | 값 |
|------|----|
| 작성일 | 2026-05-24 |
| 최근 갱신 | 2026-05-24 |
| 다음 정기 갱신 | 2026-07-01 |
| 시계 분류 | Core (2~4년) + 일부 장기 (5~15년) |
| Tier | 2 (Tier 1 깊이) |
| Confidence | Medium-High |
| 트랙 | L1A (Global) + KR 부분 |

---

## 1. 한 줄 요약 + 핵심 가설

### 한 줄 요약

> Waymo *commercial reality* 진입 (10도시, 500k/week → 1M/week 목표 2026 EOY), Alphabet $16B raise. Tesla Cybercab 4월 양산. Baidu Apollo Go 250k+/week. **상장 alpha 직접 노출은 Alphabet (GOOGL) 만 유일**. 간접 alpha 는 *Mobileye 회복*, *Uber hidden alpha*. Tesla 는 robotaxi 단독 thesis 약함 (다중 변수). **Next wave 3개 — 자율 트럭 (Aurora·Kodiak) ★ commercial 즉시, Fleet EV 충전 인프라 ★, Humanoid Robot ★★★ (AI 자율 stack 의 자연 확장, 2026~2028 본격)**.

### 핵심 가설

**가설 A — Waymo monopoly 진행, Alphabet 주가에 미반영**
- Waymo 10 도시 (Austin·SF Bay·Phoenix·Atlanta·LA + 신규)
- 2025-01 200k/week → 2025-12 500k/week → 2026 EOY 1M/week 목표
- 누적 15M paid rides (2025), 사고율 인간 대비 -90% (60M miles)
- Waymo $16B raise (2025-12), valuation $126B
- **Alphabet 시총 $2T+ 中 Waymo 비중 6%** → robotaxi 성공 충분히 미반영
- Pichai: "27~28년 Waymo 가 financials 에 의미 있게"
- Waymo IPO 가능성 2027~2028 = 다음 catalyst

**가설 B — Tesla robotaxi 단독 thesis 약함**
- Tesla Austin 31~44대 → Waymo 3,000대의 1.5%
- Cybercab Apr 2026 양산, Musk track record (delivery 일정 미스)
- camera-only vs Waymo LiDAR-multi-modal — 기술 경쟁력 의문
- 그러나 *Optimus + xAI + Robotaxi + Cybercab + Optimus Gen 3* 종합 thesis 는 별도. **Tesla 는 robotaxi 만으로 매수 X**

**가설 C — 상장사 알파 3축**

| 축 | 종목 | 매수 우선순위 |
|----|------|-----------|
| Pure-play (상장) | **Alphabet (GOOGL)** | A (AI Foundation 통합) |
| 센서·반도체 | **Mobileye (MBLY), NVIDIA (NVDA), Ambarella (AMBA)** | A (Mobileye 회복) |
| Ride-hailing 통합 | **Uber (UBER)** | A (Waymo·Aurora·WeRide partner) |
| 자율 트럭 ★ Next Wave | **Aurora (AUR), Kodiak (KDK)** | A (next wave deep) |
| LiDAR | Aeva, MicroVision, Hesai, Innoviz, Luminar, Ouster | C (변동성 매우 큼) |
| 중국 robotaxi | Baidu, Pony.ai | C (지정학) |
| 한국 자율 부품 | 현대모비스, HL만도, 현대오토에버 | C (글로벌 채택 약함) |

**가설 D — Uber hidden alpha**
- Waymo·Aurora·WeRide 다중 협력
- Q1 2026 GB $42.8B, 매출 +14% yoy, 시총 ~$170B
- **모든 robotaxi 의 공통 distribution** — 이기는 partner 한 곳만 있으면 함께 이김

**가설 E — Mobileye 회복 진행 (저평가)**
- EyeQ chip + L2/L3 통합. Hyundai·VW·BMW·Audi·Toyota 다중 OEM
- Intel spin-off 후 valuation 압축
- 2026 회복 진행, 시총 ~$15~20B, P/E ~25x

**가설 F — 한국 자율 부품 약함**
- 현대모비스 (012330), HL만도 (204320), 현대오토에버 (307950)
- 글로벌 robotaxi 채택 거의 없음
- *위성 자산* (1~3% 비중)

### 기각 조건

- Waymo 확장 지연 (인허가 막힘) — 가능성 낮음
- 큰 사고 (Cruise 식 운영 중단)
- Tesla camera-only break-through (가능성 낮음)
- 중국 robotaxi 글로벌 침투 가속

---

## 2. 4가지 잣대 채점

### 잣대 1: TAM

**점수: 4 / 5** (Major expansion, ×3~5 + 100B$+)

- 글로벌 robotaxi 시장: 2025 ~$5B → 2030 ~$50~100B → 2035 ~$200~500B
- Markets and Markets: 글로벌 robotaxi fleet 934k대 (2035), 시장 $105B
- 자율 트럭 추가: 2030 ~$30~50B (Aurora·Kodiak)
- Humanoid robot (별도 영역 후보): BofA forecast 2035 ~$3B 시작, 2040 ~$수십 B
- 5년 후 robotaxi $50~100B + 자율 트럭 $30~50B + humanoid 초기 = 합산 100B$+

**Confidence**: Medium-High

### 잣대 2: Moat

**점수: 4 / 5** (Major reshuffle + 비가역 강)

- **Waymo monopoly**: 도시별 mapping + 인허가 + 운영 노하우 1위 (4.9 별점)
- 데이터 비대칭: 15M rides 누적, 사고율 -90%
- 신규 진입 어려움: HD-map 구축 2~4년, regulatory, 자본
- Tesla camera-only vs Waymo LiDAR — 경쟁력 의문
- 중국 (Baidu·WeRide·Pony) 가속 — 미국·EU 진입 *지정학 제약*
- 비가역성: 도시 인허가 = lifetime moat (Phoenix 8년+)
- *자율 트럭* Aurora Volvo·PACCAR·Continental 협력 = *미국 트럭 OEM 절반 lock-in*

**Confidence**: Medium-High

### 잣대 3: Capital

**점수: 3 / 5** (Major capital 10~100B$/년)

- Waymo $16B raise (2025-12)
- Tesla $20B CapEx 2026 (Robotaxi + Optimus + AI)
- Cruise 종료 (2024) GM $10B+ sunk
- 자동차 OEM 자율 R&D ~$10~15B/년
- Aurora·Kodiak 누적 ~$3B raised
- Humanoid: Apptronik $935M, Figure $1B+, 1X (NEO) $11B valuation
- VC robotaxi·트럭·humanoid 합산 ~$15~20B/년

**Confidence**: Medium-High

### ~~잣대 4: Tech~~ (폐기)

### 합산

| 트랙 | 점수 | 임계 |
|------|------|------|
| L1A | **11 / 15** | Tier 1 미달, Tier 2 ✅ |

→ **Tier 2 확정** (직접 상장 alpha 약 + 본인 우선순위 정원). Tier 1 깊이 분석.

---

## 3. A·B·C 시차 평가

### A 지표 (자본 유입) — **4 / 5**
- Waymo $16B raise
- Tesla $20B 2026 CapEx
- Aurora-Hirschbach 500트럭 deal ($수억)
- Humanoid funding 가속 (Apptronik $5B, Figure NVDA-backed)
- Uber-Waymo·Aurora·WeRide 파트너십

### B 지표 (실물 변화) — **5 / 5**
- Waymo 2025: 200k → 500k weekly rides
- 10 도시 운영 (2025-02 6 → 2025-12 10)
- Aurora Q1 2026 200 트럭 EOY → $80M run-rate, 12M 자율 마일 누적
- Kodiak 28 customer trucks Q1 2026, 2026 EOY driverless launch 계획
- Cybercab Apr 2026 양산
- Tesla Optimus Gen 3 Summer 2026 양산
- Figure 02 BMW 11개월, 30,000+ 차량
- Apptronik Apollo Mercedes-Benz 협력
- Baidu Apollo Go 250k+/week

### C 지표 (가격 반영) — **3 / 5**
- Tesla 1년 +50~100% (Robotaxi + Optimus thesis)
- Alphabet 일부 반영, Waymo 시총 6% 정도 → reflect 부족
- Mobileye 회복 진행 (저평가)
- LiDAR 변동성 매우 큼
- Aurora YTD +89%, EV $12.8B — *일부 반영*
- Uber 일부 반영 (robotaxi 노출 적극 평가 안됨)

### 시차 매력도 = A + B − C = **4 + 5 − 3 = +6 (Very strong entry)**

→ 시차 매력 매우 큼. *상장 alpha 매핑 도전적* (Alphabet·Mobileye·Uber 간접 다중).

---

## 4. 산업 메가트렌드 (Step 1)

### 4.1 수요 측

**단기 (12~18개월)**
- Waymo 도시 확장: 2026 신규 5+ 도시 (DC·NYC·도쿄·런던). Lyft·Uber 가속.
- Tesla Cybercab Apr 2026 양산 (delivery 지연 risk)
- **Aurora·Kodiak 자율 트럭 commercial scale (2026 EOY)** ★ next wave
- Zoox Las Vegas·SF 유료 전환
- Baidu Apollo Go 글로벌 (UAE·홍콩·스위스·UK·독일)
- **Humanoid Robot 양산 시작 (Tesla Optimus Gen 3 Summer 2026, Apptronik·Figure·Boston Dynamics)** ★ next wave

**중기 (2~4년)**
- Waymo 1M/week → 5M/week (2027~2028)
- 상업 trucking 자율 본격화 (Aurora DaaS 2027 scale)
- 로봇·humanoid 본격 (Optimus 2028~2029 high-volume)
- 자동차 OEM L4 출시 (GM·Ford·VW·Toyota)
- 인허가 표준화 (Texas·California·Arizona)

**장기 (5~15년)**
- 개인 소유 → 공유 robotaxi 전환 = 자동차 OEM 매출 모델 격변
- 인간 운전자 직업 감소 — 사회·노조 저항
- Humanoid 가정 채택 (1X NEO·Tesla Optimus 가정용)

### 4.2 공급 측

**현재 병목 — 도시 mapping + 인허가**
- Waymo HD-map: 신규 도시 2~4년
- 인허가 주별·시별 별개 (NHTSA federal 진행 중)
- EU·아시아 보수
- LiDAR capa: 자체 + Aeva·MicroVision·Hesai·Innoviz·Velodyne

**다음 병목 — 컴퓨팅 + 데이터·AI 인프라**
- NVIDIA Drive Thor + 자체 ASIC (Tesla Dojo, Waymo TPU)
- 도시별 데이터: edge case 학습. *Waymo 우위*
- Simulation 환경 (NVIDIA Omniverse, Waymo Carcraft)

**추가 병목 — fleet 운영 + EV 충전 인프라** ★ next wave deep
- Robotaxi fleet 양산 → 전기차 충전 폭증
- Tesla Supercharger·ChargePoint·EVgo·Electrify America
- *Robotaxi 가 전체 EV 매출의 30~50%* 가능 (2030)

### 4.3 정책·지정학 변수

- 미국 NHTSA federal 표준 진행 (2026~2027)
- 트럼프 자율 친화 정책 (Musk 영향)
- EU 인허가 보수, 2030+ commercial
- 중국 자체 (Baidu·WeRide·Pony) 정부 지원 강
- 한국: K-방산·자동차 정책, 글로벌 robotaxi 미흡

---

## 5. 밸류체인 매핑 (Step 2)

### 5.1 다이어그램

```
[L1 Sensor]
  ├ LiDAR: Aeva (AEVA), MicroVision (MVIS), Hesai (HSAI), Innoviz (INVZ), Luminar (LAZR), Ouster (OUST), Waymo 자체
  ├ Camera: Sony (6758.T), 삼성·LG (간접)
  ├ Radar: Bosch (비상장), Continental (CON.DE)
  └ Ultrasound: 다중
       ↓
[L2 반도체·컴퓨팅]
  ├ NVIDIA Drive Thor·Orin — Tier 1 platform
  ├ Tesla FSD chip + Dojo (자체)
  ├ Mobileye EyeQ (MBLY) — Vision + L2/L3 통합
  ├ Ambarella (AMBA) — 저비용 vision
  ├ Qualcomm Snapdragon Ride (QCOM)
  └ Renesas R-Car (6723.T)
       ↓
[L3 Software / AI Stack]
  ├ Waymo Driver (자체), Tesla FSD (자체)
  ├ Mobileye SuperVision·Chauffeur·Drive
  ├ Wayve (비상장 영국)
  ├ Aurora Driver (AUR), Kodiak Driver (KDK)
  ├ Pony.ai (PONY), Zoox (Amazon), Apollo Go (BIDU)
       ↓
[L4 HD-Map / 측위 / Geospatial]
  ├ Waymo 자체, Mobileye REM, Tesla 자체
  ├ Trimble (TRMB), HEXAGON (HEXA-B.ST)
  └ HERE (비상장 Audi·BMW·Daimler 컨소시엄)
       ↓
[L5 Vehicle / OEM]
  ├ Waymo: Jaguar I-Pace, Hyundai IONIQ 5, Geely Zeekr
  ├ Tesla: Cybercab (자체)
  ├ Zoox: 자체 toaster
  ├ Aurora: Volvo·PACCAR·Continental (트럭)
  ├ Kodiak: Daimler·ZF (트럭)
  └ 자동차 OEM (Hyundai·GM·Ford·VW·Toyota·BYD)
       ↓
[L6 Operation / Ride-hailing 통합]
  ├ Waymo One (자체)
  ├ Uber (UBER) — Waymo·Aurora·WeRide
  ├ Lyft (LYFT) — Baidu·Wayve
  ├ Grab (GRAB) — WeRide 동남아
       ↓
[L7 충전·운영 인프라] ★ next wave
  ├ Tesla Supercharger (자체)
  ├ ChargePoint (CHPT), EVgo (EVGO)
  └ Electrify America (VW 그룹)
       ↓
[L8 End Customer]
  개인 (Waymo One·Tesla App) | 기업 (Uber Business, 트럭 Hirschbach·McLane) | 도시 transportation
```

### 5.2 레이어별 분석

| 레이어 | GM | 경쟁구도 | 중국 침투 | 진입장벽 | 본인 매력도 |
|--------|-----|---------|---------|---------|----------|
| L1 LiDAR | 30~50% | 다수, Hesai 80%+ | 매우 큼 | 자본 + 기술 | **★ 변동성** |
| L1 Camera | 매우 높음 | Sony·Samsung 과점 | 일부 | 광학 + 자본 | 간접 |
| L2 NVIDIA | 매우 높음 (80%+) | NVDA 압도 | 약함 | 매우 높음 | **★★ (AI Foundation 중복)** |
| L2 SoC (MBLY·AMBA) | 중상 (30%+) | 과점 | 일부 | IP·기술 | **★★ MBLY 저평가** |
| L3 Software | 매우 높음 | Waymo·Tesla·MBLY·Wayve·Aurora·Kodiak 다수 | 큼 (Baidu·Pony·WeRide) | 데이터·자본 | **★★★ Alphabet 직접** |
| L4 HD-Map | 중상 | Trimble·HEXAGON | 약함 | 데이터 | 간접 |
| L5 OEM | 낮음 | 다수 | 큼 | 자본 + 규모 | 자동차 영역 중복 |
| L6 Ride-hailing | 15~30% | Uber·Lyft·Grab·Didi | 큼 (Didi) | 네트워크 | **★★ Uber** |
| L7 충전 | 중간 | CHPT·EVGO·Tesla·VW | 일부 | 자본 + 규모 | **★ next wave** |

### 5.3 하위 세분화

#### Sub-area 1: Pure-play (Alphabet 유일)
- **Alphabet (GOOGL)**: Waymo 100%, $126B valuation, 1M/week 목표. **AI Foundation 중복**.

#### Sub-area 2: LiDAR (위성, 변동성)
- Aeva·MicroVision·Hesai·Innoviz·Luminar·Ouster — 1~3% 비중 max

#### Sub-area 3: 반도체·컴퓨팅 ★★ 매수 매력
- **Mobileye (MBLY)**: 저평가 회복. 시총 ~$15~20B, P/E ~25x
- **NVIDIA (NVDA)**: AI Foundation 중복
- **Ambarella (AMBA)**: 저비용 vision, 시총 ~$3B, 변동성

#### Sub-area 4: 맵·측위 — 간접
- Trimble (TRMB), HEXAGON — 시총 ~$20B, robotaxi 노출 적음

#### Sub-area 5: Ride-hailing ★★ Uber
- **Uber (UBER)**: Q1 2026 GB $42.8B, +14% yoy, $170B, P/E ~30x
- Lyft (LYFT): $8~10B, Uber 대비 약

#### Sub-area 6: 자율 트럭 ★★★ Next Wave deep
- **Aurora (AUR)**, **Kodiak (KDK)** — 6.4 next wave 에서 deep

#### Sub-area 7: 중국 robotaxi — 지정학 부담
- Baidu (BIDU), Pony.ai (PONY) — 매수 권장 안함

#### Sub-area 8: 한국 자율 — 위성
- 현대모비스 (012330) ~25조원
- HL만도 (204320) ~3~5조원
- 현대오토에버 (307950) ~3조원

---

## 6. 병목 식별 (Step 3)

### 6.1 현재 병목

| 병목 | 영향 | 수혜자 |
|------|-----|------|
| 도시 인허가 + HD-map | 신규 도시 2~4년 lead time | Waymo (이미 mapping) |
| LiDAR 가격·신뢰도 | OEM L4 채택 제약 | Hesai (가속), Aeva·MVIS·INVZ |
| Tesla camera-only 한계 | edge case 신뢰도 | Waymo·MBLY·LiDAR |
| Cybercab 양산 일정 | Apr 2026 vs delay risk | Waymo (lead 강화) |

### 6.2 다음 병목 ★ 투자 핵심

| 병목 | 등장 시점 | 수혜자 |
|------|---------|------|
| **자율 트럭 commercial scale** | 2026 EOY ~ 2027 | **Aurora (AUR), Kodiak (KDK)** ★ |
| **Robotaxi fleet 양산 + EV 충전** | 2027~2028 | Tesla SC, CHPT, EVGO ★ |
| **Humanoid Robot 양산** | 2026~2028 | **Tesla, Apptronik (비상장), Figure (비상장), Boston Dynamics (Hyundai)** ★ |
| L4 → L5 (Geofence 해제) | 2028~2030 | Waymo, Tesla |
| 자율주행 보험·법적 책임 표준 | 2026~2028 | 산업 전체 |

### 6.3 컨센서스 vs 본인 뷰

**컨센서스**: "Tesla 가 robotaxi future" Musk 약속 신뢰. LiDAR 비용 부담 → Tesla 이긴다. Alphabet Waymo 그냥 part.

**본인 뷰**:
- Waymo *actual commercial reality* (10 도시, 500k/week) — Tesla 31대 대비 14,000~16,000배
- Tesla camera-only *break-through 미발생* (Kalanick: "ChatGPT moment 아직")
- Alphabet *유일한 직접 상장 robotaxi pure-play*, 시총 노출 희석
- **자율 트럭 (Aurora·Kodiak) 이 *robotaxi 보다 빨리 commercial 도달*** (B2B, fixed route, 2026 EOY scale)
- **Humanoid Robot 이 진짜 next-next wave** — AI 자율 stack 의 자연 확장, 2026~2028 양산

### 6.4 Next Wave Deep Analysis ★★★ 본인 진짜 알파

> Waymo·Tesla·Alphabet 등 *over-known 영역*. 진짜 alpha 는 *병목 이동*. 3개 선정 — 자율 트럭, Fleet EV 충전, Humanoid Robot.

---

#### Next Wave 1: 자율 트럭 (Autonomous Trucking) ★★★ 2026 EOY ~ 2027

**왜 next wave 인가**
- 자율 트럭 = *robotaxi 보다 commercial 빠름*. B2B 고정 경로 (Dallas-Houston 등), 운전자 부족 + 비용 절감 = 즉시 가치.
- 2030 자율 per-mile cost $2.06 vs 인간 $3.21 (-38%) — 노동 비용 제거 효과
- Aurora **Q1 2026 매출 $1M (Q+10%), 200 트럭 EOY 2026, $80M run-rate** = *exit 2026 가 inflection*
- Aurora-Hirschbach 500 트럭 deal ($수억 multi-year, 2027 deliveries)
- Aurora 7개 driverless 고객 (Hirschbach, Uber Freight, Werner, FedEx, Schneider, Volvo, McLane = Berkshire Hathaway)
- Kodiak 28 customer trucks Q1 2026, 2026 EOY driverless launch 계획 (Bosch·Daimler·ZF 협력)
- Aurora 12M 자율 마일 누적, Kodiak deploying

**병목 메커니즘**
- 트럭 OEM 통합 (Aurora-Volvo·PACCAR·Continental = 미국 트럭 OEM 절반)
- HD-map highway 우선 (도심 보다 빠름)
- 트럭 stop·연료 자동화 (Aurora supervised testing 진행)
- 보험·법적 책임 표준화

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Aurora Innovation (AUR)** | US | **L4 트럭 sector leader**. Q1 2026 매출 $1M (Q+10%), 200 트럭 EOY 2026, $80M run-rate. Hirschbach 500 트럭. EV $12.8B, YTD +89% | **A 1순위 next wave** |
| **Kodiak AI (KDK)** | US | Aurora 의 *유일한 진정한 경쟁*. 28 customer trucks, Bosch·Daimler·ZF | **A 2순위 next wave (변동성)** |
| **Volvo (VLVLY)** | EU | Aurora 트럭 OEM, 자체 자율 진행 | B (위성) |
| **PACCAR (PCAR)** | US | Aurora 트럭 OEM (Kenworth, Peterbilt), 시총 ~$50B | B (안정 dividend) |
| **Continental (CON.DE)** | EU | Aurora 자율 sensor·system | C (위성) |
| **NVIDIA (NVDA)** | US | Drive Thor 트럭 platform | AI Foundation 중복 |
| **Uber (UBER)** | US | Uber Freight = Aurora 고객 | 이미 본문 매수 |
| **Daimler Truck (DTRUY)** | EU | Kodiak 협력 OEM | B (위성) |
| Plus, Embark | 비상장 | 소형, 변동 | n/a |

**한국**
- 직접 노출 약함. 현대차·기아 자율 트럭 시도하지만 글로벌 점유 없음.

**Timing & Catalyst**
- Q2 2026: Aurora 2세대 hardware kit 출시 + observer 없는 driverless 본격
- Q4 2026: Aurora 200 트럭 + Kodiak driverless launch
- 2027: Aurora DaaS (Driver as a Service) 본격 scale. Hirschbach 500 트럭 deliveries
- 2028: Aurora FCF positive 목표

**모니터링**
- Aurora 분기 (매출·트럭 수·고객 cohort) → P1
- Kodiak 분기 (driverless launch 일정) → P1
- PACCAR·Volvo·Daimler Truck 분기 자율 OEM 매출 → P2
- Aurora-Hirschbach 500 트럭 deal 확정 → P1 (catalyst)
- 미국 NHTSA federal 트럭 자율 표준 → P1

**숨겨진 매력 — Aurora (AUR)**
- *L4 트럭 sector leader, scaling 단계*
- Q1 2026 매출 $1M → 2026 EOY $80M run-rate (×80배 scale)
- 7개 driverless 고객 (Berkshire Hathaway 자회사 포함)
- Volvo·PACCAR·Continental 트럭 OEM 절반 lock-in
- **단점**: EV $12.8B 매출 대비 3,794x — 매출 가속 없으면 valuation reset 가능
- Cash burn $190-220M/q (2028 FCF positive)
- **본 영역 next wave 1순위, 변동성 큼**

**리스크**
- Aurora cash burn 가속 vs 매출 ramp 늦으면 추가 capital raise 필요
- Kodiak 가 first-mover advantage 잠식
- Tesla camera-only 트럭 (Semi) 가 validate 되면 cost 압박
- 큰 사고 시 산업 전체 운영 중단

---

#### Next Wave 2: Robotaxi Fleet Ops + EV 충전 인프라 ★★ 2027~2028

**왜 next wave 인가**
- Robotaxi fleet 양산 (Waymo 1M/week → 5M/week, Tesla Cybercab) → *EV 충전 폭증*
- Robotaxi 가 *전체 EV 매출의 30~50%* 가능 (2030 추정) — fleet 운영 모델 변화
- Tesla Supercharger·ChargePoint·EVgo 직접 수혜
- 자율 차량 충전은 *완전 자동* (로봇 arm·인덕션) 인프라 추가 필요

**병목 메커니즘**
- 충전 station 양산 + 전력 grid 통합
- 자동 충전 시스템 (로봇 arm, 인덕션 charging)
- 24/7 운영 fleet maintenance 인프라
- Robotaxi 특정 EV 모델 (Cybercab, Waymo I-Pace 후속) 표준화

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **ChargePoint (CHPT)** | US | EV 충전 station 1위. 시총 ~$300M, 변동성 매우 큼 | C (변동성) |
| **EVgo (EVGO)** | US | EV 충전 fast charging. 시총 ~$300M, 변동성 | C (변동성) |
| **Tesla (TSLA)** | US | Supercharger + Robotaxi + Cybercab + Optimus 종합 | B (별도 thesis 종합) |
| **Blink Charging (BLNK)** | US | EV 충전, 소형 | C |
| **Allego (ALLG)** | EU | 유럽 EV 충전 | C (위성) |
| **Wallbox (WBX)** | EU | 가정용·상업용 충전 | C |
| **Electrify America (VW 자회사)** | EU/US | VW 통해 노출 | 간접 |
| **TI (TXN)** | US | 800V GaN PDB (자율 차량 charging system 포함) | 전력반도체 영역 중복 |

**한국**
- **SK이노베이션 (096770)** — 배터리 + 충전 일부
- **LG에너지솔루션 (373220)** — 배터리 1위, 자율 robotaxi 노출 일부
- **삼성SDI (006400)** — 배터리, 일부 자율 노출
- 한국 직접 charging 상장 알파 약함

**Timing & Catalyst**
- 2027~2028: Robotaxi fleet 본격 양산 → 충전 인프라 폭증
- 2028~: 자동 충전 (robot arm·induction) 표준화 시그널
- 트럼프 EV 보조금 폐지 영향 (그러나 robotaxi 는 영향 작음)

**모니터링**
- ChargePoint·EVgo 분기 (수주·매출 가속) → P2
- Tesla Supercharger 분기 매출 → P2
- 빅테크 (Waymo·Tesla) 자체 charging 인프라 발표 → P2

**리스크**
- EV 충전 가격 압박 (commoditization)
- Tesla Supercharger 의 사실상 monopoly 가능성 (ChargePoint·EVgo 약화)
- 자동 충전 표준 분기

**진입 전략**
- 직접 alpha 약함, 변동성 매우 큼
- ChargePoint·EVgo *0~1% 위성 비중* 만
- Tesla 는 *별도 종합 thesis* (Robotaxi + Optimus + Supercharger + xAI)
- **추가 매수 권장 안함**

---

#### Next Wave 3: Humanoid Robot ★★★ 2026~2028 본격

**왜 next wave 인가**
- *AI 자율 stack 의 자연 확장*. 자율주행 (vision + decision + control) → humanoid (vision + manipulation + bipedal)
- Tesla CEO: "Optimus 가 Tesla 시총 대부분 차지 가능" — robotaxi 보다 큰 TAM 주장
- 2026 시작 → 2028~2029 high-volume 양산
- **Tesla Optimus Gen 3 Summer 2026 low-volume 양산** — Fremont 일부 전환 (Model S/X 종료 후), 목표 가격 $20~30k
- **Apptronik Series A $520M at $5B valuation (2026-02)**, 누적 $935M, Google DeepMind·Mercedes-Benz 협력
- **Figure AI** — Figure 02 BMW Spartanburg 11개월, 30,000+ 차량 기여, Leipzig 확장. NVIDIA-backed
- **Boston Dynamics Atlas** (Hyundai 자회사) — 2026 production 다 commit, 2028 Hyundai 양산
- **1X (NEO)** — ex-DeepMind staffers, $11B valuation 협상
- **Agility Robotics Digit** — *유일한 consistent commercial revenue* (GXO·Amazon 창고)
- **Unitree (CN)** — 2025 5,500+ 출하, 2026 10~20k 목표

**병목 메커니즘**
- Humanoid hardware (액추에이터·battery·센서) capa
- AI manipulation (정교한 손 제어) — DeepMind Gemini Robotics·Tesla FSD 확장
- Edge AI compute (NVIDIA Drive Thor·자체 ASIC)
- 인증·안전 (산업 vs 가정 환경)
- 단가 reduction ($30~50k → $20~25k → $15k)

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Tesla (TSLA)** | US | **Optimus Gen 3 Summer 2026 양산**, Fremont 전환, $20-30k 목표 | **A 1순위 (Optimus 포함 종합)** |
| **NVIDIA (NVDA)** | US | Drive Thor + Project GR00T (humanoid AI foundation model) | AI Foundation 중복 |
| **Hyundai Motor (005380)** | KR | **Boston Dynamics Atlas 100% 자회사**, 2028 양산 목표 | **A KR 1순위 (저평가 humanoid 노출)** |
| **현대오토에버 (307950)** | KR | Hyundai 그룹 자율 SW + Boston Dynamics 일부 | B (위성 KR) |
| **Apptronik (비상장)** | US | $5B valuation, Google DeepMind·Mercedes 협력 | n/a (IPO 시그널 모니터링) |
| **Figure AI (비상장)** | US | NVDA-backed, BMW Spartanburg | n/a |
| **1X (비상장)** | US | NEO 가정용, $11B valuation 협상 | n/a |
| **Agility Robotics (비상장)** | US | Digit, *유일 commercial revenue* | n/a |
| **Unitree (비상장 CN)** | CN | 2025 5,500+ 출하 | n/a (지정학) |
| **Honor (비상장 CN)** | CN | "Lightning" 마라톤 우승 (2026-04) | n/a |
| **Cognex (CGNX)** | US | machine vision 일부 (humanoid 간접) | C (위성) |
| **Brooks Automation (AZTA)** | US | factory automation, 일부 humanoid 간접 | C |
| **Rockwell Automation (ROK)** | US | factory automation | C |

**한국 — Hyundai Motor (005380) 가 진짜 hidden alpha**
- Boston Dynamics 100% 자회사 (소프트뱅크 인수 후 Hyundai 2020-12 인수, $1.1B)
- Atlas 차세대 humanoid 양산 = *글로벌 top-tier*
- Hyundai 시총 ~30~40조원, P/E 5~7x **극단적 저평가**
- *humanoid 노출이 시총에 거의 미반영* — *본 deep dive 의 hidden alpha 1위*
- 자동차 본업 + Robotaxi (Waymo IONIQ 5) + Boston Dynamics + 미국 정책 수혜 (Hyundai 미국 fab) 다중

**Timing & Catalyst**
- 2026 Summer: Tesla Optimus Gen 3 low-volume 양산 시작
- 2026~2027: Apptronik·Figure·Boston Dynamics 산업 deployment scale
- 2027~2028: 가정용 humanoid (1X NEO·Optimus 가정용) 시작
- 2028~2029: Optimus high-volume + Hyundai Boston Dynamics 본격 양산
- BofA: 2035 humanoid 시장 ~$3B → 2040 ~$수십 B → 2050 *수천 억 달러*

**모니터링**
- Tesla Optimus 분기 진척 (Musk 분기 commentary) → P1
- Hyundai 분기 (Boston Dynamics segment, Atlas 진척) → P1
- Apptronik·Figure·1X IPO 시그널 → P1 (catalyst)
- NVIDIA Project GR00T 진척 → P2
- Mercedes-Benz·BMW·Amazon·GXO humanoid 채택 확대 → P2

**숨겨진 매력 — Hyundai Motor (005380)**
- **Boston Dynamics 100% 자회사** (Atlas 글로벌 top-tier)
- 시총 ~30~40조원, **P/E 5~7x 극단적 저평가**
- humanoid 노출 *거의 시총에 미반영*
- 자동차 본업 + Robotaxi (Waymo IONIQ 5 공급) + 미국 fab + Boston Dynamics = *4개 thesis 통합*
- **본 deep dive next wave hidden alpha 1위**

**리스크**
- Humanoid 양산 일정 historically delay (Musk track record)
- 단가 reduction 더딤 → 시장 확장 늦춤
- 안전 사고 시 산업 전체 backlash
- 중국 (Unitree·Honor) 가격 폭락 가속 시 글로벌 가격 압박

---

### 6.5 Next Wave 종합 — 본인 진입 전략

**우선순위 (Timing + 상장 alpha)**

| 순위 | Next Wave | Timing | 핵심 종목 | 비중 |
|-----|---------|--------|---------|-----|
| 1 | **자율 트럭** | 2026 EOY ~ 2027 | **Aurora (AUR)**, Kodiak (KDK), PACCAR | 1~2% (Aurora 신규) |
| 2 | **Humanoid Robot** | 2026~2028 | **Hyundai Motor (005380)** ← *hidden alpha 1위*, Tesla | 2~3% (Hyundai 신규 KR) |
| 3 | **Fleet EV 충전** | 2027~2028 | ChargePoint, EVgo (변동성 매우 큼) | 0~1% (위성) |

**자율주행 영역 종합 매수 우선순위 업데이트**

1. **Alphabet (GOOGL)** — 유일 robotaxi pure-play, AI Foundation 통합 카운트
2. **Mobileye (MBLY)** — 저평가 회복, 즉시
3. **Uber (UBER)** — hidden alpha (다중 협력), 즉시
4. **Aurora (AUR)** ← **Next wave 1순위: 자율 트럭 sector leader (Q1 2026 $1M → EOY $80M run-rate)**
5. **Hyundai Motor (005380)** ← **Next wave KR 1순위: Boston Dynamics 100% 자회사, P/E 5~7x 극단적 저평가**
6. **Kodiak AI (KDK)** ← **Next wave 자율 트럭 #2 (변동성)**
7. PACCAR (PCAR) — Aurora 트럭 OEM, 안정 dividend
8. Tesla (TSLA) — robotaxi 단독 약, *Optimus + 종합 thesis 별도*

**모니터링 watchlist**
- Apptronik (비상장) — IPO 시그널
- Figure AI (비상장) — IPO 시그널
- 1X (NEO 비상장) — $11B valuation 협상, IPO 시그널
- Agility Robotics (비상장) — IPO
- Wayve (비상장 영국) — IPO
- LiDAR 전종목 (AEVA·MVIS·HSAI·INVZ·LAZR·OUST) — 변동성 위성
- ChargePoint·EVgo — 위성 (변동성)
- Trimble·HEXAGON — 간접
- 중국 robotaxi (BIDU·PONY) — 지정학 부담

**Humanoid Robot 영역 분리 고려**
- 본 deep dive 의 next wave 3으로 잡았지만, **Humanoid Robot 은 *별도 deep dive 영역* 으로 분리 후보**
- 추후 별도 deep dive 작성 시: Hyundai·Tesla·NVIDIA·Apptronik·Figure·1X·Agility·Boston Dynamics·Unitree·Honor 등
- 본 영역에서는 *자율주행 stack 의 자연 확장* 관점 유지

---

## 7. 자금 흐름 시그널 (Step 4)

### 7.1 관련 ETF

| 티커 | 시장 | 비중 |
|------|------|----|
| DRIV | US | Global X Autonomous & EV — 중간 |
| IDRV | US | iShares Self-Driving EV & Tech — 중간 |
| KARS | US | KraneShares EV — 중간 |
| HAIL | US | SPDR S&P Kensho Smart Mobility — 중간 |
| BOTZ | US | Global X Robotics & AI (humanoid 일부 포함) — 중간 |
| ROBO | US | ROBO Global Robotics — 중간 |
| KODEX 자동차 (091170) | KR | 현대차·만도·모비스 — 한국 노출 |
| TIGER 글로벌자율주행&전기차SOLACTIVE (391670) | KR | 글로벌 자율 — 중간 |

→ ETF 노출 *중간*. **직접 종목 + ETF 동시 활용**.

### 7.2 추적 지표

**P1 (분기 필수)**
- Waymo weekly rides + 도시 수
- Tesla Robotaxi/Cybercab 일정 + 양산
- Mobileye 분기 (EV·OEM 다중)
- Uber 분기 + Waymo·Aurora 협력
- NVIDIA Drive 매출 (AI Foundation 통합)
- **Aurora 분기 (매출·트럭·고객)** ← next wave
- **Kodiak 분기 (driverless launch)** ← next wave
- **Hyundai Motor 분기 (Boston Dynamics segment, 미국 fab)** ← next wave
- **Tesla Optimus 분기 (Musk commentary)** ← next wave

**P2 (분기 모니터링)**
- Waymo IPO 시그널 → P1 catalyst
- Baidu·Pony·WeRide 매출
- LiDAR 분기 (AEVA·MVIS·HSAI·INVZ·LAZR·OUST)
- ChargePoint·EVgo 분기
- Apptronik·Figure·1X IPO 시그널 → P1 catalyst

**P3 (지속)**
- Wayve IPO 시그널
- NHTSA federal 규제 진척
- EU·일본·한국 자율 인허가
- 자동차 OEM L4 출시

### 7.3 Startup Landscape

| 스타트업 | 영역 | 비고 |
|---------|------|----|
| Waymo (Alphabet) | Robotaxi | $16B raise, $126B valuation, IPO 2027~2028 |
| Zoox (Amazon) | Robotaxi | 자회사 |
| Wayve | L4 SW | $1B+ |
| Cruise (GM) | 폐쇄 | n/a |
| Apptronik | Humanoid | $935M 누적, $5B valuation |
| Figure AI | Humanoid | NVDA-backed, BMW |
| 1X (NEO) | Humanoid 가정용 | $11B valuation 협상 |
| Agility Robotics | Humanoid 산업 | GXO·Amazon, 유일 commercial revenue |
| Boston Dynamics | Humanoid Atlas | Hyundai 100% 자회사 |
| Unitree (CN) | Humanoid | 2025 5,500+, 2026 10-20k |
| Plus, Embark | 자율 트럭 | 소형·비상장 |

---

## 8. 종목 매핑 (Step 5)

### 8.1 글로벌 종목

| 티커 | 기업 | 영역 | 시총 | P/E | Tier |
|------|------|-----|-----|-----|------|
| **GOOGL** | Alphabet | L3+L4+L5 (Waymo 100%) | $2T+ | ~25x | **A 1순위 (AI Foundation 통합)** |
| **MBLY** | Mobileye | L2+L3 (EyeQ + SuperVision) | $15~20B | ~25x | **A 2순위 (회복)** |
| **UBER** | Uber | L6 (다중 협력) | $170B | ~30x | **A 3순위 (hidden)** |
| **AUR** | Aurora ★ next wave | L3+L5 (자율 트럭 sector leader) | $12.8B | n/a (P/S high) | **A 4순위 (신규 next wave)** |
| **KDK** | Kodiak ★ next wave | L3+L5 (자율 트럭 #2) | n/a | n/a | **A 5순위 (신규 변동)** |
| TSLA | Tesla | L3+L5 (Cybercab) + Optimus + Supercharger | $1T+ | ~80x | B (다중 thesis 종합) |
| NVDA | NVIDIA | L2 (Drive Thor) | $4T+ | ~25x | AI Foundation 중복 |
| **PCAR** | PACCAR | L5 (Aurora OEM, Kenworth·Peterbilt) | ~$50B | ~15x | **B 위성 안정 dividend** |
| AMBA | Ambarella | L2 (vision SoC) | $3B | ~30x | C (변동성) |
| TRMB | Trimble | L4 (정밀 측위) | ~$20B | ~20x | C (간접) |
| LYFT | Lyft | L6 (Baidu·Wayve) | ~$8~10B | ~25x | C |
| AEVA | Aeva | L1 LiDAR | $500M~1B | n/a | C |
| MVIS | MicroVision | L1 LiDAR | $200~500M | n/a | C |
| HSAI | Hesai | L1 LiDAR (중국 1위) | ~$2B | ~20x | C (미·중) |
| INVZ | Innoviz | L1 LiDAR | $200M | n/a | C |
| LAZR | Luminar | L1 LiDAR | $300M | n/a | C |
| OUST | Ouster | L1 LiDAR | $500M | n/a | C |
| BIDU | Baidu | L3+L5+L6 (Apollo Go) | ~$30B | ~10x | C (지정학) |
| PONY | Pony.ai | L3 (중국·미국) | $1~2B | n/a | C (지정학) |
| CHPT | ChargePoint | L7 (충전) | $300M | n/a | C (변동성) |
| EVGO | EVgo | L7 (충전) | $300M | n/a | C (변동성) |
| DTRUY | Daimler Truck | L5 (Kodiak OEM) | ~€30B | ~10x | C 위성 |
| VLVLY | Volvo | L5 (Aurora OEM) | ~$60B | ~15x | C 위성 |
| CON.DE | Continental | L1+L3 (Aurora 협력) | ~€10B | ~10x | C 위성 |
| HEXA-B.ST | HEXAGON | L4 (geospatial) | ~SEK 100B | ~20x | C 간접 |

### 8.2 한국 종목 (Korea transmission)

| 티커 | 기업 | 영역 | 시총 | P/E | Tier |
|------|------|-----|-----|-----|------|
| **005380** | **현대차 (Hyundai Motor)** ★ next wave | Boston Dynamics 100% + Robotaxi (Waymo IONIQ 5 공급) + 미국 fab | **30~40조원** | **5~7x 극단 저평가** | **A 1순위 KR (next wave hidden alpha 1위)** |
| 012330 | 현대모비스 | L1+L2 부품 (현대차 그룹) | ~25조원 | ~6~8x | B 위성 |
| 204320 | HL만도 | L1 ADAS | ~3~5조원 | ~10x | B 위성 |
| 307950 | 현대오토에버 | L3 SW (Boston Dynamics 일부) | ~3조원 | ~25x | B 위성 |
| 012450 | 한화에어로스페이스 | L3 (방산 중복) | ~16~25조원 | ~15x | 방산 영역 중복 |

### 8.3 각 종목의 Valuation Gate

**Alphabet (GOOGL) — 1순위**
- Waymo 100%, $126B valuation
- 2026 EOY 1M weekly rides 목표
- Waymo IPO 2027~2028 catalyst
- **AI Foundation 영역과 통합 비중**
- **진입 전략**: AI Foundation 비중 일부로 카운트

**Mobileye (MBLY) — 2순위**
- EyeQ + SuperVision, 다중 OEM
- Intel spin-off 후 valuation 압축
- P/E ~25x — 저평가
- **진입 전략**: 즉시 분할 매수

**Uber (UBER) — 3순위 hidden alpha**
- Waymo·Aurora·WeRide 다중
- Q1 2026 GB $42.8B
- *이기는 partner 한 곳만 있으면 함께 이김*
- **진입 전략**: 즉시 분할 매수

**Aurora (AUR) — 4순위 신규 (Next Wave: 자율 트럭)**
- L4 트럭 sector leader
- Q1 2026 매출 $1M → EOY 2026 $80M run-rate (×80배 scale)
- Hirschbach 500 트럭 deal
- 7개 driverless 고객 (Berkshire 자회사 포함)
- Volvo·PACCAR·Continental 트럭 OEM 절반 lock-in
- EV $12.8B 시총, YTD +89%
- **단점**: 매출 대비 valuation 부담, cash burn $190-220M/q
- **진입 전략**: 분할 매수 (1~2%), Q2 2026 hardware kit 출시 시 가속

**Hyundai Motor (005380) — 1순위 KR 신규 (Next Wave Hidden Alpha 1위!)**
- **Boston Dynamics 100% 자회사** (2020 $1.1B 인수)
- Atlas 차세대 humanoid = *글로벌 top-tier*
- Robotaxi (Waymo IONIQ 5 공급) + 미국 fab + Boston Dynamics 4개 thesis 통합
- 시총 ~30~40조원, **P/E 5~7x 극단적 저평가**
- humanoid 노출 시총에 거의 미반영
- **본 deep dive next wave hidden alpha 1위**
- **진입 전략**: 분할 매수 2~3%, Boston Dynamics 매출 segment 공개 시 가속

**Kodiak (KDK) — 5순위 신규 (자율 트럭 #2)**
- 28 customer trucks Q1 2026
- 2026 EOY driverless launch 계획
- Bosch·Daimler·ZF 협력
- 변동성 큼
- **진입 전략**: 위성 0.5~1%

**PACCAR (PCAR) — 6순위 신규 위성**
- Aurora 트럭 OEM (Kenworth·Peterbilt)
- 미국 트럭 OEM 절반
- 시총 ~$50B, P/E ~15x, 안정 dividend
- **진입 전략**: 안정 위성 매수

---

## 9. 모니터링 트리거

**즉시 (분기)**
- Waymo weekly rides (200k → 500k → 1M) → P1
- Tesla Cybercab Apr 2026 양산 → P1
- Mobileye 분기 → P1
- Uber 분기 + Waymo·Aurora 매출 → P1
- **Aurora 분기 (매출·트럭·고객)** → P1
- **Kodiak 분기 (driverless launch)** → P1
- **Hyundai Motor 분기 (Boston Dynamics, 미국 fab)** → P1
- **Tesla Optimus Gen 3 분기 진척** → P1

**정책·M&A**
- NHTSA federal 표준 진척 → P1
- **Waymo IPO 발표 (2027~2028)** → P1 catalyst
- **Apptronik·Figure·1X IPO 시그널** → P1 catalyst
- 트럼프 자율 친화 정책 → P2
- 미·중 견제 강화 → P2

**기술**
- Tesla camera-only break-through → P1
- Waymo 도시 확장 (DC·NYC·Tokyo·London) → P1
- **Aurora 2세대 hardware kit Q2 2026 출시** → P1
- **Tesla Optimus Gen 3 Summer 2026 양산** → P1
- LiDAR 가격 추가 하락 → P2

**거시**
- 자동차 OEM L4 출시 → P3
- 미·중 자율 견제 → P2

---

## 10. 리스크

**기술**
- Tesla camera-only break-through (가능성 낮으나 Waymo·LiDAR 약화)
- Waymo·Tesla 큰 사고 (Cruise 식)
- LiDAR 가격 폭락 가속 (Hesai)
- Aurora·Kodiak 사고 시 자율 트럭 산업 backlash
- Humanoid 양산 일정 historically delay

**시장**
- 빅테크 (Alphabet) Waymo 시총 6% → 직접 반영 어려움
- Mobileye 회복 지연
- 자동차 OEM L4 자체 출시 → Waymo·MBLY 약화 가능
- **Aurora cash burn 가속** vs 매출 ramp 늦으면 capital raise
- Tesla 변동성 매우 큼 (Musk 영향)

**지정학**
- 미·중 견제 (Baidu·Pony·WeRide 미국 진입 차단)
- EU 인허가 보수
- 도시 별 인허가 차이

**본인 포트폴리오 — AI Foundation 중복**
- Alphabet = AI Foundation 핵심. *본 영역 중복*
- NVIDIA = AI Foundation·Vertical·광인터커넥트 다중
- **현대차 = AI 인프라가 아닌 별도 영역** (humanoid + automotive + EV + 미국 fab)
- 총 비중 관리

---

## 11. 매크로 변수 민감도

| 변수 | 영향 | 메커니즘 |
|------|------|--------|
| 트럼프 자율 친화 | + | NHTSA federal 가속, Musk 영향 |
| Fed 금리 인하 | + | 성장주 멀티플 (Aurora·Tesla·humanoid) |
| 미·중 갈등 | + | 중국 robotaxi 견제 → 미국 종목 수혜 |
| EV 보조금 폐지 | − | Tesla Cybercab 가격 부담, 일반 EV 충전 영향 |
| 자율주행 보험·법 표준화 | ++ | 산업 본격화 가속 |
| 도시 인허가 차이 | − | expansion 변수 |
| **K-방산·K-수출 호재** | + | 현대차 미국 fab + Robotaxi + humanoid 노출 |
| 한국 원화 강세 | − | 미국 종목 환차익 감소 |

---

## 12. 본인 의사결정 메모

### 최종 매수 우선순위 (Next Wave 반영)

**Tier A — 즉시 분할 매수**
1. **Alphabet (GOOGL)** — AI Foundation 통합 비중
2. **Mobileye (MBLY)** — 저평가 회복
3. **Uber (UBER)** — hidden alpha (다중)
4. **Aurora (AUR)** ← **Next wave 자율 트럭 1순위** (Q1 $1M → EOY $80M run-rate)
5. **Hyundai Motor (005380)** ← **Next wave KR hidden alpha 1위** (Boston Dynamics + 4개 thesis, P/E 5~7x)

**Tier A 위성**
6. **Kodiak (KDK)** ← 자율 트럭 #2
7. **PACCAR (PCAR)** ← Aurora 트럭 OEM, 안정

**Tier B**
8. Tesla (TSLA) — robotaxi 단독 약, *Optimus + 종합 thesis 별도*
9. 현대모비스, HL만도, 현대오토에버 — 한국 자율 부품 위성

### 비중 가이드 (AI Foundation 중복 + 별도 영역)

- 본 영역 전체: **포트폴리오의 5~10%** (자율주행만)
- Alphabet 은 AI Foundation 통합 (별도 1~2% 가산)
- **Hyundai Motor 는 별도 카테고리** (humanoid + EV + 자동차 + 미국 fab) — 2~3%
- Mobileye + Uber 각 1~2%
- Aurora 1~2%, Kodiak·PACCAR 위성 각 0.5~1%
- LiDAR·중국 robotaxi·한국 자율 부품 위성 합산 1~3%
- 충전 위성: 0~1%

### 진입 timing

- 즉시: Mobileye, Uber, Aurora, Hyundai Motor, PACCAR
- AI Foundation 비중 일부: Alphabet
- catalyst wait: Aurora Q2 2026 hardware kit, Waymo IPO 시그널 (2027~2028), Apptronik·Figure IPO
- 별도 thesis: Tesla (종합), Kodiak (변동성)
- 위성: LiDAR·충전

### 핵심 trade-off

- Pure-play (Alphabet) vs 부품 (Mobileye): Alphabet 직접 + 희석, Mobileye 다중 OEM + 회복
- Robotaxi (Uber) vs 트럭 (Aurora): Uber 안정 + 다중, Aurora 트럭 특화 + 변동
- Tesla vs Waymo: 본인 Waymo 우선
- 미국 vs 중국: 미·중 부담, 미국 중심
- **Humanoid 별도 영역으로 분리 검토** — Hyundai·Apptronik·Figure·Boston Dynamics 등 종합 분석 필요

### 본인 친숙도

- VC 검토 친숙 — Mobility·MaaS 트렌드 친숙
- 한국 자율 부품·Hyundai 그룹 친숙
- *Hyundai Motor 의 Boston Dynamics 통합 가치* 가 한국 시장에서 *덜 인지* 됨 — 본인 정보 비대칭 우위
- 미국 글로벌 robotaxi·자율 트럭 채택 매우 약한 한국 → 본인 미국 종목 중심 자연스러움

### Next Wave 모니터링 watchlist

- Apptronik (비상장 humanoid) — IPO
- Figure AI (비상장 humanoid) — IPO
- 1X (NEO) — IPO
- Agility Robotics — IPO
- Waymo (Alphabet 자회사) — IPO 2027~2028
- Wayve (영국) — IPO
- LiDAR 전종목 — 변동성 위성
- ChargePoint·EVgo — 위성

### Humanoid Robot 별도 영역 분리 검토
- 본 deep dive next wave 3 으로 포함했지만, **별도 deep dive 후보**
- 추후 작성 시: Hyundai·Tesla·NVIDIA·Apptronik·Figure·1X·Agility·Boston Dynamics·Unitree·Honor 종합

### Track 4 등재 후보

- Alphabet (GOOGL) — AI Foundation 통합
- Mobileye (MBLY) — 2순위
- Uber (UBER) — 3순위
- **Aurora (AUR) — 4순위 (next wave 자율 트럭)**
- **Hyundai Motor (005380) — 5순위 (next wave KR humanoid hidden alpha)**
- Kodiak (KDK) — 6순위 (변동성)
- PACCAR (PCAR) — 7순위 위성

---

## 13. 업데이트 로그

| 날짜 | 변경 |
|------|------|
| 2026-05-24 | 최초 작성 (Tier 1 깊이). TAM 4 + Moat 4 + Capital 3 = 11/15. 시차 A4 B5 C3 = +6 (Very strong entry). Tier 2 확정. 본문 매수 우선순위: GOOGL > MBLY > UBER. **Next Wave Deep (6.4·6.5) 추가**: (1) **자율 트럭 (Aurora AUR 1순위 — Q1 2026 $1M → EOY $80M run-rate, Hirschbach 500 트럭 deal, 7개 driverless 고객, EV $12.8B 시총 YTD +89%)**, (2) Fleet EV 충전 (ChargePoint·EVgo 변동성, 위성), (3) **Humanoid Robot (Hyundai Motor 005380 hidden alpha 1위 — Boston Dynamics 100% 자회사 + Robotaxi + 미국 fab 4개 thesis, P/E 5~7x 극단 저평가, Tesla Optimus Gen 3 Summer 2026, Apptronik $5B/$935M, Figure 02 BMW 11개월 30k+ vehicles, 1X $11B 협상)**. 매수 우선순위 업데이트: GOOGL > MBLY > UBER > **Aurora (신규)** > **Hyundai Motor (신규 KR hidden alpha)** > Kodiak > PACCAR. **Humanoid Robot 영역 별도 deep dive 분리 검토** — Hyundai·Tesla·NVIDIA·Apptronik·Figure·Boston Dynamics 종합. |


---

# ═══════════════════════════════════════════════════
# KR Transmission Boost — KR pure-play thorough 보강
# ═══════════════════════════════════════════════════

# 자율주행 / Robotaxi — KR Transmission Boost (v2.3 추가)

> **Base document**: autonomous-driving.md (2026-05-24 작성, 44KB)
> **Boost 작성일**: 2026-05-24
> **변경 사항**: KR pure-play thorough 보강 (K-자율 비상장 + 위성 추가)
> **본 문서**: 본 deep dive 의 *5.3 Sub-area 한국 부분 + 8.2 한국 종목* 보강

---

## 본 문서 적용 가이드

기존 autonomous-driving.md 의 5.3 Sub-area 7 (한국) + 8.2 한국 종목 표를 다음 thorough 보강으로 *교체*:

---

## 5.3 Sub-area 7: 한국 — *K-자율 thorough* (보강·교체)

> v2.3 KR transmission 강화. 기존 현대차·현대모비스 외에 **K-자율 비상장 (카카오모빌리티·라이드플럭스·서울로보틱스·포티투닷) + 부품·SW 위성 추가**.

### KR 상장 pure-play (기존 본문 매수)

| 티커 | 기업 | 영역 | 시총 | 핵심 thesis | Tier |
|------|------|-----|-----|----------|------|
| **005380** | **현대차** ★ | L2+L1 (Boston Dynamics + Robotaxi + 미국 fab + 자동차) | 30~40조원 | **P/E 5~7x 극단 저평가, 4개 thesis 통합 hidden alpha 1위** | **A KR 1순위** |
| **012330** | **현대모비스** | L3 자율 부품 (LiDAR·radar·MDPS·ADAS) | 18~22조원 | 현대차 자율 부품 + 글로벌 OEM 공급 | **A KR 2순위** |
| **000270** | **기아** | L2 자동차 + 자율 통합 | 35~45조원 | P/E 4~6x 저평가, 현대차그룹 통합 | **A KR 3순위** |
| **204320** | **HL만도** | L3 ADAS·자율 부품 | 2~3조원 | 자율 부품 (EPS·braking·sensor) 글로벌 OEM | **A KR 4순위** |
| **307950** | **현대오토에버** | L2 자율 SW (IVI·OTA·HD map) | 4~6조원 | 현대차 자율 SW + HD map | **A KR 5순위** |

### KR 상장 추가 종목 (보강)

| 티커 | 기업 | 영역 | 시총 | 핵심 thesis | Tier |
|------|------|-----|-----|----------|------|
| **214330** | **HL디앤아이한라** | L3 자율 부품 (HL Klemove cross) | 5,000~7,000억원 | HL그룹 자율 부품 | **B KR 위성** |
| **011210** | **현대위아** | L3 자율 부품 (CV joint·gear·sensor) | 1~1.5조원 | 자율 부품 (구동 시스템) | **B KR 위성** |
| **272210** | **한화시스템** | L2 자율 + 위성·전자전 | 3조원 | K-방산 + 자율 위성 cross | K-방산 cross |
| **403870** | **SK 일렉링크** | L3 EV 충전 + 자율 cross | 1,000~1,500억원 | EV 충전 인프라 (자율 cross) | C KR 위성 |
| **161390** | **한국타이어앤테크놀로지** | L3 자율 타이어 (sensor·smart) | 4~5조원 | 자율 smart 타이어 | C KR 위성 (변동성) |
| **058470** | **리노공업** | L3 자율 senser 부품 (camera·LiDAR cross) | 5~7조원 | 자율 sensor 부품 (반도체 cross) | B 반도체 cross |
| **323940** | **인포뱅크** | L3 자율 SW (IVI·infotainment) | 1,000~1,500억원 | 자율 SW vendor | C KR 위성 |
| **042040** | **HL홀딩스** | L4 HL그룹 지주 (HL만도·HL D&I·HL Klemove) | 1~1.5조원 | HL그룹 자율 통합 노출 | B KR 위성 |
| **006400** | **삼성SDI** | L3 자율 battery (EV cross) | 20~22조원 | 자율 EV battery | EV 영역 cross |
| **373220** | **LG에너지솔루션** | L3 자율 battery (EV cross) | 90~100조원 | 자율 EV battery | EV 영역 cross |
| **003580** | **넥스트사이언스** | L2 자율 신생 (소형 변동성) | 1,500~2,500억원 | 자율 신생 | C 변동성 |

### KR 비상장 / IPO 후보 — *본인 정보 비대칭 우위 핵심*

| 비상장 | 영역 | 펀딩·valuation | IPO 가능성 |
|---------|------|------------|---------|
| **카카오모빌리티 (Kakao Mobility)** ★ | L2 robotaxi·mobility platform (Kakao T) | 카카오 51%, 글로벌 PE 49% (대주주 분쟁) | IPO 추진 중 (2026~2027 시그널) |
| **포티투닷 (42dot, 현대차 자회사)** ★ | L1 자율 SW · AI Foundation Model · μWay | 현대차 100% (2022 4,277억원 인수) | 자회사 → 별도 IPO 가능성 |
| **라이드플럭스 (RideFlux)** ★ | L1 자율주행 SW · 제주 robotaxi 운영 | KT·SK 등 다중 backed | IPO 시그널 |
| **서울로보틱스 (Seoul Robotics)** | L1 자율 perception (LiDAR-based) | $50M+ 누적, BMW·Volvo deal | IPO 시그널 |
| **모셔널 (Motional, 현대차-Aptiv JV)** | L1 robotaxi platform | 현대차 50% + Aptiv 50% | IPO 가능성 낮음 (JV) |
| **소네트 (Sonnet AI)** | L1 자율 SW (한국 신생) | 다중 | n/a |
| **에이아이코퍼스 (AICorpus)** | L1 자율 데이터 라벨링 | 다중 | n/a |

### KR 정책 trigger

- **현대차그룹 미국 fab + Boston Dynamics + 자율 통합 strategy** = 본인 *4 thesis 통합 hidden alpha 핵심*
- **포티투닷 → 현대차 통합** (2022) = 자율 SW + AI Foundation Model 자체 개발
- **카카오모빌리티 IPO** = K-robotaxi 직접 노출 catalyst
- **한국 자율주행 임시운행 허가 정책** = 제주·세종·판교 등 robotaxi 시범 (라이드플럭스·소네트 진출)
- **K-자율 정부 R&D** = 다중 startup 지원

### 진입 전략 (KR 우선순위 업데이트)

- **KR 1순위: 현대차 (005380)** — *4 thesis hidden alpha*, 자율 + Boston Dynamics + 미국 fab + 자동차
- **KR 2순위: 현대모비스 (012330)** — 자율 부품
- **KR 3순위: 기아 (000270)** — 현대차그룹 통합
- **KR 4순위: HL만도 (204320)** — ADAS 부품
- **KR 5순위: 현대오토에버 (307950)** — 자율 SW
- **KR 위성**: HL디앤아이·HL홀딩스·현대위아·인포뱅크·리노공업
- **EV cross**: 삼성SDI·LG에너지 = EV 영역에서 매수
- **K-방산 cross**: 한화시스템 = K-방산에서 매수

### 비상장 IPO 모니터링 ★ 본인 정보 비대칭 우위 활용

- **카카오모빌리티 IPO** (2026~2027 시그널) → catalyst 가장 큼
- **포티투닷 IPO** (현대차 자회사 별도 IPO 가능성) → catalyst
- **라이드플럭스 IPO** (제주 robotaxi 운영) → catalyst
- **서울로보틱스 IPO** (BMW·Volvo deal) → catalyst

---

## 8.2 한국 종목 — *thorough 보강 (교체)*

| 티커 | 기업 | 영역 | 시총 | P/E | Tier | 매수 우선순위 |
|------|------|-----|-----|-----|------|-----------|
| **005380** | **현대차** ★ | L2+L1 자율+humanoid+미국 fab+자동차 | 30~40조원 | **5~7x** | **A** | **KR 1순위 hidden alpha** |
| **012330** | **현대모비스** | L3 자율 부품 (LiDAR·radar·ADAS) | 18~22조원 | ~7x | **A** | **KR 2순위** |
| **000270** | **기아** | L2 자동차 + 자율 | 35~45조원 | 4~6x | **A** | **KR 3순위 (저평가)** |
| **204320** | **HL만도** | L3 ADAS·EPS·braking | 2~3조원 | ~10x | **A** | **KR 4순위** |
| **307950** | **현대오토에버** | L2 자율 SW + HD map | 4~6조원 | ~25x | **A** | **KR 5순위** |
| 042040 | HL홀딩스 | L4 HL그룹 지주 | 1~1.5조원 | n/a | **B** | KR 위성 통합 |
| 214330 | HL디앤아이한라 | L3 자율 부품 | 5,000~7,000억원 | n/a | **B** | KR 위성 |
| 011210 | 현대위아 | L3 자율 구동 부품 | 1~1.5조원 | n/a | **B** | KR 위성 |
| 058470 | 리노공업 | L3 자율 sensor 반도체 cross | 5~7조원 | ~30x | **B** | 반도체 cross |
| 323940 | 인포뱅크 | L3 자율 SW (infotainment) | 1,000~1,500억원 | n/a | C | KR 위성 |
| 161390 | 한국타이어 | L3 자율 smart 타이어 | 4~5조원 | n/a | **C** | KR 위성 변동성 |
| 006400 | 삼성SDI | L3 EV battery | 20~22조원 | n/a | B | EV cross |
| 373220 | LG에너지솔루션 | L3 EV battery | 90~100조원 | n/a | B | EV cross |

### 비상장 IPO 모니터링
- **카카오모빌리티** — IPO 2026~2027
- **포티투닷 (42dot)** — 현대차 자회사
- **라이드플럭스 (RideFlux)** — 제주 robotaxi
- **서울로보틱스 (Seoul Robotics)** — BMW·Volvo deal
- **모셔널 (Motional)** — 현대차-Aptiv JV
- **소네트 (Sonnet AI)** — 한국 신생

---

## 12 비중 분배 권장 (KR 보강 반영)

### 글로벌:KR 비중 분배 권장

- **글로벌 70% : KR 30%** (기존 본문 유지)
- 본인 *현대차 4 thesis hidden alpha 핵심*
- 종목별:
  - GOOGL (Waymo) 1~2%, MBLY 0.5~1%, UBER 1~2%, Aurora 0.5~1%, KDK 0.3%, PCAR 0.5%
  - 현대차 2~3% (KR 1순위), 현대모비스 0.5~1%, 기아 0.5~1%, HL만도 0.3~0.5%, 현대오토에버 0.3~0.5%
  - HL홀딩스·디앤아이·현대위아·인포뱅크 위성 합산 0.5%

### Cross-area 중복 카운트
- **현대차** = 자율 + humanoid (Boston Dynamics) cross → 본 영역에서 매수, humanoid 영역 위성
- **삼성SDI·LG에너지** = EV battery → EV 영역에서 매수
- **한화시스템** = K-방산 cross → K-방산에서 매수

---

## 업데이트 로그 — KR Boost (v2.3 추가)

| 날짜 | 변경 |
|------|------|
| 2026-05-24 | **KR transmission boost retrofit**. K-자율 thorough 보강: 비상장 IPO watchlist 추가 (**카카오모빌리티·포티투닷·라이드플럭스·서울로보틱스·모셔널·소네트·AICorpus**). KR 상장 추가: HL디앤아이·HL홀딩스·현대위아·인포뱅크·리노공업·한국타이어 등 위성. KR 매수 우선순위 확정: 현대차 (1) > 현대모비스 (2) > 기아 (3) > HL만도 (4) > 현대오토에버 (5) > HL/현대 위성. **카카오모빌리티 IPO (2026~2027), 포티투닷 별도 IPO 가능성, 라이드플럭스, 서울로보틱스** = K-자율 비상장 IPO catalyst watchlist 강조. |

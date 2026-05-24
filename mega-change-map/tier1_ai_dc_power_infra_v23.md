# AI 데이터센터 전력 인프라 — Tier 1 Deep Dive

> **Sample / 실제 사용 예시**: 백지 메가 체인지 맵에서 Tier 1으로 올라온 영역.
> 본인이 평소 깊게 안 보셨을 영역을 의도적으로 선택. methodology.md 의 모든 룰을 실제 적용한 결과물.
> 작성일 기준 최신 데이터 (2026년 5월 중순)로 채움.

---

## 0. 메타 정보

| 항목 | 값 |
|------|----|
| 작성일 | 2026-05-23 |
| 최근 갱신 | 2026-05-23 |
| 다음 정기 갱신 | 2026-07-01 (분기 첫 주) |
| 시계 분류 | Core (1.5~2.5년) |
| Tier | 1 (Deep) |
| Confidence (총점) | Medium (Capital High, Tech Medium, 시장 추정치 Medium) |
| 트랙 | L1A (Global) + Korea transmission 강함 |

---

## 1. 한 줄 요약 + 핵심 가설

### 한 줄 요약
> 빅테크 AI CapEx 650B$+/년이 GPU에서 전력 인프라로 옮겨붙으면서, **변압기·스위치기어·송배전망**이 진짜 병목이 됐다. 미국 데이터센터 12GW 중 5GW만 착공, 나머지는 5년 변압기 리드타임에 막혀 정체. 한국 변압기 3사 (효성·HD현대·LS) 가 미국 수출 직접 수혜.

### 핵심 가설

- **가설 A**: AI CapEx 사이클이 GPU 단계를 넘어 *그 GPU를 돌릴 전력*으로 옮겨가는 변곡. 컴퓨트 자체보다 그 후방 인프라가 더 오래·확실하게 성장.
- **가설 B**: 미국 전력망 자체가 노후 + AI 신규 수요까지 겹쳐 구조적 부족. 5년 변압기 리드타임은 단기 해소 불가. **공급자 우위 시장이 향후 2~3년 지속**.
- **가설 C**: 미국 내 변압기 생산 capa 확충은 시간 걸려서 수입 의존. 한국·캐나다·멕시코가 주 수입처. 한국 기업이 미국 변압기 시장 capa 증설 중이라 점유율 확대 기회.
- **가설 D**: 데이터센터가 송배전 한계로 인해 "BYOP (Bring Your Own Power)" 모델로 전환 — 사내 발전기·가스터빈·SMR 직결. GE Vernova 가스터빈, 나아가 원자력으로 자금 흐름 확장.

### 기각 조건
- 빅테크 합산 AI CapEx 가이던스 분기 기준 20%+ 하향 (단순 하향은 아님)
- 미국 변압기 자국 capa 폭증 (정책 자금으로 단기 해소)
- AI 모델 효율 혁신으로 전력 수요 폭증 가설 무력화 (예: 추론 전력 효율 ×10 이상 개선)
- 미국 데이터센터 신규 착공 분기 추세 30% 이상 감소 (2분기 연속)

---

## 2. 4가지 잣대 채점

### 잣대 1: TAM

| 항목 | 값 |
|------|----|
| 점수 | 4 / 5 |
| 카테고리 | Major expansion |
| Confidence | High |

**근거**:
- IEA: 글로벌 데이터센터 전력 수요 2025년 485 TWh → 2030년 ~950 TWh (×2배) — 1차 소스 ✅
- 미국 변압기 시장: 2024년 122억$ → 2034년 257억$ (CAGR 7.7%) — 1차 소스 (Wood Mackenzie 인용)
- 더 넓게 보면 전력 인프라 전체 (변압기·스위치기어·HV 케이블·배터리·가스터빈·BESS) 합산 시장은 1T$+ 규모
- 미국 데이터센터 전력 수요만 2023년 4GW → 2030년 84GW (×21배, CSIS 추정) — 데이터센터 전력 한정 시 ×10 이상

**해석**:
- 변압기 단독으로는 ×2 수준이라 4점 (Major)
- 데이터센터 전력 한정 시 ×21이라 5점 가능
- 보수적으로 4점. 전력 인프라 전체로 보면 5년 ×3~10 확실.

### 잣대 2: Moat (해자 재편 + 비가역성)

| 항목 | 값 |
|------|----|
| 점수 | 4 / 5 |
| Confidence | High |

**근거**:
- 변압기 글로벌 강자: 중국 (TBEA, China XD Group 등 합산 60% 점유) + 미국 GE/Eaton + 유럽 Siemens Energy/Hitachi Energy + 한국 효성·HD현대
- 미국 시장에서는 중국산 의존도 증가 (2022년 1,500대 → 2025년 8,000대, ×5)
- 그러나 미국 안보 우려로 중국 의존 줄이려는 압력 → 한국·캐나다·멕시코로 이전
- **Moat 재편 진행 중**: 미국이 자국 capa 충당 못해서 동맹국 (한국 중심) 으로 의존 구조 재편. 5년 시계에서 한국 기업 점유율 ×2 가능성.

**비가역성 평가** (2026-05-23 통합 후 추가):
- 미국 자국 capa 증설 (Eaton 1.2B$, GE Vernova) 의 효과는 2027~2028. 그 사이 의존 구조는 굳어짐.
- 한국 기업의 미국 공장 capa 증설 (효성 멤피스 ×2, HD현대 앨라배마 1850억) 은 sunk cost. 되돌리려면 비용 폭발.
- 5년 변압기 리드타임 = 발주 후 5년간은 변경 불가. 구조적 lock-in.
- **비가역성 강함**. 5년 시계에서 한국 기업이 미국 변압기 시장 점유율 확대는 사실상 되돌리기 어려움.

**해석**:
- 기존 강자 (서구) 의 한계 + 신규 강자 (한국) 의 부상 동시 진행. 변화 비가역적.
- 마진 구조 재편: 변압기 ASP 상승 (장기 공급 부족), 한국 기업 매출 ×2 수준
- 4점 (Major reshuffle + 비가역 강), 5점은 아님 (완전 도태가 아니라 점유율 이동)

### 잣대 3: Capital

| 항목 | 값 |
|------|----|
| 점수 | 5 / 5 |
| Confidence | High |

**근거** (출처 명시):
- 빅테크 4사 (Alphabet, Amazon, Meta, Microsoft) 2026 AI CapEx 합계: ~650B$+ (Bloomberg)
- 이 중 전력 인프라 직접 투입 추정: 100~150B$ (CapEx의 15~20%, 산업 추정)
- 미국 정부 정책 자금: DOE 변압기 capa 보조금 (수십억$ 규모, 미미)
- 한국 정부: K-전력기기 산업 육성 지원
- ETF AUM: AIPO ETF (Defiance AI & Power Infrastructure) 출시 9개월 만에 300M$+ — 빠른 자금 유입 시그널
- **합계**: 연 100~150B$ (전력 인프라 직접 투입분)

**중복 카운트 확인**: 빅테크 CapEx의 전력 인프라 부분과 정부 정책 자금은 중복 없음. ETF AUM은 시장 가격에 이미 반영된 후속 시그널이므로 별도 카운트 안 함.

**해석**:
- 100B$+ 수준이면 잣대 3점 (30~100B$) 와 4점 (100~500B$) 사이
- 단, 빅테크 CapEx 전체 (650B$) 가 결국 전력 인프라 없이는 못 돌아가므로 **간접적으로 전체가 이 영역의 자본 유입**
- 보수적 4점부터 적극 5점까지 가능. **5점** (연 500B$+ 간접 포함) 부여, Confidence High.

### ~~잣대 4: Tech~~ (폐기)

> Tech 잣대는 2026-05-23 폐기. 비가역성은 Moat에 흡수, 성숙도는 B 지표(실물 변화)에서 측정. 본 영역의 기술 변화 (HVDC, SST, BYOP) 는 위 Moat 비가역성 평가와 아래 B 지표에 통합됨.

### 합산

| 트랙 | 합산 점수 | 통과 임계 | Tier 1 임계 |
|------|---------|---------|-----------|
| L1A | **13 / 15** | ≥ 9 ✅ | ≥ 12 ✅ |

**영역 전체 Confidence**: High (모든 잣대 High)

→ Tier 1 승급 조건 (12점 이상) 충족. **Tier 1 유지**.

> **재채점 비교** (Tech 잣대 폐기 전 후):
> - 기존: TAM 4 + Moat 4 + Capital 5 + Tech 3 = 16 / 20 (Conf. Medium, Tech가 약점)
> - 신규: TAM 4 + Moat 4 + Capital 5 = 13 / 15 (Conf. High)
> - 결론 동일 (Tier 1 유지). 다만 Confidence 가 Medium → High 로 상승. 채점이 더 정직해짐.

---

## 3. A·B·C 시차 평가

### A 지표 (자본 유입)
| 항목 | 값 |
|------|----|
| 점수 | **5 / 5** (정점 진입 중) |
| 갱신일 | 2026-05-23 |

**근거**:
- 빅테크 CapEx 가이던스: 2025 400B$ → 2026 650B$ (75% 증가). 가속 페이즈.
- VC 펀딩: AI 인프라 (전력·냉각·BMS) 영역 시리즈 B~C 라운드 분기 다수
- ETF AUM: AIPO ETF 9개월 만에 300M$+
- 핵심 종목 backlog: GE Vernova 150B$ (Q1 2026, +13B$ q/q), Vertiv 15B$ (+109% YoY)

→ 자본은 이미 정점 가까이. 5점.

### B 지표 (실물 변화)
| 항목 | 값 |
|------|----|
| 점수 | **3 / 5** (진행 중, 절반 못 미침) |
| 갱신일 | 2026-05-23 |

**근거**:
- 미국 데이터센터 2026 계획 12GW 중 5GW만 착공 (40%). 나머지 7GW는 전력 인프라 부족으로 정체.
- 변압기 리드타임 5년: 2026년 발주분이 2031년 인도. 실물 변화는 2026~2027 약하고, 2027~2029 본격화.
- Eaton 2026 organic 성장률 가이던스 9~11%. GE Vernova 2026 매출 가이던스 41~42B$ (전년 대비 강세).
- 한국 변압기 3사 수주잔고 합산 33조원+ (5년치 일감)
- **실물은 막 따라오기 시작. 절반 못 미침.** 3점.

### C 지표 (가격 반영)
| 항목 | 값 |
|------|----|
| 점수 | **4 / 5** (상당 부분 반영) |
| 갱신일 | 2026-05-23 |

**근거**:
- GEV (GE Vernova): YTD +55%, P/E (TTM) ~31x, Forward P/E ~37x, 시총 282B$
- ETN (Eaton): Forward P/E ~28x, 2026 EPS 가이던스 13.05~13.50$
- VRT (Vertiv): Forward P/E ~35x, 2026 매출 가이던스 13.5~14.0B$
- PWR (Quanta): Forward P/E ~32x
- 한국: HD현대일렉트릭 2025 영업이익 +36%, 효성중공업 +46%, LS일렉트릭 +21% (컨센서스). 주가는 이미 상당 반영
- AIPO ETF YTD +30% (2026.1~4)

→ 가격 상당 반영. 단, 메가 체인지 영역 멀티플 (PER 35~50배) 기준으론 아직 과열까진 아님. 4점.

### 시차 매력도 = A + B − C

| 항목 | 값 |
|------|----|
| 계산 | 5 + 3 − 4 = **4** |
| 카테고리 | **Good entry** |

**해석**:
- 자본은 들어왔고 (A=5), 실물은 막 시작 (B=3), 가격은 상당 반영 (C=4)
- 진입 황금기는 아니지만 **여전히 매력적**. B가 본격화되는 2027년까지 매수·보유 후 청산 검토.
- 핵심: B → 4점으로 올라갈 때 (2027년 분기 실적·수주 추이로 확인) 까지 보유, 그 시점에 C가 5점으로 가면 청산.

---

## 4. 산업 메가트렌드 (Step 1)

### 4.1 수요 측
- **AI 데이터센터 전력 수요 폭증**: 미국 데이터센터 전력 2023년 4GW → 2030년 84GW (×21배)
- 글로벌 데이터센터 전체 전력 수요 2025 485 TWh → 2030 950 TWh (×2)
- 미국 전체 전력 수요 중 데이터센터 비중: 2025년 3~4% → 2028년 10% 도달 전망
- 추가 수요원: EV, 전기난방, 산업 전기화 — 데이터센터 외에도 그리드 부하 증가
- **구조적**. 사이클 아님. AI 사이클이 둔화돼도 그리드 노후 교체 수요 자체가 ×2 수준.

### 4.2 공급 측
- 미국 변압기 capa 부족 심각. 자국 생산 미달.
- 고압 변압기 리드타임: 2020년 24~30개월 → 2026년 60개월 (5년)
- 자국 capa 증설 진행 중이나 시간 걸림 (3~5년)
- 수입 의존 증가: 캐나다·멕시코·**한국** 중심
- 중국산 수입도 폭증 (1,500대 → 8,000대) 하지만 안보 이슈로 제한 가능성
- **공급 부족 2~3년 지속 확실**

### 4.3 정책·지정학 변수
- 미국 DOE 변압기 자국 capa 보조금 (규모 미미)
- 데이터센터 신규 인허가 지연 (커뮤니티 반대)
- 미중 갈등 → 중국산 전력 인프라 의존 줄이려는 정책 압력
- 한국·미국 동맹 구조에서 한국 기업 capa 증설은 정책 우호
- **한국 변압기 미국 수출은 정책적 우호 + 수요 폭증의 이중 수혜**

---

## 5. 밸류체인 매핑 (Step 2)

### 5.1 다이어그램
```
[발전 (Generation)]
   ├─ 원자력 (기존 + SMR, 별도 영역)
   ├─ 가스터빈 (GE Vernova, Siemens Energy)
   ├─ BESS (배터리 저장)
   └─ 재생에너지
        ↓
[송전 (Transmission, HV)]
   ├─ HV 변압기 ★ 핵심 병목 (효성·HD현대·GE/Eaton)
   ├─ HVDC 시스템 (Hitachi Energy, 효성, ABB)
   ├─ HV 스위치기어 (Eaton, Siemens, 한국 3사)
   └─ HV 케이블
        ↓
[배전 (Distribution, MV/LV)]
   ├─ MV 변압기
   ├─ MV 스위치기어
   ├─ UPS (Vertiv, Schneider)
   └─ 배전 자동화
        ↓
[데이터센터 내부 (DC Power)]
   ├─ PDU (Power Distribution Unit) (Vertiv)
   ├─ Rack PSU (Delta, Vertiv)
   ├─ 액침 냉각·D2C 냉각 (Vertiv, CoolIT)
   └─ BYOP 발전 (가스터빈·BESS·미래 SMR)
        ↓
[그리드 시공 (EPC)]
   └─ Quanta Services, MasTec
```

### 5.2 레이어별 분석

| 레이어 | 마진 수준 | 경쟁 강도 | 중국 침투 | 진입장벽 |
|--------|---------|---------|---------|---------|
| HV 변압기 (765kV급) | **매우 높음** (공급 부족) | 낮음 (글로벌 5~10개사) | 일부 침투, 안보 견제 | 기술+자본+인증 (UL) |
| HVDC | 높음 | 낮음 (글로벌 3~4개사) | 거의 없음 | 기술 |
| HV 스위치기어 | 높음 | 중간 | 일부 | 인증 |
| MV 변압기·스위치기어 | 중간 | 높음 | 큼 | 자본 |
| UPS·PDU | 중간 | 높음 | 큼 | 채널 |
| EPC | 중하 | 높음 | 거의 없음 (현장) | 인력·현지 라이선스 |
| 가스터빈 | 매우 높음 | 매우 낮음 (GE·Siemens 과점) | 거의 없음 | 기술 |

### 5.3 하위 세분화 (Sub-areas)

#### Sub-area 1: HV 변압기 (★ 핵심 병목)
- 정의: 765kV / 345kV 급 초고압 변압기. 데이터센터·송전망 핵심
- 핵심 플레이어: GE Vernova (Prolec), Eaton, Siemens Energy, Hitachi Energy, 효성중공업, HD현대일렉트릭, LS일렉트릭, 산일전기 (한국 신생)
- 현재 매력도: **최상**. 5년 리드타임, 공급자 절대 우위.

#### Sub-area 2: HVDC (초고압 직류송전)
- 정의: 장거리 송전 + 재생에너지·해상풍력 연결
- 핵심: Hitachi Energy, GE Vernova, Siemens Energy, ABB, 효성중공업 (전압형 HVDC 독자)
- 매력도: 높음. 신규 시장 형성 단계.

#### Sub-area 3: 스위치기어 (HV/MV)
- 정의: 차단기·계전기·배전반
- 핵심: Eaton, Schneider, Siemens, ABB, 한국 3사
- 매력도: 중상. 변압기만큼 병목은 아니지만 동반 수혜.

#### Sub-area 4: UPS / PDU / DC Power
- 정의: 데이터센터 내부 전력 분배·백업
- 핵심: Vertiv, Schneider, Delta Electronics, ABB
- 매력도: 중상. AI 인프라 직결.

#### Sub-area 5: 가스터빈 + BYOP 발전
- 정의: 데이터센터용 사내 발전 (그리드 우회)
- 핵심: GE Vernova, Siemens Energy, Mitsubishi Heavy
- 매력도: 높음. BYOP 트렌드 직접 수혜. **하이퍼스케일러 PPA 직접 체결 사례 증가**.

#### Sub-area 6: 그리드 EPC
- 정의: 송배전망 설계·시공
- 핵심: Quanta Services (PWR), MasTec
- 매력도: 중상. 미국 그리드 확충 시공 직접 수혜.

#### Sub-area 7: 데이터센터 냉각 (별도 영역으로 분리 가능)
- 액침 냉각·D2C 냉각
- 핵심: Vertiv, CoolIT (PE), Asetek
- 매력도: 중. 전력 인프라와는 별개 영역으로 다루는 게 더 정밀할 수 있음.

---

## 6. 병목 식별 (Step 3)

### 6.1 현재 병목
- **HV 변압기 (765kV/345kV)**: 5년 리드타임, 미국 자국 capa 부족
- 누가 쥐고 있나: GE Vernova (Prolec), Eaton, 효성중공업, HD현대일렉트릭, Hitachi Energy
- 얼마나 오래: 2~3년 지속 확실. 자국 capa 증설 (Eaton 1.2B$, GE Vernova) 효과는 2027~2028 부터.

### 6.2 다음 병목 ★ 투자 핵심
- **그리드 자체 (transmission line, substation)**: 변압기 해결돼도 송전선 건설이 더 느림 (인허가·환경규제·5~10년)
- **BYOP 발전 (가스터빈, BESS, 추후 SMR)**: 그리드 못 기다린 하이퍼스케일러가 자체 발전으로 우회
- **숙련 노동력**: 송배전 EPC 인력 부족 (Quanta 등 수혜)
- **HV DC 송전**: 장거리·재생에너지 연결 수요로 향후 5년 카테고리 형성

→ 본인 선제 포지셔닝 후보: **가스터빈 (GEV) + BYOP 솔루션 + 그리드 EPC (PWR) + HVDC**

### 6.3 컨센서스 vs 본인 뷰의 갭
- 시장이 현재 보고 있는 것: 변압기 부족 → 변압기 제조사 수혜. 일부 반영됨.
- 본인이 추가로 보고 있는 것:
  - BYOP가 단순 임시 우회가 아니라 **새 표준**이 될 가능성. 데이터센터-발전 직결 모델.
  - 한국 변압기 3사가 미국 점유율 ×2 시나리오 (캐나다·멕시코보다 한국이 capa·기술 우위)
  - 그리드 EPC (Quanta) 의 long-tail 수혜 — 변압기 다음 병목
- 갭의 크기: 중간. 시장이 모르는 건 아니나, BYOP·Korean exporters의 점유율 확대 정도는 아직 다 반영 안 됨.

---

## 7. 자금 흐름 시그널 (Step 4)

### 7.1 관련 ETF
| ETF 티커 | 시장 | 영역 노출도 | 비고 |
|---------|------|---------|------|
| AIPO | US | 직접 (전용 ETF) | Defiance AI & Power Infra, 9개월 300M$+ |
| GRID | US | 부분 | 그리드 인프라 |
| PAVE | US | 부분 | 미국 인프라 전반 |
| XLU | US | 부분 | 유틸리티 (발전사 중심) |

### 7.2 추적 지표 (대시보드)
- [ ] 빅테크 CapEx 가이던스 (분기) — Alphabet/Amazon/Meta/Microsoft
- [ ] 미국 데이터센터 신규 착공 (Sightline Climate 분기)
- [ ] 변압기 리드타임 추이 (Wood Mackenzie 보고서)
- [ ] 핵심 종목 backlog (GEV, ETN, VRT, PWR) 분기
- [ ] 한국 중대형 변압기 수출 통계 (관세청 월간 — moneyrecipe.blog 등)
- [ ] AIPO ETF AUM 변화

### 7.3 Startup Landscape (L2 신호)

최근 12개월 주요 라운드 (전력·BYOP·BESS·SST 영역):
- (구체 라운드는 시스템 운영 시 채움. Crunchbase·The Information 활용)

**시그널 해석**:
- 상장사 중 수혜: GEV, ETN, VRT, PWR, 한국 변압기 3사
- 위협받는 상장사: 일부 전통 유틸리티 (BYOP 우회 시) — 단, 유틸리티는 별도 영역

---

## 8. 종목 매핑 (Step 5)

### 8.1 글로벌 종목

| 티커 | 기업명 | 밸류체인 위치 | Sub-area | 핵심 매수 논리 | 비고 |
|------|-------|------------|---------|-------------|------|
| GEV | GE Vernova | 발전 + 변압기 + HVDC | 1, 2, 5 | Q1 2026 데이터센터 주문 단일 분기에 2025 전체 초과. backlog 150B$. 가스터빈 + 변압기 + HVDC 수직통합 | 5월 기준 YTD +55%, Forward P/E 37x |
| ETN | Eaton | 스위치기어 + 변압기 + 액침냉각 | 1, 3, 7 | Electrical Americas Q1 2026 매출 3.6B$, backlog +44% YoY. Boyd Thermal 인수로 냉각까지 확장 | Forward P/E 28x |
| VRT | Vertiv | 데이터센터 내부 전력·냉각 | 4, 7 | backlog 15B$ (+109% YoY), 2026 매출 가이던스 13.5~14.0B$. 액침 냉각 직접 수혜 | Forward P/E 35x |
| PWR | Quanta Services | 그리드 EPC | 6 | 그리드 시공 absolute leader. 다음 병목 (송전선) 의 직접 수혜 | Forward P/E 32x |
| HUBB | Hubbell | 전력 부품 | 3 | 배전 부품 강자. 변동성 낮음 | |
| AEIS | Advanced Energy | DC power | 4 | 데이터센터 내부 전력. AI 비중 증가 중 | |

### 8.2 한국 종목 (Korea transmission)

| 티커 | 기업명 | 밸류체인 위치 | Sub-area | 핵심 매수 논리 | 비고 |
|------|-------|------------|---------|-------------|------|
| 298040 | 효성중공업 | HV 변압기 + HVDC | 1, 2 | 미국 멤피스 공장 capa ×2 증설. HVDC 국내 최초 독자개발. 2025 영업이익 +46%. 수주잔고 13.85조원. | |
| 267260 | HD현대일렉트릭 | HV 변압기 | 1 | 앨라배마 공장 1,850억 추가 투입 2027 가동. 미국 수출 비중 40%, 누적 수주 19.2억$. | |
| 010120 | LS일렉트릭 | HV/MV 변압기 + 스위치기어 | 1, 3 | 텍사스 배스트럽 캠퍼스 준공. KOC전기 인수로 capa 확대. | |
| 062040 | 산일전기 | 중대형 변압기 (신생) | 1 | 신규 진입, capa 확장 중. 미·중 시장 동시 노출 가능성. | 검증 필요 |

### 8.3 각 종목의 Valuation Gate
각 종목은 `valuation-gates/[ticker].md` 에 별도 채점. 다음 단계.

---

## 9. 모니터링 트리거

- [ ] **GEV / ETN / VRT / PWR 분기 실적** — backlog 변화, 가이던스 → P3 (강한 변동 시 P2)
- [ ] **빅테크 4사 CapEx 가이던스 변경** ±10% 이상 → P1
- [ ] **미국 변압기 리드타임 변화** (Wood Mackenzie 보고서) — P2
- [ ] **한국 변압기 3사 분기 실적·수주** — P3 (강한 변동 시 P2)
- [ ] **한국 중대형 변압기 월별 수출** (관세청) — P3 트래커
- [ ] **AIPO ETF AUM·자금흐름** 월간 — P3 트래커
- [ ] **미국 정부 변압기 자국 capa 정책** 발표 — P1
- [ ] **중국 변압기 수출 통계** 분기 — P3 (한국 경쟁 강도 시그널)
- [ ] **하이퍼스케일러 BYOP 신규 발표** (PPA, SMR 직결 등) → P2

---

## 10. 리스크

- **AI CapEx 사이클 둔화** (가장 큰 리스크) — 빅테크 분기 가이던스 지속 모니터링. 20%+ 하향 시 기각 조건.
- **AI 모델 효율 혁신** (예: DeepSeek류 효율 ×10) — 전력 수요 가설 약화. 다만 인퍼런스 수요 자체가 폭증해서 상쇄 가능성.
- **미국 변압기 자국 capa 폭증** — 정책 자금으로 가속화 시 한국 수출 매력 약화. 다만 3~5년 걸리는 작업.
- **중국 변압기 수출 추가 폭증** — 한국 점유율 위협. 미중 갈등으로 견제되는 중.
- **데이터센터 인허가 지연 누적** — 신규 착공 자체가 더 줄면 변압기 발주 자체가 감소.
- **금리 변동** — 인프라 기업 멀티플 민감.

---

## 11. 매크로 변수 민감도

| 매크로 변수 | 영역 영향 | 메모 |
|-----------|---------|------|
| 원/달러 강세 | **+** (한국 변압기 수출 마진 ↑) | 한국 종목 수익 직접 ↑ |
| 원/달러 약세 | − (한국 변압기 마진 ↓) | 미국 종목엔 영향 적음 |
| Fed 금리 인하 | + (인프라 기업 멀티플 ↑) | 단, 본 영역은 수요 자체가 강해 금리 민감도는 일반보다 낮음 |
| 미중 갈등 심화 | + (한국 기업 점유율 확대 + 중국산 견제) | 한국 종목 추가 수혜 |
| 빅테크 CapEx 둔화 | **−−** (가장 직접적 부정 영향) | 분기마다 모니터링 |
| 미국 그리드 정책 가속 | + | DOE 자금 집행 가속 시 |

---

## 12. 본인 의사결정 메모

> 시스템은 매수 결정 안 함. 본인 참고용.

- 현재 보유 종목: (본인 입력)
- 추가 매수 검토 종목: (본인 입력)
- 청산 검토 종목: (본인 입력)
- 다음 의사결정 시점: 2026 Q2 실적 시즌 (7~8월) 이후 시차 재평가

---

## 13. 업데이트 로그

| 날짜 | 변경 사항 | 점수 변화 |
|------|---------|---------|
| 2026-05-23 | 최초 작성 | TAM 4, Moat 4, Capital 5, Tech 3 → 합산 16 / Conf. Medium. 시차 A5 B3 C4 = +4 (Good entry) |
| 2026-05-23 | Tech 잣대 폐기 (methodology Decision 8), Moat에 비가역성 흡수 후 재채점 | TAM 4, Moat 4, Capital 5 → 합산 13 / 15. Conf. **Medium → High**. 시차 그대로 +4 (Good entry). Tier 1 유지. |


---

# ═══════════════════════════════════════════════════
# v2.3 UPGRADE — Next Wave Deep + KR Transmission
# ═══════════════════════════════════════════════════

> *아래 내용은 v2.3 retrofit 으로 위 v2.1 본문에 추가된 섹션입니다. 기존 본문은 그대로 유지하고 적용*

---

# AI Data Center Power Infrastructure — v2.3 Retrofit Delta

> **Base document**: sample_ai_dc_power_infra_v2.1.md (v2.1, 22KB)
> **Retrofit 작성일**: 2026-05-24
> **변경 사항**: Next Wave Deep (6.4·6.5) + KR transmission 강화

---

## 본 문서 적용 가이드

- **6.4 Next Wave Deep Analysis** — *신규 추가*
- **6.5 Next Wave 종합** — *신규 추가*
- **5.3 Sub-area X: 한국** — *thorough 보강 (KR 그리드 alpha 강)*
- **8.2 한국 종목** — *thorough 보강*
- **12 비중 분배 권장** — KR 강화
- **13 업데이트 로그** — v2.3 retrofit 진입

---

## 5.3 Sub-area X: 한국 — *KR pure-play thorough* (보강)

> v2.3 KR transmission 강화. **K-그리드·전력기기 미국 수출 가속 + 본인 정보 비대칭 우위**.

### KR 상장 pure-play

| 티커 | 기업 | 영역 | 시총 | 핵심 thesis | Tier |
|------|------|-----|-----|----------|------|
| **298040** | **효성중공업** ★ | L2 변압기·SST·MV/HV 전력기기 | 7~10조원 | **K-그리드 1위**. 미국 변압기·STATCOM·SST 직접 수출. SST (Solid-State Transformer) MV→800V DC 데이터센터 변환 next-gen | **A KR 1순위** |
| **267260** | **현대일렉트릭** ★ | L2 변압기·고압·grid 솔루션 | 5~7조원 | **K-그리드 2위**. 미국 변압기 + grid 모더니제이션 직접 수혜 | **A KR 2순위** |
| **010120** | **LS ELECTRIC** | L2 전력기기·자동화·EV 충전 | 4~5조원 | 전력기기 다중. AI 데이터센터 변환기·차단기·UPS | **A KR 3순위** |
| **009150** | **삼성전기** | L3 MLCC (AI 서버 고용량) | 12~15조원 | AI 서버 MLCC 1위 lead 잠재 (NVDA blackwell 대용량). 반도체 영역 cross | **A KR 4순위 (반도체 cross)** |
| **006400** | **삼성SDI** | L3 데이터센터 ESS·battery | 20~22조원 | 데이터센터 백업 ESS + EV battery cross | **B KR 5순위 (EV cross)** |
| **373220** | **LG에너지솔루션** | L3 데이터센터 ESS·battery | 90~100조원 | 데이터센터 백업 ESS + EV 영역 cross | **B KR 6순위 (EV cross)** |
| **207940** | **삼성바이오로직스** | n/a | n/a | 데이터센터 X | 영역 외 |
| **051910** | **LG화학** | L3 소재·battery 모회사 | 25~30조원 | 다중 | C 위성 |
| **108670** | **LG이노텍** | L3 AI 서버 component | 4~5조원 | AI 서버 부품 (전력 회로) | B 위성 |
| **011200** | **HMM** | n/a | n/a | 영역 외 | - |
| **036460** | **한국가스공사 (KOGAS)** | L5 utility (간접) | 2~3조원 | 한국 utility, 간접 노출 | C 위성 |
| **015760** | **한국전력 (KEPCO)** | L5 utility | 25~30조원 | nuclear 영역 cross + AI DC 전력 직접 수혜 | A nuclear cross |
| **036570** | **엔씨소프트** | n/a | n/a | 영역 외 | - |
| **042660** | **한화오션** | n/a | n/a | 영역 외 | K-방산 |

### KR Sub-area 핵심

- **K-그리드 글로벌 export**: 효성중공업·현대일렉·LS ELECTRIC — *미국 utility·grid 직접 수혜*
- **AI 서버 MLCC·부품**: 삼성전기·LG이노텍 — 반도체 영역 cross
- **데이터센터 ESS / battery**: LG에너지·삼성SDI — EV 영역 cross
- **Utility**: 한국전력 (KEPCO) — nuclear 영역 cross

### KR 정책 trigger

- **미국 변압기·grid 부족** = K-전력기기 직접 수혜 (효성중공업·현대일렉)
- **K-그리드 미국 fab 진출** = 한화·현대·삼성 미국 fab 인근 데이터센터 전력 인프라 공급
- **한국 K-반도체 fab + 미국 fab** = 전력기기 + MLCC 공통 수혜

### 진입 전략 (KR 우선순위)

- **KR 1순위: 효성중공업 (298040)** — K-그리드 1위, 미국 변압기·SST 직접
- **KR 2순위: 현대일렉트릭 (267260)** — K-그리드 2위, 미국 grid 모더니제이션
- **KR 3순위: LS ELECTRIC (010120)** — 전력기기 다중
- **KR 4순위: 삼성전기 (009150)** — AI 서버 MLCC (반도체 cross)
- **KR 5~6순위 EV cross**: LG에너지·삼성SDI — EV 영역에서 매수, 본 영역 위성
- **KR 7순위 nuclear cross**: 한국전력 — nuclear 영역에서 매수, 본 영역 위성

---

## 6.4 Next Wave Deep Analysis ★★★ (신규 추가)

> v2.3 mandatory. Vertiv·Eaton·Schneider over-known. 다음 알파 3개 — SST·HVDC·AI DC Backup ESS.

---

### Next Wave 1: SST (Solid-State Transformer) MV→800V DC ★★★ 2026~2028

**왜 next wave 인가**
- **NVIDIA Blackwell + Rubin 800V DC** rack architecture = SST 절박
- **Navitas-EPFL 250kW SST 시연 (2025)** — GaN-based SST
- **GE Vernova + Siemens Energy 자체 SST 개발**
- 효성중공업 SST 진입 (K-그리드 next wave)
- MV grid → 800V DC 직변환 = 데이터센터 전력 효율 +5~10%
- SST = 변압기 + AC/DC 변환기 통합 (효율 + 공간 절약)
- 2026~2028 본격 상업 deploy

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **GE Vernova (GEV)** | US | SST + grid 모더니제이션 | B 본문 매수 (nuclear cross) |
| **Siemens Energy (ENR.DE)** | DE | SST + HVDC + grid | A 위성 EU |
| **ABB (ABBN.SW)** | CH | 전력기기 종합 + SST | B 위성 EU |
| **Navitas Semiconductor (NVTS)** | US | GaN SST (250kW EPFL 시연) | 전력반도체 영역 cross |
| **효성중공업 (298040)** ★ | KR | **K-SST 직접 진입 + 미국 변압기 본업** | **A 1순위 next wave KR** |
| **현대일렉트릭 (267260)** ★ | KR | 미국 그리드 모더니제이션 | **A 2순위 next wave KR** |
| **LS ELECTRIC (010120)** | KR | 전력기기 다중 | B KR 위성 |

**Timing**: 2026~2027 SST 본격 상업 deploy, 2028~ 표준화

**숨겨진 매력 — 효성중공업 (298040) KR**: K-그리드 1위 + SST 진입 + 미국 변압기 직접 수출 = 본 next wave KR 1순위 hidden alpha

---

### Next Wave 2: HVDC + Grid Modernization ★★ 2026~2028

**왜 next wave 인가**
- **AI DC 캠퍼스 가속 → MV→HVDC 광역 전력 inter-DC 전송**
- 미국 utility infrastructure 노후 (40+ 년) = grid 모더니제이션 메가 사이클
- **Inflation Reduction Act (IRA) + BIL grid funding $50B+**
- HVDC = 장거리 전력 손실 reduction (15~20% → 3~5%)
- 빅테크 데이터센터 캠퍼스 (1~5GW) HVDC inter-connect

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Quanta Services (PWR)** ★ | US | 미국 grid 모더니제이션 1위 (utility EPC) | **A 1순위 next wave** |
| **MasTec (MTZ)** | US | utility EPC + 5G | A 2순위 next wave |
| **Hitachi Energy (HTHIY)** | JP | HVDC + 변압기 | B 위성 |
| **Siemens Energy (ENR.DE)** | DE | HVDC + SST + grid | A 위성 EU |
| **ABB (ABBN.SW)** | CH | HVDC + 변압기 | B 위성 EU |
| **GE Vernova (GEV)** | US | grid 모더니제이션 | B 본문 매수 |
| **EATON (ETN)** | US | 전력기기 종합 | B 본문 매수 (냉각 cross) |
| **효성중공업 (298040)** | KR | 미국 변압기 + HVDC 진입 | next wave 1 중복 |

**Timing**: 2026~2028 grid 모더니제이션 본격, IRA·BIL funding 가속

**숨겨진 매력 — Quanta Services (PWR)**: 미국 grid 모더니제이션 1위 EPC. 시총 ~$45B, P/E ~30x. AI DC 캠퍼스 grid 직접 수혜

---

### Next Wave 3: AI DC Backup ESS / Battery Energy Storage ★ 2026~2027

**왜 next wave 인가**
- **AI DC 정전 backup = 대형 ESS 필수** (UPS 한계, 분 단위 → 시간 단위 필요)
- **Fluence (FLNC), Form Energy (비상장)** — long-duration ESS 가속
- **LG에너지·삼성SDI** = K-ESS battery 직접 (EV 영역 cross)
- **Tesla Megapack** = ESS 가속
- AI DC backup ESS = 데이터센터 reliability 99.999% 핵심

**상장 alpha**

| 종목 | 시장 | 노출 | 매수 우선순위 |
|------|------|------|-----------|
| **Fluence Energy (FLNC)** | US | grid-scale ESS 1위 | B 위성 |
| **Tesla (TSLA)** | US | Megapack | 별도 종합 thesis |
| **Form Energy (비상장)** | US | iron-air long-duration | n/a (IPO 시그널) |
| **LG에너지솔루션 (373220)** | KR | ESS battery + EV cross | EV 영역 cross |
| **삼성SDI (006400)** | KR | ESS battery + EV cross | EV 영역 cross |
| Stem Inc (STEM) | US | ESS software | C 변동성 |

**Timing**: 2026~ AI DC backup ESS 본격, 2027~ long-duration ESS

---

## 6.5 Next Wave 종합 — 본인 진입 전략

**우선순위 (Timing + 상장 alpha)**

| 순위 | Next Wave | Timing | 핵심 종목 | 비중 |
|-----|---------|--------|---------|-----|
| 1 | **SST MV→800V DC** | 2026~2028 | **효성중공업 (KR 1위), 현대일렉 (KR 2위)**, Navitas, GE Vernova, Siemens Energy | 2~3% |
| 2 | **HVDC + Grid Modernization** | 2026~2028 | **Quanta Services (PWR), MasTec (MTZ)**, Hitachi, ABB | 1~2% |
| 3 | **AI DC Backup ESS** | 2026~2027 | Fluence, LG에너지·삼성SDI (EV cross) | 0.5~1% |

### AI DC Power 영역 종합 매수 우선순위 업데이트

**Tier A — 즉시 분할 매수**

**글로벌**
1. **Vertiv (VRT)** — 본문 1순위 (조정 시 가속)
2. **Eaton (ETN)** — 본문 다중 (냉각 cross)
3. **Schneider Electric (SU.PA)** — 본문 EU 다중
4. **GE Vernova (GEV)** — grid + nuclear cross
5. **nVent (NVT)** — 본문 안정
6. **Quanta Services (PWR)** ← **Next wave HVDC 1순위**
7. **MasTec (MTZ)** ← **Next wave HVDC**
8. **Hitachi Energy, ABB, Siemens Energy** — EU 위성

**KR (Tier A) — 본인 정보 비대칭 우위**
1. **효성중공업 (298040)** ★ **KR 1순위 next wave SST + 미국 변압기**
2. **현대일렉트릭 (267260)** **KR 2순위 next wave HVDC + 미국 grid**
3. **LS ELECTRIC (010120)** **KR 3순위**
4. **삼성전기 (009150)** — AI 서버 MLCC (반도체 cross)
5. **LG에너지·삼성SDI** — ESS battery (EV cross, 위성)
6. **한국전력 (KEPCO 015760)** — utility (nuclear cross)

**모니터링 watchlist (비상장 IPO)**
- **Form Energy IPO** (long-duration ESS)
- **국내 한미반도체·STX파워** — 위성 IPO

### 글로벌:KR 비중 분배 권장

- **글로벌 60~70% : KR 30~40%** (K-그리드 미국 수출 본인 정보 비대칭 우위 강)

---

## 12 본인 의사결정 메모 — 비중 분배 권장 (v2.3 추가)

### 비중 가이드 (KR 강화)

- 본 영역 전체: **포트폴리오의 5~8%** (AI DC Power)
- *AI 인프라 합산 25~35% 상한* 인지 (Foundation + Vertical + 광인터 + 전력반도체 + 냉각 + AI DC Power)
- **글로벌 60~70% : KR 30~40%** (K-그리드 미국 수출 정보 비대칭 우위 강)
- 종목별:
  - VRT 1~1.5%, ETN 0.5~1%, SU.PA 0.5~1%, GEV 0.5%, NVT 0.3~0.5%
  - PWR 0.5~1%, MTZ 0.3~0.5%, Hitachi·ABB·Siemens Energy 합산 0.5%
  - 효성중공업 1~1.5%, 현대일렉 0.5~1%, LS ELECTRIC 0.5%
  - 삼성전기 0.3~0.5% (반도체 cross), LG에너지·삼성SDI = EV 영역 cross
  - 한국전력 = nuclear 영역 cross

### Cross-area 중복 카운트
- **Eaton (ETN)** = 냉각 영역 cross → 한쪽만 매수
- **GE Vernova (GEV)** = nuclear 영역 cross → 한쪽만
- **삼성전기 (009150)** = 반도체 영역 cross → 반도체에서 매수, 본 영역 위성
- **LG에너지·삼성SDI** = EV 영역 cross → EV에서 매수, 본 영역 위성
- **한국전력 (015760)** = nuclear 영역 cross → nuclear에서 매수, 본 영역 위성
- **Navitas (NVTS)** = 전력반도체 영역 cross → 한쪽만

---

## 13 업데이트 로그 — v2.3 retrofit 진입

| 날짜 | 변경 |
|------|------|
| 2026-05-24 | **v2.1 → v2.3 retrofit**. Next Wave Deep (6.4·6.5) 신규 추가, KR transmission thorough 보강. 매수 우선순위 업데이트: **VRT > ETN (냉각 cross) > SU.PA > GEV (nuclear cross) > NVT + PWR (next wave HVDC) > MTZ (next wave) > Hitachi·ABB·Siemens Energy 위성** + **KR: 효성중공업 (KR 1순위 next wave SST·미국 변압기) > 현대일렉트릭 (KR 2순위 next wave HVDC·미국 grid) > LS ELECTRIC > 삼성전기 (AI 서버 MLCC 반도체 cross) > LG에너지·삼성SDI (EV cross 위성) > 한국전력 (nuclear cross 위성)**. **Next Wave Deep 3개**: (1) **SST MV→800V DC** (NVDA Blackwell 800V DC architecture, Navitas-EPFL 250kW 시연 2025, GE Vernova·Siemens Energy 자체 SST, **효성중공업·현대일렉 KR next wave hidden alpha 1·2위**), (2) **HVDC + Grid Modernization** (Quanta Services PWR 1순위 EPC, MasTec MTZ, Hitachi·ABB·Siemens Energy, IRA·BIL grid funding $50B+), (3) **AI DC Backup ESS** (Fluence FLNC, Form Energy 비상장, LG에너지·삼성SDI EV cross). **KR 비중 분배 권장 60~70% : 30~40%** (K-그리드 미국 수출 정보 비대칭 우위 강). |
| (이전) | v2.1 본문 작성 |

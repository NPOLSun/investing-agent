# 통합 관리 안내 (Integration Management) — v2.3 완료

> **작성일**: 2026-05-24
> **현재 상태**: methodology v2.3 + 8개 신규 deep dive + 5개 Tier 1 retrofit + 4개 KR boost 완료
> **다음 actions**: GitHub repo 구조 + EC2 sync + 일일 digest 업데이트 + 포트폴리오 비중 통합

---

## 1. 완료 파일 인벤토리 (전체)

### 1.1 Methodology
- **methodology_v2.1.md** (38KB) — 기존 PC 유지
- **methodology_v2.3.md** (24KB) — v2.3 업그레이드 ★

### 1.2 신규 Deep Dive (8개, v2.3 패턴 — Next Wave Deep + KR thorough 적용)

| # | 영역 | 파일 | 크기 | 시차 | Tier |
|---|------|------|-----|----|------|
| 1 | 광인터커넥트 (CPO) | optical-interconnect-cpo.md | 40KB | +5 | 2 (Tier 1 깊이) |
| 2 | 전력반도체 (GaN·SiC) | power-semi-gan-sic.md | 36KB | +7 ★ | 2 (Tier 1 깊이) |
| 3 | 데이터센터 냉각 | data-center-cooling.md | 36KB | +6 | 2 (Tier 1 깊이) |
| 4 | 자율주행 / Robotaxi | autonomous-driving.md | 44KB | +6 | 2 (Tier 1 깊이) |
| 5 | 우주 (위성·발사체) | space.md | 48KB | +5 | 2 (Tier 1 깊이) |
| 6 | 국방·드론 | defense-drones.md | 48KB | +7 ★ | 2 (Tier 1 깊이) |
| 7 | 정밀 종양학 | precision-oncology.md | 48KB | +6 | 2 (Tier 1 깊이) |
| 8 | 휴머노이드 로봇 | humanoid-robot.md | 48KB | +6 | 2 (Tier 1 깊이) |

### 1.3 Tier 1 Retrofit Delta (5개, v2.1 → v2.3)

| # | 영역 | 파일 | 크기 |
|---|------|------|-----|
| 1 | GLP-1 ecosystem | glp1_retrofit_delta.md | 24KB |
| 2 | Nuclear Renaissance | nuclear_retrofit_delta.md | 16KB |
| 3 | AI Foundation Horizontal | ai_foundation_retrofit_delta.md | 16KB |
| 4 | AI Application Vertical | ai_vertical_retrofit_delta.md | 12KB |
| 5 | AI DC Power Infra | ai_dc_power_retrofit_delta.md | 16KB |

### 1.4 KR Boost Retrofit (4개, 기존 deep dive 점검)

| # | 영역 | 파일 | 크기 |
|---|------|------|-----|
| 1 | 자율주행 | autonomous_kr_boost.md | 12KB |
| 2 | 광인터커넥트 | optical_kr_boost.md | 8KB |
| 3 | 전력반도체 | power_semi_kr_boost.md | 8KB |
| 4 | 데이터센터 냉각 | cooling_kr_boost.md | 8KB |

### 1.5 합계
- **총 파일 19개 + methodology 2개 = 21개**
- **총 크기 ~412KB**

---

## 2. 권장 폴더 구조 (Windows PC + EC2 sync)

```
investing-agent/
├── mega-change-map/
│   ├── methodology/
│   │   ├── methodology_v2.1.md (구버전, archive)
│   │   └── methodology_v2.3.md ★ (현재)
│   ├── tier1/  (Tier 1 영역 5개)
│   │   ├── 01_glp1_ecosystem.md (v2.1 본문)
│   │   ├── 01_glp1_retrofit_delta.md ★ (v2.3 추가)
│   │   ├── 02_nuclear_renaissance.md (v2.1)
│   │   ├── 02_nuclear_retrofit_delta.md ★ (v2.3)
│   │   ├── 03_ai_application_foundation_horizontal.md (v2.1)
│   │   ├── 03_ai_foundation_retrofit_delta.md ★ (v2.3)
│   │   ├── 04_ai_application_vertical.md (v2.1)
│   │   ├── 04_ai_vertical_retrofit_delta.md ★ (v2.3)
│   │   ├── 05_ai_dc_power_infra.md (v2.1)
│   │   └── 05_ai_dc_power_retrofit_delta.md ★ (v2.3)
│   ├── tier2/  (Tier 2 영역 8개, Tier 1 깊이)
│   │   ├── 06_optical-interconnect-cpo.md ★
│   │   ├── 06_optical_kr_boost.md ★ (KR 추가)
│   │   ├── 07_power-semi-gan-sic.md ★
│   │   ├── 07_power_semi_kr_boost.md ★ (KR 추가)
│   │   ├── 08_data-center-cooling.md ★
│   │   ├── 08_cooling_kr_boost.md ★ (KR 추가)
│   │   ├── 09_autonomous-driving.md ★
│   │   ├── 09_autonomous_kr_boost.md ★ (KR 추가)
│   │   ├── 10_space.md ★
│   │   ├── 11_defense-drones.md ★
│   │   ├── 12_precision-oncology.md ★
│   │   └── 13_humanoid-robot.md ★
│   ├── watchlist/
│   │   ├── track4_watchlist.md (60+ 종목 통합)
│   │   ├── ipo_watchlist.md (비상장 IPO 후보)
│   │   └── catalyst_calendar.md (월별 catalyst 일정)
│   └── INTEGRATION_MANAGEMENT.md ★ (본 문서)
└── ec2-bot/
    └── (Telegram bot 기존 setup)
```

### 2.1 Sync workflow

1. **Windows PC**: 파일 작성·수정
2. **Git push from PC**: `git push origin main`
3. **SSH to EC2 Seoul**: `ssh ubuntu@<ec2-ip>`
4. **EC2 git pull**: `cd ~/investing-agent && git pull`
5. **Bot restart**: `sudo systemctl restart investing-agent-bot`
6. **Verify**: Telegram `/deepdive humanoid` 등으로 새 영역 인식 확인

---

## 3. Track 4 통합 Watchlist (60+ 종목)

### 3.1 글로벌 — Tier A (즉시 분할 매수)

**AI Foundation (Megacap)**
- NVIDIA (NVDA), Microsoft (MSFT), Alphabet (GOOGL), Meta (META), Amazon (AMZN), Apple (AAPL)
- Salesforce (CRM), ServiceNow (NOW), Adobe (ADBE), Qualcomm (QCOM), AMD (AMD)

**AI Vertical**
- Palantir (PLTR), Cadence (CDNS), Synopsys (SNPS), Intuitive Surgical (ISRG)
- MSCI, Moody's (MCO), S&P Global (SPGI), Veeva (VEEV)

**AI DC 인프라**
- Vertiv (VRT), Eaton (ETN), Schneider Electric (SU.PA), GE Vernova (GEV), nVent (NVT)
- Quanta Services (PWR), MasTec (MTZ)
- Modine (MOD), Henkel (HEN3.DE), Chemours (CC)
- Coherent (COHR), Marvell (MRVL), Lumentum (LITE), Ciena (CIEN)
- STMicro (STM), Infineon (IFX), Vicor (VICR), Power Integrations (POWI), MPS (MPWR)

**Nuclear Renaissance**
- Constellation Energy (CEG), Cameco (CCJ), Vistra (VST)
- NuScale (SMR), Oklo (OKLO), Centrus (LEU), BWXT

**Robotaxi / 자율주행**
- Alphabet/Waymo, Mobileye (MBLY), Uber (UBER), Aurora (AUR)
- Kodiak (KDK), PACCAR (PCAR)

**우주**
- Rocket Lab (RKLB), AST SpaceMobile (ASTS), Intuitive Machines (LUNR)
- Globalstar (GSAT), SpaceX (IPO 2026-06-12 SPCX), ispace (9348.T)
- Iridium (IRDM), Planet Labs (PL)

**국방·드론**
- AeroVironment (AVAV), Kratos (KTOS), Lockheed (LMT), RTX, L3Harris (LHX), Northrop (NOC), GD

**정밀 종양학**
- Pfizer (PFE), Merck (MRK), Daiichi Sankyo (4568.T), AstraZeneca (AZN), AbbVie (ABBV)
- Gilead (GILD), BMS (BMY), Lantheus (LNTH), Telix (TLX.AX)

**GLP-1**
- Eli Lilly (LLY), Novo Nordisk (NVO)

**휴머노이드**
- Harmonic Drive (6324.T), Tesla (TSLA, 종합 thesis)

### 3.2 KR — Tier A (본인 정보 비대칭 우위)

**자율주행 + Humanoid (Hyundai 4 thesis cross)**
- **현대차 (005380)** ★★★ — *4 thesis hidden alpha 1위*
- 현대모비스 (012330), 기아 (000270), HL만도 (204320), 현대오토에버 (307950)
- 레인보우로보틱스 (277810), 에스피지 (058610), 로보티즈 (108490), 두산로보틱스 (454910)

**K-방산**
- 한화에어로스페이스 (012450), 현대로템 (064350), LIG넥스원 (079550)
- KAI (047810), 한화오션 (042660), 한화시스템 (272210), 풍산 (103140), 한화 지주 (000880)
- 비츠로테크·빅텍·휴니드·퍼스텍 (위성)

**우주**
- 쎄트렉아이 (099320), 루미르 (470170), 컨텍 (451760), 이노스페이스 (462350), AP위성 (211270)
- 인텔리안테크 (189300)

**K-바이오 (정밀 종양학·GLP-1)**
- 리가켐바이오 (141080), 알테오젠 (196170), 에이비엘바이오 (298380)
- 유한양행 (000100), 삼성바이오로직스 (207940), 셀트리온 (068270)
- 펩트론 (087010), 한미약품 (128940)
- 루닛 (328130), 뷰노 (338220)

**Nuclear / K-원전**
- 두산에너빌리티 (034020), 한전기술 (052690), 한국전력 (015760)
- 일진파워 (094820), 한전산업개발 (130660)
- 한신기계·보성파워텍·우진·STX엔진·프로텍 (위성)

**AI DC Power + 전력반도체 + 광인터커넥트**
- 효성중공업 (298040), 현대일렉트릭 (267260), LS ELECTRIC (010120)
- 삼성전기 (009150), DB하이텍 (000990)
- 오이솔루션 (138080), 라이파이텍 (425500)

**AI Foundation / Vertical (Sovereign + Medical)**
- NAVER (035420), 카카오 (035720), 솔트룩스 (304100)
- 루닛·뷰노·큐렉소 (의료 cross)

**반도체 메가 (cross)**
- 삼성전자 (005930), SK하이닉스 (000660), 한미반도체 (042700), 이수페타시스 (007660)

### 3.3 비상장 IPO Watchlist (catalyst 가장 큰 모니터링)

| 영역 | 비상장 | IPO 시그널 |
|------|------|---------|
| 우주 | **SpaceX (SPCX, $1.75T)** | **2026-06-12 nasdaq IPO 확정** ★ |
| 국방·드론 | **Anduril ($61B)** | 2026 후반~2027 |
| 휴머노이드 | **Apptronik ($5B)** | 2026 후반~2027 |
| 휴머노이드 | **Figure AI (NVDA-backed)** | 2027~ |
| 휴머노이드 | **1X NEO ($11B 협상)** | 2027~ |
| 휴머노이드 | **Agility Robotics (commercial revenue)** | 2026~2027 |
| Nuclear | **X-energy (Amazon $500M)** | 2026~2027 |
| Nuclear | TerraPower (Gates) | 2027~ |
| AI Foundation | **OpenAI** | 2026~2027 시그널 |
| AI Foundation | Anthropic, xAI, Mistral | 시그널 |
| K-자율주행 | **카카오모빌리티** | 2026~2027 ★ |
| K-자율주행 | 포티투닷 (현대차 자회사), 라이드플럭스, 서울로보틱스 | 시그널 |
| K-바이오 | 삼성바이오에피스 (Samsung Bio 자회사) | 시그널 |
| K-전력반도체 | **예스파워테크닉스 (SiC)** | 2026~2027 |
| K-AI | 업스테이지·마음AI·노타 | 시그널 |

---

## 4. 영역별 비중 분배 권장 (통합)

### 4.1 영역별 권장 비중

| 영역 | 권장 비중 | KR 비중 |
|------|--------|------|
| AI Foundation (Megacap) | 10~15% | KR 10~15% (NAVER·카카오) |
| AI Vertical | 5~8% | KR 15~25% (루닛·뷰노·금융) |
| 광인터커넥트 | 3~5% | KR 20% (오이솔루션·라이파이텍) |
| 전력반도체 | 3~5% | KR 30% (삼성전기·DB하이텍·예스파워) |
| 데이터센터 냉각 | 3~5% | KR 20% (LG전자·신성·코오롱) |
| AI DC Power | 5~8% | KR 30~40% (효성중공업·현대일렉) ★ |
| 자율주행 | 5~10% | KR 30% (현대차·현대모비스) |
| 우주 | 3~7% | KR 30~40% (쎄트렉·루미르·컨텍·이노) |
| 국방·드론 | 10~15% | KR 40~50% (한화에어로·현대로템·LIG·KAI) ★ |
| 정밀 종양학 | 8~12% | KR 30~40% (리가켐·알테오젠·에이비엘) ★ |
| 휴머노이드 | 5~8% | KR 70~80% (현대·레인보우·에스피지) ★★ |
| GLP-1 | 5~10% | KR 15~25% (펩트론·한미) |
| Nuclear Renaissance | 6~10% | KR 25~35% (두산에너빌·한전기술) ★ |

### 4.2 AI 인프라 합산 25~35% 상한

다음 영역 합산은 **25~35% 상한** (중복 카운트 방지):
- AI Foundation + AI Vertical + 광인터커넥트 + 전력반도체 + 냉각 + AI DC Power = **25~35%**

### 4.3 K-시장 정보 비대칭 우위 활용 영역 (KR 비중 강)

본인 *K-VC 친숙도 + 정보 비대칭 우위* 영역:
1. **휴머노이드** — KR 70~80% (Hyundai·레인보우·에스피지·로보티즈)
2. **K-방산** — KR 40~50% (한화·현대로템·LIG·KAI·풍산·한화시스템·한화오션)
3. **K-바이오 (정밀 종양학)** — KR 30~40% (리가켐·알테오젠·에이비엘·유한양행)
4. **K-원전** — KR 25~35% (두산에너빌·한전기술·한국전력)
5. **K-그리드 (AI DC Power)** — KR 30~40% (효성중공업·현대일렉)
6. **우주 K-위성** — KR 30~40% (쎄트렉·루미르·컨텍·이노)

---

## 5. Daily Digest Cron Job 업데이트

기존 cron 06:30 KST → v2.3 영역 반영하도록 업데이트:

```bash
# /etc/crontab on EC2
30 6 * * * cd /home/ubuntu/investing-agent && python daily_digest.py --version v2.3
```

`daily_digest.py` 업데이트 항목:
- 영역 list: Tier 1 (5개) + Tier 2 깊이 (8개) = 13개
- Next Wave catalyst 우선 체크 (Anduril·SpaceX·OpenAI·Apptronik·X-energy IPO 등)
- KR 신규 KOSPI/KOSDAQ 종목 추적 (현대차·레인보우·에스피지·효성중공업·리가켐 등)
- Cross-area 중복 인지 (NVIDIA·Hyundai·Eaton·삼성·SK 등)

---

## 6. 다음 분기 검토 (v2.4 후보)

- **새 영역 추가 검토**: 양자 컴퓨팅, 핵융합 (Helion·Commonwealth IPO 후), digital fab, hyperscaler PSU, gene editing
- **Track 5 자동화**: 시뮬레이션·backtesting
- **KR pure-play 자동 발굴 시스템** (KIND·KIND·DART 연동)
- **Cross-area 비중 시뮬레이션** (시나리오 분석)
- **본인 portfolio actual vs methodology 권장 비교 dashboard**

---

## 7. 이번 v2.3 작업 핵심 takeaways

1. **Next Wave Deep (6.4·6.5) mandatory** = *over-known 영역 이후 다음 알파 식별*. 본인 *bet on the pickaxe* 전략 표준화
2. **KR Transmission MANDATORY** = 글로벌 commercial 점유 약하더라도 본인 정보 비대칭 우위 영역이면 포함. *우주 KR 누락 사례 학습*
3. **본인 진정한 hidden alpha 발견**:
   - **현대차 (005380)** — 자율 + humanoid + 미국 fab + 자동차 4 thesis P/E 5~7x
   - **에스피지 (058610)** — humanoid 정밀 감속기·26종 액추에이터 + 삼성자산운용 5.03%
   - **효성중공업 (298040)** — K-그리드 미국 변압기 + SST
   - **리가켐바이오 (141080)** — ADC 10조원 기술수출
   - **펩트론 (087010)** — Lilly GLP-1 depot direct partnership
4. **catalyst 일정 인지**:
   - 2026-06-12: SpaceX IPO ★
   - 2026-07: 미 ERCA K9 자주포 숏리스트 (한화에어로 catalyst)
   - 2026-12: Lilly Retatrutide TRIUMPH-5
   - 2026~2027: Anduril·X-energy·Apptronik·1X·OpenAI 등 IPO 가능성
   - 2026 Q3~Q4: 카카오모빌리티 IPO 시그널

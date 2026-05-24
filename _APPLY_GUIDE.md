# v2.3 통합본 적용 가이드

## 최종 구조 (통합본 — 영역당 1파일)

```
investing-agent/
├── .gitignore
├── methodology.md                                    ← v2.3 교체
├── methodology_v2.1_archive.md                       ← 백업 (선택)
├── INTEGRATION_MANAGEMENT.md                         ★ 신규
│
├── calendar/                                         (그대로)
├── digests/                                          (그대로)
├── infra/                                            (그대로)
├── templates/                                        (그대로)
├── watchlist/                                        (그대로)
│
└── mega-change-map/
    ├── 00_dashboard.md                               (기존 유지)
    │
    ├── tier1_glp1_ecosystem_v23.md                   ★ 통합 (base + v2.3)
    ├── tier1_nuclear_renaissance_v23.md              ★ 통합
    ├── tier1_ai_foundation_horizontal_v23.md         ★ 통합
    ├── tier1_ai_vertical_v23.md                      ★ 통합
    ├── tier1_ai_dc_power_infra_v23.md                ★ 통합
    │
    ├── tier2_optical_interconnect_cpo_v23.md         ★ 통합 (본문 + KR boost)
    ├── tier2_power_semi_gan_sic_v23.md               ★ 통합
    ├── tier2_data_center_cooling_v23.md              ★ 통합
    ├── tier2_autonomous_driving_v23.md               ★ 통합
    ├── tier2_space_v23.md                            ★ 통합 (KR 이미 본문)
    ├── tier2_defense_drones_v23.md                   ★ 통합
    ├── tier2_precision_oncology_v23.md               ★ 통합
    └── tier2_humanoid_robot_v23.md                   ★ 통합
```

→ **mega-change-map/ 안에 14개 파일** (00_dashboard + Tier1 5개 + Tier2 8개)

---

## 적용 (PowerShell)

### Step 1. 백업

```powershell
cd C:\path\to\investing-agent

# methodology 백업
Copy-Item methodology.md methodology_v2.1_archive.md

# mega-change-map 전체 백업 (안전)
Copy-Item -Recurse mega-change-map mega-change-map_backup_v21
```

### Step 2. 기존 파일들 정리

```powershell
cd mega-change-map

# 기존 v2.1 본문 4개 삭제 (통합본으로 교체될 것)
Remove-Item glp1-ecosystem.md
Remove-Item nuclear-renaissance.md
Remove-Item ai-application-foundation-horizontal.md
Remove-Item ai-application-vertical.md

cd ..

# 루트 sample_ai_dc_power_infra.md 삭제 (통합본으로 교체될 것)
Remove-Item sample_ai_dc_power_infra.md

# 00_dashboard.md 는 그대로 유지
```

### Step 3. v2.3 zip 풀고 복사

```powershell
# 다운로드 폴더 가정
cd $env:USERPROFILE\Downloads
Expand-Archive investing-agent-v2.3-final.zip -DestinationPath .\v23-temp

cd C:\path\to\investing-agent

# 루트
Copy-Item $env:USERPROFILE\Downloads\v23-temp\v23final\methodology.md . -Force
Copy-Item $env:USERPROFILE\Downloads\v23-temp\v23final\INTEGRATION_MANAGEMENT.md .

# mega-change-map 안 통합본 13개
Copy-Item $env:USERPROFILE\Downloads\v23-temp\v23final\mega-change-map\* mega-change-map\
```

### Step 4. 확인

```powershell
tree /F /A
```

### Step 5. Git + EC2

```powershell
git add .
git commit -m "v2.3 upgrade: consolidated single-file per area (Tier 1 + Tier 2)"
git push origin main
```

```bash
ssh ubuntu@<ec2-ip>
cd ~/investing-agent && git pull
sudo systemctl restart investing-agent-bot
```

---

## 각 통합 파일 내부 구조

각 `tier1_*_v23.md` / `tier2_*_v23.md` 안에:

```
[v2.1 본문 (또는 신규 Tier 2 본문)]
   ↓
─────────────────────────────────
v2.3 UPGRADE 섹션 (separator)
─────────────────────────────────
   ↓
[v2.3 retrofit / KR boost 내용]
```

→ 영역 하나 보면 v2.1 본문부터 v2.3 추가까지 한 파일에서 다 확인 가능

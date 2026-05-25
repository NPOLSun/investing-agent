# Investing Agent

> **Mega Change Map 기반 투자 리서치 시스템** (methodology v2.3)
>
> 단순 종목 추천이 아니라 *Next Wave Deep* + *KR Transmission* 두 축으로 hidden alpha 를 발굴.
> *Bet on the pickaxe, not the gold miners.*

---

## 핵심 문서

- **[방법론 v2.3](methodology.md)** — 14 sections, Next Wave Deep (6.4·6.5) MANDATORY, KR Transmission MANDATORY
- **[Mega Change Map Dashboard](mega-change-map/00_dashboard.md)** — 13 영역 채점·시차·진입 우선순위
- **[통합 관리](INTEGRATION_MANAGEMENT.md)** — 전체 인벤토리, 비중 분배, cron, takeaways

---

## Tier 1 — Deep Dive (5개)

| 영역 | 합산 | 시차 | 카테고리 |
|---|---|---|---|
| [GLP-1 생태계](mega-change-map/tier1_glp1_ecosystem_v23.md) | 13 | +5 | Strong |
| [원자력 르네상스](mega-change-map/tier1_nuclear_renaissance_v23.md) | 12 | +5 | Strong |
| [AI Application: Foundation / Horizontal](mega-change-map/tier1_ai_foundation_horizontal_v23.md) | 14 | +4 | Good entry |
| [AI Application: Vertical / AI-native](mega-change-map/tier1_ai_vertical_v23.md) | 13 | +4 | Good entry |
| [AI 데이터센터 전력 인프라](mega-change-map/tier1_ai_dc_power_infra_v23.md) | 13 | +6 | Very strong |

## Tier 2 — Tier 1 깊이 (8개)

| 영역 | 합산 | 시차 | 카테고리 |
|---|---|---|---|
| [차세대 전력반도체 (GaN·SiC)](mega-change-map/tier2_power_semi_gan_sic_v23.md) | 12 | **+7** ★ | **Maximum** |
| [국방·드론](mega-change-map/tier2_defense_drones_v23.md) | 13 | **+7** ★ | **Maximum** |
| [데이터센터 냉각](mega-change-map/tier2_data_center_cooling_v23.md) | 12 | +6 | Very strong |
| [자율주행 / Robotaxi](mega-change-map/tier2_autonomous_driving_v23.md) | 14 | +6 | Very strong |
| [정밀 종양학 (ADC·CAR-T·RDC)](mega-change-map/tier2_precision_oncology_v23.md) | 13 | +6 | Very strong |
| [휴머노이드 로봇](mega-change-map/tier2_humanoid_robot_v23.md) | 13 | +6 | Very strong |
| [광인터커넥트 (CPO)](mega-change-map/tier2_optical_interconnect_cpo_v23.md) | 12 | +5 | Strong |
| [우주 (위성·발사체)](mega-change-map/tier2_space_v23.md) | 13 | +5 | Strong |

---

## 운영 정보

- 시스템 갱신: 분기 첫 주 (다음: 2026-07-01)
- 일간 다이제스트: EC2 cron 06:30 KST → Telegram 푸시
- 봇 명령: `/megamap`, `/deepdive <alias>`

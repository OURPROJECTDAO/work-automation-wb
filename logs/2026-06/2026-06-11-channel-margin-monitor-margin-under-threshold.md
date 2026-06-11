# 2026-06-11 channel-margin-monitor — 마진미달 판정 임계 -1%로 좁힘

## 무엇
마진미달 판정 기준을 `탐지 < 0` → `탐지 < -0.01`(기준마진율보다 1%p 이상 낮음)로 변경.
core에 `MARGIN_UNDER_THRESHOLD = -0.01` 상수 신설 → `_stats` 카운트 + 페이지 '마진미달만' 필터 + KPI 모두 이 상수 참조(단일 출처).

## 왜
사용자: 79개는 너무 넓음. 기준마진율보다 살짝 낮은 정도 말고 1%p↑ 미달한 상품만 집중해 보고 싶음.

## 변경 (app repo)
- core/workflows/channel_margin_monitor.py: `MARGIN_UNDER_THRESHOLD = -0.01` 상수 추가. `_stats`의 마진미달 카운트 `탐지<0` → `탐지<MARGIN_UNDER_THRESHOLD`.
- app/pages/6_채널마진모니터.py: '마진미달만' 필터 `탐지<0` → `탐지<cmm.MARGIN_UNDER_THRESHOLD`. 체크박스·KPI에 help("기준마진율보다 1%p 이상 낮음") 추가.

## 검증
- 실데이터 712건: 탐지<0=79(기존 KPI와 일치 재확인), 탐지<-0.01=**24**, 탐지<-0.02=22. → 79→24로 좁아짐.
- ast 양쪽 OK. 커밋 core·page 200.

## 다음 / 상태
- ⚠️ core 신규 상수 → **Reboot app 1회 필요**(page가 `cmm.MARGIN_UNDER_THRESHOLD` 참조 → 미부트 시 AttributeError). Reboot 후 KPI '마진 미달' 24 표시 확인.
- 임계는 전역 단일값(현재 전 채널 공통). 채널별로 다르게 할 거면 CHANNEL_CONFIG로 이동.

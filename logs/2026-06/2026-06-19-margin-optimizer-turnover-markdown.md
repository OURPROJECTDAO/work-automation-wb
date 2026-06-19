# 2026-06-19 두뇌④ ② 회전 markdown 결합 (노브2)

## 무엇 / 왜
재고가 안 빠지는(장기소진·과잉) 상품은 마진을 일시 낮춰 재고를 턴다(청산 마크다운). 두뇌④가 매출·순이익·볼륨만 보던 데 **재고 건강(소진예측일)** 신호를 결합 = 두뇌④ 마지막 노브.

## 소스 (재적재 0)
- 두뇌②(stockout) `소진예측일` = 현재고(product_master 최종재고 낱개) ÷ 최근3개월 일소진(매출자료). pm+sales로 계산(cadence 무관 — 소진예측일은 lead와 독립). 페이지 load_turnover→forecast 재사용.
- ⚪사장재고(매출0)는 cells에 애초 없음(작업목록 밖) → 회전 대상 = **매출은 있는데 소진예측일 긴(과잉)** 상품.

## 규칙 (§5 노브2)
- 트리거 = 소진예측일 > TURN_LONG_DAYS(180). 심각도 비례 마크다운: 램프 180→360일 = 0→**−2%p 캡(TURN_CAP_PP)**.
- 단방향(회전이 기존 권장보다 더 깊게 내릴 때만 적용·빨리 빠진다고 ↑ 안 함). 베이스 아래 허용(청산). 바닥 = 나들 마진(있으면)/0(역마진 금지).
- 이미 저마진(<베이스)/바닥 근처라 더 못 내림 → **🔴 사람판단**(충돌, §7 추천탭).
- 자동복귀 = 재고 풀리면 다음 사이클 소진예측일 정상화 → 신호 사라짐 → 베이스 권장 복귀(사람 적용).
- 액션 라벨 `↓ 회전`(ACT·MIN_DELTA 셋 포함). 

## 변경 (work-automation-app · core+page)
- `core/intelligence/margin_optimizer.py`: 상수 TURN_LONG_DAYS 180·TURN_CAP_PP .02. `recommend_code(..., turnover_days=None)` — ⑦ override 다음 회전 블록(램프·단방향·floor·🔴 충돌). `worklist(..., turnover_map=None)` — 관리코드별 소진예측일 주입.
- `app/pages/13_…py`: import stockout. `load_turnover(pat,repo)`=depletion_rate(sales,3)+forecast(pm,dep,{})→{관리코드:소진예측일}. build_worklist가 turnover_map 전달. ACT에 `↓ 회전`·캡션.

## 검증 (합성)
- 360일 → −2%p(8→6%)·270일 → −1%p(8→7%)·100일 → 회전없음·저마진+장기 → 🔴·나들없음도 −2%p(바닥0). ast 3파일 OK.

## 다음 · 상태
- ② 회전 = **완료**. 두뇌④ 설계 노브 전부 구현(베이스·4분면·측정루프·⑧·⑦·②). ★core 변경 → **재배포+Reboot 1회**(이번 세션 5종 묶어 1회).
- 잔여(나이스투해브): cmm 편집창 직접 prefill(현재는 '기준마진율도 함께 변경' 토글로 baseline_margin.csv 직접 write로 갈음) · margin_floor.csv 제조원가 하한 명시 클램프.

## 관련
workflows/margin-optimizer.md §5·§6·§17 · 두뇌②(stockout.py·9_재고지능) · ADR 0026

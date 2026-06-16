# 2026-06-17 — 데일리 대시보드 확장판①: 채널별 요약 + 가격 변동 알림

## 무엇
데일리 대시보드(0b)에 두 데일리 인사이트 추가(사용자 요청).
1. **채널별 요약(당일)** — 당일 마진 점검을 채널 groupby: 매출(net)·원가·택배·마진·마진율·품목수.
2. **가격 변동 알림(±N%)** — 전체 상품 중 직전 대비 매입가/판매가가 ±N%(기본 2%) 인상·인하된 건 알림.

## 왜
- 채널별 매출 마진율을 매일 한눈에. (당일 마진 데이터 이미 채널 단위 → groupby만)
- "재고 들어오는 거 보여주듯, 가격 2%↑↓ 변동도 알림" — 1b 스냅샷이 매입단가·매출단가까지 매일 적립 중이라 재고 전이탐지와 동형으로 가격 변동 감지 가능.

## 변경 (코드 — app repo)
- `core/intelligence/stock_history.py` — `detect_price_changes(snaps, threshold=0.02, fields=(매입단가,매출단가))` + `PRICE_FIELDS` 추가. detect_transitions(재고) 자매: 상품코드별 연속 스냅샷 shift 비교·직전 결측/0이하/신규등재 제외·구분(매입가/판매가)·방향(인상/인하)·변동률(%). 커밋(core).
- `app/pages/0b_데일리대시보드.py` — ① import stock_history ② `_price_changes(days, threshold)` cached(data repo 최근 3개월 파티션·ttl30분) ③ '💲 가격 변동 알림' 섹션(품절 알림판 뒤·당일 마진 앞: 최근 N일·임계% 슬라이더·구분 필터·인상/인하 메트릭·표·XLSX) ④ '채널별 요약(당일 매출·마진율)' 표(메트릭 아래·이상치표 위). 커밋(page).

## 검증
- `detect_price_changes` 합성 스냅샷 단위검증: 매입 600→612(+2.0%, 경계 포함)=인상·매출 1000→950(-5%)=인하 2건 산출 / +1%(임계미달)·신규등재(직전없음) 제외 / 임계 5%로 올리면 1건. 정상.
- 코드 2종 ast.parse 통과(편집 anchor assert count==1).
- 채널별 요약: ddf(채널,관리코드)→채널 groupby, 마진율=Σ마진/Σ매출(당일 마진 점검과 동일 분모).

## 다음 · 상태
- 상태: 배포 커밋 완료. **core(stock_history) 수정 → Reboot app 1회.** 실사용 확인 대기.
- ⚠️ 1b 스냅샷 forward 적립(2026-06-15~) → 가격 변동 이력 현재 며칠치뿐, 상품관리 업로드일마다 누적. 업로드 sparse면 연속 스냅샷 비교가 자동 대응(직전 기록 대비).
- KB: workflows/daily-dashboard.md 섹션·state 인덱스·systemmap daily-dashboard 노드 line/roadmap(done 2건).
- 다음 한 수 = 확장판② 후보(재고 경고 결합·당일 물류량·발주/품절 추이) 또는 시장지능 nadl(최우선·행사샘플 대기).

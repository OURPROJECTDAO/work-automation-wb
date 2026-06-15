# 2026-06-15 intelligence-layer 1b — 상품관리 재고 스냅샷 적립 + 전이탐지

## 무엇 / 왜
지능 레이어 Phase 1 1b (ADR 0018). 매일 상품관리 업로드가 product_master.csv를 덮어써 재고·매입가 역사 소실 → 덮어쓰기와 같은 시점에 **새 업로드 df를 날짜본으로 private data repo에 적립**. 입고/품절 전이(두뇌② 입력)·as-of 재고/마진 토대. 1a(가격이력)에 이어 이력 엔진 두 번째 브릭.

## 설계 확정 (사용자: A)
- 스냅샷일자 = **파일명 `Exp{YYMMDD}` 추출일**(ERP가 찍은 실제 재고시점). 없으면 업로드 당일 폴백.
- 스냅샷 대상 = **새 업로드 df**(오늘의 진실). "덮어쓰기 직전" = 훅 시점이지 옛 master가 아님.
- 파티션 = `snapshots/stock_YYYY-MM.parquet`(월). dedup키=(스냅샷일자·상품코드) keep=last → 같은 날 재업로드 멱등.

## 변경
- work-automation-app:
  - `core/intelligence/stock_history.py`(신규) — `parse_snapshot_date`(Exp정규식) · `snapshot_from_master`(위치인덱스 7컬럼 정규화: [3]상품코드(_code6 6자리)·[4]관리코드·[14]박스재고·[9]박스매입단가·[8]매입단가·[12]매익률·[10]매출단가, _num 콤마제거 float) · `read_snapshots`/`list_snapshot_months`/`read_all_snapshots` · `ingest_snapshot`(월 그룹 dedup-append 멱등) · `detect_transitions`(상품코드별 연속 박스재고 0이하↔양수 → 입고/품절 이벤트). price_history.py와 동형(자체 GitHub R/W, (pat,repo) 인자).
  - `app/pages/3_연동데이터관리/1_상품관리.py` — `_data_secret`([data] pat 우선·GITHUB_PAT 폴백) + `_accumulate_snapshot(df, uploaded.name)` 훅을 업로드&저장 핸들러 master 저장 직후 삽입. **비차단**(try/except·st.toast) — 적립 실패가 상품관리 저장을 막지 않음. 미설정 시 조용히 건너뜀.

## 검증 (실 product_master.csv 4,340행)
- 컬럼 위치 재대조: KB 인덱스 정확([3]상품코드 000001 6자리 제로패딩·4340 유니크, [8]매입단가·[9]박스매입·[10]매출·[12]매익률·[14]박스). 
- snapshot_from_master: 4340입력→4340스냅샷·상품코드 유니크 4340·키중복 0·박스재고/매입단가 결측 0·dtypes(일자 datetime·코드 string·수치 float64).
- parquet 라운드트립 4340 무손실. dedup 멱등(2x concat→4340 불변).
- detect_transitions: 인위 시나리오(0→5·3→0) 입고/품절 정확 분류.
- parse_snapshot_date: Exp260615→2026-06-15·비매칭→None.
- ast.parse 양 파일 OK. PUT 201(모듈 b11c931b·페이지 396435d3).

## 다음 / 상태
- ⚠️ **core 신규 import(`core.intelligence.stock_history`) → 첫 배포 후 Reboot app 1회** 필요(모듈 캐시).
- 적립은 **forward**(훅 이후 업로드부터). 과거 소급 불가(상품관리 일자본 미보관). 첫 실업로드=스냅샷#1, 두 번째부터 전이 탐지.
- ✅ **시드 완료(사용자 승인)**: 현재 product_master.csv(4,340행)를 스냅샷#1로 적립 — `snapshots/stock_2026-06.parquet`, 일자 2026-06-14(updated.txt 기준). 읽기재검증 4340·키중복0·멱등 재실행 added 0. **리부트 완료** → 다음 상품관리 업로드=스냅샷#2부터 전이 탐지.
- 다음 ★ = 두뇌① 마진 침식 경보(매입가↑+판매가 정체, 1a 역재생 활용) or 1c 리드타임. 두뇌② 입고/품절 예측은 1b 스냅샷+1c 리드타임 위에.
- 지능 레이어 status=design 유지(적립=infra·passive; 사용자向 진단/추천 UI는 두뇌부터).

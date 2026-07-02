# 2026-07-02 — salt로 6월 주문 재처리 + "직접 적립" 업로드 기능 신규 구축

## 무엇
1. customer_key_salt(사용자 제공)로 6월 EasyAdmin 주문 재파싱·재적재 — 고객키·합포박스키 100% 채움(이전엔 빈값).
2. `app/pages/3_연동데이터관리/2_데이터현황.py`에 **"📤 직접 적립"** 섹션 신규 추가 — 매출·주문·가격이력·매입현황
   4종을 앱에서 바로 업로드→미리보기→적재할 수 있게 함(기존엔 읽기 전용, "다음 단계"로만 표시돼 있었음).
3. `core/intelligence/coverage.py` CATALOG의 매입현황 upload 상태 `planned`→`direct`로 갱신(위젯 생겼으므로).

## 왜
- 오늘 6월 자료 4종(영업이익현황·매입현황·가격이력·주문)을 전부 챗에서 수작업(core 모듈 직접 import+실행)으로
  적재했는데, 다음 달부턴 사용자가 앱에서 직접 할 수 있어야 함(로드맵에 있던 "다음 단계" 항목).

## 변경 (기술)
- 새 섹션 구조: selectbox(자료 종류 4개) → file_uploader(종류별 확장자/헬프 문구) → 파싱 미리보기(행수·기간·head8)
  → "📤 적재" 버튼 → 각 core 모듈의 ingest() 호출 → 성공 시 캐시 클리어+rerun.
- 매출: core/dashboard/sales_data.py+store.py(store.ingest가 raw bytes 받아 내부에서 parse). 나머지 3개(주문·
  가격이력·매입현황): core/intelligence/{orders,price_history,purchases}.py — 다 (new_df, pat, repo) 시그니처라
  미리 parse한 결과를 그대로 ingest에 넘기는 방식으로 통일.
- 주문(orders)은 `st.secrets["data"]["customer_key_salt"]`를 앱이 직접 읽어서 씀 — 이제 salt 있는 상태로
  적재되므로 이번 6월 이후부터는 고객키·합포박스키 처음부터 정상 적재됨.
- KeyError(필수 컬럼 누락, 예: 오늘 겪은 "jrkf" 헤더오염 같은 사례)는 별도 catch해서 "헤더가 깨졌을 수 있다"고
  안내(자동수정은 안 함 — 조용히 넘어가면 진짜 포맷 변경을 놓칠 위험).
- 상품관리 페이지(1_상품관리.py)의 업로드→미리보기→버튼→spinner→success→rerun 패턴 그대로 재사용(일관성).

## 검증
- ast.parse 문법 검증 통과(양쪽 파일).
- 6월 주문 재처리: 고객키·합포박스키 채움 비율 100%/100%(이전 세션 0%/0%에서 개선), 재적재 후 행수 10,387 그대로
  (date_range_replace가 정확히 같은 구간을 교체).

## 다음·상태
- ⚠️ **core/intelligence/coverage.py를 건드렸으므로 Streamlit 앱 Reboot 필요**(sys.modules 캐시). 페이지 .py
  (2_데이터현황.py)는 자동 반영되지만, coverage.py의 upload 상태 갱신은 Reboot 전까진 옛 캐시로 "예정"이라 보일 수 있음.
- 매입현황(purchases) 통파일 경로는 아직 실사용 검증 안 함(오늘은 개별 export만 테스트) — 다음에 통파일로 올라오면
  헤더명 매핑이 잘 맞는지 한 번 더 확인.
- 발주자료(demand)는 이번에 안 건드림(여전히 planned) — 별도 파이프라인 필요.

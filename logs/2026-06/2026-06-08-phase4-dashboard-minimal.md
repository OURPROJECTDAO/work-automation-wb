# 2026-06-08 Phase 4 대시보드 — 최소버전 페이지 배포

## 무엇
대시보드 페이지 최소버전 구현·배포(사용자 요청: 가장 쉬운 것부터, 매출 KPI + 구분/거래처/상품/관리코드별 집계만).

## 변경 (work-automation-app)
- `app/pages/3_대시보드.py`: 플레이스홀더 → 최소 대시보드.
  - load_sales(@st.cache_data ttl 1h): store.load_master → make_classifier로 구분 부여.
  - 시크릿: `st.secrets["data"]["pat"/"repo"]` 우선, 없으면 `GITHUB_PAT` 폴백. reference(분류표·product_master)는 로컬 csv.
  - UI: 연도/구분 필터 → 매출 KPI(총매출·건수·기간) → 집계기준 selectbox(구분/거래처/상품/관리코드) → 매출 표(순위·매출·비중) + CSV 다운로드.
- `requirements.txt`: pyarrow>=14, python-calamine>=0.2 추가.

## 검증
- 비-streamlit 로직(load_master+classify+groupby) 실데이터 스모크: 총매출 939.2억/313,293건. 구분 음료64.1·식품21.9·선물11.5·미분류2.6%. 거래처 860·상품 1,592·관리코드 1,551 고유, 상위 집계 정상.
- ast.parse OK. UI는 배포 후 확인.

## 다음·상태
- requirements 변경 → Community Cloud 자동 재설치+재배포(수동 reboot 불필요).
- 점진 추가 후보: 월별 추이 차트 / 이익률 KPI / 물류량 / 콤보차트 / 거래처 그룹 관리 / 증분 업로더. 사용자 우선순위대로 1개씩.

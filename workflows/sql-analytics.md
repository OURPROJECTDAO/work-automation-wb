# sql-analytics — DuckDB SQL 분석 층
> 2026-07-21 신설. 위치: work-automation-app/analytics/ (duck_views.sql · queries/01~08 · run_sql.py · README).

## 무엇
- work-automation-data parquet(매출 sales_* 42파티션 43만행 · 매입 buyin_* 6.6만행 · groups/store_groups.csv)를
  DuckDB read_parquet 글롭으로 **파일 그대로** SQL 뷰(sales/purchases/store_groups/online_sales)에 얹음.
- 대시보드 핵심 지표를 SQL로 재현: 연간 KPI(01), 상반기 YoY(02, LAG), 월별 추이+3M 이동평균(03),
  채널 순위·비중(04, RANK/QUALIFY), 상품 매출순위·누적기여(05), 마진 침식(06), 최신 매입단가(07, ROW_NUMBER), 판매가×매입가 검수(08).

## 사용
`python analytics/run_sql.py --list | <쿼리명> | all` · 데이터 루트 `--data` 또는 `WA_DATA` (하위 master/ purchases/ groups/).
채팅 세션에서: parquet 로컬 다운로드 후 WA_DATA 지정하면 즉시 동작.

## 검증 (2026-07-21)
- pandas 파이프라인과 **원 단위 골든 일치**: 2025 온라인 매출 11,103,105,175 · 2026 H1 6,106,986,665.
- 전 쿼리 스모크 통과. ast.parse OK.

## 함정/메모
- duckdb는 한글 컬럼 그대로 지원. strftime(ts,'%Y') 반환은 VARCHAR → CAST 필요.
- QUALIFY는 윈도우 필터 전용(표준 SQL 아님) — 이식 시 서브쿼리로.
- 00-12(택배비) 행은 상품 분석 쿼리(05·06·08)에서 제외, 총액 집계(01~04)에는 포함(대시보드 관례와 동일).

## 유래
쿠팡 지원 서류 검수(5인 리뷰)에서 SQL 실무 근거 부재가 1순위 지적 → 실사용 층을 실제 구축해 해소.
운영 실익: 파티션 통합 임시분석 표준화. 향후: 대시보드 임시분석 진입점으로 확장 가능.

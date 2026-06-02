# 로그: 발주서출력업무 골든 대조 테스트 작성

## 무엇
pytest 골든 대조 테스트 + fixture 커밋. 회귀 방지 안전장치.

## 변경 (work-automation-app)
- tests/fixtures/logistics/ : sales_input.xls, product_master.csv(골든 상품관리 스냅샷),
  classification/unit_list/spec_master.csv(기준데이터 스냅샷), golden_물류팀.csv, golden_품절목록.csv.
- tests/test_logistics_order.py : 4개 테스트.
  1. test_archive_is_8col_prededup : 아카이브 8열·중복제거 전 검증.
  2. test_logistics_matches_golden : 물류팀 102행 erp별 (총수량,재고) 1:1.
  3. test_stockout_matches_golden : 품절목록 10행 1:1.
  4. test_split_merged_cells : 셀나누기 ÷2 단위테스트.

## 검증
- 로컬 pytest 4 passed.
- 테스트는 pm_df/cls_df/spec_df/unit_df를 fixture로 명시 주입 → 라이브 기준데이터 편집과 무관하게 결정적.

## 주의
- code repo public이지만 매출 데이터는 고객 PII 아님 → 사용자 승인하에 실데이터 fixture 사용.

## 다음·상태
- 완료. Phase 3 발주서출력업무 = 구현+디자인+테스트까지 마무리.
- Phase 3 계속: 다음 템플릿 사용자 안내 대기.

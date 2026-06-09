# 2026-06-09 ESM 양식 영속화 + 상품등록 자산 위치 점검

## 무엇
ESM 빈 양식(NEW 일반상품 261열)을 app repo `reference/esm_bulk_template.xlsx`로 커밋. 상품등록 채널들의 안정 자산(양식·카테고리표) 저장 현황 점검.

## 왜
ESM 양식이 어디에도 영속 저장 안 돼 있어 6/9 배치는 세션 업로드 파일로 처리 → 다음 배치 때 재업로드 필요했음. 양식·카테고리 같은 거의 안 변하는 자산을 고정 위치에 두자는 논의.

## 점검 결과 (변경 전 실물 확인)
- 앱 코드 참조: esm_category/smartstore_category/bulk_template/category_food 전부 **0건** → 양식·카테고리표는 웹앱 미사용, 대화창 전용.
- 이미 저장됨: reference/esm_category_food.csv(291행), reference/smartstore_category_food.csv, reference/smartstore_bulk_template.xlsx.
- 누락: ESM 양식 — app repo·Drive 어디에도 없음.

## 변경
- 업로드 파일(esmnew전체20260120.xlsx) 검증: 시트 'NEW 일반상품', 261열, 행4 필드명(상품명·카테고리코드·G노출코드·G판매가 등) 일치, 33,077 bytes.
- app repo 신규 커밋: reference/esm_bulk_template.xlsx (commit 2f9489bf).
- 배치당 채널 자산 ~20 엑셀 수준 → repo 용량 무부담 판단(기존 product_master 596KB 등 대비).

## 검증
- 커밋 후 응답 size 33077 일치.

## 다음 / 상태
- esm-register.md '자산 위치' 섹션 추가, 카테고리표 '승인대기'→'완료' 정정.
- (선택) smartstore/easyadmin도 양식·카테고리 위치를 각 workflows/*.md '자산 위치'로 통일 기록하면 일관. 미적용.
- Drive 상품등록/esm/ 에는 소스·결과만 유지(양식·카테고리는 repo 정본).

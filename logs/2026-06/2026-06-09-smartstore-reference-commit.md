# 2026-06-09 스마트스토어 reference 자산 app repo 커밋

## 무엇
스마트스토어 상품등록용 영구 reference 2종을 공개 app repo(reference/)에 커밋.
- reference/smartstore_category_food.csv (카테고리 630, 식품)
- reference/smartstore_bulk_template.xlsx (일괄등록 양식 원본, 93열)

## 왜
오랫동안 갱신 불필요한 채널 reference. 코드/세션에서 룩업·양식 복사용으로 영구 보관(스마트스토어에서 다운로드한 공개 자료, PII 없음).

## 변경 / 검증
- 사용자 승인 후 PUT(신규 생성). csv 631행·xlsx 일괄등록 시트 무결성 확인 후 커밋.
- KB(smartstore-register.md·state.md) "승인 대기" → "커밋 완료"로 갱신.

## 다음 / 상태
- product_master.csv와 함께 app repo reference/에 정착.
- 미해결(불변): 이미지 확장자 자동검증 · 면세 처리 · 보유N 외/N8 중복 · 엔진/캐시.

# 로그: SKU단가표 탭 추가 (기준데이터관리)

## 무엇
기준데이터관리 페이지(2_기준데이터관리.py)에 SKU단가표 탭 추가.

## 왜
sku_list.csv가 합계:판매가 산출의 기준이므로 앱 UI에서 직접 편집·저장 가능해야 함.

## 변경
- `app/pages/2_기준데이터관리.py`: REF_CONFIG에 SKU단가표 항목 추가 (large=False, key_col=관리코드).
- 기존 탭 렌더링 로직(st.data_editor + GitHub 저장)을 그대로 재사용. 추가 코드 없음.

## 검증
- GitHub 커밋 OK, grep으로 항목 확인.

## 다음·상태
- 완료. 앱 재배포 후 기준데이터관리 > SKU단가표 탭에서 109개 SKU 인라인 편집 가능.

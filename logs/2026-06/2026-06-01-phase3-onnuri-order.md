# 로그: Phase 3 — 온누리양식_발주서 워크플로우 구현

## 무엇
Phase 3 첫 번째 템플릿: `_2-a_온누리양식v2.xlsm` 발주서 처리를 Python으로 이관.

## 왜
사용자가 Phase 3 착수 요청. 양식 xlsm + 입력 발주서 + 골든 결과물 3개 파일 제공.

## 분석
- VBA 모듈명: `OC_JT_FillG_And_SaveConfirm`
- 로직: 입력 발주서 데이터 → 천년경영업로드 시트 수식 재계산 → 합계:판매가 열 역기입 → (확인).xlsx 저장
- 수식 역추적: `F2=E2*C2*B2+G2` → 합계 = 공급가 × 수량 × 합포 + 배송비나누기 × 배송비기본
  - 배송비나누기 N = ROUNDUP(수량 / 최대합포수량)  → Python: `math.ceil(qty / max_bundle)`
  - 골든 파일 15행 전수 검증 100% 일치 확인 후 구현

## 변경
- `reference/sku_list.csv` 신규 (109 SKU, UTF-8-sig)
- `core/workflows/onnuri_order.py` 신규 (108줄)
- `app/pages/1_파일처리.py` import 한 줄 추가

## 검증
- `골든 일치: True` (15/15 행 전수)
- 3개 파일 GitHub 커밋 확인

## 주의 / 배운 점
- openpyxl read_only 셀 값은 숫자도 str 반환 → int() 명시 필수
- SKU 중복 관리코드 존재 (23-18 × 2) → drop_duplicates keep='first'
- 우편번호는 입력 xlsx에 이미 문자열 "08206" 형태로 저장 → 별도 처리 불필요

## 다음·상태
- 완료. 앱 재배포로 워크플로우 선택 목록에 자동 노출.
- Phase 3 계속: 다음 이관 템플릿 사용자 안내 필요.

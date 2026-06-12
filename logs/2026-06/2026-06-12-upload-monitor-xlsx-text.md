# 2026-06-12 — upload-monitor 다운로드 CSV→XLSX (코드 텍스트 서식)

## 무엇
- 다운로드를 CSV→XLSX로 교체. 상품코드·관리코드 컬럼 문자열셀+@ 서식 → 엑셀 자동변환 방지.

## 왜 (사용자 발견 공통 오류)
- CSV를 엑셀로 열면 **상품코드 앞자리0 제거**(000001→1)·**관리코드 날짜 자동변환**(14-01→날짜). CSV 한계(텍스트엔 맞으나 엑셀이 열 때 추론).

## 변경 (page-only)
- `_to_xlsx(df, text_cols)` 헬퍼(openpyxl): 행 append(numpy 스칼라 .item()) + text_cols(_CODE_COLS={상품코드,관리코드}) 컬럼 number_format='@'. 숫자(박스재고·매입가·재고금액)는 number 유지(정렬 OK).
- 평문/이미지 두 다운로드 다 XLSX(mime=spreadsheet, .xlsx). StringIO→BytesIO. 라벨 'CSV'→'엑셀(XLSX)'.

## 검증
- 상품코드 '003601'·관리코드 '45-21' = 문자열셀+@(엑셀 변환X 확인). 박스재고 int 유지. 빈 관리코드 공란. ast.parse OK.

## 다음 · 상태
- 배포(page-only → Reboot 불요). 다음 = L4 핸드오프.

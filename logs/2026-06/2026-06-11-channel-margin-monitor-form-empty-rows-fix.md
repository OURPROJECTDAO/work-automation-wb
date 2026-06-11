# 2026-06-11 channel-margin-monitor — 가격변경 양식 빈 <row> 완전 제거 (openpyxl delete_rows 함정)

## 무엇
가격 일괄변경 양식 출력에서 **데이터 행 외 빈 행이 플랫폼에 빈 상품으로 등록되는 문제** 해결. 사용자 골든 대조로 확정.

## 증상 / 원인
- 출력 .xlsx를 셀 값으로 보면 헤더5+체크행만(openpyxl max_row=6) 정상으로 보이나, **sheet XML에는 `<row r=7..717>` 빈 행 요소가 잔존**(셀 없이 ht/customHeight만). 플랫폼은 이 빈 `<row>`를 빈 상품행으로 인식.
- 원인: **openpyxl `delete_rows`는 셀은 지우지만 `ws.row_dimensions`(행 높이/서식 메타)를 정리하지 않음** → 빈 `<row>` 요소로 직렬화. 원본 export가 전 데이터행에 customHeight를 갖고 있어 대량 잔존.

## 변경 (core build_bulk_price_xlsx)
- delete_rows 후 **마지막 데이터행(keep_last=data_start-1+남긴수) 초과 row_dimensions 키 삭제**:
  `for rr in [x for x in ws.row_dimensions if x > keep_last]: del ws.row_dimensions[rr]`

## 검증
- 최악 raw(전 데이터행 customHeight) + 1체크 → 출력 sheet XML `<row>` 요소 = 1~6행만(헤더5+체크1). 골든 구조 일치. dimension A1:CP6.
- 데이터 무결성: 행6 F판매가 11500·G=N·BF 비움·헤더 보존. ast OK, 커밋 200.

## 다음 / 상태
- ⚠️ Reboot app 1회(core).
- 교훈(전역 함정 후보): **openpyxl delete_rows는 row_dimensions를 남긴다 → 빈 <row> 제거 시 row_dimensions도 정리 필수**. 외부 파서(플랫폼 업로드)에선 max_row가 아니라 <row> 요소 존재가 기준.

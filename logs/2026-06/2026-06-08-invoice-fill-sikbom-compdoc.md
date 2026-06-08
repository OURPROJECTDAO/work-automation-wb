# 2026-06-08 invoice-fill 식봄 .xls CompDocError 읽기 픽스

## 무엇
식봄 채널 .xls 템플릿이 앱에서 "아예 안 들어가는" 버그 수정.
원인은 송장 매칭 로직이 아니라 **읽기 단계 전체 실패**.

## 왜
식봄배송20260608.xls = 진짜 OLE2 BIFF(Composite Document V2). 그런데 `xlrd.open_workbook(file_contents=bytes)` 가
`CompDocError: Workbook corruption: seen[2] == 4` 로 예외 → 파싱 자체가 죽어 송장 0건 기입.
파일은 Excel에선 정상 열림(비표준 CompDoc 디렉터리를 xlrd 기본 파서만 거부).

## 변경
- repo work-automation-app: core/workflows/invoice_fill.py `_parse_template_xls`
  `xlrd.open_workbook(file_contents=file_bytes, ignore_workbook_corruption=True)` 로 변경(옵션 한 개).
  정상 파일엔 무영향. write(xlwt) 출력은 표준 OLE2라 옵션 불필요.
- 커밋 163bf67.

## 검증 (실물 end-to-end)
- 파싱: 시트 '송장번호 일괄입력 템플릿', 헤더 15열(상품주문번호 c1·택배사 c13·송장번호 c14), 안내문 r1='수정/삭제 불가', 데이터 r2~ 68행.
- 마스터 __송장0608.xlsx(682행·lookup키 552) ↔ 식봄 상품주문번호 VLOOKUP: **matched 64 · na 4 / 68**.
  (na 4건 = 상품주문번호가 마스터에 없음 — 합포장 후보 또는 미발주, 정상 흐름.)
- write→재독: 출력 .xls 기본 xlrd 파서로 정상 개방, 보존 64행 전부 송장(숫자)·택배사='한진택배' 기입.
- ast.parse OK.

## 다음 · 상태
- 운영 가능. **core/ 모듈 변경 → Streamlit Cloud Reboot app 필요**(올웨이즈 픽스와 같은 배포건이면 1회 리부트로 둘 다 반영).
- 식봄 송장형식은 그대로 **숫자(int)** 유지 — 이번 업로드는 처리전(빈칸) 템플릿이라 골든 부재. 식봄 골든 확보 시 형식(숫자 vs 문자열) 실측 재확인 권장(올웨이즈가 문자열이었던 전례 있음).
- 전역 함정 pitfalls.md에 'OLE2 .xls xlrd CompDocError' 항목 추가(향후 신규 OLE2 채널 공통).

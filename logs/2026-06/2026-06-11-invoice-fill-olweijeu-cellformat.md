# 2026-06-11 invoice-fill 올웨이즈 송장 셀 서식 @(텍스트)

## 무엇
올웨이즈 송장처리 출력의 운송장번호 셀을 **값은 숫자(int) 유지, 셀 number_format만 텍스트(@)** 로 기입하도록 수정.

## 왜
사용자가 실측 발견: 올웨이즈 업로드는 운송장번호 **셀 서식을 텍스트로만** 바꾸면 성공. 셀 값 자체는 숫자 그대로여도 됨.
골든(`올웨이즈20260611배송_-_골든.xlsx`) raw 확인:
- 기준: `<c r="W2" t="n"><v>537083316195</v></c>` (숫자 + General)
- 골든: `<c r="W2" s="5"><v>537083316195</v></c>` — 값 `<v>` 숫자 그대로, 스타일 s=5 → numFmtId 49(`@` 텍스트).
→ **값=숫자 / 서식=@** 라는 조합. 기존 as_text(값 자체를 문자열)와는 다른 제3변형.
(서식 이력: 0608 문자열 → 0610 int+General → 0611 int값+@서식)

## 변경 (work-automation-app, core/workflows/invoice_fill.py)
- 채널 스키마에 선택키 `invoice_cell_format` 추가(기본 "General"). 송장 셀의 number_format 제어. as_text(값 문자열화)와 독립.
- 올웨이즈 config: `invoice_cell_format="@"` (as_text는 미설정 → 값은 to_invoice_number=int 유지).
- `_write_template_xlsx`: 송장 셀 서식을 하드코딩 "General" 대신 `cfg.get("invoice_cell_format","General")` 적용(as_text 분기·일반 분기 공통). 값 기입 로직은 분기 유지(as_text=문자열 / else=숫자).
- 다른 채널: 식봄(xls경로 무관)·캐시노트(int+General 유지)·배민(as_text=True, 서식 기본 General 유지) — 전부 기존 동작 불변.

## 검증
- ast.parse OK.
- 모듈 로드 후 실제 write_template 경로로 기준파일 처리 → 골든 운송장번호 **8/8 전건 일치**(value·number_format·data_type 동일), 불일치 0.
- 재현 raw `<c r="W2" s="5" t="n"><v>537083316195</v></c>` = 골든과 동치(t="n"은 명시/생략 차이만, 의미 동일).
- 커밋 2d07e607.

## 다음 / 상태
- **운영중**. ⚠️ core/ 수정 → Streamlit **Reboot app 1회 필요**(페이지 새로고침 불충분, sys.modules 캐시).
- 참고: 올웨이즈 출력은 기존부터 openpyxl in-place 경로 → sharedStrings 없는 inlineStr 저장(상태 변동 없음, 업로드 기존 정상). 이번 변경은 송장 셀 서식만 영향.

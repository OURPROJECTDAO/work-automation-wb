# 2026-06-18 천년경영: 리테일앤인사이트 분배 + 추가 판매처 매출통계 병합 입력

## 무엇
천년경영 업로드에서 **제이티유통·리테일앤인사이트** 두 판매처가 결과물에 자동 분배되도록 확장.
- 리테일앤인사이트 → **리테일전체/리테일낱개 신규 시트**(H=F/D·수수료 없음·선결제비 G 복사, 제이티와 동일). 제이티유통은 이미 GROUP_TO_SHEET에 있었음.
- 천년경영 도구에 **선택 입력칸 ④ 추가 판매처 매출통계** 신설 — ERP "판매처상품매출통계" export(HTML형 가짜 .xls / 진짜 .xlsx)를 받아 발주자료 행에 자동 병합.

## 왜
이 두 채널 매출이 **맨날 다름** — 발주자료에 이미 섞여 들어올 때도, "판매처상품매출통계" 파일로 따로 받을 때도 있음(사용자). 그래서 양쪽 모두 자동 처리:
- 발주자료에 섞여 있으면 → 매핑(리테일 추가)만으로 분배됨.
- 따로 받으면 → ④에 올리면 병합됨.

## 변경 (app repo)
- `core/workflows/cheonnyeon_upload.py` (2d2c4dd)
  - `GROUP_TO_SHEET["리테일앤인사이트"]="리테일전체"`, ALL_SHEETS/FULL_TO_UNIT/UNIT_SHEETS에 리테일전체·리테일낱개, simple H dict에 `리테일전체:1.0`(F/D).
  - 신규 `parse_sales_stats(file_bytes) -> (rows, skipped)`: stdlib `html.parser`로 바깥 table 행/셀만 추출(셀 안 중첩 table 토큰 분리). PK매직이면 openpyxl(.xlsx) 분기. 콤마 숫자(`23,275`) 정제. **빈 erp코드 행 → 옵션추가항목1(8열) 코드 보정**: 코드 1개면 채움, 2개+(묶음)·없음은 skipped 경고.
  - `run(... , stats_files=None)`: 발주자료 행에 stats 병합, **5-tuple 반환**(out, stats, sheets, units, merge_info). merge_info={"added", "skipped"}.
- `app/pages/1_파일처리.py` (1fd4d48): 천년경영 탭에 ④ 선택 업로더(accept_multiple_files, type xls/xlsx/html). run 5-tuple 언패킹. 병합 N행 info + 제외(묶음) 경고 표.
- `tests/test_cheonnyeon_upload.py` (f6399bb): `test_parse_sales_stats_basic`(콤마정제·단일코드보정·묶음스킵)·`test_stats_routing_retail_and_jt`(리테일전체/제이티전체 분배·H=F/D) 추가. golden 픽스처를 신규시트(골든에 없음)에 빈목록 가드.

## 검증
- 실파일(`판매처상품매출통계_…_제이티_리테일.xls`, HTML형) parse: **11행 파싱·1행 스킵**. 코카콜라제로 빈코드→31-22-02 보정→제이티전체(3행). 리테일앤인사이트 8행→리테일전체. 티오피(24-174|24-175) 묶음→skipped 경고.
- process 분배 + generate_output_xlsx **end-to-end**: 총 29시트(전체15+낱개14), 리테일전체 8행, H=F/D(런천미트 248400/5=49680·D=1행은 E와 일치).
- xlsx(PK) 분기도 파싱 OK. 신규 테스트 3종 로컬 통과.
- ast.parse 3파일 OK.

## 다음 · 상태
- ✅ 완료·커밋. **⚠️ core(cheonnyeon_upload) 변경 → 재배포(1~2분) 후 Reboot app 1회 필요**(페이지가 import). Reboot 후 사용자 실사용 확인 대기: ④에 이 파일 올려 실행 → 리테일전체/제이티전체 분배·묶음 경고 표시.
- ★ 관찰(비차단): 이 stats export에서 D>1 행의 평균단가(E) ≠ F/D (런천미트 E=9936 vs F/D=49680). H=F/D는 사용자 확정 규칙이라 그대로 출력. 숫자 이상하면 사용자가 잡기로(기존 원칙).
- 백로그: 묶음(코드 2개+) 행 자동 분할 — 분할 규칙 불명확해 현재 경고만. 규칙 생기면 split 구현.

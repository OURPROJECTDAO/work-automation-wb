# 2026-06-10 invoice-fill 올웨이즈 운송장번호 int+General 수정

## 무엇
올웨이즈 배송처리 최종 출력 시트의 운송장번호가 텍스트(str)로 출력되던 것을 숫자(int)+일반(General) 서식으로 변경.

## 왜
사용자 요청. 출력 파일에서 운송장번호가 텍스트 값으로 저장돼 Excel이 좌정렬/숫자저장경고로 표시.
일반(General) 숫자값으로 출력되어야 함.

## 변경 (app repo commit 743f0a4)
- `CHANNEL_CONFIG["올웨이즈"]`: `invoice_as_text: True` 제거 (디폴트 False = int 경로).
- `_write_template_xlsx`: as_text 분기를 if/else로 재구성.
  - as_text=True: str값 + number_format="General" (배민 등 유지)
  - as_text=False: int값 + number_format="General" 명시 추가 (기존 '@' 서식 잔류 방어)

## 영향
- 올웨이즈: 운송장번호 → int(숫자값) + General 서식. 우정렬, 경고 없음.
- 배민상회: invoice_as_text=True 유지 → str+General 그대로(무영향).
- 식봄(.xls): _write_template_xls 경로, 무관.
- 캐시노트: invoice_as_text 없음(False), 이제 number_format="General" 명시 추가됨 — 무영향(기존도 숫자 정상이었음).

## 검증
코드 dry-run 패치 확인 + app repo 커밋 정상.
배민 to_invoice_text/General 경로 영향 없음 확인.

## 다음 / 상태
완료. 실 파일로 운송장번호 숫자 확인 권장.

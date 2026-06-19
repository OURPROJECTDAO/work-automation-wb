# 2026-06-19 invoice-fill 올웨이즈 송장 셀 서식 @→일반(General) 복귀

## 무엇
올웨이즈 배송(송장) 업로드 양식에서 운송장번호 셀 서식을 텍스트(@)에서 일반(General)으로 되돌림.

## 왜
사용자: "올웨이즈 채널 송장 란을 일반 서식으로 바꿔야 하나봐" + 골든 파일(올웨이즈20260619배송.xlsx) 제공.
골든 실측 = 운송장번호(W열) 값은 숫자(int, 537129279982 등) + 셀 서식 General, 택배사(V) 한진택배 General.
즉 올웨이즈가 요구하는 송장 서식이 0611의 @(텍스트)에서 다시 General로 바뀐 것(업로드 거부 회피).

## 변경
- core/workflows/invoice_fill.py: CHANNEL_CONFIG["올웨이즈"]에서 `"invoice_cell_format": "@"` 키 **제거**.
  - 제거 효과: `cfg.get("invoice_cell_format","General")`이 General 반환 + invoice_as_text 미설정 → 값 int 유지.
  - 결과 = int값 + General = 골든 일치.
  - 커밋 1e1cd34.
- 코드 로직(_write_template_xlsx 값/서식 두 축 분기)은 무변경 — 설정값만 빠짐.

## 검증
- 골든 5/5(데이터행) 운송장 = int + General, 택배사 General 확인.
- 수정 후 cfg: invoice_cell_format 없음 → get 기본 General, invoice_as_text=None → int. 골든과 정확히 일치.
- ast.parse 통과·교체 1회.

## 다음·상태
- status=완료. 재배포(1~2분) 자동 반영. invoice_fill은 페이지(5_송장처리.py)가 import하는 core 모듈 → **안 보이면 Reboot 1회**(설정 dict 변경이라 보통 자동반영되나 모듈 캐시 시 1회).
- 사용자 실업로드 확인 대기.
- 교훈: **채널이 요구하는 송장 값타입/셀서식은 시기별로 바뀔 수 있음** — 업로드 거부 시 골든 받아 두 축(int/str · General/@) 재대조. 올웨이즈 서식 이력 0608 문자열 → 0610 int+General → 0611 int+@ → 0619 int+General.

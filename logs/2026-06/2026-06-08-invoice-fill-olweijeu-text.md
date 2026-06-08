# 2026-06-08 invoice-fill 올웨이즈 운송장번호 문자열 기입 정정

## 무엇
올웨이즈 채널 송장처리에서 운송장번호를 **숫자(int)**로 기입하던 것을 **문자열+일반(General)** 기입으로 정정.
CHANNEL_CONFIG["올웨이즈"]에 `"invoice_as_text": True` 추가.

## 왜
사용자가 골든(올웨이즈20260608배송.xlsx)을 제공. 마스터(__송장0608.xlsx '송장출력')가 좌측, 올웨이즈 골든이 우측.
골든의 운송장번호(W열) 실측 = **data_type='s' (문자열) + number_format='General'**. 마스터 '송장번호' 열도 문자열.
기존 코드는 올웨이즈를 invoice_as_text 미설정 → to_invoice_number(int)로 기입해 골든과 타입 불일치.

## 변경
- repo work-automation-app: core/workflows/invoice_fill.py — 올웨이즈 config에 invoice_as_text=True 한 줄.
- write 경로는 이미 as_text 분기(to_invoice_text + cell.number_format='General') 보유 → config만으로 충족, 코드 로직 변경 없음.
- 커밋 f90ec16.

## 검증
- 골든 W열 6셀 정밀 타입 확인: 전부 data_type='s', nf='General' (예 '537052925802').
- 마스터 주문번호 ↔ 골든 주문아이디(UUID) VLOOKUP 로컬 전건 대조: **17/17 일치, 미존재 0, 불일치 0**. to_invoice_text 출력(순수 숫자 문자열)이 골든 W와 완전 동일.
- ast.parse OK.

## 다음 · 상태
- 운영 가능. 단 **core/ import 모듈 변경 → Streamlit Cloud Reboot app 필요**(페이지 .py 아님, sys.modules 캐시). 사용자에게 안내함.
- 식봄은 여전히 숫자(int). 식봄 골든 재확인은 미수행(이번 건은 올웨이즈만). 추후 식봄도 실측 권장.

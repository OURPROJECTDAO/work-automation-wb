# 2026-06-05 송장처리 — 배민 송장번호 텍스트+일반(General) 형식 픽스

## 무엇
배민 처리후 파일의 \*송장번호가 **숫자**로 들어가 업로드 거부됨 → **문자열+일반(General)** 형식으로 변경.

## 왜 / 근본
- 사용자가 배민 처리후 파일(배민배송20260605.xlsx) 제출하며 "송장번호 형식이 숫자 아니라 일반이어야 들어간다(배민)" 지적.
- 실측: 작동하는 파일의 \*송장번호 = 문자열 값 + number_format 'General'(data_type 's').
- 원인: 앞선 숫자화 픽스(to_invoice_number→int)는 식봄/올웨이즈엔 맞지만, 배민은 송장 셀이 숫자면 파서가 거부. 배민 원본 템플릿 \*송장번호 열 형식은 '@'(텍스트)인데 거기 int를 써서 부적합.

## 변경 (work-automation-app / core/workflows/invoice_fill.py)
- `to_invoice_text(v)` 헬퍼 추가: 문자열화 + '....0' float 꼬리표 제거.
- CHANNEL_CONFIG 배민상회에 `invoice_as_text: True`.
- `_write_template_xlsx`: invoice_as_text면 송장 = to_invoice_text(문자열) + `cell.number_format='General'`. 아니면 기존 숫자(int).
- `_write_template_xls`: 동일 분기(텍스트/숫자) — 향후 텍스트형 xls 채널 대비.
- 페이지 변경 없음(write_template에 cfg 전달 이미 됨).

## 검증 (실 마스터 0605 + 실파일)
- 배민: \*송장번호 전부 **문자열+General**, 택배사 한진택배, 트래킹/3시트 보존, 40/40 매칭. → 사용자 확인 파일과 동일 상태 재현.
- 올웨이즈: 운송장번호 **숫자(int) 유지**(회귀 없음).
- 식봄(.xls 합성): 송장번호 **숫자 유지**(회귀 없음).
- ast.parse 통과.

## 주의 / 다음
- import 모듈 변경 → **Streamlit Reboot 필요**.
- Reboot 후 실제 배민 처리전(암호) → 처리후 업로드까지 사용자 최종 확인.
- 교훈: 송장번호 형식(숫자 vs 텍스트/일반)은 **플랫폼 업로드 파서마다 다름** → 채널별 invoice_as_text로 관리. 신규 채널 추가 시 처리후 업로드 성공까지 확인할 것.

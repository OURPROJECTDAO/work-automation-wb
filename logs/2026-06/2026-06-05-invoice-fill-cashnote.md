# 2026-06-05 송장처리 — 캐시노트 채널 추가 (배송상태 변환 신규 동작)

## 무엇
invoice-fill 4번째 채널 **캐시노트** 추가. 신규 동작: **배송상태 값 변환(배송준비중→배송중)**.

## 캐시노트 양식 (실파일)
- 평문 xlsx, 시트 Sheet0, 안내문 행 없음(데이터 r1~). 49행, 헤더 29열.
- 컬럼: E **ORD코드**(매칭키), F **배송상태**(배송준비중), P **택배사**(빈), Q **송장번호**(빈, General형식), S 주소, W 수령인명 등.
- 멀티아이템: 49행 / 고유 ORD코드 35.

## 사용자 지정
- match_col=ORD코드, 택배사·송장번호 기입, **배송상태 배송준비중→배송중**.

## 변경 (work-automation-app / core/workflows/invoice_fill.py)
- CHANNEL_CONFIG 캐시노트 추가(status_col=배송상태, status_map={배송준비중:배송중}, addr_col=주소, recv_col=수령인명, courier=한진택배).
- status_col/status_map 신규 지원: `_write_template_xlsx`·`_write_template_xls` 출력 시 상태값 치환.
- **버그픽스**: `_parse_template_xlsx`의 read_only=True가 캐시노트 dimension 오인(A1:A1) → 헤더 1개·0행 파싱. **read_only 제거**로 해결(천년경영 스스주문 동류).

## 검증 (실 마스터 0605 + 실파일)
- 캐시노트: 49행 → 매칭 44, N/A 5삭제, keep 44. 송장(int)·택배사 한진택배·**배송상태 전부 배송중** 확인. ORD코드⟷마스터 주문번호 매칭(고유 30/35 + 멀티아이템).
- 회귀: 배민 송장 문자열 유지 / 올웨이즈 운송장 숫자 유지.
- ast.parse 통과.

## 주의 / 다음
- import 모듈 변경 → **Streamlit Reboot 필요**.
- **송장번호 형식 미검증**: 캐시노트 송장 셀 원본 General → 일단 숫자(int)로. 배민처럼 텍스트여야 할 수 있음 → 업로드 실패 시 cfg에 invoice_as_text=True 한 줄.
- courier=한진택배 가정(전 채널 공통). 다르면 cfg.courier 수정.
- Reboot 후 실제 캐시노트 처리전 → 처리후 **업로드 성공**까지 사용자 확인.
- 현재 invoice-fill 4채널: 식봄·올웨이즈·배민상회·캐시노트.

# 2026-06-05 송장처리 — 배민상회(.xlsx, 암호) 채널 추가

## 무엇
invoice-fill 3번째 채널 **배민상회** 추가. 암호 걸린 xlsx 복호화 지원.

## 배민 양식 파악 (실파일 복호화 후)
- 파일: Seller_판매사_주문_배송_목록_*.xlsx. **항상 열기 암호 "qwer"**(msoffcrypto-tool 복호화).
- 시트 3개: 주문관리목록(active)·택배사명(공통)·업로드주의사항(공통). 안내문 행 없음(데이터 r1~, 1-based r2~).
- 컬럼: A 주문번호, H **\*택배사**(빈칸), I **\*송장번호**(빈칸), J 받는분, M 도로명 주소, N 지번 주소, R \*트래킹번호 등. 헤더 `*`=필수값.
- 업로드주의사항: ① 택배사명은 '택배사명' 시트 표기 정확히 ② **출력은 암호 제거 필수**(평문) ③ `*`필드 중 택배사명·송장번호만 수정 허용(나머지 수정 시 업로드 거부).
- 멀티아이템: 같은 주문번호에 여러 품목행 존재(VLOOKUP 첫매칭으로 동일 송장 → 같은 박스, 정상).

## 사용자 확정
- 택배사=한진택배, 합포 주소=도로명 주소, match_col=주문번호(⟷ 마스터 주문번호).

## 변경 (work-automation-app)
- `core/workflows/invoice_fill.py`:
  - CHANNEL_CONFIG에 배민상회 추가(password=qwer, courier_col=\*택배사, invoice_col=\*송장번호, addr_col=도로명 주소, recv_col=받는분).
  - `decrypt_if_needed(bytes,cfg)` 신규: cfg.format=xlsx면 msoffcrypto로 암호 분기 복호화, 평문/미리푼 파일도 is_encrypted()로 허용.
- `app/pages/5_송장처리.py`: 업로드 시 `orig_bytes = decrypt_if_needed(getvalue(), cfg)`.
- requirements: msoffcrypto-tool 이미 존재(천년경영 때). 추가 불필요.

## 검증 (실 암호파일 + 합성 마스터)
- 복호화 True→평문ZIP, parse 40행/멀티아이템 10건. 매칭 13. 멀티아이템 2행 동일 송장 확인.
- 출력: 평문ZIP, 3시트 보존, *송장 전부 숫자('....0' float·int 정수화), *택배사 전부 한진택배, **\*트래킹번호 보존**(미수정), 데이터행=keep, N/A 27삭제.
- 올웨이즈 평문 xlsx·식봄 .xls는 decrypt_if_needed 무변경 통과(회귀 없음). ast.parse 통과.

## 주의 / 다음
- import 모듈 변경 → **Streamlit Reboot 필요**.
- Reboot 후 실제 배민 처리전(암호본) + 당일 마스터로 재검증(사용자). 0매칭이면 master_key 확인.
- 보안: 채널 다운로드 암호(qwer)는 PII/계정자격 아님(배민이 전 셀러 파일에 거는 고정 암호, 배민 안내문에도 명시) — 천년경영 스스주문 '1323' 선례와 동일 취급. 고객 PII는 여전히 세션 only·미저장.

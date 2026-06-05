# 워크플로우: 송장처리 / 송장번호 일괄입력 (invoice-fill)

> 이 워크플로우를 건드리기 전 이 파일을 읽는다. 전역 함정은 pitfalls.md.

## 요약
- 채널별 **'송장번호 일괄입력 템플릿'**(처리전; 송장 빈칸)에 공통 **송장 마스터**(송장출력.xlsx)의 송장번호를 VLOOKUP으로 채워, **원본 양식(.xls/.xlsx) 그대로** 출력.
- 원리는 전 채널 공통, **양식·포맷·스키마만 채널별로 다름** → `CHANNEL_CONFIG` 설정으로 흡수.
- 사용자 내부 명칭: **(채널)배송 업무** (예: 식봄 송장, 올웨이즈 배송).
- 현재 채널: **식봄**(.xls), **올웨이즈**(.xlsx).

## 코드 / UI
- `core/workflows/invoice_fill.py` (함수형, Workflow 베이스 미사용)
- UI: `app/pages/5_송장처리.py` (단일 페이지, root)
- tests/test_invoice_fill.py

## 채널 설정 스키마 (CHANNEL_CONFIG) ★
| 키 | 의미 |
|---|---|
| format | "xls"(OLE2, xlrd/xlwt) \| "xlsx"(openpyxl) |
| match_col | 처리전 템플릿에서 VLOOKUP 키 컬럼 |
| master_key | 송장 마스터에서 매칭 컬럼 (보통 주문번호) |
| courier | 택배사 열 일괄 기입값 (없으면 lookup 택배사 fallback) |
| courier_col | 택배사 컬럼명 |
| invoice_col | 송장번호 컬럼명 — **숫자 형식**으로 기입 |
| addr_col | 합포장 동일주소 판정 컬럼 |
| recv_col | 수령인 표시 컬럼 |
| has_guide_row | 헤더 다음 안내문 행 유무 (있으면 데이터 r3~, 없으면 r2~ / 1-based) |

### 현재 채널 값
- **식봄**: format=xls, match_col=상품주문번호, master_key=주문번호, courier=한진택배, courier_col=택배사, invoice_col=송장번호, addr_col=배송지, recv_col=수취인명(받는사람), has_guide_row=True.
- **올웨이즈**: format=xlsx, match_col=주문아이디, master_key=주문번호, courier=한진택배, courier_col=택배사, invoice_col=**운송장번호**, addr_col=주소, recv_col=수령인, has_guide_row=False.

## 처리 흐름 (2-phase + 합포장 게이트)
1. 공통 송장 마스터(.xlsx, 시트 '송장출력') 세션 적재 — **PII 포함, 서버 미저장**.
2. 채널 처리전 템플릿 업로드(포맷=cfg.format) → `parse_template` → `vlookup_fill`(match_col ⟷ master_key, 첫 매칭) → 택배사·송장번호.
3. N/A 행: 동일 addr_col(NFC+trim)에 송장 채워진 박스 있으면 **합포장 후보** → 사용자가 어느 박스인지 선택(자동 불가). 없으면 독립 N/A.
4. `apply_decisions` → `finalize` → `write_template`: 잔존 N/A 행 삭제 후 원본 양식으로 출력 + N/A 건수 보고.

## 입출력 포맷별 처리 ★중요
- **xls**(식봄): 진짜 OLE2 BIFF .xls(코드페이지 949) — **마켓 HTML-테이블 .xls 아님**(pitfalls .xls=HTML 함정과 구분). xlrd 읽기, xlwt로 헤더+안내문+데이터 재작성(셀타입 보존).
- **xlsx**(올웨이즈): openpyxl. 출력은 **원본 .xlsx를 in-place 편집**(서식 완전 보존) — 송장/택배사 열 기입 후 잔존 N/A 행을 아래→위로 delete_rows. 인덱스 정렬 위해 parse 시 빈 행도 안 건너뜀.
- **행 정렬**: parsed['rows'][i] = 엑셀 행(base+i). base = has_guide_row면 3, 아니면 2(1-based).

## 전용 함정
- **택배사·송장번호 출력 규칙**: 택배사 = courier 일괄(없으면 lookup _택배사). 송장번호 = `to_invoice_number`로 **숫자**(전부 숫자면 int, '....0' float 꼬리표 제거). (2026-06-05)
- **포맷 분기**: parse/write는 cfg.format으로 xls/xlsx 분기. 새 채널이 또 다른 포맷이면 `_parse_template_*`/`_write_template_*` 추가.
- **올웨이즈 invoice_col은 '운송장번호'**(식봄은 '송장번호'). courier_col은 둘 다 '택배사'.
- VLOOKUP은 **첫 매칭만**. NFC 정규화 필수(전역 한국어 함정).
- 합포장 자동 판정 불가 — 같은 주소 박스 여럿이면 사람만 앎. 반드시 사용자 선택.
- **master_key 가정**: 올웨이즈 주문아이디(UUID)가 마스터 '주문번호' 열에 들어있다고 가정. 실제 마스터 컬럼명이 다르면 0 매칭 → cfg.master_key 수정.

## 채널 추가 방법
`CHANNEL_CONFIG`에 위 스키마대로 한 채널 dict 추가. 양식이 기존 포맷(xls/xlsx)이면 코드 수정 불필요. 새 포맷이면 parse/write 분기 함수만 추가.

## 관련 로그
- logs/2026-06/2026-06-05-invoice-fill-courier-number.md (택배사 일괄·송장 숫자 + 최초 문서화)
- logs/2026-06/2026-06-05-invoice-fill-olweijeu-xlsx.md (포맷/스키마 일반화 + 올웨이즈 채널)

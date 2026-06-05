# 워크플로우: 송장처리 / 송장번호 일괄입력 (invoice-fill)

> 이 워크플로우를 건드리기 전 이 파일을 읽는다. 전역 함정은 pitfalls.md.

## 요약
- 채널별 **'송장번호 일괄입력 템플릿'**(.xls, 송장번호 빈칸)에 공통 **송장 마스터**(송장출력.xlsx)의 송장번호를 VLOOKUP으로 채워, 원본 .xls 양식 그대로 출력.
- 원리는 전 채널 공통, 템플릿 양식만 다름. 채널 추가 = `CHANNEL_CONFIG`에 한 줄.
- 사용자 내부 명칭: **(채널)배송 업무** (예: 식봄 송장).
- 현재 채널: **식봄** (match_col=상품주문번호 ⟷ master_key=주문번호, courier=한진택배).

## 코드 / UI
- `core/workflows/invoice_fill.py` (워크플로우 로직, Workflow 베이스 미사용 — 함수형)
- UI: `app/pages/5_송장처리.py` (단일 페이지, root)
- tests/test_invoice_fill.py

## 처리 흐름 (2-phase + 합포장 게이트)
1. 공통 송장 마스터(.xlsx, 시트 '송장출력') 세션 적재 — **PII 포함, 서버 미저장**.
2. 채널 처리전 템플릿(.xls) 업로드 → `vlookup_fill`: match_col ⟷ master_key 첫 매칭 → 택배사·송장번호.
3. N/A(매칭 실패) 행: 동일 배송지(NFC+trim)에 송장 채워진 박스 있으면 **합포장 후보** → 사용자가 어느 박스인지 선택(자동 불가). 없으면 독립 N/A.
4. `apply_decisions` → `finalize`: 잔존 N/A 행 삭제 후 원본 양식으로 출력 + N/A 건수 보고.

## 입출력 포맷 ★중요
- 입력 처리전·출력 처리후 = **진짜 OLE2 BIFF .xls** (Composite Document, 코드페이지 949). **마켓 HTML-테이블 .xls 아님**(pitfalls의 .xls=HTML 함정과 구분). 읽기 `xlrd`, 쓰기 `xlwt`.
- 양식: r0=헤더, r1=안내문("수정/삭제 불가" 등), r2+=데이터. 셀 타입 보존(`parse_template_xls`가 types 저장 → 출력 시 숫자 셀 숫자로 재현).
- 식봄 양식 컬럼(15): A상품주문ID B상품주문번호 C주문번호 D결제일시 E주문일시 F구매자명 G구매자연락처 H수취인명(받는사람) I수취인연락처 J상품명 K수량 L배송지 M배송방법 **N택배사 O송장번호**. 시트명 "송장번호 일괄입력 템플릿".

## 전용 함정
- **택배사(N열)·송장번호(O열) 출력 규칙** (2026-06-05 픽스):
  - 택배사 = 채널 `CHANNEL_CONFIG[ch]["courier"]` 일괄 기입(식봄=한진택배). courier 미설정 채널은 lookup `_택배사` fallback. (이전 코드는 택배사 열을 아예 안 채웠음 — 원본 빈값 그대로 나감.)
  - 송장번호 = **숫자 형식**(`to_invoice_number`로 int 변환, '....0' float 꼬리표 제거). 이전엔 `str()` 텍스트로 나가 일부 업로드에서 거부.
  - 두 규칙 모두 `write_template_xls`에서 처리. 채널 courier는 `5_송장처리.py`가 `cfg.get("courier")`로 전달.
- VLOOKUP은 **첫 매칭만**(분할배송 첫 박스 의미). `build_master_lookup`이 OrderedDict로 첫 키만 유지.
- 배송지/주문번호 매칭 전 **NFC 정규화**(nfc()) — 전역 한국어 함정 참조.
- 합포장은 **자동 판정 불가** — 같은 주소 박스가 여럿이면 사람만 어느 박스인지 앎. 반드시 사용자 선택.

## 채널 추가 방법
`CHANNEL_CONFIG`에 `"<채널>": {"match_col": "<처리전 키컬럼>", "master_key": "주문번호", "courier": "<택배사>"}` 한 줄. 양식이 같으면 그걸로 끝(역추적 불필요). courier가 채널마다 다르면 지정.

## 관련 로그
- logs/2026-06/2026-06-05-invoice-fill-courier-number.md (택배사 일괄·송장 숫자 픽스 + 워크플로우 최초 문서화)

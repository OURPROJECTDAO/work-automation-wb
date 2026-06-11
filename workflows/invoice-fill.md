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
| password | (선택) 다운로드 파일에 항상 걸린 열기 암호 — 복호화용 |
| invoice_as_text | (선택) True면 송장번호를 **문자열+일반(General)** 형식으로 기입(숫자셀 거부 채널). 기본 False=숫자(int) |
| invoice_cell_format | (선택) 송장 셀의 number_format (기본 "General"). **"@"=텍스트 서식**. 올웨이즈는 값=숫자(int)지만 셀 서식만 텍스트(@)여야 업로드 성공. as_text(값 자체 문자열화)와 독립 — 이쪽은 값 유지·서식만 바꿈 |
| status_col | (선택) 출력 시 값 변환할 상태 컬럼명 |
| status_map | (선택) {원값:새값} 매핑 (예: {"배송준비중":"배송중"}) |

### 현재 채널 값
- **식봄**: format=xls, match_col=상품주문번호, master_key=주문번호, courier=한진택배, courier_col=택배사, invoice_col=송장번호, addr_col=배송지, recv_col=수취인명(받는사람), has_guide_row=True.
- **올웨이즈**: format=xlsx, match_col=주문아이디, master_key=주문번호, courier=한진택배, courier_col=택배사, invoice_col=**운송장번호**, addr_col=주소, recv_col=수령인, has_guide_row=False, **invoice_cell_format="@"**. 운송장번호 = **값은 숫자(int) 유지 + 셀 서식만 텍스트(@)**. (서식 이력: 0608 문자열값 → 0610 int+General → **0611 int값+@서식**으로 재수정. 사용자 실측: 셀 서식만 텍스트로 바꾸면 업로드 성공, 골든 8/8 대조)
- **배민상회**: format=xlsx(**암호 qwer 항상**), match_col=주문번호, master_key=주문번호, courier=한진택배, courier_col=**\*택배사**, invoice_col=**\*송장번호**, addr_col=도로명 주소, recv_col=받는분, has_guide_row=False, **invoice_as_text=True**. 멀티시트(주문관리목록+택배사명+업로드주의사항).
- **캐시노트**: format=xlsx(평문), match_col=**ORD코드**, master_key=주문번호, courier=한진택배, courier_col=택배사, invoice_col=송장번호, addr_col=주소, recv_col=수령인명, has_guide_row=False, **status_col=배송상태 / status_map={배송준비중→배송중}**. 송장번호 숫자(int) — 업로드 정상 확인(2026-06-05).

## 처리 흐름 (2-phase + 합포장 게이트)
1. 공통 송장 마스터(.xlsx, 시트 '송장출력') 세션 적재 — **PII 포함, 서버 미저장**.
2. 채널 처리전 템플릿 업로드(포맷=cfg.format) → `parse_template` → `vlookup_fill`(match_col ⟷ master_key, 첫 매칭) → 택배사·송장번호.
3. N/A 행: 동일 addr_col(NFC+trim)에 송장 채워진 박스 있으면 **합포장 후보** → 사용자가 어느 박스인지 선택(자동 불가). 없으면 독립 N/A.
4. `apply_decisions` → `finalize` → `write_template`: 잔존 N/A 행 삭제 후 원본 양식으로 출력 + N/A 건수 보고.

## 입출력 포맷별 처리 ★중요
- **xls**(식봄): 진짜 OLE2 BIFF .xls(코드페이지 949) — **마켓 HTML-테이블 .xls 아님**(pitfalls .xls=HTML 함정과 구분). xlrd 읽기(**`ignore_workbook_corruption=True` 필수** — 식봄 export OLE2 디렉터리가 비표준이라 기본 파서는 CompDocError로 송장 0건 기입; 0608 픽스), xlwt로 헤더+안내문+데이터 재작성(셀타입 보존).
- **xlsx**(올웨이즈): openpyxl. 출력은 **원본 .xlsx를 in-place 편집**(서식 완전 보존) — 송장/택배사 열 기입 후 잔존 N/A 행을 아래→위로 delete_rows. 인덱스 정렬 위해 parse 시 빈 행도 안 건너뜀.
- **행 정렬**: parsed['rows'][i] = 엑셀 행(base+i). base = has_guide_row면 3, 아니면 2(1-based).
- **암호 채널(배민상회)**: 다운로드 파일에 항상 열기 암호("qwer"). 업로드 시 `decrypt_if_needed`(msoffcrypto-tool)로 복호화 후 평문 bytes를 orig_bytes로 사용. **출력은 평문**(배민 업로드 주의사항: 암호 제거 필수). 평문 파일·미리 푼 파일도 is_encrypted() 분기로 허용.
- **배민 멀티시트**: 주문관리목록(active)만 편집, 택배사명(공통)·업로드주의사항(공통) 보존(openpyxl in-place라 자동 보존).
- **배민 ★ 필드 주의**: 헤더 `*`는 필수값. **택배사명·송장번호만 수정 허용**, 그 외 `*`필드(\*트래킹번호·\*주문상품상세번호·\*배송상품번호)는 수정 시 업로드 거부 → courier_col/invoice_col만 기입하므로 자동 충족.
- **배민 멀티아이템 주문**: 같은 주문번호에 여러 품목행(예: 코카콜라+사이다) → VLOOKUP 첫매칭으로 전부 동일 송장(같은 박스). 정상 동작.

## 전용 함정
- **송장번호 형식은 채널별**: 식봄 = **int+General** (`to_invoice_number`, number_format 기본 General). **배민 = 문자열값+일반(General)** (`to_invoice_text`, `invoice_as_text=True`) — 배민 원본 \*송장번호 열은 '@'(텍스트) 형식이라 숫자값 넣으면 업로드 거부. **올웨이즈 = int값 유지 + 셀서식만 @(텍스트)** (`invoice_cell_format="@"`) — 값은 숫자인데 셀 서식이 텍스트여야 업로드 성공(사용자 실측 0611). 캐시노트 = int+General. **세 축이 독립**: ①값을 문자열로(as_text) ②셀 서식(invoice_cell_format). `_write_template_xlsx`는 값 분기(as_text)와 서식(`cfg.get("invoice_cell_format","General")`)을 따로 적용. (이력: 올웨이즈 0608 문자열값 → 0610 int+General → 0611 int값+@서식)
- **택배사 출력**: courier 일괄(없으면 lookup _택배사).
- **상태 컬럼 변환(캐시노트)**: status_col/status_map 설정 시 출력 행의 상태값 치환(배송준비중→배송중). write 단계에서 적용, 다른 채널은 미설정→무영향.
- **★ xlsx read_only 차원 오인**: 일부 채널 파일(캐시노트)은 dimension 레코드가 잘못돼 `load_workbook(read_only=True)`가 A1:A1로 오인 → 헤더 'X 1개'·0행. `_parse_template_xlsx`는 **read_only 미사용**(비 read_only)로 calculate_dimension 정확히. (천년경영 스스주문과 동류 함정)
- **포맷 분기**: parse/write는 cfg.format으로 xls/xlsx 분기. 새 채널이 또 다른 포맷이면 `_parse_template_*`/`_write_template_*` 추가.
- **올웨이즈 invoice_col은 '운송장번호'**(식봄은 '송장번호'). courier_col은 둘 다 '택배사'.
- VLOOKUP은 **첫 매칭만**. NFC 정규화 필수(전역 한국어 함정).
- 합포장 자동 판정 불가 — 같은 주소 박스 여럿이면 사람만 앎. 반드시 사용자 선택.
- **master_key 검증완료(2026-06-05)**: 0605 실 마스터로 올웨이즈 13/13·배민상회 40/40(고유 18/18) 전건 매칭 확인. 올웨이즈 주문아이디(UUID)·배민 주문번호 모두 마스터 '주문번호' 열에 그대로 존재. 신규 채널은 동일하게 match_col↔'주문번호'로 시작.

## 채널 추가 방법
`CHANNEL_CONFIG`에 위 스키마대로 한 채널 dict 추가. 양식이 기존 포맷(xls/xlsx)이면 코드 수정 불필요. 새 포맷이면 parse/write 분기 함수만 추가.

## 공통 마스터(송장출력) 참조
- 시트 '송장출력', 컬럼 10: 상태·관리번호·발주일·**판매처**·**주문번호**·수령자·주소·상품명·**택배사**·**송장번호**. (수령자·주소 = PII, 세션 only·미저장)
- 모든 채널 매칭 키 = 마스터 '주문번호'. 채널의 주문식별자(상품주문번호/주문아이디/주문번호)가 여기에 그대로 들어감(0605 검증).
- 판매처 값(채널 식별)에 등장: 식봄(마켓보로)·올웨이즈·배민상회·캐시노트·쿠팡(자동)·G마켓·스마트스토어·옥션·알리익스프레스자동·태동마트자사몰.
- **다음 채널 후보 = 캐시노트** (0605 마스터에 44건 존재, CHANNEL_CONFIG 주석 placeholder). 처리전 샘플 받으면 추가.

## 관련 로그
- logs/2026-06/2026-06-05-invoice-fill-courier-number.md (택배사 일괄·송장 숫자 + 최초 문서화)
- logs/2026-06/2026-06-05-invoice-fill-olweijeu-xlsx.md (포맷/스키마 일반화 + 올웨이즈 채널)
- logs/2026-06/2026-06-08-invoice-fill-olweijeu-text.md (올웨이즈 운송장번호 문자열 기입 정정 — 골든0608 대조)
- logs/2026-06/2026-06-08-invoice-fill-sikbom-compdoc.md (식봄 .xls CompDocError 읽기 픽스 — ignore_workbook_corruption, 64/68 매칭)
- logs/2026-06/2026-06-11-invoice-fill-olweijeu-cellformat.md (올웨이즈 송장 셀 서식 @ — 값=숫자 유지·서식만 텍스트, invoice_cell_format 키 신설, 골든 8/8)

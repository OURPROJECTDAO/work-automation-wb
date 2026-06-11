# 2026-06-11 channel-margin-monitor: 캐시노트 가격변경 양식 추가

## 무엇
캐시노트 가격 일괄변경 양식(`(캐시노트)양식`) 생성 기능 추가. 모니터에서 선택 상품 → 권장가로 '옵션 일괄수정' 양식 채워 내보내기. 식봄 append 로직을 채널 무관 헬퍼로 일반화(식봄·캐시노트 공용).

## 왜
state.md 다음 한 수 — 캐시노트 가격변경(이전 세션 보류). 사용자가 양식 실물(`캐시노트_가격바꾸기.xlsx`) 제공 + 채움 규칙 지정.

## 사용자 지정 채움 규칙
- A(상품코드=OFR)·D(옵션코드=SKU): **다운로드 Q(17)·R(18)에 있음**. listing엔 미저장이었음("대시보드는 날렸지만") → extra_cols로 보존.
- **F(변경타입)="수정"·L(진열여부)="Y"·N(재고수량)=9999 고정.**
- G(판매단가)=권장가 · H(할인전단가)=max(정가,권장가) · O(입점사 관리코드)=관리코드.
- (B 상품명·C 순서·E 옵션명·P 모델명 = 공백. 양식 예시행과 동일.)

## 변경 (work-automation-app)
- `core/workflows/channel_margin_monitor.py` (→b06f9b9)
  - 캐시노트 config: `extra_cols{오퍼코드:17, 옵션코드:18}`(다운로드 OFR/SKU 보존) + `price_form`(mode append, template cashnote_price_template.xlsx, sheet '(캐시노트)양식', data_start 4, cols/source/fixed{6:수정,12:Y,14:9999}, price_field 판매단가, jeong_field 할인전단가).
  - `parse_download`: extra_cols 캡처 + 오퍼코드/옵션코드 기본 공백(전 채널 rec에 키 존재).
  - `LISTING_COLS` + recs_to_csv + csv_text_to_recs: 오퍼코드·옵션코드 컬럼 추가(구 listing CSV는 .get 기본공백 — 하위호환).
  - **`build_append_items(pf,rows,recs,pids)` 신규**: source(양식필드→소스키, row 우선)·price_field·jeong_field로 items+preview+skipped 생성. 채널 무관.
  - `build_price_form_append` 범용화: cols{필드→컬럼} writer + fixed{컬럼→값}. 식봄 내부 정가max·int 로직은 build_append_items로 이동.
  - 식봄 price_form도 source 기반으로 갱신(동작 동일 — 합성 양식 회귀 PASS).
- `app/pages/6_채널마진모니터.py` (→5c38f7c): append 분기를 `cmm.build_append_items` 호출로 교체(식봄 인라인 제거). 양식 안내 캡션 채널 동적.
- `reference/cashnote_price_template.xlsx` (→5e54519): 업로드 양식 그대로 커밋(빌드시 예시행 r4~ 제거).

## 검증 (실데이터 end-to-end)
- 다운로드 → 오퍼/옵션코드 100% 캡처 → listing CSV 라운드트립 보존 ✅.
- 권장가 표본 5건 양식 생성: A=OFR·D=SKU·F=수정·G=권장가·H=정가(≥G)·L=Y·N=9999·O=관리코드 전건 일치, 예시행 제거·잔행 0, max_row=헤더3+데이터5 ✅.
- 식봄 회귀(합성 양식): items·양식(A상품번호·B코드·C상품명·D정가≥판매단가·E='n'·F판매단가)·예시행 제거 PASS — 동작 보존 ✅.
- ast.parse OK(core+page).

## 다음 / 상태
- **운영 가능**. ⚠️ **core 수정 → Reboot app 1회**. 캐시노트 **첫 '상품관리 갱신' 필요**(이때부터 오퍼/옵션코드 listing 저장 — 기존 listing 없으면 무영향). 갱신 후 표 선택 → '가격 일괄변경 양식 생성' → .xlsx 다운로드 → 캐시노트 업로드.
- 캐시노트 모니터+가격변경 모두 완료. 다음 채널: 쿠팡·알리(레시피 동일, 가격변경 양식 있으면 price_form만).

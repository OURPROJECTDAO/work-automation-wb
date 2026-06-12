# 2026-06-12 channel-margin-monitor: ESM 가격변경(append) 추가

## 무엇
ESM(G마켓) 가격 일괄변경 양식 생성 추가. 8채널 모니터 / **7채널 가격변경**(스마트스토어·식봄·캐시노트·배민·쿠팡·올웨이즈·ESM).

## 왜
ESM 모니터에 이어 가격변경 구현(roadmap). 권장가를 ESM '(ESM)양식'에 기입.

## 양식 구조 (실물 esm가격바꾸기.xlsx)
- 시트 '(ESM)양식', **A=순번(1~500 데코)·B=사이트 상품번호(필수,키)·C=판매가(필수)**. r1~5 보호블록(r1 안내 '상품정보 6행부터 입력, 1~5행 삭제/변경 시 오류'·r2 헤더·r3 필수·r4 안내·r5 예시 'D200000000'/100000) → **data_start 6**. 정가/할인전단가 칸 없음. 외부링크 없음.
- **★ 양식 키 = B 사이트 상품번호(다운로드 col2)** — 모니터키 A(마스터상품번호)와 다름(양식B ∩ 다운로드B 8/8·∩A 0). → **extra_cols{사이트상품번호:2}로 listing 보존** 필수.

## 변경 (core + template, 페이지 무수정)
- `reference/esm_price_template.xlsx` 신규: 업로드 양식에서 r6+ 데이터 제거(클린 r1~5)·row_dimensions 정리.
- core CHANNEL_CONFIG['esm']:
  - **extra_cols{사이트상품번호:2}** (다운로드 B 보존, _pid 정수화).
  - **price_form**(append, esm_price_template.xlsx, '(ESM)양식', data 6, **seq_col 1**(A순번 1,2,3…), cols{사이트상품번호:2,판매가:3}, source{사이트상품번호:사이트상품번호}, price_field 판매가(=권장가), **int_fields[사이트상품번호]**(B 숫자셀), **jeong_field 없음**(정가 칸 없음)).
- `build_price_form_append`: **`seq_col`** 지원 추가(지정 컬럼에 1,2,3… 순번 기입). 미설정 채널 무영향.
- 페이지: 무수정 — append 분기·stale 가드(extra∩source) 모두 제네릭이라 ESM 자동 커버.

## 검증 (end-to-end)
- parse 사이트상품번호 보존 + CSV 라운드트립 일치(_deflo). 양식 30표본 — **B(사이트상품번호)=다운로드B·C=권장가 전건 일치(0 불일치)**, B/C 전건 숫자셀, A 순번 1..N, r1~5 보호블록 보존, 예시행 제거, max_row 정확, 외부링크 0, skipped 0. preview 정가 공백(jeong 없음). ast.parse OK.

## 다음·상태
- **⚠️ core 수정 → Reboot app 1회 필요.**
- **★ 기존 ESM listing 있으면 '전체 교체' 1회 재파싱 필요** — 사이트상품번호는 이 변경 후 저장본에만 존재(stale 가드가 경고). 단 ESM은 아직 첫 갱신 전이라 무관.
- 가격변경 흐름: 모니터 표에서 선택 → '가격 일괄변경 양식 생성' → '(ESM)양식'(B=사이트상품번호·C=권장가) 다운로드 → ESM Plus 업로드.
- 미검증: ESM 실업로드 inlineStr 허용 여부(openpyxl 저장 — 식봄/캐시노트/배민/올웨이즈와 동일. 거부 시 쿠팡식 네이티브 수술). 정가 없어 무늬용 가짜정가 미생성(양식 자체에 칸 없음).

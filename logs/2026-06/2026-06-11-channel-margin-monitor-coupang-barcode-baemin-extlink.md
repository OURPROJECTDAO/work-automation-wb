# 2026-06-11 channel-margin-monitor — 쿠팡 로켓그로스 제외 + 배민 양식 외부링크/옵션번호 수정

## 무엇/왜
사용자 피드백 2건.
1. **쿠팡 판매자택배 모니터링**: 쿠팡 상품 다운로드의 **E열(바코드)** 은 판매자택배 상품이면 항상 공백. 값이 있으면 **로켓그로스**(배송방식 다름, 미매칭 아님)라 판매자택배 마진 모니터 대상이 아님 → 모니터에 올라오면 안 됨.
2. **배민 가격변경 출력파일 에러**: 숫자는 다 맞는데 엑셀에서 열 때 경고. 원인 = `baemin_price_template.xlsx`가 원본 마스터 통합문서를 가리키는 **고아 외부참조**(externalLinks)를 품고 있고, openpyxl 저장이 이를 그대로 전파 → "외부 연결 업데이트 불가" 경고. (데이터 셀은 전부 inlineStr/숫자 리터럴이라 수식 의존 없음.) 부수로 **C열(옵션번호)이 `510609.0` float**로 찍힘(숫자ID float 함정 — extra_cols가 `_nfc`로 숫자셀 읽음).

## 변경 (core/workflows/channel_margin_monitor.py)
- **쿠팡 config**: `exclude_row_if_col_filled: 5`(E열) 추가.
- **parse_download**: `excl_col` 처리 — 그 컬럼에 값 있으면 행 자체 skip(쿠팡 로켓그로스 제외). 채널 무관 일반 플래그.
- **parse_download extra_cols**: `_nfc` → `_pid`(정수값 float만 int화). 옵션번호 `510609.0`→`510609`. 수수료raw `4.5`·옵션명 텍스트는 불변.
- **`_deflo` 헬퍼 신설 + csv_text_to_recs**: else 분기 `_deflo(_nfc(v))`. 구 listing에 이미 `510609.0`으로 저장된 숫자ID를 **재파싱 없이** 라운드트립에서 정수 복원(`-?\d+\.0`만). 양식 출력 즉시 정상화.
- **`_strip_external_links` 헬퍼 신설**: xlsx zip에서 ① xl/externalLinks/* ② workbook.xml `<externalReferences>` ③ rels externalLink 관계 ④ Content_Types override 제거. 외부링크 없으면 무손실 no-op.
- **3개 출력 빌더**(build_price_form_append·build_bulk_price_xlsx·build_filter_price_xlsx) return을 `_strip_external_links`로 감쌈(방어). cashnote/sikbom 템플릿·쿠팡 raw는 외부링크 없어 no-op.

## 변경 (reference/baemin_price_template.xlsx)
- 고아 외부링크 4종 제거한 정리본 커밋(템플릿 자체도 깨끗하게 열림). cashnote/sikbom 템플릿은 원래 외부링크 0건 — 무관.

## 검증
- 쿠팡 합성 다운로드 4건(바코드 2건/공백 2건) → parse 결과 2건(로켓그로스 OPT1002·OPT1004 제외, 판매자택배 OPT1001·OPT1003 포함). 타 채널 exclude=None 무영향.
- 배민 템플릿: ext (2parts,ref,rels,ct) → (0,0,0,0), `(배민)양식` 시트 보존, openpyxl 정상 로드.
- append 양식 end-to-end: 출력 외부링크 0. csv 라운드트립 옵션번호 `510609.0`→`510609`(수수료raw `4.5` 불변), 라운드트립 rec로 생성한 양식 C2=`510609`(정수). J2 변경판매가·E2 관리코드 정상.
- ast.parse OK.

## 다음/상태
- **운영 반영**: core import 모듈 수정 → **Reboot app 1회 필요**.
- **쿠팡 기존 listing 보정**: 로켓그로스 행은 바코드를 저장한 적이 없어 소급 필터 불가 → 쿠팡 '상품관리 갱신 → 전체 교체' 1회 재파싱해야 기존 로켓그로스 행이 listing에서 빠짐('신규만 추가'는 기존 행 유지). 재파싱 후엔 자동 제외.
- **배민 기존 listing 옵션번호**: `_deflo` 라운드트립으로 재파싱 없이 양식 생성 시 정수 복원됨(추가 조치 불필요). 새 다운로드는 `_pid`로 처음부터 정수.
- 미해결(기존): baseline↔product_master 조인 갭.

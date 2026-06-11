# 2026-06-11 channel-margin-monitor: 캐시노트 가격변경 양식 A/D 공란 — 구 listing 스키마

## 증상
캐시노트 가격변경 양식 생성 시 A(상품코드 OFR)·D(옵션코드 SKU)만 공란, 나머지(F·G·H·L·N·O)는 정상.

## 원인 (코드 아님 — 데이터)
앱이 불러온 `listing_cashnote.csv`가 **extra_cols 도입(b06f9b9) 전**에 저장된 스냅샷이라 오퍼코드·옵션코드 컬럼 자체가 없음 → csv_text_to_recs가 "" 반환 → build_append_items가 빈 A/D 기입. O(관리코드)는 원래 listing에 있어 정상.
- 재현 확인: 구 LISTING_COLS(OFR/SKU 없음)로 CSV 생성 → 양식 A/D 공란(사용자 파일과 동일). 현재 코드로 재파싱한 listing → A/D 정상.

## 조치 / 변경 (work-automation-app)
- **사용자 조치**: 캐시노트 '📥 상품관리 갱신 → [전체 교체]' 1회 → listing 재파싱(OFR/SKU 채워짐). **'신규만 추가'(merge)는 기존 행 미채움** → 반드시 전체 교체.
- **가드 추가** `app/pages/6_채널마진모니터.py` (→79f7b69): listing 로드 후, price_form이 쓰는 extra_cols 필드(예 오퍼/옵션코드)가 저장본에 **전부 비면** st.warning('전체 교체' 안내). page-only(자동 반영). 식봄 등 extra_cols 없는 채널은 미발동.

## 교훈 (전 워크플로우 공통 가능)
- **listing/스냅샷 스키마에 컬럼을 추가하면, 추가 전 저장된 스냅샷은 그 값이 빈 채로 남는다**(append-only CSV 마이그레이션 없음). 새 필드가 다운스트림(가격변경 양식 등)에 필수면 ① 전체 재생성 안내 ② 빈 값 가드 둘 다 필요. 조용한 공란 산출물은 외부 업로드 실패로 이어짐.

## 다음 / 상태
- 가드 배포됨. 사용자 전체 교체 후 양식 A/D 채워짐 확인 예정.

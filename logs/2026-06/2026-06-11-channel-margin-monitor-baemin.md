# 2026-06-11 channel-margin-monitor: 배민상회 채널 추가 (모니터)

## 무엇
채널 마진 모니터에 **배민상회** 추가(모니터 — 가격변경 양식 미제공이라 보류). 신규 축: **상품별 수수료**(다운로드에 내장). + 스키마 유연 listing CSV(extra_cols 자동 보존).

## 왜
로드맵 다음 후보. 사용자가 상품관리 다운로드(`판매사_상품_목록_*.xlsx`, 암호 없음) + 골든(`배민_골든.xlsx`) 제공.

## 핵심 — 상품별 수수료 (앞 3채널과 결정적 차이)
- 배민상회 수수료는 **채널 단일값이 아니라 상품별**. 다운로드 **BU(73) '상품별 수수료(중개-할인)'** 에 % 내장(4.5·5.0·5.5·7.0…). 골든 J식 = `BU/100 + 0.03`(추가 고정수수료). bm_commission.csv(천년경영용)는 모니터에서 **미사용**(다운로드가 직접 보유).
- 정산식은 표준과 동일: 정산가 = 판매가×(1−수수료) + 배송비×0.967. 실택배비만 2700 표준(골든 3000/3700 미채택).

## 변경 (work-automation-app)
- `core/workflows/channel_margin_monitor.py` (→7696161)
  - CHANNEL_CONFIG['배민상회']: `commission_source="download"`·`commission_field="수수료raw"`·`commission_div=100`·`commission_add=0.03` · ship_settle 0.967 · real_ship 2700 · baseline_col 배민상회 · n_source "ref" · sheet sheet1 · header 2 · data 3 · cols{상품번호1(A),코드22(V 관리용상품명),상품명2(B),판매가24(X),정가23(W 소비자가)} · ship_fee_policy{col60(BH 배송방법),map{무료배송:0},default3000} · extra_cols{수수료raw:73}.
  - `compute`: 수수료를 행별로 — commission_source="download"면 `수수료raw/div + add`, 아니면 단일 `commission`. rate=1−comm 행별.
  - `recs_to_csv`/`csv_text_to_recs`: **스키마 유연화** — LISTING_COLS + extra_cols 키(수수료raw 등) 자동 포함/복원. 구 CSV 하위호환(누락 컬럼 기본값).
- `app/pages/6_채널마진모니터.py` (→2ee2f2d): _col_config·헤더 캡션이 단일 commission 없는 채널 허용(상품별=텍스트 표기). 구 listing 가드에 commission_field(수수료raw) 비었는지 검사 추가.

## 검증 (실데이터 골든 394/394)
- 골든∩계산 394/394(상품번호 A 키). 입력 — 판매가 394/394·배송비 394/394·**수수료(상품별 BU/100+0.03) 394/394**·N(합포) 394/394·base매입단가 392/393(1 vintage). **정산가 394/394 일치**(정산식 동일 — 실택배비만 표준차라 마진율/권장가에만 영향).
- listing 라운드트립: 수수료raw 보존 확인.
- run: 394건·미매칭0·미설정6·마진미달20·제한35·평균마진율 10.2%.
- ast.parse OK(core+page). 타 채널(스마트스토어/식봄/캐시노트) 표시 로직 회귀 없음.

## 다음 / 상태
- **운영 가능**. ⚠️ **core 수정 → Reboot app 1회**. 배민상회 **첫 '상품관리 갱신'** 필요(수수료raw 보존). 다운로드 암호 없음(송장 다운로드와 달리).
- 배민상회 가격변경 보류(양식 미제공). 재개 시 양식 실물 필요.
- 다음 채널: 쿠팡(BU식?)·알리. 동일 레시피 — 수수료가 단일이면 commission, 상품별이면 commission_source.

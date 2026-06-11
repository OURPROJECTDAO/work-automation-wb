# 워크플로우: channel-margin-monitor (채널 가격·마진 모니터)

> 이 워크플로우를 건드리기 전 이 파일을 읽는다. 전역 함정은 pitfalls.md, 공유자산 연결은 manifest.md.

## 요약
- 판매 채널의 라이브 리스팅(상품관리 다운로드)을 받아 상품별 마진율을 계산 → 기준마진 대비 이탈 탐지 + 기준마진 달성 권장가를 역산하는 모니터.
- 등록(신규)이 아니라 **운영 중 리스팅 점검**. 사용자 엑셀([1]마스터 수식 조인본) 대체.
- 상태: **운영중** — 스마트스토어(모니터+가격일괄변경) · 식봄(모니터+가격변경) · 캐시노트(모니터+가격변경) · **배민상회(모니터+가격변경, 2026-06-11; 상품별 수수료)**. 타 채널은 레시피로 점진 추가(baseline_margin이 10채널 보유).
- **표준 정산식 = 웹앱 스마트스토어형**(사용자 확정 2026-06-11). 새 채널은 골든이 다른 값을 쓰더라도 **스마트스토어 구조(2700 flat 실택배비·ceil 권장가)에 맞추고 수수료율만 채널별**로 둔다. 골든은 입력 검증용 참고(마진율/권장가는 골든과 의도적으로 다를 수 있음).

## 입력 (저장본 자동 로드, 갱신 시에만 업로드)
- **저장 listing** `reference/listing_<key>.csv`(연동데이터, app repo) 를 자동 로드 → 매번 업로드 불필요. + `.meta.json`(갱신일 KST·건수).
- **갱신**: 페이지 '📥 상품관리 갱신'에서 새 다운로드(.xlsx 전체 업로드) → [전체 교체] / [신규만 추가](merge) → API 커밋.
- 채널별 다운로드 파싱:
  - **스마트스토어** (`[일괄수정 (전체 업로드)]`): r2=헤더, r3~5=가이드, r6+=데이터. A 상품번호·B 판매자상품코드·D 상품명·F 판매가·AO(41) 기본배송비·BF(58) 즉시할인·BQ(69) 포인트·BZ(78) 판매자바코드(N).
  - **식봄** (`식봄붙여넣기` 시트): r1~3 유의사항, **r4=헤더, r5+=데이터**. A(1) 상품no(키)·B(2) 상품코드(관리코드)·F(6) 상품명·**S(19) 판매단가(=판매가)**. **즉시할인·포인트·배송비(숫자)·바코드 컬럼 없음.** P(16)=정가(취소선용, 미사용). M(13)=택배배송비'명'(숫자 아님 → 배송비는 상수 3000).
  - **캐시노트** (`상품` 시트, KCD 마켓): **r3=헤더, r4+=데이터**. A(1) ID(상품번호 키)·E(5) 입점사 관리 코드(관리코드)·C(3) 상품명·**N(14) 판매 단가(=판매가)**·O(15) 할인 전 단가(정가). F(6) 요율(=6, 수수료율). **즉시할인·포인트·바코드 컬럼 없음(식봄형).** Y(25) 배송 정책 코드 → 배송비 조건부(아래). 둘째 시트 `상품 필드값`은 드롭다운값(무관). ⚠️ ID가 숫자셀 → `_pid` 정수정규화 필수.
  - **배민상회** (`sheet1`): **r2=헤더, r3+=데이터**. A(1) 상품번호(키)·**V(22) 관리용 상품명(=관리코드)**·B(2) 상품명·**X(24) 판매가**·W(23) 소비자가(정가). **BU(73) 상품별 수수료(%) → 수수료 내장**(extra_cols 캡처). BH(60) 배송방법 → 배송비 조건부. **즉시할인·포인트·바코드 없음(식봄형).** 상품번호 숫자셀 → _pid. 암호 없음.
- listing CSV 컬럼 = 상품번호·코드·상품명·판매가·정가·배송비·즉시할인·포인트·바코드·**오퍼코드·옵션코드**(없는 채널은 0/공백). 배송비는 파싱 시점에 해소된 숫자로 저장(캐시노트 정책 조건부도 숫자로 baked). **오퍼코드(OFR)·옵션코드(SKU)** = 캐시노트 가격변경 양식 A/D용, 다운로드 Q(17)·R(18)에서 `extra_cols`로 캡처(listing에 보존, 양식 생성 시 다운로드 불필요).

## 마진 계산 (확정 공식 — 스마트스토어 표준)
```
N        = 합포량(판매배수). 스마트스토어=판매자바코드(다운로드), 그 외=hapo_multiplier(상품번호). 빈값/0→1. 분수 가능.
매입가    = (코드해석 base 4-tier) × N
판매가net = 판매가 − 즉시할인 − 포인트                 (식봄·캐시노트는 즉시할인·포인트 없음 → net=판매가)
정산액    = 판매가net × (1−수수료) + 배송비 × 0.967      (배송비: 스마트스토어=다운로드 / 식봄=상수3000 / 캐시노트=배송정책코드 조건부)
이익      = 정산액 − 매입가 − 실택배비(2700 단일)
마진율    = 이익 / 정산액
탐지      = 마진율 − 확정마진율(baseline 채널열)
권장가    = ⌈ ((매입가 + 2700)/(1−확정마진율) − 배송비×0.967) / (1−수수료) ⌉   (100원 올림)
```
- **실택배비 = 2700 단일·권장가 = 올림(ceil)** 이 표준(전 채널 공통). 합포 묶음 +700(3000/3700) 및 ROUND 반올림은 **채널 골든에 있어도 채택 안 함**(스마트스토어 기준).
- 수수료율은 채널별 단일: 스마트스토어 6% · 식봄 7% · 캐시노트 6%. **배민상회는 상품별**(다운로드 BU/100 + 0.03 추가수수료) → config `commission_source="download"`(compute가 행별 산출).
- **마진미달 판정**: `탐지 < MARGIN_UNDER_THRESHOLD`(= **-0.01**). 전 채널 공통 단일상수(core).

## 코드 해석 (매입가/재고/규격) — 4-tier (전 채널 공통, 불변)
| 코드 형태 | base 매입가 | 재고 | 규격 | 소스 |
|---|---|---|---|---|
| 박스 (`24-07`·`BT10EA-28-50` 알파뉴메릭 포함) | 박스매입단가[9] | 박스[14] | 규격[6] | product_master (관리코드[4]) |
| PC낱개 (`PC`+상품코드6자리) | 매입단가[8] | **박스[14]** | 규격[6] | product_master (상품코드[3], PC 제거). 재고=그 상품코드 행의 박스재고(낱개 아님, 2026-06-11 수정) |
| 소분 (`변환코드-원코드`) | 원박스매입단가 ÷ 내품나누기 | 원코드 박스재고 | 소분규격 | sobun.csv + product_master |
| 합포 (`코드1-CB-코드2[-CB-코드3]`) | Σ 박스매입단가 + 700 | Σ 박스재고 | 다운로드/합포규격 | -CB- 파싱 + product_master (reference 없음) |
- 최종 매입가 = base × N. **N(합포량/판매배수)과 -CB-(구성)는 직교** — 둘 다 적용.
- 식봄 검증: 485코드 = 박스429·소분39·합포(-CB-)17, **매입가 미해결 0건**(골든 합포관리 Σ+700과 일치).
- 캐시노트 검증: 골든 base매입단가 461/463 일치(2 vintage), 미매칭 4건은 빈코드(E열 관리코드 공백).

## Reference (app `reference/`)
- `baseline_margin.csv` (1,228): 관리코드 + 10채널 확정마진율(스마트스토어·자사몰·ESM·배민상회·식봄·올웨이즈·캐시노트·쿠팡·토마토·알리). 채널 열만 골라 씀. **다중채널 공유**(manifest A).
- `hapo_multiplier.csv` (3,339): **상품번호·합포량·채널**. 바코드 없는 채널의 N 공급(스마트스토어 판매자바코드의 외부판). **상품번호 단일키**(플랫폼마다 고유 → **채널 무관 조회**, 채널열 비어도 조회됨), 미등록 N=1, 분수 가능. 식봄·캐시노트 공용. 공용·manifest A.
- `margin_floor.csv` (48): 관리코드·제한내용(텍스트). 제조사 단가하한. 숫자 클램프 X — 권장가 칸 텍스트 표시. 전 채널 적용.
- `sobun.csv` (136): 변환관리코드·원코드·내품나누기·소분규격. 매입가/재고 런타임 산출.
- `listing_<key>.csv`(+meta): 채널 저장 상품관리 스냅샷(정가 컬럼 포함). `listing_<key>.xlsx`: 스마트스토어 원본 일괄변경 양식(filter 원천).
- `sikbom_price_template.xlsx`: 식봄 '상품 일괄수정' 양식 고정 템플릿(append 원천). manifest A-2.
- `cashnote_price_template.xlsx`: 캐시노트 '옵션 일괄수정' 양식 고정 템플릿((캐시노트)양식, append 원천). manifest A-2.
- `baemin_price_template.xlsx`: 배민상회 가격변경 양식 고정 템플릿((배민)양식, append 원천). manifest A-2.
- 연동: `product_master.csv`(매입가·재고·규격·박스내품).

## CHANNEL_CONFIG (채널 추가 = 여기에 한 세트)
필드: key·commission·ship_settle·real_ship(=2700)·baseline_col·apply_floor·sheet·header_row·data_start·cols.
- **`ship_fee_const`**: 다운로드에 배송비 숫자가 없는 채널은 상수로(식봄=3000).
- **`ship_fee_policy`**(신규 2026-06-11): 특정 컬럼값 조건부 배송비. `{col, map, default}` — 다운로드 col값이 map에 있으면 그 값, 없으면 default. 캐시노트={col25(배송정책코드 Y), map{DVP212991:3000}, default0}. 우선순위 ship_fee_const > ship_fee_policy > cols['배송비'].
- **`n_source`**: `"download"`(=바코드 col, 스마트스토어 기본) / `"ref"`(=hapo_multiplier 상품번호 조회, 식봄·캐시노트).
- cols에서 없는 컬럼(즉시할인·포인트·배송비·바코드)은 **생략 가능** → parse_download가 0/상수/None 처리.
- 식봄: commission 0.07 · ship_fee_const 3000 · n_source "ref" · sheet 식봄붙여넣기 · header 4 · data 5 · cols{상품번호1,코드2,상품명6,판매가19,정가16}.
- **캐시노트**: commission 0.06 · ship_fee_policy{col25,map{DVP212991:3000},default0} · n_source "ref" · sheet 상품 · header 3 · data 4 · cols{상품번호1(A),코드5(E),상품명3(C),판매가14(N),정가15(O)} · **extra_cols{오퍼코드17(Q),옵션코드18(R)}** · **price_form**(append, cashnote_price_template.xlsx, '(캐시노트)양식', data 4, fixed{F=수정,L=Y,N=9999}, G=판매단가(권장가)·H=할인전단가(max(정가,권장가))·O=관리코드). baseline_col 캐시노트.
- **`commission_source`**(신규): `"download"`면 수수료가 채널 단일값이 아니라 **상품별**(다운로드 컬럼). compute가 `_num(rec[commission_field])/commission_div + commission_add` 로 행별 산출. 없으면 단일 `commission`.
- **배민상회**: commission_source "download"·commission_field 수수료raw·div 100·add 0.03 · ship_fee_policy{col60(BH 배송방법),map{무료배송:0},default3000} · n_source "ref" · sheet sheet1 · header 2 · data 3 · cols{상품번호1(A),코드22(V),상품명2(B),판매가24(X),정가23(W)} · extra_cols{수수료raw:73,옵션번호:18,옵션명:21} · **price_form**(append, baemin_price_template.xlsx, '(배민)양식', data 2, J=변경판매가(권장가)·**H=변경소비자가=권장가+(정가−판매가) gap유지(jeong_gap)**·G/I=현재 소비자가/판매가·C=옵션번호·D=옵션명·E=관리코드). baseline_col 배민상회. bm_commission.csv(천년경영용)는 **미사용** — 다운로드 BU가 수수료 직접 보유.

## 전용 함정
- 다운로드 가이드행 skip(채널별 header_row/data_start). 판매자상품코드 빈 행 존재.
- **N(합포)**: 스마트스토어=판매자바코드(BZ), 그 외=hapo_multiplier. **매입가×N 반드시 반영**(빼면 N>1/<1 리스팅 마진 오류).
- **★ 상품번호 정수정규화(`_pid`, 2026-06-11)**: 캐시노트 다운로드 ID(A열)는 **숫자셀** → openpyxl이 46903.0(float)로 읽음. `_nfc`만 쓰면 '46903.0'이 되어 hapo_multiplier 키('46903')·골든과 매칭 실패 → **N 전건 1·마진 전건 오류**(증상: 평균마진율 음수). `_pid`가 정수값 float만 int화. 식봄은 상품번호가 텍스트라 안 걸렸음 — **숫자 키 채널은 반드시 _pid**.
- **식봄·캐시노트 정산식은 골든과 의도적으로 다름**: 골든은 실택배비 3000/3700·권장가 ROUND. 우리는 **스마트스토어 표준(2700 flat·ceil)** → 마진율이 골든보다 (3000-2700)/정산액 만큼 높게 나옴(정상). 골든 대조는 입력(판매가·배송비·매입가·N)만 일치 확인용.
- **캐시노트 6%/7% 혼재**: 골든 정산가(K)는 일반 0.93(7%)이나 요율컬럼=6·천년경영 0.94·권장가(O) 0.94·헤더 "6%기준" 다수 근거 → **6% 채택**(K는 시트 내부 불일치). (ADR 0014)
- **캐시노트 행사(이벤트) 차등 무시**: 골든은 캐시노트행사 시트 상품에 0.88(12%) 적용하나 모니터에 행사 목록 소스 없음 → 단일 수수료. 필요 시 행사 상품번호 reference화.
- **캐시노트 배송비 조건부**: 배송정책코드(Y=25) DVP212991→3000, DVP447716 등→0. 식봄 상수와 다름(ship_fee_policy). 골든 배송비 484/33 분포와 일치.
- **배민상회 상품별 수수료(2026-06-11)**: 수수료가 채널 단일이 아니라 다운로드 **BU(73)**에 상품별로 내장(4.5·5.0…). 정산식 수수료 = BU/100 + 0.03(추가 고정). compute가 행별 rate=1−수수료 적용. listing에 수수료raw 보존(없으면 commission=0.03만 적용되는 오류 → 가드 등재). bm_commission.csv는 천년경영 전용, 모니터 미사용.
- **배민상회 컬럼 함정**: 관리코드 = **V(22) 관리용 상품명**(B 상품명 아님). 판매가=X(24)(소비자가 W(23)는 정가). 배송비=BH(60) 배송방법=='무료배송'?0:3000.
- **listing CSV 스키마 유연(2026-06-11)**: recs_to_csv/csv_text_to_recs가 LISTING_COLS + extra_cols 키(오퍼/옵션코드·수수료raw) 자동 포함·복원. 새 extra_cols 채널은 CSV 코드 수정 불필요(하위호환).
- **구 listing 스키마 공란(2026-06-11)**: `extra_cols`(캐시노트 오퍼코드·옵션코드)는 도입 후 저장된 listing에만 존재. 도입 전 스냅샷은 그 컬럼이 없어 가격변경 양식 A/D가 빈 채로 나감 → **'상품관리 갱신 → 전체 교체' 1회 재파싱 필요**('신규만 추가'는 기존 행 미채움). 페이지 가드: price_form이 쓰는 extra_cols 필드가 저장본에 전부 비면 경고. (logs/2026-06-11-cashnote-stale-listing)
- **골든 BCD 버림(캐시노트)**: 골든 결과페이지 A(상품번호)만 매칭 키. B(상품코드)·C(옵션코드)·D(옵션ID)는 구 붙여넣기 레이아웃이라 값 불일치(B=0,C=9999) → 미사용.
- **식봄 가격변경 = '상품 일괄수정' 양식(다운로드와 별개)**. 양식은 `reference/sikbom_price_template.xlsx`에 선택 행만 채우는 append. E열=n 고정, 판매단가=권장가, 정가는 listing 저장값 유지.
- **시트명 폴백**: 다운로드 실제 시트명이 cfg['sheet']와 다를 수 있음 → `_pick_ws`가 명시시트 부재 시 첫 시트. cfg['sheet']는 '있으면 우선' 힌트.
- 미해결: baseline↔product_master 조인 갭, sobun↔unit_list↔sub_list 개념중복.

## 가격 일괄변경
- **스마트스토어** (원본 filter형): 표에서 상품 선택 → CSV 또는 가격 일괄변경 양식(.xlsx). 타깃=권장가. **할인 우선 규칙**(`adjust_price`): 인상 시 즉시할인 먼저↓, 인하 시 먼저↑, 포인트 불변. 양식=원본 전 컬럼 보존·변경행만 출력(미체크/빈행 삭제). ⚠️ delete_rows row_dimensions 잔존 → keep_last 초과 키 삭제 필수(전역 pitfalls). 함수: `compute_new_prices`·`build_bulk_price_xlsx`·`append_rows_to_raw`.
- **식봄·캐시노트** (append형 — 채널 '일괄수정' 양식에 선택 행만 기입): `build_append_items(pf,rows,recs,pids)`(채널 무관 — source{양식필드→소스키}·price_field·jeong_field로 items+preview 생성) → `build_price_form_append`(cols{필드→컬럼} writer + fixed{컬럼→값}, 예시행 제거·keep_last 정리). 판매단가=권장가. jeong_field 3모드 — ① `jeong_fake`(캐시노트): 판매가×(1+랜덤pct)·단위 반올림 ② `jeong_gap`(배민상회): 판매가+(정가−판매가) 마크업 유지(정가≤판매가면 판매가) ③ 기본(식봄): max(실제정가,판매가) 보존.
  - 식봄: `sikbom_price_template.xlsx`('(식봄)양식', data 7), fixed{E열='n'}. A=상품번호·B=코드·C=상품명·D=정가·F=판매단가.
  - **캐시노트**: `cashnote_price_template.xlsx`('(캐시노트)양식', data 4, 헤더 r2·안내 r1/r3), **fixed{F변경타입='수정',L진열여부='Y',N재고수량=9999}**. A=오퍼코드(OFR)·D=옵션코드(SKU)·G=판매단가(권장가)·**H=할인전단가=무늬용 가짜 정가(권장가×(1+랜덤 0.20~0.30)·100원 반올림·>판매가, `jeong_fake`)**·O=입점사 관리코드. (B상품명·C순서·E옵션명·P모델명 공백). **A/D는 다운로드 Q/R에만 있어 extra_cols로 listing 보존 필수**. **할인전단가는 실제 가격 아님 — 마진/모니터는 판매단가(N)만 사용**, 양식 H는 listing 정가 보존이 아니라 매번 생성(식봄은 jeong_fake 없음 → 실제 정가 보존).

## 코드 / 페이지
- `core/workflows/channel_margin_monitor.py`: CHANNEL_CONFIG + load_references(+hapo) + resolve_code(4-tier) + `_pid`(상품번호 정수정규화) + parse_download(missing-col tolerant·`_ship`(ship_fee_const/ship_fee_policy/cols 3종)·`extra_cols` 보존(OFR/SKU)·_pick_ws·정가) + compute(n_source 분기) + run + **build_append_items(append형 items 생성, 채널무관) + build_price_form_append(필드→컬럼 writer, 식봄·캐시노트)** + build_bulk_price_xlsx(스마트스토어).
- `app/pages/6_채널마진모니터.py`: 채널선택(`CHANNEL_CONFIG.keys()` 자동 — 캐시노트 자동 노출) → 저장 listing 자동로드 → KPI + 검색 + 필터 + st.dataframe 다중행 선택 + CSV/가격일괄변경 양식(price_form 있는 채널만). 전 컬럼 헤더 수식 help(`_col_config` — 배송비 출처에 ship_fee_policy 분기 포함).
- reference는 배포본 로컬 `reference/`에서 읽음. **core import 모듈 수정 → 첫 배포 후 Reboot app 1회 필요.**

## 검증
- **스마트스토어 골든 705/706** (2026-06-10): 정산액 707/707·base매입단가 706/707·마진율 705/706.
- **식봄 골든 대조** (식봄결과페이지 716행, 2026-06-11): 정산가 H 485/485·합포 N 485/485·매입가 480/485(5 vintage). 로직 불일치 0.
- **캐시노트 골든 대조** (캐시노트결과페이지 513행, 2026-06-11): 골든∩계산 **513/513**. 입력 — 판매가 509/513(4 가격변동)·**배송비 513/513**·**N(합포) 513/513**·base매입단가 461/463(2 vintage, 50 골든#N/A). run: 544건·미매칭4(빈코드)·미설정10·마진미달26·제한36·평균마진율 9.2%. 정산가/마진율은 2700표준이라 골든과 의도적 차이.
- **캐시노트 가격변경 양식** (end-to-end, 2026-06-11): 오퍼/옵션코드 100% 캡처·listing 라운드트립 보존. 표본 5건 양식 — A=OFR·D=SKU·F=수정·G=권장가·H=정가(≥G)·L=Y·N=9999·O=관리코드 전건 일치, 예시행 제거·잔행 0. 식봄 회귀(합성) PASS.
- **배민상회 가격변경 양식**(end-to-end, 2026-06-11): 옵션번호/옵션명/수수료raw 캡처·라운드트립 보존. 표본 양식 — A상품번호·C옵션번호·D옵션명·E관리코드·G현재소비자가·I현재판매가·J변경판매가(권장가)·**H변경소비자가=J+(정가−판매가)** 전건 일치(마크업 0이면 H=J), 예시행 제거.
- **배민상회 골든 대조** (배민결과페이지 395행, 2026-06-11): 골든∩계산 394/394. 입력 — 판매가 394/394·배송비 394/394·**수수료(상품별 BU/100+0.03) 394/394**·N 394/394·base 392/393(1 vintage). **정산가 394/394 일치**(정산식 동일, 실택배비만 표준차). run: 394건·미매칭0·미설정6·마진미달20·제한35·평균마진율 10.2%.

## 채널 추가 레시피 (★앞으로 채널 다수 — 이 순서)
새 채널 = 보통 **CHANNEL_CONFIG 한 세트** 만(정산식은 스마트스토어 표준 고정). 코드 4-tier·reference·페이지·listing 저장은 공통(수정 불필요).
1. **다운로드 샘플 확보**(.xlsx 1개) — 컬럼 위치·헤더행·데이터행 채널마다 다름, 실물 필수.
2. **컬럼 매핑(cols)**: 상품번호·코드·상품명·판매가 (+ 있으면 배송비·즉시할인·포인트·바코드). 없으면 생략.
3. **배송비**: 다운로드 숫자 있으면 cols['배송비'], 상수면 ship_fee_const, 컬럼값 조건부면 ship_fee_policy(예 캐시노트 배송정책코드).
4. **N 출처**: 바코드 컬럼 있으면 "download", 없으면 "ref"(hapo_multiplier — 채널 무관 조회). **상품번호가 숫자셀이면 _pid가 처리(이미 적용)**.
5. **수수료율**: commission만 채널별. 골든이 6%/7% 혼재면 다운로드 요율컬럼·천년경영 H식·헤더 다수결로 결정.
6. **기준마진율 컬럼**: baseline_margin에 그 채널 열 존재 확인(10채널 보유).
7. **apply_floor**: margin_floor 적용 여부.
8. CHANNEL_CONFIG 한 세트 추가 → 페이지 selectbox 자동 노출.
9. **골든 입력 대조**(판매가·배송비·매입가·N) — 마진율/권장가는 표준(2700·ceil)이라 골든과 다를 수 있음(정상). 골든 ID(A)만 키로.
10. **Reboot app 1회**(core 수정 시). listing은 첫 '상품관리 갱신' 시 자동 생성.

## 관련
- decisions/0013-sikbom-margin-monitor.md (식봄 + 스마트스토어 표준 채택 + hapo_multiplier N)
- decisions/0014-cashnote-margin-monitor.md (캐시노트 + 6% 단일 + ship_fee_policy + _pid)
- logs/2026-06/2026-06-11-channel-margin-monitor-cashnote.md · -cashnote-price-change.md · -cashnote-fake-jeongga.md · -cashnote-stale-listing.md · -baemin.md · -baemin-price-change.md
- logs/2026-06/2026-06-11-channel-margin-monitor-sikbom.md · -price-change-form.md · 2026-06-10-references.md
- manifest.md (A baseline_margin·product_master·hapo_multiplier / A-2 margin_floor·sobun·listing)

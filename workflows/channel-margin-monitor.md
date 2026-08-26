# 워크플로우: channel-margin-monitor (채널 가격·마진 모니터)

> 이 워크플로우를 건드리기 전 이 파일을 읽는다. 전역 함정은 pitfalls.md, 공유자산 연결은 manifest.md.

## 요약
- 판매 채널의 라이브 리스팅(상품관리 다운로드)을 받아 상품별 마진율을 계산 → 기준마진 대비 이탈 탐지 + 기준마진 달성 권장가를 역산하는 모니터.
- 등록(신규)이 아니라 **운영 중 리스팅 점검**. 사용자 엑셀([1]마스터 수식 조인본) 대체.
- 상태: **운영중** — 스마트스토어(모니터+가격일괄변경) · 식봄(모니터+가격변경) · 캐시노트(모니터+가격변경) · 배민상회(모니터+가격변경; 상품별 수수료) · **쿠팡(모니터+가격변경, 2026-06-11; filter형 가격변경)** · **올웨이즈(올팜)(모니터+가격변경, 2026-06-12; append형)** · **알리(AliExpress)(모니터+가격변경, 2026-06-12 / 가격변경 2026-08-11; 다중시트 자동정제·multi_filter형)** · **ESM(G마켓)(모니터+가격변경, 2026-06-12; 지마켓 필터+A중복제거·append형 가격변경)** · **자사몰(카페24)(모니터+가격변경, 2026-08-04; CSV 다운로드·csv_filter형)**. 타 채널은 레시피로 점진 추가(baseline_margin이 10채널 보유). (**10채널 모니터 / 10채널 가격변경** — 알리 가격변경 2026-08-11·리테일앤인사이트 신설 2026-08-11, 둘 다 multi_filter형.)
- **표준 정산식 = 웹앱 스마트스토어형**(사용자 확정 2026-06-11). 새 채널은 골든이 다른 값을 쓰더라도 **스마트스토어 구조(2700 flat 실택배비·ceil 권장가)에 맞추고 수수료율만 채널별**로 둔다. 골든은 입력 검증용 참고(마진율/권장가는 골든과 의도적으로 다를 수 있음).

## 입력 (저장본 자동 로드, 갱신 시에만 업로드)
- **저장 listing** `reference/listing_<key>.csv`(연동데이터, app repo) 를 자동 로드 → 매번 업로드 불필요. + `.meta.json`(갱신일 KST·건수).
- **갱신**: 페이지 '📥 상품관리 갱신'에서 새 다운로드(.xlsx 전체 업로드) → [전체 교체] / [신규만 추가](merge) → API 커밋.
- 채널별 다운로드 파싱:
  - **스마트스토어** (`[일괄수정 (전체 업로드)]`): r2=헤더, r3~5=가이드, r6+=데이터. A 상품번호·B 판매자상품코드·D 상품명·F 판매가·AO(41) 기본배송비·BF(58) 즉시할인·BQ(69) 포인트·BZ(78) 판매자바코드(N).
  - **식봄** (`식봄붙여넣기` 시트): r1~3 유의사항, **r4=헤더, r5+=데이터**. A(1) 상품no(키)·B(2) 상품코드(관리코드)·F(6) 상품명·**S(19) 판매단가(=판매가)**. **즉시할인·포인트·배송비(숫자)·바코드 컬럼 없음.** P(16)=정가(취소선용, 미사용). M(13)=택배배송비'명'(숫자 아님 → 배송비는 상수 3000).
  - **캐시노트** (`상품` 시트, KCD 마켓): **r3=헤더, r4+=데이터**. A(1) ID(상품번호 키)·E(5) 입점사 관리 코드(관리코드)·C(3) 상품명·**N(14) 판매 단가(=판매가)**·O(15) 할인 전 단가(정가). F(6) 요율(=6, 수수료율). **즉시할인·포인트·바코드 컬럼 없음(식봄형).** Y(25) 배송 정책 코드 → 배송비 조건부(아래). 둘째 시트 `상품 필드값`은 드롭다운값(무관). ⚠️ ID가 숫자셀 → `_pid` 정수정규화 필수.
  - **배민상회** (`sheet1`): **r2=헤더, r3+=데이터**. A(1) 상품번호(키)·**V(22) 관리용 상품명(=관리코드)**·B(2) 상품명·**X(24) 판매가**·W(23) 소비자가(정가). **BU(73) 상품별 수수료(%) → 수수료 내장**(extra_cols 캡처). BH(60) 배송방법 → 배송비 조건부. **즉시할인·포인트·바코드 없음(식봄형).** 상품번호 숫자셀 → _pid. 암호 없음.
  - **쿠팡** (`data` 시트): **r3=헤더, r4+=데이터**. **C(3) 옵션ID(키 — 골든 조인·hapo키. 업체상품ID A는 multi-option)**·F(6) 업체상품코드(관리코드)·G(7) 쿠팡 노출 상품명·**J(10) 판매가격**·K(11) 할인율기준가(정가). 즉시할인·포인트·바코드 없음. 다운로드가 **조회(A~O)+변경요청(P~S) 컬럼형** — 가격변경에 재사용.
  - **올웨이즈(올팜)** (`…수정용` 단일 시트): **r1=헤더, r2=가이드, r3=예시, r4+=데이터**. **A(1) 상품 ID(ObjectId 문자열 키)**·E(5) 판매자상품코드(관리코드)·B(2) 상품명·**K(11) 팀구매가(=판매가)**·J(10) 개인구매가(=정가). 즉시할인·포인트·배송비·바코드 컬럼 없음(식봄형). ⚠️ D '일반 가격(팀구매가*1.1)' 헤더는 **거짓 라벨** — 실제 D=개인구매가.
  - **알리(AliExpress)** (`ALIPRODUCT` 대량등록 export — **카테고리별 다중시트**): 커피음료·탄산수 등 25개 카테고리 시트 + 각 `*_hide`·`global_hide`(숨김) + 다단헤더(r1 그룹·**r2 라벨**·r3 옵션필수·r4~5 설명/예시). **보이는 시트만**(숨김 제외) 통합, r2 라벨로 **id(알리상품번호)·*제품 이름(상품명)·*제품 소매 가격(판매가)·SKU 코드(관리코드)** 추출. data r5+(예시 '--' 행은 숫자ID 필터 제거). 매크로(ALI상품매크로V2) 정제를 parse에서 자동화. 즉시할인·포인트·배송비·바코드·정가 없음.
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
- 수수료율: 스마트스토어 6% · 식봄 7% · 캐시노트 6% · **쿠팡 12%** · **올웨이즈 10.5%** · **알리 9%** · **ESM 17.5%**(단일 — 골든 정산 가격×0.825 정확재현, O열 판매이용료 13/11/9%는 카테고리수수료라 미사용, 헤더 '17%'·권장가 0.83은 내부불일치로 미채택). **배민상회는 상품별**(다운로드 BU/100 + 0.03) → `commission_source="download"`.
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
- `margin_floor.csv` (48): **관리코드·상품명·비고·제한내용**. 제조사 단가하한/마진민감. 숫자 클램프 X — 권장가 칸에 '제한내용' 텍스트 표시. 전 채널 적용. **등록/해제는 페이지 '🔒 제한 상품 등록/해제'(parse_floor_dict 라이브read·update_floor_csv·compute_listing floor_override 즉시반영)**. 두뇌④ load_locked 공용.
- `sobun.csv` (136): 변환관리코드·원코드·내품나누기·소분규격. 매입가/재고 런타임 산출.
- `listing_<key>.csv`(+meta): 채널 저장 상품관리 스냅샷(정가 컬럼 포함). `listing_<key>.xlsx`: 스마트스토어 원본 일괄변경 양식(filter 원천).
- `sikbom_price_template.xlsx`: 식봄 '상품 일괄수정' 양식 고정 템플릿(append 원천). manifest A-2.
- `cashnote_price_template.xlsx`: 캐시노트 '옵션 일괄수정' 양식 고정 템플릿((캐시노트)양식, append 원천). manifest A-2.
- `baemin_price_template.xlsx`: 배민상회 가격변경 양식 고정 템플릿((배민)양식, append 원천). manifest A-2.
- `esm_price_template.xlsx`: ESM 가격변경 양식 고정 템플릿('(ESM)양식' 클린 r1~5, append 원천). manifest A-2.
- 연동: `product_master.csv`(매입가·재고·규격·박스내품).

## CHANNEL_CONFIG (채널 추가 = 여기에 한 세트)
필드: key·commission·ship_settle·real_ship(=2700)·baseline_col·apply_floor·sheet·header_row·data_start·cols.
- **`ship_fee_const`**: 다운로드에 배송비 숫자가 없는 채널은 상수로(식봄=3000).
- **`ship_fee_policy`**(신규 2026-06-11): 특정 컬럼값 조건부 배송비. `{col, map, default}` — 다운로드 col값이 map에 있으면 그 값, 없으면 default. 캐시노트={col25(배송정책코드 Y), map{DVP212991:3000}, default0}. 우선순위 ship_fee_const > ship_fee_policy > cols['배송비'].
- **`n_source`**: `"download"`(=바코드 col, 스마트스토어 기본) / `"ref"`(=hapo_multiplier 상품번호 조회·채널무관, 식봄·캐시노트·올웨이즈·알리·**ESM(A 마스터상품번호)**).
- **`exclude_row_if_col_filled`**(신규 2026-06-11): 지정 컬럼에 값이 있으면 그 **행을 parse에서 제외**. 쿠팡=5(E열 바코드) → 값 있으면 **로켓그로스**(배송방식 다름)라 판매자택배 모니터 비대상. parse_download가 `excl_col` 처리(채널 무관).
- cols에서 없는 컬럼(즉시할인·포인트·배송비·바코드)은 **생략 가능** → parse_download가 0/상수/None 처리.
- 식봄: commission 0.07 · ship_fee_const 3000 · n_source "ref" · sheet 식봄붙여넣기 · header 4 · data 5 · cols{상품번호1,코드2,상품명6,판매가19,정가16}.
- **캐시노트**: commission 0.06 · ship_fee_policy{col25,map{DVP212991:3000},default0} · n_source "ref" · sheet 상품 · header 3 · data 4 · cols{상품번호1(A),코드5(E),상품명3(C),판매가14(N),정가15(O)} · **extra_cols{오퍼코드17(Q),옵션코드18(R)}** · **price_form**(append, cashnote_price_template.xlsx, '(캐시노트)양식', data 4, fixed{F=수정,L=Y,N=9999}, G=판매단가(권장가)·H=할인전단가(무늬용 가짜=표준 FAKE_JEONG)·O=관리코드). baseline_col 캐시노트.
- **`commission_source`**(신규): `"download"`면 수수료가 채널 단일값이 아니라 **상품별**(다운로드 컬럼). compute가 `_num(rec[commission_field])/commission_div + commission_add` 로 행별 산출. 없으면 단일 `commission`.
- **배민상회**: commission_source "download"·commission_field 수수료raw·div 100·add 0.03 · ship_fee_policy{col60(BH 배송방법),map{무료배송:0},default3000} · n_source "ref" · sheet sheet1 · header 2 · data 3 · cols{상품번호1(A),코드22(V),상품명2(B),판매가24(X),정가23(W)} · extra_cols{수수료raw:73,옵션번호:18,옵션명:21} · **price_form**(append, baemin_price_template.xlsx, '(배민)양식', data 2, J=변경판매가(권장가)·**H=변경소비자가=무늬용 가짜(표준 FAKE_JEONG)**·G/I=현재 소비자가/판매가·C=옵션번호·D=옵션명·E=관리코드). baseline_col 배민상회. bm_commission.csv(천년경영용)는 **미사용** — 다운로드 BU가 수수료 직접 보유.
- **쿠팡**: commission 0.12 · ship_fee_const 0(배송비 항상 0) · n_source "ref"(옵션ID) · sheet data · header 3 · data 4 · cols{상품번호3(C 옵션ID),코드6(F),상품명7(G),판매가10(J),정가11(K)} · **`exclude_row_if_col_filled`:5(E열 바코드)** · **price_form{mode "filter", write{판매가16(P),정가17(Q)}}**. baseline_col 쿠팡.
- **올웨이즈(올팜)**: commission **0.105**(10.5% 단일) · ship_fee_const **0** · n_source "ref"(올팜상품번호 ObjectId — 다운로드 바코드 없음) · sheet None(단일) · header 1 · data 4(r2가이드·r3예시 skip) · cols{상품번호1(A ObjectId 문자열),코드5(E 판매자상품코드),상품명2(B),**판매가11(K 팀구매가)**,**정가10(J 개인구매가)**} · 즉시할인·포인트·배송비·바코드 없음. baseline_col 올웨이즈. **extra_cols{카테고리코드3,판매상태4,옵션명1:6,옵션값1:7,재고수량12}**(2옵션·옵션ID는 항상공백→미캡처). **price_form**(append, allways_price_template.xlsx, '(올웨이즈)양식', data 4, **K팀구매가=권장가·J개인구매가=무늬용 가짜 FAKE_JEONG**, source{상품ID·상품명·카테고리코드·판매상태·관리코드·옵션명1·옵션값1·재고수량}, **int_fields[카테고리코드,재고수량]**).
- **ESM(G마켓)**: commission **0.175**(17.5% 단일) · ship_settle 0.967 · real_ship 2700 · baseline_col **"ESM"** · apply_floor True · n_source "ref"(hapo **A 마스터상품번호**·채널무관 — 다운로드 바코드 없음. ⚠️ 골든 N=#REF! 대조불가) · sheet None(시트명 가변) · header 1 · data 2 · cols{상품번호1(**A 마스터상품번호**=키),코드5(**E 판매자관리코드**),상품명3(C),판매가9(I),**배송비35(AI)**}. 즉시할인·포인트·바코드·정가 컬럼 없음. **`include_row_if_col_value`{col6(F 사이트),value"지마켓"}**(옥션 제외) + **`dedup_key`"상품번호"**(A 중복제거) · **`multi_file`True**(다운로드 500상품 한도 → 여러 배치 한번에 업로드·자동 병합, 수기병합 불요). **배송비 AI는 텍스트**('무료'→0/'3,000'→3000, _num 콤마허용). **extra_cols{사이트상품번호:2}**(다운로드 B — 가격변경 양식 키). **price_form**(append, esm_price_template.xlsx, '(ESM)양식', data 6, **seq_col 1**(A순번), cols{사이트상품번호:2,판매가:3}, source{사이트상품번호:사이트상품번호}, price_field 판매가=권장가, **int_fields[사이트상품번호]**, **jeong 없음**(정가 칸 無)). (ADR 0015)
- **알리(AliExpress)**: commission **0.09**(9% 단일) · ship_fee_const **0** · n_source "ref"(알리상품번호 — 골든 N 677/677) · baseline_col 알리 · **`consolidate`{header_row 2, data_start 5, skip_sheets[지침], require_numeric_id True, labels{상품번호:id, 상품명:*제품 이름, 판매가:*제품 소매 가격, 코드:SKU 코드}}** (cols/sheet 미사용 — 다중시트 정제). 즉시할인·포인트·배송비·바코드·정가 없음. **가격변경 = `price_form{mode:"multi_filter", price_label:"*제품 소매 가격", price_decimals:2}`**(2026-08-11 — AliExpress 가격 수정도 같은 대량등록 양식이라 저장 원본을 재사용).
- **`price_form.mode`**: `append`(템플릿에 선택행 기입 — 식봄/캐시노트/배민/**올웨이즈**) · **`filter`(원본 다운로드의 변경요청 컬럼에 기입, 선택만 남김 — 쿠팡 `build_filter_price_xlsx`, **zip레벨 수술로 네이티브 포맷 보존**)** · 없으면 smartstore(원본 판매가 직접 수정). filter/smartstore는 '전체 교체' 저장 원본(.xlsx) 필요(**쿠팡은 반드시 전체 교체 — 네이티브 raw**).
- **`int_fields`**(신규 2026-06-12, append형): 지정 양식필드의 all-digit 문자열을 int 셀로 기입(올웨이즈 카테고리코드·재고수량 텍스트화 방지). 미설정 채널 무영향.
- **`consolidate`**(신규 2026-06-12, 알리): 다중시트 export 정제 통합. {header_row, data_start, skip_sheets, require_numeric_id, labels{레코드필드:헤더라벨}}. parse_download가 `cfg.get('consolidate')`면 `_consolidate_parse`로 분기 — 보이는 시트(숨김 제외) 순회·라벨로 컬럼 조회·숫자ID 필터. cols/sheet 미사용. 매크로(VBA) 정제 대체.
- **`include_row_if_col_value`**(신규 2026-06-12, ESM): `{col,value}` — 그 컬럼값==value 행만 parse(나머지 제외). ESM 사이트(F)=='지마켓'만 모니터(옥션 제외). `exclude_row_if_col_filled`(쿠팡)의 inclusion판.
- **`dedup_key`**(신규 2026-06-12, ESM): parse 말미 그 레코드 필드로 중복제거(keep first). ESM A(마스터상품번호) — 여러 배치 다운로드 합본·재업로드 안전. (merge_listing도 상품번호로 dedup하지만 단일 '전체교체' 합본 보호)
- **`_num` 콤마 허용**(2026-06-12): "3,000"(천단위 콤마)→3000, "무료"→0. ESM 배송비 AI열이 텍스트라 필수. 전 채널 무해(타 채널 판매가=숫자셀).
- **`seq_col`**(신규 2026-06-12, append형): 양식 지정 컬럼에 순번 1,2,3… 기입(ESM (ESM)양식 A열). 미설정 채널 무영향.

## 전용 함정
- 다운로드 가이드행 skip(채널별 header_row/data_start). 판매자상품코드 빈 행 존재.
- **N(합포)**: 스마트스토어=판매자바코드(BZ), 그 외=hapo_multiplier. **매입가×N 반드시 반영**(빼면 N>1/<1 리스팅 마진 오류).
- **★ 상품번호 정수정규화(`_pid`, 2026-06-11)**: 캐시노트 다운로드 ID(A열)는 **숫자셀** → openpyxl이 46903.0(float)로 읽음. `_nfc`만 쓰면 '46903.0'이 되어 hapo_multiplier 키('46903')·골든과 매칭 실패 → **N 전건 1·마진 전건 오류**(증상: 평균마진율 음수). `_pid`가 정수값 float만 int화. 식봄은 상품번호가 텍스트라 안 걸렸음 — **숫자 키 채널은 반드시 _pid**.
- **식봄·캐시노트 정산식은 골든과 의도적으로 다름**: 골든은 실택배비 3000/3700·권장가 ROUND. 우리는 **스마트스토어 표준(2700 flat·ceil)** → 마진율이 골든보다 (3000-2700)/정산액 만큼 높게 나옴(정상). 골든 대조는 입력(판매가·배송비·매입가·N)만 일치 확인용.
- **캐시노트 6%/7% 혼재**: 골든 정산가(K)는 일반 0.93(7%)이나 요율컬럼=6·천년경영 0.94·권장가(O) 0.94·헤더 "6%기준" 다수 근거 → **6% 채택**(K는 시트 내부 불일치). (ADR 0014)
- **캐시노트 행사(이벤트) 차등 무시**: 골든은 캐시노트행사 시트 상품에 0.88(12%) 적용하나 모니터에 행사 목록 소스 없음 → 단일 수수료. 필요 시 행사 상품번호 reference화.
- **캐시노트 배송비 조건부**: 배송정책코드(Y=25) DVP212991→3000, DVP447716 등→0. 식봄 상수와 다름(ship_fee_policy). 골든 배송비 484/33 분포와 일치.
- **쿠팡 키=옵션ID(2026-06-11)**: 업체상품ID(A)는 multi-option(499 ID/2058 옵션)이라 키 부적합. 골든 조인·hapo·관리코드 조회 전부 **옵션ID(C)** 기준 → 상품번호=옵션ID.
- **쿠팡 빈 관리코드 미매칭(2026-06-11)**: 다운로드 일부(155건)는 업체상품코드(F) 빈값 → 매입가 미해결(미매칭). 골든도 동일하게 미해결(매입가 NA)이라 우리 결과가 골든과 일치 — 버그 아님. 골든 `RIGHT(관리코드,LEN-2)` fallback은 접두코드용(이미 4-tier로 풀림)이라 미구현.
- **★ 쿠팡 가격변경 openpyxl→inlineStr 업로드 실패(2026-06-11)**: `build_filter_price_xlsx`가 `load_workbook→wb.save()`로 라운드트립하면 openpyxl이 **전 문자열 셀을 inlineStr로 재직렬화**(sharedStrings 없음·XML선언 없음) → **쿠팡 업로더가 거부**(골든=네이티브 sharedStrings `t="s"`). 해결: openpyxl 저장 제거, **원본 .xlsx(전체 교체=업로드 바이트 그대로=네이티브)를 zip레벨 수술**(헤더행 보존+선택행 연속 재번호+P/Q 숫자 기입, sharedStrings/styles/mergeCells/네임스페이스/XML선언 원본 유지). 검증: 출력 row4가 골든 row4와 완전 일치·파트목록 동일. **전제: raw가 네이티브** → 쿠팡은 '전체 교체' 사용('신규만 추가'=`append_rows_to_raw` openpyxl 저장이 raw를 inlineStr로 변질). 헬퍼: `_sheet_part`·`_read_sst`·`_cell_text`·`_set_num_cell`·`_renumber_row`·`_col_letter`. (logs/2026-06-11-coupang-filter-native)
- **★ 쿠팡 raw가 '신규만 추가'로 inlineStr 오염 → 수술 출력도 inlineStr(2026-06-11)**: 네이티브 수술이 정상이어도 **읽는 원본 `reference/listing_coupang.xlsx`가 inlineStr이면 수술이 충실히 보존해 출력도 inlineStr** → 쿠팡 거부("양식 맞는데 데이터 못잡음"). 원인: 과거 '신규만 추가'(`append_rows_to_raw`=openpyxl load→save)가 raw 데이터행 전부를 inlineStr로 변질(헤더만 t=s 남음). 진단: raw 데이터행 t=s 0·inlineStr 다수 = 오염. 해결 ①raw 치유(inlineStr→sharedStrings 무손실 역변환: 셀 `t="s"`+`<v>idx</v>`, 스타일 `s=` 보존, 빈셀은 빈 스타일셀, sst 기존 si verbatim+신규 append) ②**가드: filter형 채널은 '신규만 추가' 비활성화**(page `native_raw=cfg['price_form']['mode']=='filter'` → `disabled`). 검증: openpyxl 전수 24,985셀 무손실·엔드투엔드 수술 출력 inlineStr 0·골든 네이티브 일치. Reboot 불필요(reference 런타임·page 자동·수술 라이브). (logs/2026-06-11-coupang-heal)
- **★★ 수술 자체가 sharedStrings 정규화 — raw 의존 제거(2026-06-11)**: 치유 후에도 실패 재현 → 앱이 가격변경 시 **치유 raw가 아닌 옛 오염 raw 사용**(GitHub raw API/CDN 캐시·미재배포). "raw가 네이티브여야" 전제가 캐시/배포 타이밍에 깨짐. 근본 해결: `build_filter_price_xlsx`가 남긴 행의 inlineStr 셀을 **항상 `t="s"`로 변환 + sharedStrings.xml 재구성**(헬퍼 `_inline_cells_to_shared`, 스타일 s= 보존·빈셀은 빈 스타일셀·sst verbatim+신규 append·count/uniqueCount 갱신). 엑셀 '값만 붙여넣기' 동치. **원본 raw가 inlineStr(오염·구 스냅샷·stale)이든 native든 출력 항상 네이티브** → 캐시/배포 무관 업로드 성공. 사용자 발견: 실패 파일을 엑셀 '값만 붙여넣기'하니 성공(=골든) → 거부원인 inlineStr 확정. 검증: 오염 raw 입력→출력 inlineStr 0·t=s·값 무손실(골든 일치). 스타일 s=11(출력) vs s=5(엑셀정규화 골든)·행height 차이는 cosmetic(거부원인 아님). **⚠️ core 수정 → Reboot app 필요.** 치유·가드는 유지(모니터 read·재오염 방지)나 가격변경은 비의존. (logs/2026-06-11-coupang-normalize)
- **배민상회 상품별 수수료(2026-06-11)**: 수수료가 채널 단일이 아니라 다운로드 **BU(73)**에 상품별로 내장(4.5·5.0…). 정산식 수수료 = BU/100 + 0.03(추가 고정). compute가 행별 rate=1−수수료 적용. listing에 수수료raw 보존(없으면 commission=0.03만 적용되는 오류 → 가드 등재). bm_commission.csv는 천년경영 전용, 모니터 미사용.
- **배민상회 컬럼 함정**: 관리코드 = **V(22) 관리용 상품명**(B 상품명 아님). 판매가=X(24)(소비자가 W(23)는 정가). 배송비=BH(60) 배송방법=='무료배송'?0:3000.
- **쿠팡 바코드=로켓그로스 제외(2026-06-11)**: 쿠팡 다운로드 **E열(5)=바코드**. 판매자택배 상품은 항상 공백, 값이 있으면 로켓그로스(미매칭 아님—배송방식 차이) → `exclude_row_if_col_filled`:5로 parse 단계 행 제외. **기존 쿠팡 listing은 바코드를 저장한 적 없어 소급 필터 불가 → '상품관리 갱신→전체 교체' 1회 재파싱 필요**('신규만 추가'는 기존 행 유지).
- **★ extra_cols 숫자ID float(2026-06-11)**: parse_download의 extra_cols는 `_pid`로 읽음(과거 `_nfc` → 배민 **옵션번호**가 숫자셀이라 `510609.0`으로 양식 C열에 찍힘). `_pid`는 정수값 float만 int화(수수료raw `4.5`·옵션명 텍스트 불변). 구 listing에 이미 `510609.0` 저장된 건은 **csv_text_to_recs의 `_deflo`**(`-?\d+\.0`→정수)가 라운드트립에서 재파싱 없이 복원.
- **listing CSV 스키마 유연(2026-06-11)**: recs_to_csv/csv_text_to_recs가 LISTING_COLS + extra_cols 키(오퍼/옵션코드·수수료raw) 자동 포함·복원. 새 extra_cols 채널은 CSV 코드 수정 불필요(하위호환).
- **구 listing 스키마 공란(2026-06-11)**: `extra_cols`(캐시노트 오퍼코드·옵션코드)는 도입 후 저장된 listing에만 존재. 도입 전 스냅샷은 그 컬럼이 없어 가격변경 양식 A/D가 빈 채로 나감 → **'상품관리 갱신 → 전체 교체' 1회 재파싱 필요**('신규만 추가'는 기존 행 미채움). 페이지 가드: price_form이 쓰는 extra_cols 필드가 저장본에 전부 비면 경고. (logs/2026-06-11-cashnote-stale-listing)
- **골든 BCD 버림(캐시노트)**: 골든 결과페이지 A(상품번호)만 매칭 키. B(상품코드)·C(옵션코드)·D(옵션ID)는 구 붙여넣기 레이아웃이라 값 불일치(B=0,C=9999) → 미사용.
- **식봄 가격변경 = '상품 일괄수정' 양식(다운로드와 별개)**. 양식은 `reference/sikbom_price_template.xlsx`에 선택 행만 채우는 append. E열=n 고정, 판매단가=권장가, 정가는 listing 저장값 유지.
- **시트명 폴백**: 다운로드 실제 시트명이 cfg['sheet']와 다를 수 있음 → `_pick_ws`가 명시시트 부재 시 첫 시트. cfg['sheet']는 '있으면 우선' 힌트.
- **올웨이즈 판매가=팀구매가(K11)·정가=개인구매가(J10)(2026-06-12)**: 개인구매가(J) 아님 — 정산은 팀구매가 기준(G=팀×0.895, 수수료10.5%). 골든 D 헤더 '일반가격(팀구매가*1.1)'은 거짓 — 실제 D=개인구매가(621/621). 정가는 표시용(마진 미반영).
- **올웨이즈 상품ID=ObjectId 문자열(2026-06-12)**: 키 A열이 `64cb…` 24자리 hex 문자열 → 숫자키 아님(_pid 무해). hapo_multiplier에 이 ObjectId 332건 등록(채널열 공백·채널무관 조회) → N 748/748 재현. 다운로드에 합포/바코드 컬럼 없어 n_source=ref 필수.
- **올웨이즈 데이터 r4 시작·헤더 거짓라벨(2026-06-12)**: r1=헤더·r2=가이드·r3=예시 → data_start 4. 배송비 컬럼 없음(상수 0; 골든 F 746/748=0, −700 2건 합포변칙 무시).
- **올웨이즈 가격변경=append('(올웨이즈)양식')(2026-06-12)**: 양식이 다운로드와 컬럼 동일하나 별도 템플릿 → append 채택(스마트스토어 raw편집 아님). **전 컬럼 재업로드형**(필수 多)이라 카테고리코드·판매상태·1옵션명/값·재고를 extra_cols로 보존 후 재기입. K=권장가·J=FAKE_JEONG(골든 O 대응). 2옵션명/값·옵션ID는 선택+항상공백 → 미캡처(stale 가드 거짓경고 방지). 카테고리·재고는 int_fields. ⚠️ openpyxl inlineStr 저장 — 올웨이즈 실업로드 미검증(식봄/캐시노트/배민 동일·정상). 거부 시 쿠팡식 네이티브 수술 필요.
- **알리=다중시트 자동정제(consolidate)(2026-06-12)**: AliExpress 대량등록 export는 카테고리별 다중시트(+`_hide`·`global_hide` 숨김)+다단헤더. 매크로(ALI상품매크로V2 CopyDataFromAnotherWorkbook)를 `_consolidate_parse`로 흡수 — **보이는 시트만**(`sheet_state!="visible"` 제외, 매크로 xlSheetVisible 동치), r2 라벨로 id·*제품 이름·*제품 소매 가격·SKU 코드 추출, data r5+(예시'--' 행 require_numeric_id로 제거). 관리코드=SKU코드(G)·상품명=*제품 이름(B 한글 클린)·판매가=*제품 소매 가격(E 텍스트 '13400.00'→_num)·알리상품번호=id(A 16자리). 별도 정제 업무 불요. olevba 전수 — Module2(Sheet1 비우기)는 저장 아님, 숨은 SaveAs 없음.
- **알리 '신규만 추가' raw append 스킵(2026-06-12)**: append_rows_to_raw가 cfg['cols']['상품번호'] 참조 → 알리(cols 없음=consolidate) KeyError → 페이지에서 consolidate 채널은 raw append 스킵(up_bytes 유지), CSV 머지(merge_listing)만. 알리 raw는 모니터에서 미사용. '전체 교체' 권장(주기적 전체 export).
- **★ ESM 채널키 'esm'(소문자) 명명 예외(2026-06-17)**: CHANNEL_CONFIG의 ESM 딕셔너리 키만 'esm'(영문 소문자) — 타 채널은 한글 표시명. cross-module에서 채널명을 'ESM'(대문자)로 넘기면 CHANNEL_CONFIG.get(ESM)=None → listing/권장가 전부 누락. 데일리 SHEET_TO_CMM='ESM'와 충돌해 ESM 행만 빈 버그 발생(데일리에서 _cmm_key 대소문자 무시 매칭으로 방어). 잠복 지뢰 — cmm를 다른 모듈과 교차할 땐 채널명 키 정합 주의. 근본 해결안=키 'esm'→'ESM' 통일(미적용·Reboot 필요).
- - 미해결: baseline↔product_master 조인 갭, sobun↔unit_list↔sub_list 개념중복.

## 가격 일괄변경
- **알리(AliExpress)** (**multi_filter형**, 다중시트 zip 수술 2026-08-11): 저장된 원본(`reference/listing_ali.xlsx` = ALIPRODUCT 대량등록 export)을 그대로 재사용 — AliExpress는 **가격 수정도 같은 대량등록 양식**. `build_multi_filter_xlsx`가 **보이는 카테고리 시트마다**(숨김 `*_hide`·`global_hide`·skip_sheets 제외 = parse와 동일 기준) ① 헤더행(r1~4)·**비숫자 id 예시행('--')은 원본 그대로 보존** ② 숫자 id 데이터행 중 **선택분만 남기고** 연속 재번호 ③ 가격 컬럼(`*제품 소매 가격`)만 권장가로 교체(`'21200.00'` 텍스트 = 원본 표기 유지, 스타일 s= 보존). **컬럼 위치는 하드코딩이 아니라 헤더행(r2) 라벨 조회** — 시트마다 열 순서가 달라도 안전. **재고(F)·상품명 등 나머지 전 컬럼 미변경**. 정가 칸 없음(할인 개념 없음 → jeong 없음).
  - ★ **openpyxl 미사용(zip 수술)** — 이 양식은 `workbookProtection lockStructure` + 시트별 `sheetProtection password` + `dataValidations`(OFFSET으로 숨김시트 참조)를 갖고 있어 openpyxl 라운드트립이 이들을 변형/유실시킬 위험. 수술 방식이라 **손대지 않은 파트는 바이트 동일**(검증: 59파트 중 보이는 시트 25개만 변경).
  - ★ **'신규만 추가' 비활성**(2026-08-11 가드 확장): 다중시트라 raw 병합이 불가능해 부분 export가 raw가 되면 가격변경 양식에서 나머지 상품이 통째로 누락 → **'전체 교체'만** 사용(쿠팡·자사몰과 같은 규칙, 이유는 다름).
  - ⚠️ **실업로드 미검증** — 알리 대량등록에 실제로 올려본 적 없음(첫 업로드 시 확인 필요). 형식은 원본 export의 부분집합이라 구조적 위험은 낮음.
- **쿠팡** (filter형, 네이티브 수술 2026-06-11): 원본 다운로드(조회 A~O + 변경요청 P~S) 자체가 변경요청 컬럼형. `build_filter_price_xlsx`가 **openpyxl 저장 없이 zip레벨 수술** — 헤더행 보존, 선택 옵션ID(C열) 행만 남겨 연속 재번호, P(16)=권장가·Q(17)=가짜정가(`t`없는 숫자) 기입, sharedStrings 등 원본 포맷 보존. openpyxl 라운드트립은 inlineStr 변질로 쿠팡 업로드 실패(전용 함정 참조). 전제: raw 네이티브('전체 교체'). **★ filter형 채널은 '신규만 추가' 비활성(가드, 2026-06-11) — append가 raw를 inlineStr로 오염시키므로 '전체 교체'만 허용.** **★★ 수술이 남긴 행을 항상 sharedStrings로 정규화(2026-06-11) — raw가 inlineStr(오염·stale 캐시)이든 출력은 항상 네이티브(`_inline_cells_to_shared`+sst 재구성). 캐시/배포 타이밍 무관 업로드 성공. Reboot app 필요.**
- **스마트스토어** (원본 filter형): 표에서 상품 선택 → CSV 또는 가격 일괄변경 양식(.xlsx). 타깃=권장가. **할인 우선 규칙**(`adjust_price`): 인상 시 즉시할인 먼저↓, 인하 시 먼저↑, 포인트 불변. 양식=원본 전 컬럼 보존·변경행만 출력(미체크/빈행 삭제). ⚠️ delete_rows row_dimensions 잔존 → keep_last 초과 키 삭제 필수(전역 pitfalls). 함수: `compute_new_prices`·`build_bulk_price_xlsx`·`append_rows_to_raw`.
- **올웨이즈(올팜)** (append형 — '(올웨이즈)양식'에 선택 행 기입): 전 컬럼 재업로드형(필수 多). build_append_items→build_price_form_append. **K(팀구매가)=권장가**·**J(개인구매가)=무늬용 가짜(FAKE_JEONG, 골든 O 가짜가격 대응)**. 상품명·카테고리코드·판매상태·1옵션명/값·재고는 listing 보존값 그대로 재기입(H/I/M 선택=공백). 카테고리코드·재고는 int_fields로 숫자 셀. ⚠️ openpyxl 저장(inlineStr) — 올웨이즈 업로더 허용 여부 실업로드 미검증(식봄/캐시노트/배민과 동일 방식, 그 3채널은 정상).
- **ESM(G마켓)** (append형 — '(ESM)양식'에 선택 행 기입): build_append_items→build_price_form_append. **B(사이트 상품번호)=다운로드 col2** — 모니터키 A(마스터상품번호)와 달라 **extra_cols로 listing 보존** 필수(양식B ∩ 다운로드B 8/8·∩A 0). **C(판매가)=권장가**·**A=순번(seq_col, 데코)**. data_start 6(r1~5 보호블록·예시 r5 보존 — 안내 '6행부터 입력, 1~5행 삭제 시 오류'). **정가 칸 없음 → 무늬용 가짜정가 미생성**(jeong_field 없음). int_fields[사이트상품번호]로 B 숫자셀. 양식 30표본 B/C 전건 일치·외부링크 0. **✅ ESM 실업로드 성공 사용자 확인(2026-06-12)** — openpyxl inlineStr 저장을 ESM Plus가 허용(식봄/캐시노트/배민/올웨이즈와 동일·정상, 쿠팡만 예외).
- **식봄·캐시노트** (append형 — 채널 '일괄수정' 양식에 선택 행만 기입): `build_append_items(pf,rows,recs,pids)`(채널 무관 — source{양식필드→소스키}·price_field·jeong_field로 items+preview 생성) → `build_price_form_append`(cols{필드→컬럼} writer + fixed{컬럼→값}, 예시행 제거·keep_last 정리). 판매단가=권장가. **jeong_field(정가/할인전단가/소비자가)는 전 채널 표준 `FAKE_JEONG`** — 권장가×(1+랜덤 0.20~0.30)·100원 반올림·>권장가, 매번 생성(실정가/마크업 보존 아님). 채널이 pf['jeong_fake']로 %만 오버라이드 가능. (사용자 표준 확정 2026-06-11)
  - 식봄: `sikbom_price_template.xlsx`('(식봄)양식', data 7), fixed{E열='n'}. A=상품번호·B=코드·C=상품명·**D=정가(무늬용 가짜=표준 FAKE_JEONG)**·F=판매단가(권장가).
  - **캐시노트**: `cashnote_price_template.xlsx`('(캐시노트)양식', data 4, 헤더 r2·안내 r1/r3), **fixed{F변경타입='수정',L진열여부='Y',N재고수량=9999}**. A=오퍼코드(OFR)·D=옵션코드(SKU)·G=판매단가(권장가)·**H=할인전단가=무늬용 가짜 정가(표준 FAKE_JEONG)**·O=입점사 관리코드. (B상품명·C순서·E옵션명·P모델명 공백). **A/D는 다운로드 Q/R에만 있어 extra_cols로 listing 보존 필수**. **할인전단가는 실제 가격 아님 — 마진/모니터는 판매단가(N)만 사용**, 양식 H는 listing 정가 보존이 아니라 매번 생성(식봄은 jeong_fake 없음 → 실제 정가 보존).

## 제한 상품 등록 / 해제 (margin_floor — 권장가 ↔ 제한) (2026-06-22)
- **권장가/제한 컬럼 출처**: 제한(margin_floor에 관리코드 등록 시 '제한내용') > 미매칭비고 > 기준미설정 > 권장가(역산). compute `fl=refs["floor"].get(rec["코드"])`→제한내용 or 비고. 키=listing 관리코드 원본.
- **등록/해제 UI**: 표 선택 → '🔒 제한 상품 등록/해제' 섹션 data_editor(제한내용✏️). 입력=등록/수정·비움(기존 제한)=해제·빈칸+무제한=무변경. 저장→margin_floor.csv 반영→tblver+1+rerun(즉시 반영·선택 풀림).
- **core**: `parse_floor_dict`(text→{관리코드:{상품명,비고,제한내용}}) · `update_floor_csv(text,upserts,removes)`(헤더/BOM/CRLF/타코드 보존, update_baseline 패턴) · `compute_listing(...,floor_override=)`(refs["floor"] 교체·즉시반영, compute 무수정).
- 두뇌④(load_locked)와 동일 파일 — 등록 시 그 상품 작업목록 제외. 제한내용 기본=빈칸(일괄 오등록 방지).
- **필터(2026-06-22·page-only·filter_sig 동기)**: 검색·코드유형·마진미달만·**기준 초과만**(탐지>0)·제한상품만·**제한 제외**·미매칭만·재고N이상·**전월매출(이채널) 범위 ≥/≤**(빈값=0)·**상품명 키워드 제외**(쉼표 구분·OR 부분일치 제외, 예 `일화,피클`).
- ⚠️ core 신규 → Reboot 1회.

## 전월매출 (박스/낱개/소분 통일) — 표 참고 컬럼 (2026-06-22)
- **목적**: 가격 변경 시 판매 볼륨 맥락. 표 맨 끝(권장가/제한 옆) **전월매출(이채널)** + **전월매출(전체)** 2컬럼.
- **데이터**: 적재 최신월 매출 파티션 1개(`store.read_partition`·data repo). "전월"=적재 최신월(현 2026-05, 6월분 7월초 적재 시 자동 롤). 금액=판매금액(천년경영 정산 진실). 가벼움(파티션 1개).
- **★ 박스/낱개/소분 통일 = `canonical_code(code, refs)`**: listing 행 관리코드를 **원박스로 정규화**(소분→원코드·PC낱개→그 상품코드 행의 관리코드·박스/합포/미매칭→자기자신). resolve_code 매핑 재사용.
  - **매출자료는 정규화 불요** — 실데이터 검증(2026-05 10,053행): 매출자료 관리코드는 **전부 박스코드**, PC낱개·합포(-CB-)·소분 **0건**(정산 시점 박스 환원). listing 쪽만 canonical → 박스코드 매출과 join.
- **채널→매출자료 상호명**(`_CH_TO_SANGHO`): 1:1, **쿠팡만 2개**(오픈마켓 쿠팡 (윙배송)+쿠팡(로켓창고)) 합산. 이채널=그 상호명(들) 필터 / **전체=내 관리 8채널 합**(나들·B2B 제외·_CH_TO_SANGHO 전부, 두뇌④ _MANAGED 동개념).
- **함정**: ① 같은 canonical 여러 행(박스+낱개 동시 등록)은 **같은 매출값** 표시 → **세로 합산 금지**(행별 참고). ② 매출 없으면 빈칸(None). ③ data repo PAT(_data_secret) 없으면 두 컬럼 빈값.
- **베이스(%) 보류**: 두뇌④ 베이스도 요청됐으나 성능(18개월+주문38만+ship_alloc 실측=첫 로딩 십수 초)으로 사용자 보류. 추후 build_prod core 추출해 공용화 시 결합 가능.
- ⚠️ **core canonical_code 신규 → Reboot 1회**(page가 cmm.canonical_code 참조).

## 코드 / 페이지
- `core/workflows/channel_margin_monitor.py`: CHANNEL_CONFIG + load_references(+hapo) + resolve_code(4-tier) + **canonical_code(원박스 통일·전월매출)** + **parse_floor_dict·update_floor_csv(제한 R/W)·compute_listing floor_override** + `_pid`(상품번호·extra_cols 정수정규화) + `_deflo`(구 listing float ID 복원) + `_strip_external_links`(템플릿 외부링크 제거) + **_consolidate_parse(알리 다중시트 정제 — 보이는 시트·라벨조회·숫자ID 필터, 매크로 대체)** + parse_download(consolidate 분기·**include_row_if_col_value(지마켓 keep)·dedup_key(A 중복제거)**·missing-col tolerant·`_ship`(ship_fee_const/ship_fee_policy/cols 3종)·`extra_cols` 보존(OFR/SKU)·_pick_ws·정가) + **_num(콤마 허용 '3,000'→3000·'무료'→0)** + compute(n_source 분기) + **compute_listing(baseline_override 라이브 기준마진)** + run + **기준마진율 편집(parse_baseline_dict·propose_baseline·update_baseline_csv·_fmt_margin)** + **build_append_items(append형 items 생성, 채널무관) + build_price_form_append(필드→컬럼 writer + **seq_col 순번**, 식봄·캐시노트·올웨이즈·**ESM**)** + build_bulk_price_xlsx(스마트스토어) + **build_multi_filter_xlsx(알리 다중시트 zip 수술 — 보이는 시트별 선택행만 남기고 라벨조회로 가격컬럼만 교체) + _sheet_parts(workbook.xml 순서 [(시트명,파트,state)]) + _set_text_cell(inlineStr 기입·스타일 보존)** + **build_filter_price_xlsx(쿠팡, zip 수술·openpyxl 미사용, 출력 sharedStrings 정규화) + 수술 헬퍼(_sheet_part·_read_sst·_cell_text·_cell_in_row·_set_num_cell·_renumber_row·_col_letter·`_inline_cells_to_shared`(inlineStr→t=s))**.
- `app/pages/6_채널마진모니터.py`: 채널선택(`CHANNEL_CONFIG.keys()` 자동 — 캐시노트 자동 노출). **`multi_file` 채널(ESM)은 업로더 `accept_multiple_files=True` → 여러 배치 파일 parse·이어붙이기·`dedup_key` 교차 중복제거 후 전체교체/신규추가(multi는 raw 저장 생략=모니터전용)** → 저장 listing 자동로드 → KPI + 검색 + 필터 + st.dataframe 다중행 선택 + CSV/가격일괄변경 양식(price_form 있는 채널만). 전 컬럼 헤더 수식 help(`_col_config`). **하단 '🎯 기준마진율 설정' 섹션**(선택→현재 마진율을 그 채널 기준으로, 충돌 라디오·0.1%p반올림·offset 프리셋). baseline은 **GitHub 라이브 read**(`_load_baseline_text` 캐시)로 편집 즉시 반영(compute_listing override).
- reference는 배포본 로컬 `reference/`에서 읽음. **core import 모듈 수정 → 첫 배포 후 Reboot app 1회 필요.**
- **이력 1d listing 가격 스냅샷 적립(2026-06-18)**: page가 listing 커밋(전체교체/신규추가) 직후 `_accumulate_listing(key, committed)` → 그 채널 가격을 날짜본으로 private data repo `snapshots/listing_YYYY-MM.parquet` 적립(비차단 toast·`_data_secret` [data] pat/repo·forward). core `core/intelligence/listing_history.py`(stock_history 1b 동형). 두뇌③ A/B 가격변경 전후 토대. import 신규 → Reboot 1회.

## 챗 네이티브 가격변경 생성 (앱 페이지 미경유 — 2026-06-25)
- 앱 page 6 글루를 오프라인 재현해 챗에서 직접 가격변경 시트 생성 가능. core + reference만 있으면 됨.
- 절차: ① listing_<key>.csv → `csv_text_to_recs` ② `compute_listing(recs, channel, ref_dir)` → rows ③ 대상 상품번호 sel_pids 선정 ④ 빌더 분기:
  - **append형**(식봄·캐시노트·배민상회·올웨이즈·ESM): `build_append_items(pf, rows, recs, sel_pids)` → `build_price_form_append((REF/pf['template']).read_bytes(), items, pf)`.
  - **smartstore**(default): `compute_new_prices(rows, recs, sel_pids)` → `build_bulk_price_xlsx(listing_smartstore.xlsx bytes, new_prices, cfg)`. (즉시할인 조정으로 net↑, 판매가 유지)
  - **쿠팡**(filter형): `build_filter_price_xlsx(listing_coupang.xlsx bytes, rows, sel_pids, cfg)`. raw는 '전체 교체' 네이티브 전제.
- **매입가 인상 이벤트 판단 규칙**: 미달(탐지 < -1%p)만 권장가로 인상, 기준 초과분은 유지(자동 인하 안 함 — 인상 취지 역행, 사용자 판단). 권장가=현 매입가로 기준마진 달성가(2,700·ceil).
- ★ 권장가는 **현재 저장 listing·기준마진율 스냅샷 기준** — 매입가/기준 재변경 시 갱신 후 재실행. (로그 2026-06-25-cmm-pricechange-coke-cost-increase)

### 브랜드 단위 인상(다품목) 확장 — 2026-07-29 코카콜라 3라인 8%
단품 2~3개가 아니라 **브랜드/라인 전체**가 오를 때의 추가 절차. (사례: 코카콜라·스프라이트·킨사이다 8%)
1. **영향 코드 추출** = product_master 상품명 정규식으로 원박스 코드 집합 생성 → 8채널 listing 코드를
   4-tier로 펼쳐 판정. 소분·PC낱개는 `canonical_code()`로 원박스에 접는다.
2. ★★ **합포(-CB-)는 이름이 아니라 구성코드로 판정** — `any(part in 영향집합)`.
   매입가 = Σ 박스매입단가 + 700 이라 구성 하나만 올라도 영향인데, **합포는 product_master에 행이
   없어 이름 매칭으로는 전량 누락**된다. 코카콜라 건에서 10건이 오직 이 경로로만 잡혔다.
3. **인상 반영** = reference 통째 복제한 샌드박스에서 **product_master의 영향 행만**
   매입단가·박스매입단가 ×(1+인상률). 합포·소분·낱개는 resolve_code가 원박스에서 파생하므로 손대지 않는다.
4. **인상 전/후 2회 compute_listing**(refs / refs_up, 같은 recs) → 기존 미달 vs 인상으로 전환된 건 분리.
   코카콜라 건: 영향 279 리스팅 중 인상전 미달 42 → 인상후 243, 인상대상 236.
5. ★ **인상률이 원 인상률(8%)을 넘는 건이 정상** — 인상 전부터 미달이던 리스팅은 권장가가 기존
   미달분까지 같이 회수한다. 균등 인상이 아니라 기준마진 역산이라 채널 수수료·배송비·N에 따라 갈린다
   (코카콜라 건 실측 채널평균 4.1~7.5%, 개별 최대 16.6%).
6. ~~알리는 가격변경 미구현이라 항상 수기~~ → **2026-08-11부터 알리도 양식 생성 가능**(multi_filter). 챗 네이티브로 만들 땐 저장 원본(listing_ali.xlsx)에 `build_multi_filter_xlsx`를 그대로 돌리면 된다.
7. ★ 샌드박스 계산은 앱에 반영되지 않는다. 인상이 확정되면 **app repo product_master를 실제로
   갱신**하는 별도 단계 필요.
- 로그: 2026-07-29-coke-8pct-price-adjust.md (29 원박스 + 합포 10 = 39코드 / 8채널 236건)

## 검증
- **스마트스토어 골든 705/706** (2026-06-10): 정산액 707/707·base매입단가 706/707·마진율 705/706.
- **식봄 골든 대조** (식봄결과페이지 716행, 2026-06-11): 정산가 H 485/485·합포 N 485/485·매입가 480/485(5 vintage). 로직 불일치 0.
- **캐시노트 골든 대조** (캐시노트결과페이지 513행, 2026-06-11): 골든∩계산 **513/513**. 입력 — 판매가 509/513(4 가격변동)·**배송비 513/513**·**N(합포) 513/513**·base매입단가 461/463(2 vintage, 50 골든#N/A). run: 544건·미매칭4(빈코드)·미설정10·마진미달26·제한36·평균마진율 9.2%. 정산가/마진율은 2700표준이라 골든과 의도적 차이.
- **캐시노트 가격변경 양식** (end-to-end, 2026-06-11): 오퍼/옵션코드 100% 캡처·listing 라운드트립 보존. 표본 5건 양식 — A=OFR·D=SKU·F=수정·G=권장가·H=정가(≥G)·L=Y·N=9999·O=관리코드 전건 일치, 예시행 제거·잔행 0. 식봄 회귀(합성) PASS.
- **쿠팡 모니터 골든 대조**(쿠팡결과페이지 1989행, 2026-06-11): 골든∩계산 1989/1989(옵션ID). 판매가·배송비(0) 1989/1989·**정산가(판매가×0.88) 1831/1831**·N(옵션ID) 1989/1989. base 1815/1826(11 vintage). 미매칭 158(155 관리코드 빈값)=골든도 동일 미해결(정상).
- **올웨이즈 모니터 골든 대조**(올팜결과페이지 748행 ↔ 다운로드 621행, 2026-06-12): 다운로드↔골든 ID조인 621/621(관리코드·판매가·정가). 입력 — **판매가 621/621**·**N(합포) 621/621**(hapo 올팜ObjectId 조회==골든 P열 748/748)·**정산액 617/619**(예외 2=−700 합포변칙). base 597/608(비CB; 11 불일치=소분 2원 반올림+vintage). 미매칭 2(`11-40-001-CB-…`)=골든도 #N/A 동치. run: 621건·미매칭2·미설정9·마진미달20·제한44·평균마진율 9.6%. 정산/마진율 2700표준이라 골든과 의도적 차(골든=base×N+700·실택배비3000).
- **올웨이즈 가격변경 양식**(end-to-end, 2026-06-12): parse→CSV 라운드트립(extra_cols 보존)→compute→양식. 표본 3건 — C카테고리/L재고 int·D판매상태·E관리코드·F/G옵션=상품명·**J개인구매가=FAKE_JEONG>K팀구매가(권장가)**·H/I/M 공백·예시r3 보존·샘플행 제거·외부링크 0. K=모니터 권장가 일치. stale 가드 거짓경고 0. 페이지 무수정(mode append 자동분기).
- **알리 모니터 + 자동정제**(ALIPRODUCT 25시트 → 정제 322 ↔ 골든 677, 2026-06-12): 정제 재현 322건(예시'--' 25 제거)·골든 교집합 322·정제전용 0. 입력 — 관리코드(SKU) **322/322**·상품명 **322/322**·판매가(소매가) **322/322**·N(hapo 알리상품번호==골든N) **322/322**(골든 677/677). 정산액==골든F 321/322(1 골든 중복ID 가격차)·base 314/320(6 vintage). 수수료 9%(F=판매가×0.91 322/322·배송0). run: 322건·미매칭1·미설정3·마진미달15·제한34·평균마진율 10.1%. VBA olevba 전수 — 숨은 저장 Sub 없음.
- **ESM(G마켓) 모니터 + consolidation**(11+22+33 2185행 → 지마켓 1193 → A중복제거 1193 ↔ 사용자 중복제거 1193, 2026-06-12): consolidation **1193/1193 완전일치**(차이 0). 골든(esm결과페이지, A키 조인 교집합 1193) — 판매가 **1193/1193**·배송비 **1193/1193**(무료636/3000 557, _num 콤마)·정산액(가격×0.825+배송비×0.967) **1189/1193**(4 stale/NA)·base 박스매입단가 **1170/1187**(17 vintage·0 미해결). N(hapo A·채널무관) N>1 389건 — **골든 N=#REF!라 N 자체 대조 불가**. run: 1193건·미매칭4·미설정13·마진미달49·제한82·평균마진율 9.5%. 정산/마진율 2700표준이라 골든(3000/3700) 의도적 차.
- **쿠팡 가격변경 filter**(2026-06-11): 선택만 남김·P=권장가·Q=가짜(+20~30%)·R/S 공란·조회(J/K) 보존·preview=파일 일치.
- **배민상회 가격변경 양식**(end-to-end, 2026-06-11): 옵션번호/옵션명/수수료raw 캡처·라운드트립 보존. 표본 양식 — A상품번호·C옵션번호·D옵션명·E관리코드·G현재소비자가·I현재판매가·J변경판매가(권장가)·**H변경소비자가=표준 FAKE_JEONG(권장가+20~30% 랜덤)** 기입, 예시행 제거. (초기 gap유지 → 사용자 요청으로 전 채널 랜덤 표준화)
- **배민상회 골든 대조** (배민결과페이지 395행, 2026-06-11): 골든∩계산 394/394. 입력 — 판매가 394/394·배송비 394/394·**수수료(상품별 BU/100+0.03) 394/394**·N 394/394·base 392/393(1 vintage). **정산가 394/394 일치**(정산식 동일, 실택배비만 표준차). run: 394건·미매칭0·미설정6·마진미달20·제한35·평균마진율 10.2%.
- **배민 양식 외부링크 수정(2026-06-11)**: `baemin_price_template.xlsx`가 원본 마스터 통합문서를 가리키는 **고아 외부참조**(externalLinks)를 품어 출력 파일을 엑셀에서 열 때 '외부 연결 업데이트 불가' 경고(숫자는 리터럴이라 다 맞음). 템플릿 정리본 커밋 + **`_strip_external_links`**(zip레벨: externalLinks 파트·workbook `<externalReferences>`·rels·Content_Types 제거, 외부링크 없으면 no-op)를 **append/bulk/filter 3개 출력 빌더 전부**에 적용(방어). cashnote/sikbom 템플릿은 외부링크 0건이라 무영향. 검증: 템플릿 ext (2,T,T,T)→(0,F,F,F), 양식 출력 ext 0, 시트 보존.

## 기준마진율 편집 (현재 마진율 → 기준, 전 채널 공통)
- **목적**: 선택 상품의 현재 마진율을 그 채널의 기준마진율(baseline_margin)로 저장. 미달 상품을 목표로 인정 → 미달 해제. (ADR 0016)
- **위치**: 모니터 페이지 하단, 표 다중선택(sel_pids) 재사용. 버튼 1개 → **새 기준 인라인 편집(st.data_editor)** → 저장. (offset 프리셋 폐기 2026-06-12)
- **충돌**: baseline 키=관리코드, 행=상품번호. 같은 관리코드 여러 상품번호가 현재마진 다르면 → 표 '현재 마진율' 칸에 `5.3% / 6.8% ⚠️`로 후보 표시(기본=최저), 사용자가 **새 기준 칸에 직접 입력**(라디오 폐기). `propose_baseline`이 (proposals, conflicts) 분리.
- **인라인 편집**: data_editor 새 기준(%) NumberColumn(percent·step 0.1·0~100), 기본값=현재 마진율(round 0.1%p). 저장 시 값/100→round(_,3). 빈 칸 행은 제외. `_fmt_margin` 저장표기(끝 0 제거).
- **채널 컬럼만**: `update_baseline_csv`가 baseline_col 컬럼만 수정(타 채널·타 관리코드·헤더/열순서/BOM/CRLF 보존). 없는 관리코드 행 추가.
- **즉시 반영**: baseline를 배포본 로컬(load_references) 대신 **GitHub 라이브**(`_load_baseline_text` @cache_data)로 읽어 `compute_listing(baseline_override=)` 주입 → 저장 시 cache clear+rerun, 재배포 불요. (기존엔 reference 로컬 read라 재배포 전 미반영)
- **검증**: 미달 10(관리코드 유니크)→baseline=현재→전부 미달 해제, 전체 49→29. 구조·타채널 보존, override 즉시반영.
- **UX 안정화(2026-06-22)**: 체크박스 stale(이상한 값 체크·간헐 미작동) 해소 — 두뇌④ 패턴 이식. ① 메인 표 key에 **`cmm_tblver` 버전카운터**(저장 시 +1로 선택 강제 초기화·filter_sig 무관) ② **인라인화**(버튼+`bl_{key}` session_state 2단계 → 선택 즉시 data_editor 1단계) ③ 저장 후 tblver+1+rerun → 즉시 반영+체크박스 풀림. page-only.
- 향후: ③일괄 규칙(필터 전체=고정값).

## 자사몰(카페24) — 9번째 채널 (2026-08-04)
- **다운로드가 CSV**(BOM UTF-8, 88열, 암호 zip). 전 채널 중 유일 → `file_format: "csv"`
  + `_parse_csv_download()`. `parse_download` 가 `load_workbook` 전용이라 분기 신설.
  cols 는 xlsx 와 동일한 **1-indexed 위치** 지정(헤더명 아님) — 열이 늘어도 A~T 고정이라 안전.
- **★ `모델명`(L=12)이 `[45-11` 형태로 여는 대괄호만 달려 나온다**(468/468, 닫는 괄호 0).
  안 벗기면 product_master 매칭 **전건 실패** → `code_strip_chars: "[]"` + `_strip_code()`.
  `자체 상품코드`(B)가 원래 관리코드 자리인데 전건 공백 — 모델명에 넣어 운영 중.
- **열 수 이력**: 구 VBA 86열 → 현재 88열(제조사명 49·브랜드명 52 추가).
  **A~T 구간 완전 동일**(판매가 20·모델명 12 불변) → 위치 지정 유지 가능.
- 수수료 = **PG 3.3% 단일**(판매수수료 없음, 사용자 확정). 배송비는 다운로드에 없음
  (관련 열 전건 공백) → `ship_fee_const` 3000(타 오픈마켓 동일).
- **정가 없음** — `소비자가`(Q) 전건 0.00 → jeong_field 없음(FAKE_JEONG 미생성).
  `상품가`(S)=판매가/1.1(VAT 제외가) 468/468 일치 — 마진은 **판매가만** 사용.
- **가격변경 = `csv_filter` 신설 모드**. 별도 업로드 양식 없음 — 다운로드 원본에서 선택 행만
  남기고 **T열(판매가)만 교체 → xlsx 출력**(입력 CSV / 출력 xlsx, 사용자 확정).
  ★ **상품가(S) 미기입** — 카페24가 판매가에서 자동 재계산(구 VBA `JasaMall_UpdateAndColor` 가
  T열만 건드린 것이 근거). 쿠팡 filter형 zip 수술 불필요(입력 CSV라 보존할 네이티브 포맷 없음).
- raw 저장이 `listing_{key}.xlsx` 고정이었음 → `_raw_ext(cfg)` 로 채널별 확장자
  (`listing_cafe24.csv`). **'신규만 추가' 비활성**(`append_rows_to_raw` 가 openpyxl 전용).
- 구 1세대 자산: `오픈마켓가격바꾸기V4.xlsm` 의 `CAFE24Module1~3` +
  `(자사몰)일괄수정/양식/매크로파일` 3시트. 3단계(행 대조복사 → T열 기입 → 시트 저장)를
  `build_csv_filter_xlsx()` 하나로 대체.
- **run 실측(2026-08-04, 468건)**: 미매칭 1(`26-01`)·미설정 6·미달 42·제한 41·**평균 9.89%**.
  코드해석 박스 459·소분 8(BT10EA/BT15EA)·미매칭 1.
- ⚠️ **카페24 실업로드 미검증** — openpyxl 생성 xlsx 수용 여부 미확인
  (식봄·캐시노트·배민·올웨이즈·ESM 정상, 쿠팡만 거부 전례).

## ★ raw 저장경로가 listing 경로와 충돌 — csv 채널 전용 함정 (2026-08-04)
`_listing_path(key)` 는 채널 무관 **항상** `reference/listing_{key}.csv` 다.
`_raw_path(key, ext)` 를 `listing_{key}.{ext}` 로 두면 **ext=="csv"(자사몰)에서 두 경로가 완전히 겹친다.**
→ `_commit_raw` 가 파싱된 listing 을 원본(88열) CSV 로 덮어쓰고, 모니터는 그걸 listing 으로 읽어
`코드` 열을 못 찾아 **관리코드 전건 빈값**이 된다. (xlsx 채널은 확장자가 달라 안 걸림 — csv 채널만.)
- 증상: 마진모니터에서 관리코드가 안 잡힘. 저장 listing 의 md5 가 업로드 원본과 동일하면 확진.
- 처방: `_raw_path` 가 ext=="csv" 일 때 **`listing_{key}_raw.csv`** 반환.
- 새 csv 채널 추가 시 반드시 `_listing_path` vs `_raw_path` 충돌 여부부터 확인할 것.

## ★ 합포(N) 미등록이 역마진으로 오탐된다 (2026-08-04)
`n_source: "ref"` 채널에서 `hapo_multiplier.csv` 에 상품번호가 없으면 **N=1 폴백** →
선물세트처럼 박스에 여러 세트가 든 상품은 매입가가 배수로 부풀려져 **역마진으로 오탐**된다.
- 실례: 자사몰 `45-11` 복합1호 — P0000BCK(미등록·N=1) 매입 97,500 → **마진 −283.78%**.
  **같은 관리코드** P0000BBA(등록·N=0.2) 매입 19,500 → 마진 7.80% 정상.
- 즉 **product_master 매입가 오류가 아니다.** 역마진이 보이면 hapo 등록 여부부터 볼 것.
  동일 관리코드의 다른 상품번호와 N 을 비교하면 즉시 판별된다.

## 채널 추가 레시피 (★앞으로 채널 다수 — 이 순서)
새 채널 = 보통 **CHANNEL_CONFIG 한 세트** 만(정산식은 스마트스토어 표준 고정). 코드 4-tier·reference·페이지·listing 저장은 공통(수정 불필요).
1. **다운로드 샘플 확보**(.xlsx 1개) — 컬럼 위치·헤더행·데이터행 채널마다 다름, 실물 필수.
   - **정제형(알리 등)**: 원본이 다중시트·다단헤더·매크로 정제를 거치면, 매크로 VBA를 olevba로 전수 추출(숨은 저장 Sub 채집) 후 `consolidate` config로 흡수(별도 정제 업무 없이 parse 자동). 골든은 정제본 기준.
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
- logs/2026-06/2026-06-11-channel-margin-monitor-cashnote.md · -cashnote-price-change.md · -cashnote-fake-jeongga.md · -cashnote-stale-listing.md · -baemin.md · -baemin-price-change.md · -fake-jeong-standard.md · -coupang.md
- logs/2026-06/2026-06-11-channel-margin-monitor-sikbom.md · -price-change-form.md · 2026-06-10-references.md
- manifest.md (A baseline_margin·product_master·hapo_multiplier / A-2 margin_floor·sobun·listing)

_갱신: 2026-06-11 (쿠팡 바코드 로켓그로스 제외 + 배민 양식 외부링크 strip + extra_cols 옵션번호 정수화)_

_갱신: 2026-06-11 (쿠팡 가격변경 filter 네이티브 zip 수술 — openpyxl inlineStr 업로드 실패 해소)_

_갱신: 2026-06-11 (쿠팡 raw inlineStr 오염 치유 + filter형 '신규만 추가' 비활성 가드)_

_갱신: 2026-06-11 (쿠팡 수술 출력 sharedStrings 정규화 — raw inlineStr/stale 무관 네이티브 보장, Reboot 필요)_

_갱신: 2026-06-12 (올웨이즈(올팜) 채널 추가 — 모니터. 판매가=팀구매가·10.5%·배송비0·N=hapo(올팜ObjectId). 골든 판매가/N 621/621. 가격변경 미구현)_

_갱신: 2026-06-12 (올웨이즈 가격변경(append) 추가 — K=권장가·J=FAKE_JEONG, extra_cols+int_fields. 6채널 전부 모니터+가격변경. 실업로드 미검증)_

_갱신: 2026-06-12 (알리(AliExpress) 채널 추가 — 모니터 + 다중시트 자동정제(consolidate, 매크로 대체). 수수료9%·N=hapo. 골든 입력 322/322. 7채널)_

_갱신: 2026-06-12 (ESM(G마켓) 채널 추가 — 모니터. 17.5% 단일·키=A마스터상품번호·지마켓필터+A중복제거(include_row_if_col_value·dedup_key)·_num 콤마. 골든 입력 판매가/배송비 1193/1193. **8채널 모니터/6채널 가격변경.** core 수정 → Reboot 필요. ADR 0015)_

_갱신: 2026-06-12 (ESM 다중파일 업로드 — multi_file·page accept_multiple_files. 배치 500상품 다운로드 한번에 병합(이어붙이기+A교차dedup), 수기병합 제거. core+page → Reboot)_

_갱신: 2026-06-12 (ESM 가격변경(append) 추가 — B=사이트상품번호·C=권장가·A순번(seq_col), extra_cols 보존, jeong 없음. esm_price_template.xlsx. 양식 30표본 전건 일치 + **실업로드 성공 사용자 확인**. **8채널 모니터/7채널 가격변경.** core → Reboot)_

_갱신: 2026-06-12 (기준마진율 편집(현재→기준) 추가 — 전 채널 공통. 선택→현재 마진율을 그 채널 baseline으로, 충돌 사용자선택·0.1%p반올림·baseline 라이브read 즉시반영. ADR 0016. core+page → Reboot)_

_갱신: 2026-06-17 (ESM 채널키 'esm' 소문자 명명 예외 함정 — cross-module 'ESM' 대문자와 불일치 잠복지뢰. 데일리는 _cmm_key로 방어)_

_갱신: 2026-06-18 (이력 1d — listing 커밋 시 채널 가격 날짜본 스냅샷 적립 훅(_accumulate_listing). core listing_history.py 신규. forward·비차단. import 신규→Reboot 1회)_

_갱신: 2026-06-22 (전월매출 2컬럼(이채널·전체) — 표 참고. core canonical_code(박스/낱개/소분→원박스 통일)·page _load_prev_sales/_CH_TO_SANGHO(쿠팡=윙+로켓). 매출자료=박스코드(낱개·합포·소분 0건 검증)→listing만 정규화. 같은 canonical 행 같은값=세로합산금지. 베이스(%)는 성능으로 보류. core→Reboot 1회. 커밋 core 9c265d12·page 4aee8eb0)_

_갱신: 2026-06-22 (제한 상품 등록/해제 UI — 표 선택→제한내용 입력/비움→margin_floor.csv 등록/수정/해제. core parse_floor_dict·update_floor_csv·compute_listing floor_override(즉시반영). 권장가↔제한. 두뇌④ load_locked 공용. core→Reboot. 커밋 core f8726dcd·page 18af7eb4)_

_갱신: 2026-06-22 (기준마진율 설정 UX 안정화 — 인라인화(2단계→1단계)+표 버전카운터 cmm_tblver(저장 시 선택 강제 초기화), 두뇌④ mo_tblver 패턴 이식. 체크박스 stale 해소. page-only. 커밋 13b33e56)_

_갱신: 2026-06-22 (전월매출(전체) 정의 정정 — '전 거래처'가 아니라 **내 관리 8채널 합**(나들·B2B 제외, 사용자 정정). _load_prev_sales total을 _CH_TO_SANGHO 상호명으로 한정. page-only. 커밋 474885c0)_

_갱신: 2026-06-24 (단건 관찰 — 쿠팡 '택배비 무료 적용건'은 우리가 실택배비 2,700 미부담 → 표준 정산식에서 **실택배비 2,700 차감 제외**. 동일 매입/판매가도 마진 급변(11-75-05: 차감1.75% vs 미차감25.1%). 수수료·배송비식은 동일. 현재 단건이라 코드 규칙화 보류, 다건 시 채널/상품 플래그로 정식화. 로그 2026-06-24-sikbom-event-5th-md-submission §학습)_
- logs/2026-08/2026-08-04-cafe24-channel.md (자사몰 채널 추가·csv_filter·CSV 파싱)

## ★ 알리 가격변경(multi_filter) 검증 — 2026-08-11
실데이터(listing_ali 312건·원본 51시트/25 visible) 골든:
- **선택 16건**(권장가 없는 4건 포함) → 기입 12 · 제외(권장가 없음) 4 · 누락 0.
- **zip 파트 대조**: 59/59 파트 중 **변경분 = 보이는 시트 25개뿐**(숨김 26개·styles·workbook.xml·dataValidations 전부 바이트 동일).
- **셀 단위 무손실**: 남긴 행은 **E(가격) 외 전 셀 원문 동일**(스타일 s=64 보존·행 속성 ht/customHeight 보존), 행번호만 연속 재번호.
- **선택 0건 시트**(콜라 등): 헤더 r1~5만 남고 데이터 0행 — 업로드 시 처리 대상 없음.
- **라운드트립 재파싱**(`parse_download` consolidate): 12/12 · 판매가 = 권장가로 정확히 반영.

_갱신: 2026-08-11 (알리 가격 일괄변경 추가 — multi_filter형 다중시트 zip 수술. 9채널 모니터/9채널 가격변경. 원본이 곧 가격수정 양식이라 저장 raw 재사용·'전체 교체' 전용. 데일리 대시보드 가격변경 시트에도 multi_filter·csv_filter 분기 추가(자사몰은 종전 bulk 폴백으로 크래시 경로였음). 커밋 core dfa72d70·page6 c207b256·daily aa1ec33d. ⚠️ core 변경 → Reboot 1회 · 알리 실업로드 미검증)_

## 표 내보내기 = XLSX (2026-08-11, 구 CSV 대체)
`_export_xlsx`(page-only, openpyxl 직접 작성). 대상 = 선택분 있으면 선택 / 없으면 현재 필터 전체.
- **텍스트 강제**: 상품번호·관리코드·상품명·규격·코드유형·탐지·권장가/제한·비고.
  ★ CSV 시절 엑셀이 관리코드를 날짜(`45-21`)로, 알리 상품번호 16자리를 지수표기로 깨뜨리던 문제 해소.
- **숫자 `#,##0`**: N·재고·매입가·판매가·배송비·정산액·전월매출 2종 / **퍼센트 `0.0%`**: 마진율·기준마진율(소수 원값 → 엑셀 정렬·필터 가능).
- 빈값은 빈칸 유지(0 채움 금지) · 헤더 볼드+음영 · freeze A2 · auto_filter · 컬럼 폭.
- 권장가/제한은 제한 문구가 섞이는 혼합 컬럼이라 텍스트(`'21,200'`) — 숫자 정렬 필요 시 별도 숫자 컬럼 추가.

_갱신: 2026-08-11 (표 내보내기 CSV→XLSX — 코드 텍스트 박제·금액 콤마·마진율 %·헤더고정/필터. page-only 커밋 8491a6a0)_

## 리테일앤인사이트(토마토) — 10번째 채널 (2026-08-11)
B2B 공급처. **cmm 최초로 다운로드에 우리 관리코드가 없고 바코드(EAN-13)만 오는 채널.**

### 설정
`key retail` · 수수료 **2%** · `ship_fee_const 0`(배송비 수입 없음) · `real_ship 2700` ·
`baseline_col "토마토"`(열 이름=플랫폼명, 채널 표시명은 리테일앤인사이트) · `n_source "ref"` ·
`header_row 1` · **`data_start 3`** · 즉시할인·포인트·배송비 컬럼 없음. 정산식은
retail-insight-pricing 워크플로우에서 확정한 것과 동일(정산액=판매가×0.98, 이익=정산액−매입가−2,700).

### ★ 신규 축 `cols_by_header` — 컬럼 위치 고정 포기 (2026-08-25)
**리테일은 다운로드 양식이 예고 없이 바뀐다.** 2026-08-25 **17열 → 9열**로 축소되며
컬럼 전체가 한 칸 왼쪽으로 밀렸고(A=상품코드), **등급별 할인가 컬럼이 사라졌다**.
위치 고정 `cols` 는 상품명을 코드로 읽어 **전건 미매칭 + 판매가 0** 으로 listing 을 오염시켰다(사고 기록 아래).

```python
"cols_by_header": {
    "상품번호": "상품코드", "코드": "상품코드", "상품명": "상품명",
    "판매가": ["기본등급 할인가", "정상가"],   # 앞에서부터 있는 것 채택 = v1/v2 동시 수용
    "정가": "정상가",
},
"extra_cols_by_header": {"리테일규격": "규격", "입수": "입수", "품절여부": "품절여부"},
```
- `_resolve_cols_by_header(ws, cfg)` 가 `header_row` 라벨 → 컬럼 인덱스로 해소. **v1/v2 를 명시
  분기하지 않는다** — 라벨만 같으면 v3·v4 도 무수정 수용.
- **필수 컬럼(상품번호·코드·상품명·판매가) 미발견 시 즉시 `ValueError`** + 실제 헤더 목록 출력.
  조용한 오염 경로를 구조적으로 차단(이 채널의 핵심 안전장치).
- **서브헤더 행 방어**: 코드 칸 값이 헤더 라벨 집합에 있으면 skip. `data_start` 만으론 불충분하다
  (v1 = r2 배송유형 서브헤더 / v2 = r2 공백).
- 타 채널은 `cols` 위치 고정 경로 그대로(`by_header` 분기) — 회귀 없음.
- **정상가 = 수수료 2% 붙기 전 가격**(사용자 확정 2026-08-25) → 판매가 자리에 그대로 넣으면
  기존 정산식(정산액 = 판매가×0.98)과 정합. 등급 할인이 생기면 이 전제가 깨지므로 재확인 필요.
- v2 는 **부분 export**(전건 `Trade전시여부=Y ∧ 품절여부=N`, 331/559). 마진 모니터엔 무해하나
  **전수 판정(미등재 탐지)은 품절 포함 전체 export 로만** 할 것.

### 신규 축 `code_map` — 바코드 → 관리코드 (조회 시점 변환)
`cfg["code_map"]={"file":"retail_barcode_map.csv"}` → `load_references(ref_dir, code_map_file)`가
`refs["code_map"]`(바코드 키)로 로드 → **`compute`가 조회 시점에 치환**한다(parse 시점 아님).
listing엔 바코드가 그대로 저장되므로 **변환표만 고치면 상품관리 재다운로드 없이 즉시 반영**.
변환표에 없으면 `비고="바코드 미매핑"`(→ 변환표 등록) — `관리코드 미등록`(→ product_master 등록)과 조치가 다르므로 구분.
편집 = 기준데이터관리 > **리테일앤인사이트** 페이지(검색·인라인·전체교체).

### ★ N(합포량)이 이 채널의 진짜 난점
리테일 등재 1건 ≠ 우리 박스 1개. 예: '코카콜라 355ml 업소용' 38,600원 ≈ 박스매입 15,931 **×2**.
N=1로 두면 **173건이 마진 30%+** 로 뜬다(전부 오탐).
- **다운로드 `입수` 컬럼은 신뢰 불가** — 스팸 클래식(입수40·규격 200g\*20 → 2)처럼 맞는 행도 있고,
  칠성사이다 제로(입수24·규격 355ml\*24 → 1인데 실제는 2박스)처럼 어긋나는 행도 있다. 자동계산 금지.
- **`hapo_multiplier.csv`가 바코드 키라 177건은 이미 채워져 있다**(스마트스토어가 바코드를 N 소스로 쓰는 덕).
  적용 시 마진 중앙값 6.6%로 정상화.
- ⚠️ **hapo는 채널 무관 가정 → 리테일에서 어긋나는 케이스 존재**(티오피 200ml hapo N=3인데 리테일은 2 → −54.7% /
  참맑은 175ml 7종 hapo N=3 → −3~−5%). → **변환표 `N` 열이 채널 전용 override.**
  우선순위 = **변환표 N → hapo(바코드) → 1**.
- 진단 요령: 마진 25%↑ = N 과소 · 마진 −2%↓인데 N>1 = N 과대 · N=1인데 판매가÷박스매입 ≥1.8 = N 미설정.

### 가격변경 = 알리와 동일(multi_filter)
별도 업로드 양식 없음 → **다운로드 원본이 곧 업로드 양식**(사용자 확정). `build_multi_filter_xlsx`를 일반화해 재사용:
기하/라벨을 `price_form` 우선(→consolidate→채널 기본)으로 읽고, **복수 가격칸**(`price_labels`)·**숫자셀**(`price_cell:"num"`) 지원.
리테일은 정상가·기본등급 할인가가 전건 동일(할인율 0)이라 **두 칸에 같은 권장가**를 기입한다.
**'전체 교체' 전용**(multi_filter는 native_raw 가드 대상).

### 검증 (2026-08-11 실데이터)
파싱 559 · 바코드→관리코드 **548/559** · 매입가 해소 539 · 마진 중앙값 6.6% · 기준마진 미설정 0(토마토 열 1,230행 보유).
미해결 21 = 바코드 미매핑 11(합성코드 monsterset1~3·MAEIL3·'신규바코드필요') + 관리코드 미등록 5 + 매입가 0 (5).
가격변경 양식 = 선택 8 → 8/8 기입 · zip 파트 중 `sheet1.xml`만 변경 · 헤더 r1/서브헤더 r2 보존 · 라운드트립 8/8.

### 미완
① **N 검수**(대상 49건, 산출 `리테일앤인사이트_N검수_20260811.xlsx`) — 확정 전 마진율은 참고치.
② **리테일 실업로드 미검증** — 특히 정상가까지 함께 바꾸는 게 맞는지(아니면 `price_labels`에서 정상가 제거).
③ 전월매출 빈칸(`_CH_TO_SANGHO`에 리테일 상호명 미등록).

_갱신: 2026-08-11 (리테일앤인사이트 10번째 채널 — 바코드 code_map 축 신설·N override·multi_filter 가격변경. 커밋 core e66de968·map 18fb5bd1·page b25adf50. ⚠️ Reboot 1회·N 검수 미완·실업로드 미검증)_

## ★ 옥션 거래 종료 (2026-08-12, 사용자 확정)
ESM(G마켓+옥션 통합) 중 **옥션은 거래 종료**. 실적상 이미 반영 — EasyAdmin 주문 기준 선물세트 ESM 내
옥션 비중이 추석24 54.2% → 추석25 28.9% → **설26 0.5%**로 소멸했고, 옥션 판매중지일이 2025-11-14
(추석25 종료 직후)에 집중돼 있다.
- cmm ESM 파싱의 `include_row_if_col_value {"col":6,"value":"지마켓"}`는 원래 **다운로드 중복제거** 목적이었으나
  이제 **거래 정책과 일치**한다. 지마켓 행만 남기는 것이 곧 우리 판로 전부 = 필터 유지가 정답.
- 다운로드 raw에는 여전히 옥션 행이 딸려온다(마스터상품 단위 export). raw의 옥션 판매중지 행은 **정상**이며
  조치 대상이 아니다.
- ⚠️ **함정**: 저장된 `listing_esm.xlsx`(raw)는 500상품 한도 **다중 배치 중 한 개**만 저장된다(`multi_file`).
  CSV는 전 배치 병합본이라 **raw ≠ CSV 출처**. raw로 CSV 행의 판매상태를 역추적하면 안 된다
  (키 포맷도 다름 — raw 상품번호는 `D854086293` 영문+숫자, CSV 사이트상품번호는 순숫자).
  2026-08-12에 이 역추적으로 "listing에 판매중지 113건 혼입" 이라는 **잘못된 결론**을 냈다가 철회.
- ⚠️ 미확인: 옥션 종료가 선물세트 한정인지 **전 품목**인지. 전 품목이면 ESM 기준마진·목표 실적 기저를
  지마켓 단독으로 재점검 필요(대시보드 ESM 채널 실적 포함).

_갱신: 2026-08-12 (옥션 거래 종료 — 지마켓 필터=정책 일치 · raw는 부분 배치라 상태 역추적 금지)_

## 자사몰(카페24) — 무료배송 리스팅 배송비 0 분기 (2026-08-20, 커밋 `bf88a36`)

자사몰 config 는 `ship_fee_const: 3000` 이라 **전 리스팅이 배송비 3,000 을 받는다고 가정**했다.
무료배송 리스팅은 실제로 배송비를 안 받으므로 정산액이 `3,000 × 0.967 = 2,901` 만큼 부풀고
마진이 **+2.9 ~ +10.5%p 과대**로 표시됐다.

**판별 필드 = `공급사`.** 카페24의 공급사는 공급처가 아니라 **배송조건 그룹**으로 운영 중이다
(`S00000HC/HD/HE/HJ/HK/HL` = 일반합포2/3/4/5/6/8, **`S00000HM` = 무료배송**). 정본 = `workflows/cafe24-register.md` §2.

```python
"ship_fee_const": 3000,
"ship_fee_zero_if": {"col_name": "공급사", "values": ["S00000HM"], "col_fallback": 50},
```
`_parse_csv_download` 에 `_ship(row)` 분기 추가 — 해당 공급사면 배송비 0, 아니면 기존 상수.

- ★ **컬럼은 헤더명으로 찾고 위치는 폴백으로만 쓴다.** 공급사는 50열로 기존 A~T(1~20) 고정 구간 밖이라
  다운로드 양식이 바뀌면 밀린다. `header_row` 를 읽어 라벨 매칭 → 실패 시 `col_fallback`.
- ★ **상품명으로 판정하면 안 된다.** 이름에 `무료배송` 이 없는데 HM 인 건(`P0000BCK`)과
  이름에 있는데 HM 이 아닌 건(`P00000QM` 17차)이 실제로 공존한다.

**골든(730행 실 export)**: 배송비 3000→0 **정확히 3건**(`P0000BCK`·`P0000BCJ`·`P0000BCI`),
나머지 727건 불변, **배송비 외 전 필드 동일**. 공급사 앞에 더미 컬럼을 끼운 CSV 로도 3건 정상 판정.

효과: `P0000BCK` 16.12% → **실제 5.64%**(이후 24,000→24,900 정정해 9.05%), `P0000BCI` 14.72% → 11.86%.

⚠️ `core/` 모듈 변경 → **Reboot 1회 필요**.

### 자사몰 무료배송 가격 규칙
`무료배송가 = 일반 1세트가 + 3,000`, **마진율 불변**.
자사몰은 PG 3.3% 가 판매가·배송비에 동일하게 붙으므로 배송비 수입을 판매가로 옮겨도 정산액이 같다
(`2,901 ÷ 0.967 = 3,000`). 박스 리스팅도 동일: `1세트가 × 세트수 + 3,000`.

### 자사몰 hapo N (2026-08-20)
`n_source:"ref"` → `hapo_multiplier.csv`, 키 = **상품코드**(`P0000…`), 채널 컬럼 공란(기존 자사몰 52건 관행).
1세트 리스팅 `N = 1 ÷ 박스내품`. 2026-08-20 선물세트 신규 50건 등록(3,358 → 3,408행).
⚠️ **판매Y 필터 export 만 보면 판매중지분이 빠진다** — 여러 export 를 합쳐 유니크 상품코드로 등록할 것.

_갱신: 2026-08-25 (리테일 `cols_by_header` 축 신설 — 양식 17열→9열 변경 대응. 판매가=[기본등급 할인가, 정상가] 폴백·필수컬럼 미발견 시 즉시 예외·서브헤더 행 방어. 위치고정 파싱이 전건 미매칭+판매가 0 으로 listing 을 조용히 오염시킨 사고 동반 → **전체 교체 재파싱 필요**. 커밋 core ecc77d4d. 골든 5종 통과·타 채널 무회귀. 데일리대시보드 당일마진 테이블 검색창 추가(관리코드·상품명·채널 / 공백=AND·쉼표=OR, 커밋 51c6e9e3·Reboot 불요))_

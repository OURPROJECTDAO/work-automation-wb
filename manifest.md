# manifest.md — 연결 맵 (자산·의존 역색인)

> **공유 자산을 바꾸기 전 여기서 영향범위(blast radius)를 확인한다.** 워크플로우별 상세는 workflows/<name>.md.
> 이 파일은 캐치업 상시읽기 세트가 아님 — 공유 reference/체인을 건드릴 때만 읽는다.
> 갱신 규칙: 공유 reference 추가·소비자 변동, 워크플로우 간 체인/상속 추가, 등록 채널 자산 위치 변동 시 갱신.

## A. 공유 reference → 소비자 (영향범위) ★다중소비자 = 바꾸면 여러 곳 영향
| 파일 | 위치 | 소비 워크플로우 | 편집 경로 | 비고 |
|---|---|---|---|---|
| `product_master.csv` | app `reference/` | logistics-order(재고 iloc14)·dashboard(중분류·박스내품)·smartstore/easyadmin/esm-register(매입가·박스내품·규격)·**upload-monitor**(박스재고·매입가·상품코드 키) | 연동데이터관리>상품관리 (매일 갱신·타임스탬프) | **연동데이터**(매일 변동). 컬럼 위치참조(iloc4=관리코드,14=박스재고) 깨지면 logistics 재고 오류 |
| `logistics_classification.csv` | app `reference/` | logistics-order(구분 GATE A)·cheonnyeon-upload(구분 룩업,읽기만)·dashboard(1차 구분) | 발주서출력업무 페이지 + 대시보드 🏷분류 도우미 | 코드 추가는 발주 GATE 줄이기만(안 깨짐). 단 발주 안 거치는 코드 오분류 시 그 분류로 처리 주의 |
| `product_attributes.csv` | app `reference/` | dashboard(세분류=최종분류 차원 + 식품음료=구분 3차 fallback)·upload-monitor(합포수량=L4 prefill) | 합포데이터.xlsx(Drive 작성용)에서 추출 재커밋 | 관리코드 속성표(1,134). **4컬럼만**: 식품음료·합포수량·최종분류(ADR 0011, 브랜드·b2b·정제규격 폐기). PII 없음. 구분 source=logistics_classification 별도유지 |

| `baseline_margin.csv` | app `reference/` | channel-margin-monitor(확정마진율, 채널별 열) | 추후 연동데이터 페이지 | 관리코드+10채널 확정마진율(1,229). 키에 박스/PC/소분/합포 혼재. **향후 전 채널 모니터 공용** |
| `hapo_multiplier.csv` | app `reference/` | channel-margin-monitor(합포량 N, 바코드 없는 채널) | 상품몇개합포인지.xlsx에서 추출 재커밋 | 상품번호·합포량·채널(3,339). 골든 '마진율예외처리시트'. **상품번호 단일키**(채널무관), 미등록 N=1, 분수 가능. 스마트스토어 판매자바코드의 외부판 — **다중채널 공용**(ADR 0013) |

## A-2. 단일소비자 reference (소유 워크플로우 전용 — 영향 국소)
| 파일(app `reference/`) | 소유 |
|---|---|
| dosan_list / dosan_except_list / filter_list / undelivered_list | openmarket-merge |
| sku_list | onnuri-order |
| unit_list / spec_master | logistics-order |
| bm_commission / sub_list | cheonnyeon-upload |
| smartstore_category_food / smartstore_bulk_template | smartstore-register |
| `product_input_form_v2.xlsx` (배치 입력폼, **멀티채널 공유**) | smartstore + esm (구 smartstore_input_form_v1 deprecated) |
| esm_category_food / esm_bulk_template | esm-register |
| (easyadmin 양식 — **미보관, C 참조**) | easyadmin-register |
| margin_floor / sobun | channel-margin-monitor |
| `listing_<channel>.csv` (+meta) — 채널 상품관리 스냅샷, 페이지에서 교체/병합 | channel-margin-monitor (**upload-monitor 읽기 공유**) |
| `sikbom_price_template.xlsx` — 식봄 '상품 일괄수정' 가격변경 양식 고정 템플릿(append) | channel-margin-monitor |
| `cashnote_price_template.xlsx` — 캐시노트 '옵션 일괄수정' 가격변경 양식 고정 템플릿(append, (캐시노트)양식) | channel-margin-monitor |
| `baemin_price_template.xlsx` — 배민상회 가격변경 양식 고정 템플릿(append, (배민)양식) | channel-margin-monitor |
| `groups/store_groups.csv` (data repo, private) | dashboard |
| `master/sales_YYYY-MM.parquet` (data repo, private) | dashboard |

## B. 워크플로우 의존 그래프 (체인·상속·공유)
- **cheonnyeon-upload ← logistics-order**: 발주자료 아카이브(★★발주자료) 앞 7열을 입력으로 받음 + logistics_classification.csv 공유. (decisions/0005)
- **dashboard ⇄ logistics-order**: logistics_classification.csv 공유(대시보드 1차 구분 = 발주 분류표). 대시보드 🏷도우미가 이 표에 쓰기(decisions/0007).
- **dashboard ← product_master**: 중분류 2차 fallback·박스내품(물류량).
- **dashboard ← product_attributes**: 세분류(최종분류) 차원 + 식품음료=구분 **3차** fallback(1차 logistics_classification → 2차 product_master 중분류 → 3차 식품음료). 구분 source 별도유지. (브랜드·b2b 차원은 ADR 0011로 폐기.)
- **smartstore / easyadmin / esm-register → product-registration-common 상속**: 공통 개념(낱개·박스·합포N·판매가공식·상품명·서식). 공통 규칙 바꾸면 3채널 전부 영향. (decisions/0009)
- **3 등록채널 ← product_master**: 매입가·박스내품·규격.
- **channel-margin-monitor ← product_master·baseline_margin·sobun·hapo_multiplier**: product_master(매입가/재고/규격/박스내품, 코드 4-tier 해석)·baseline_margin(확정마진율 채널열)·sobun(소분 변환코드→원코드·내품나누기). 합포 -CB-는 코드파싱(reference 없음). 합포량 N(판매배수)은 바코드 없는 채널(식봄 등)에서 hapo_multiplier(상품번호) 조회 — 스마트스토어는 다운로드 바코드. ⚠️sobun ↔ logistics `unit_list` ↔ cheonnyeon `sub_list` 소분/낱개 개념 중복 — 통합 추후 검토.
- **invoice-fill ← 송장 마스터(송장출력.xlsx)**: 세션 업로드(PII, 미저장). ⚠️openmarket-merge '송장출력' 시트 계열로 보이나 문서상 명시 연결 없음 — 확인 필요.
- **upload-monitor ← product_master·listing_<channel>·sobun·resolve_code(채널마진모니터)·product_attributes**: 재고(박스[14])·박스매입가·상품코드 키. listing 8채널 스냅샷 공유(마진모니터 소유, **읽기**). resolve_code 4-tier 분류 재사용(`resolve_identity` 래퍼=상품코드 반환). sobun=소분 환원. product_attributes 합포수량=L4 등록 prefill. **→ register(product_input_form_v2.xlsx) 인계**(스마트스토어·ESM 자동폼, 6채널 CSV). (decisions/0017)

## C. 상품등록 채널 자산 위치 (챗 네이티브)
> 양식·카테고리 = 거의 불변(정본 = app `reference/`). 소스·결과 = 배치별(Drive).
| 채널 | 양식 | 카테고리표 | 소스/결과 (Drive) |
|---|---|---|---|
| smartstore | `reference/smartstore_bulk_template.xlsx` (출력양식) · `reference/smartstore_input_form_v1.xlsx` (배치 입력폼) | `reference/smartstore_category_food.csv` | 상품등록/(smartstore 폴더 미생성) |
| esm | `reference/esm_bulk_template.xlsx` | `reference/esm_category_food.csv` | 상품등록/esm/ (소스 `[소스]글로벌하베스트.xlsx`) |
| easyadmin | **미보관(다음 배치 때 확보)** | 불필요(정산채널) | 상품등록/(easyadmin 폴더 미생성) |

입력 수집 양식(공통, 멀티채널): `reference/product_input_form_v2.xlsx` — smartstore·esm 공용(대상 채널 선택). 구 `smartstore_input_form_v1.xlsx` deprecated.

Drive 폴더ID: 업무자동화-KB=14A71qcaYm90gDxnbwSglEoMShccnn1-0 · inputs=1XtcfqkLbUd4mhKFYWSnI8cEYB3lN6D9W · outputs=1oAExNiKw_uV9NLWVOa3a2ImDsMtpMU30 · 상품등록=1f3h8XrIfOT2ctBYxI8KfShroY17ghKUF · 상품등록/esm=1Vsf5iQb8X40BwUvra1_FbymD8JXG21vy

## D. 공유 코드/페이지 (app repo — 한 파일이 여러 워크플로우 호스팅)
- `app/pages/1_파일처리.py` — **openmarket-merge · logistics-order · cheonnyeon-upload** 탭 공존. 탭 추가/순서 변경 시 st.stop() 전역중단 함정(pitfalls) 주의.
- `app/pages/2_기준데이터관리/` — 각 워크플로우 reference 편집 페이지. 편집표 검색+merge-back 패턴(pitfalls) 공통.
- `app/pages/3_연동데이터관리/1_상품관리.py` — product_master 업로드(다중 소비자 자산 갱신 지점).
- `core/dashboard/`, `core/workflows/` — import 모듈 변경은 Reboot app 필요(pitfalls).

## 관련
- 등록 공통 → workflows/product-registration-common.md · 설계결정 → decisions/

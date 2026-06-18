# 현재 상태 (스냅샷)
> 워크플로우 상세 = workflows/<name>.md · 작업 이력 = logs/ · 백로그 = roadmap.md · 전역 함정 = pitfalls.md · 결정 = decisions/

## 운영 인프라
- KB 기억 시스템: GitHub OURPROJECTDAO/work-automation-wb (main).
- 코드 저장소: GitHub OURPROJECTDAO/work-automation-app (main, public).
- 엑셀 작업물: Google Drive 업무자동화-KB/templates·inputs·outputs.
- 웹 앱: Streamlit Community Cloud 배포·운영 중.

## 워크플로우 인덱스 (이관 완료 = 운영 중)
> 상태는 통제어휘(운영중/진행중/이슈/개념doc). **상세·검증·미해결·자산은 각 workflows/<name>.md**. 연결=manifest.md. **구조화 정본(노드 status·로드맵·연결)=systemmap.json (ADR 0019); 아래 표·다음 한 수는 사람용 서사 미러.**

| 워크플로우 (내부명) | Phase | 상태 | 상세 |
|---|---|---|---|
| openmarket-merge (오픈마켓합포도서산간확인V7) | 1 | 운영중 | workflows/openmarket-merge.md |
| onnuri-order (온누리양식_발주서/제이티발주) | 3 | 운영중 | workflows/onnuri-order.md |
| logistics-order (발주서출력업무) | 3 | 운영중 | workflows/logistics-order.md |
| cheonnyeon-upload (천년경영업로드V15) | 3 | 운영중 | workflows/cheonnyeon-upload.md |
| invoice-fill (송장처리) | 3 | 운영중 (4채널) | workflows/invoice-fill.md |
| dashboard (영업이익현황) | 4 | 운영중 (이익률·물류량 점진) | workflows/dashboard.md |
| product-registration-common (등록 공통) | — | 개념doc | workflows/product-registration-common.md |
| smartstore-register (스마트스토어) | — | 운영중 (챗) | workflows/smartstore-register.md |
| easyadmin-register (이지어드민·정산채널) | — | 운영중 (챗) | workflows/easyadmin-register.md |
| esm-register (ESM=G마켓) | — | 운영중 (챗) | workflows/esm-register.md |
| cashnote-register (캐시노트=KCD) | — | 운영중 (1차 87건 업로드 성공·검증완료) | workflows/cashnote-register.md |
| channel-margin-monitor (채널 가격·마진 모니터) | — | 운영중 (8채널 모니터 / 7채널 가격변경) | workflows/channel-margin-monitor.md |
| upload-monitor (업로드감시) | — | 운영중(업로드제외 등록/해제, L4 대기) | workflows/upload-monitor.md |
| intelligence-layer (지능 레이어·이력엔진+두뇌) | — | 진행중 (1a·1b·두뇌①·주문 39개월·판매가검증·P2·매입현황·탭D·두뇌②·고객키/합포박스키 적재·**ship_alloc 합포 ceil(팩/3) 교정**·**두뇌③ A/B v1**(서술+마진율별판매량 탄력성)·**상품360카드 v1** 완료) 두뇌3종+통합카드 완성·다음=사용자선택 | workflows/intelligence-layer.md |
| daily-dashboard (데일리 대시보드) | — | 진행중 (당일점검+세션인계+품절알림판+채널요약+가격변동알림+이상치→가격변경시트) | workflows/daily-dashboard.md |

## 완료된 Phase
- Phase 0: 코드 repo 스캐폴딩. 2026-06-01.
- Phase 1: openmarket_merge 8단계 + pytest. 2026-06-01.
- Phase 2: Streamlit 앱 + Community Cloud 배포 + 기준데이터 관리 UI. 2026-06-01.
- Phase 3 (진행 중): 4종 완료 (onnuri-order, logistics-order, cheonnyeon-upload, invoice-fill). 나머지 템플릿 대기.
- Phase 4 (운영 최소): 대시보드 — 데이터계층+저장어댑터+3개년 적재(313K행)+최소 페이지(매출 집계)+증분 업로더([데이터 추가] 탭) 배포. 차트/물류량/이익률/거래처그룹 점진추가. 2026-06-08. (decisions/0006)

## 막힌 것 / 이슈
- 없음. (B2 인프라 완료 — repo·PAT R/W·st.secrets 검증됨 2026-06-08.)

## 다음 한 수
- **★★ 다음 세션 최우선 착수 — 시장 지능(경쟁가) nadl 로컬 수집기 (2026-06-16, ADR 0025).** nadl.kr(사람검수 B2B몰·행사 근사최저가·중복없음) 1순위. **클라우드(Streamlit/Actions=해외IP) 지오펜스+robots로 도달 불가** → KR 로컬 수집기(회사 PC·Windows 스케줄러·주1회·저속) → parquet push(work-automation-data) → 두뇌① 시장대비 권장가. 네이버 쇼핑 API=클라우드 보완 후순위. **막힘=nadl 행사 페이지 실물 1장 대기(파서 작성용).** 상세 ADR 0025·logs/2026-06/2026-06-16-market-intel-nadl-feasibility.md.
- **★★ 세션 클로즈 (2026-06-16): 데일리 대시보드 품절 알림판 + 품절목록 cadence 완성.** 이번 세션 완료 — ①품절 알림판 v1(ADR 0024: 발주 품절목록 자동등록·박스재고>0 재입고 입고로그+자동삭제·수동삭제·영속) ②품절목록 E/F/G(최근입고일·평균매입주기·입고횟수 **1년 윈도우**·logistics generate_result_xlsx·purchases.cadence_by_code) ③매입현황 2026-06(1~15일) 적재(개별 export 742행·54파티션·66,741행·거래처관리코드 alias로 거래처 78% 보존) ④품절 알림판 표에도 E/F/G 표시(board_to_frame cadence·최근 13개월 로드). **⚠️ 미적용 = Reboot app 1회 필요** (이번 세션 core 변경분: daily_inbox·stockout_board·purchases·logistics_order). **재배포(1~2분)+Reboot 후 테스트**: (a)파일처리 실행→데일리 대시보드 자동 인계 (b)발주 Phase2→품절 알림판 자동등록 + 물류팀 품절목록 E/F/G (c)상품관리 갱신(재고>0)→알림판 재입고 자동삭제+입고로그 (d)알림판 표 최근입고·평균주기·입고(1년) 표시. ⚠️ 최근입고일 상한=적재된 매입현황 최신(~2026-06-15) — 월1회 개별 export 적재 운영. **다음 한 수=데일리 대시보드 확장판**(추가 데일리 인사이트 — 사용자와 설계). 로그 logs/2026-06/: daily-dashboard-v1·stockout-board·stockout-list-cadence(+window)·buyin-2026-06-ingest·board-cadence-cols.
- **★ 데일리 대시보드 품절 알림판 v1(2026-06-16, ADR 0024)** — 발주(Phase2) 품절목록을 알림판에 자동 등록(시작일=그날·전건) → 상품관리 갱신 후 **박스재고>0 재입고 시 입고로그+자동삭제**·수동 1클릭 삭제(로그없음)·'MM월DD일부터 N일째' 표시. 영속(history/stockout_board.json·restock_log.csv·비-PII). 신규 core stockout_board.py·수정 0b/1_파일처리. **새 core→Reboot 1회.** 다음=확장판(추가 데일리 인사이트). 상세 workflows/daily-dashboard.md.
- **★ 데일리 대시보드 v1 완료(2026-06-16, ADR 0023)** — 당일 점검(구 마진침식 탭D)을 독립 페이지로 승격(네비 첫 그룹·지도·로드맵 아래) + **세션 자동 파일 인계**(파일처리 오픈마켓→송장출력·천년경영→output을 daily_inbox 세션 인박스에 push → 재업로드 불요·슬롯별 수동 갱신 override). 상품관리=reference 라이브. 인박스=세션 휘발성(송장 PII로 미저장). 마진침식 3탭 축소. 신규 0b_데일리대시보드.py+core daily_inbox.py·수정 1_파일처리/8_마진침식/streamlit_app. **새 core(daily_inbox) → 안 보이면 Reboot 1회.** 다음=**확장판**(추가 데일리 인사이트 — 사용자와 설계). 상세 workflows/daily-dashboard.md.
- **★ 두뇌③ 탄력성 v1 완료(2026-06-16)** — 가격 A/B 하단 '마진율별 판매량'(page-only). 레버=마진율·18개월·관리코드×채널 월별 산점도(당시 실현마진율→판매량)+구간평균표. 매출자료 실현마진 재사용. **행사감별/품절보정/forward적립 전부 안 함**(사용자 확정). 커밋 7a8443f·Reboot 불요. **두뇌 3종(①침식 ②재고 ③A/B)+통합 상품360 카드 전부 v1 완성.** 다음 한 수=사용자 선택(후보: Phase3 템플릿·dashboard 이익/물류량 콤보·intel listing 스냅샷/행사로깅·upload-monitor 두뇌② 결합). ★폐기(2026-06-16): 1c 진짜 리드타임(cadence 확정·ADR 0022)·dashboard 물류량 차트·알리 가격변경.
- **★ 상품 360도 카드 v1 완료(2026-06-16)** — 신규 11_상품360.py(page-only). 관리코드 1개 → 8채널 등재현황+현재가/마진/기준여유+**목표마진 N% 역산** · 채널별 실판매(매출/볼륨/실현마진) · 매입가 추이(실입고+수정로그)+최근입고 · 재고소진. 조회전용·다중리스팅 행펼침. 커밋 완료(page b81b682·nav b130bd7)·**page-only Reboot 불요 예상**(안 보이면 1회). 사용자 실사용 확인 대기. intelligence-layer 잔여 next=두뇌③ 탄력성.
- **★★ 재개점 (2026-06-15): 주문 백필 완료 ✅(2023-03~2026-05·398,873행·2023 여름 갭만). 데이터현황 페이지 1단계 ✅(통합 데이터 관리·적재 범위/갭·가격이력 포함·x축 YYYY-MM). **2단계 업로드=나중에 일괄**(매입현황 등 적재 대상 다 갖춘 뒤·사용자 확정). **두뇌①·② 완료(2026-06-15)** → 다음=**두뇌③ 채널 가격 A/B**(채널명 정규화 선행) or 상품360카드. 로드맵 정본=systemmap.json. ⚠️ 두뇌① core 수정 → Reboot app 1회.**
  - **P2 완료**: core `ship_alloc.py` — EA 송장그룹 박스배분÷매출낱개=택배강도 + (상호명,월) 00-12 정합, 대시보드 온라인마진 탭 추정송장·k 교체(토글 use_actual 기본 ON·EA 미경유 6채널 추정 fallback). 골든 reconcile 채널 총택배==00-12 정확(diff0)·rate 커버 100%·기존추정 +28% 과대. ★단위=매출낱개≠EA판매단위. ⚠️core→**Reboot app 1회**.
  - **적재 완료**: orders/easyadmin_2026-{01~05}.parquet 51,641행(PII제거·송장그룹 해시·발주일 기준·core `orders.py`). velocity+송장그룹 토대. 다음 백필=2025(컨테이너, Streamlit 1GB 회피).
  - **판매가 신뢰도 검증 완료**(3중: 매출자료 gross/net·현재 listing·정산서/원장 — 상세 logs/2026-06-15-easyadmin-price-reliability.md): EasyAdmin 판매가 = "주문 시점 실제가"로 **신뢰**. 채널별 — 알리 원장 89% 정확·보조금 없음(가설 기각)·**고가 세트/번들만 EA 과소**(예 스팸세트 EA 35,600 vs 진실 136,500); 식봄 정산서 쿠폰 0건(사용자 기억 할인=마켓보로 *플랫폼 즉시할인* → EasyAdmin/정산서 미포착=정상)·15% 갭=가격 인하 drift; 올웨이즈 EA<listing=수수료 변동 가격 선인상(시간차); 나머지 신뢰. **수수료 가정 검증**=알리 9%(ERP 0.91·모니터 0.09, 실측 8.8%)·식봄 7%(실측 6.6%) 둘 다 정확·보수적.
  - **보정 보류(백로그)**: 고가 세트/번들 EA 판매가 과소 → velocity/A/B에서 listing 보정. 사용자: "나중에 숫자 이상하면 맞추자"(지금 안 함).
  - **현재 순서(ADR 0020 재배열·정본=systemmap.json)**: ① 두뇌① 강화 ✅(3렌즈+velocity, velocity는 두뇌①에 흡수) → ② ✅**두뇌② 재고 지능**(현재고÷소진율 품절·재발주 4구간·9_재고지능) → ③ **두뇌③ 채널 가격 A/B**[v1 서술✅] → **상품 360도 카드[next·사용자 선택]**(탄력성은 후순위). 토대(이력엔진·P2 송장실배분·주문 398K 백필·매입현황 66K 적재) 모두 완료.
- **★ intelligence-layer(지능 레이어·이력엔진+두뇌) 설계확정·미구현(ADR 0018, 2026-06-12)**: 관찰↔실행 사이 두뇌(진단·추천·측정) 신설. 매일/3년 데이터를 private repo 이력으로 적립 → ①마진 침식·제시 ②입고·품절 예측 ③채널 가격 A/B. ★정산 진실=매출자료(EasyAdmin/erp 정산은 raw), 택배 실배분=송장번호 그룹(추정송장·k 대체), 매입가=master(수정로그). 데이터 카탈로그 9종·단계별 구현 = workflows/intelligence-layer.md. **이력 엔진 1a(수정로그 가격이력 적재+역재생)·1b(상품관리 재고 스냅샷 적립) 완료(2026-06-15).** 1b=업로드 훅이 새 업로드 df를 날짜본으로 `snapshots/stock_YYYY-MM.parquet` 적립(dedup 멱등·전이탐지 0↔양수), core `stock_history.py`, **forward 축적**(과거 소급 불가), ⚠️core→Reboot. **두뇌① 마진 침식 v1 완료(2026-06-15)** — 신규 `8_마진침식.py`+`margin_erosion.py`. **채널 baseline 기준**(매익률=오프라인이라 폐기, 사용자 확정)·최근 3개월 매입인상∩채널 미달·이미 재설정분 자동제외·8채널 통합·권장가(cmm 재사용). 검증 89관리코드 인상→침식 50건(게토레이 4채널·동원참치 +30%). 한계=합성코드 미조인. ⚠️core→Reboot. **EasyAdmin 주문 적재 1차 완료(2026-06-15)** — orders/easyadmin_2026-{03,04,05}.parquet 25,821행(PII제거·송장그룹 해시·**발주일 기준**, core `orders.py`). velocity·송장그룹 토대 확보. **2026 전체(1~5월) 51,641행 적재 완료.** 다음=2025 백필(컨테이너·Streamlit 1GB 회피). ★정확도 함정=EasyAdmin≠매출자료 100% 아님(발주후 일괄입력·취소송장 00-12 미차감) → velocity는 월/주 단위, 정산진실=매출자료. velocity 연결 후보=두뇌① 정렬(침식×판매량)·두뇌③ 가격 A/B·P2 송장배분(진짜 마진). 운영=월1회 수정로그 재수신 ingest(침식 정확도).
- **Phase 4 대시보드 점진 확장**: 매출집계·증분업로더·거래처그룹·구분분류·기간 날짜범위·일/월/연 추이·**이익 모드(택배비=ERP 00-12 라인, 3000/2500 보정 토글, 이익률=이익/매입가, 전체 거래처)** 배포 완료(decisions/0008). 다음 후보 — ① 물류량(수량÷박스내품) ② 이익/물류량 콤보(이중축). 상세 workflows/dashboard.md.
- core/ 신규 모듈을 페이지가 import → 첫 배포 후 Reboot app 필요(pitfalls 모듈캐시).
- **상품등록 운영 중**(챗 네이티브, ADR 0009): smartstore·esm·easyadmin. **멀티채널 배치 입력폼 v2**(`reference/product_input_form_v2.xlsx`, 대상 채널=스마트스토어/G마켓/둘 다) 배포 완료(2026-06-10) — smartstore·esm 공용, 구 v1 deprecated. 이미지확장자=URL 실검사 자동판별 확정. 미해결 — 결정적 엔진/캐시 미구현. 상세 workflows/product-registration-common.md·*-register.md.
- **대시보드 product_attributes**: ✅ 슬림화(ADR 0011, 2026-06-10) — 4컬럼(식품음료·합포수량·최종분류). 차원=세분류만 + 식품음료 구분 3차 fallback(브랜드·b2b 폐기). **Reboot app 필요.** 451 합포수량 채우면 병합. 상세 workflows/dashboard.md.
- **상품마진(온라인) 탭**: ✅ 신설(ADR 0012, 2026-06-10) — 합포×내품 택배배분 추정 + 채널 보정계수(실제송장÷추정송장). 온라인 거래처 자동스코프. page-only. 상세 workflows/dashboard.md.
- **channel-margin-monitor**(채널 가격·마진 모니터, 운영중): 스마트스토어·식봄·**캐시노트** 모니터. 스마트스토어·식봄은 가격변경도. 표준 정산식=스마트스토어형(2700·ceil), 수수료만 채널별(스마트스토어/캐시노트 6%·식봄 7%). **캐시노트 추가 완료(2026-06-11, ADR 0014)** — 골든 513/513 입력 일치(N·배송비 전건). 신규 축: `ship_fee_policy`(배송정책코드 조건부 배송비)·`_pid`(상품번호 숫자셀 정수정규화). 행사 차등수수료는 무시(소스 없음). **캐시노트 가격변경 완료(2026-06-11)** — '(캐시노트)양식' append(A=OFR·D=SKU 다운로드 Q/R `extra_cols` 보존, F=수정·L=Y·N=9999 고정, G=권장가·H=정가). 식봄 append 로직 `build_append_items` 헬퍼로 공용화. **⚠️ core 수정분 Reboot app 필요**. 미해결 — baseline↔product_master 조인 갭. **배민상회 추가 완료(2026-06-11, 모니터)** — 골든 394/394 입력 일치(수수료·정산가 전건). 신규 축: **상품별 수수료**(`commission_source="download"` — 다운로드 BU/100+0.03, 채널 단일값 아님)·listing CSV 스키마 유연화(extra_cols 자동 보존). **배민상회 가격변경도 완료(2026-06-11)** — '(배민)양식' append, J=변경판매가(권장가)·H=변경소비자가=무늬용 가짜(표준 FAKE_JEONG). 옵션번호/옵션명 extra_cols 보존. **무늬용 가짜정가=전 채널 표준 단일화**(권장가+20~30% 랜덤·100원, jeong_field 있으면 기본) — 식봄·배민도 적용(2026-06-11). **쿠팡 추가 완료(2026-06-11, 모니터+가격변경)** — 골든 1989/1989(정산가·N·판매가). 수수료 12% 단일·배송비 0·키=옵션ID. 가격변경은 **filter형 신설**(다운로드 자체가 조회+변경요청 컬럼형 → 원본 P/Q 기입, build_filter_price_xlsx). 5채널(스마트스토어·식봄·캐시노트·배민상회·쿠팡) 전부 모니터+가격변경. **쿠팡 로켓그로스(바코드 E열) 모니터 제외 완료(2026-06-11)** — `exclude_row_if_col_filled`:5, parse 단계 행 제외(기존 listing은 '전체 교체' 재파싱 필요). **배민 가격변경 양식 외부링크 경고 수정(2026-06-11)** — 템플릿 고아 externalLinks 제거 + `_strip_external_links`(append/bulk/filter 전 빌더). 옵션번호 float `510609.0`→정수(`_pid` extra_cols·`_deflo` 라운드트립). **쿠팡 가격변경 filter 네이티브 zip 수술 완료(2026-06-11)** — openpyxl 저장이 inlineStr로 변질→쿠팡 업로드 거부 → `build_filter_price_xlsx`를 원본 네이티브 zip 수술로 교체(골든 바이트 일치). **쿠팡은 '전체 교체'로 raw 네이티브 유지 필수.** **⚠️ core 수정분 Reboot app 필요.** **쿠팡 raw inlineStr 오염 치유 + filter형 '신규만 추가' 비활성 가드 완료(2026-06-11)** — 저장 raw가 과거 '신규만 추가'로 inlineStr 오염→수술 출력도 inlineStr(업로드 거부) → raw 무손실 네이티브 역변환 커밋 + page 가드(price_form.mode=filter면 신규만추가 disabled). Reboot 불필요. **쿠팡 수술 출력 sharedStrings 정규화 완료(2026-06-11, 최종)** — 치유 후에도 실패 재현(앱이 캐시/stale 옛 오염 raw 사용) → `build_filter_price_xlsx`가 남긴 행을 항상 `t="s"`로 변환+sst 재구성(`_inline_cells_to_shared`). **raw가 inlineStr이든 native이든 출력 항상 네이티브** → 캐시/배포 무관 업로드 성공(엑셀 '값붙' 동치). 검증: 오염 raw 입력→출력 inlineStr 0·값 무손실. **⚠️ core 수정 → Reboot app 1회 필요.** **✅ Reboot+재생성 후 쿠팡 업로드 성공 사용자 확인(2026-06-11) — 가격변경 5채널 전부 완료·검증.** **올웨이즈(올팜) 추가 완료(2026-06-12, 모니터+가격변경)** — 6번째 채널. 판매가=팀구매가(K)·정가=개인구매가(J)·수수료10.5% 단일·배송비0·N=hapo(올팜ObjectId 748/748). 골든 입력 판매가/N 621/621·정산617/619. **가격변경=append('(올웨이즈)양식')** — K=권장가·J=FAKE_JEONG, extra_cols(카테고리·판매상태·옵션명/값·재고)+int_fields, 양식 end-to-end 검증. 페이지 무수정(mode append 자동). 미검증=올웨이즈 실업로드 inlineStr 허용. **⚠️ core 수정 → Reboot app 필요.** **6채널(스마트스토어·식봄·캐시노트·배민상회·쿠팡·올웨이즈) 모니터+가격변경. 알리(AliExpress) 모니터 추가 완료(2026-06-12)** — 7번째. **다중시트 export 자동정제(consolidate, 매크로 ALI상품매크로V2 흡수)** — 보이는 카테고리 시트만 통합·r2 라벨조회·숫자ID 필터, 별도 정제 업무 불요. 수수료9%·배송0·N=hapo(알리상품번호). 골든 입력 관리코드/상품명/판매가/N 전부 322/322. ⚠️ core+page 수정 → Reboot 필요. 알리 가격변경 미구현(AliExpress 다중시트 양식 별도). **ESM(G마켓) 모니터 추가 완료(2026-06-12, ADR 0015)** — 8번째. 17.5% 단일(골든 정산 가격×0.825 재현, O열 판매이용료 미사용)·키=A마스터상품번호·N=hapo(A·채널무관). G마켓+옥션 통합 다운로드(500상품 한도 다회배치)를 **F=='지마켓' 필터+A중복제거 parse 자동화**(신규 knob `include_row_if_col_value`·`dedup_key`, 수기 합치기 불필요)·`_num` 콤마 허용(배송비 '3,000'/'무료'). 골든 입력 판매가/배송비 1193/1193·정산액 1189/1193·base 1170/1187. consolidation 1193/1193. 골든 N=#REF! 대조불가. 가격변경 미구현(알리처럼). **다중파일 업로드(multi_file)** — 500상품 한도 배치를 한번에 올려 자동 병합(수기병합 불요). **가격변경(append) 추가(2026-06-12)** — '(ESM)양식'에 B=사이트상품번호(extra_cols 보존·모니터키 A와 다름)·C=권장가·A=순번(seq_col), 정가칸 없어 jeong 없음. esm_price_template.xlsx. 양식 30표본 전건 일치. **8채널 모니터/7채널 가격변경(알리만 가격변경 미구현).** ⚠️ core 수정 → Reboot. **ESM 실업로드 성공 사용자 확인(2026-06-12).** **8채널 모니터 / 6채널 가격변경. 다음: 추가 채널(요청 시) — ★ESM 가격변경=완료(2026-06-12)·알리 가격변경=폐기(2026-06-16, 당장 계획 없음).** 상세 workflows/channel-margin-monitor.md.
- **기준마진율 편집(현재 마진율→기준) 추가 완료(2026-06-12, ADR 0016)** — 전 채널 공통. 모니터 표 선택→버튼 1개→**새 기준 인라인 편집(data_editor, 기본값=현재 마진율, 직접 수정)**·충돌은 후보표시+직접입력·0.1%p. (offset 라디오 폐기 2026-06-12) 그 채널 baseline_col 컬럼만 수정(타채널 보존). **baseline을 GitHub 라이브read(compute_listing override)로 바꿔 저장 즉시 반영**(재배포 불요). 미달 상품 목표 인정→미달 해제(검증: 미달 10→0, 전체 49→29). 향후 ②인라인 ③일괄. ⚠️ core+page → Reboot.
- **upload-monitor(업로드감시) 설계확정·미구현(ADR 0017, 2026-06-12)**: 박스재고 있는데 채널 미업로드 탐지 → 등록 인계. base 정체 collapse(resolve_code 재사용 `resolve_identity`, 키=**상품코드**), listing 8채널 공유(마진모니터 스냅샷), 재고=박스재고·우선순위=재고금액 desc, 품절 단일판정. MVP = L1매트릭스+L2갭+L4(스마트스토어·ESM 자동폼/6채널 CSV)+L6 건수KPI. 제외=L5 채널확장(11번가·셀러허브·자사몰·토마토)·추이·예상마진. 코어+페이지 운영 — 8채널 매트릭스·KPI·채널 체크박스+컬럼별 상태필터(AND)·채널별 업로드제외(skip) 등록/해제(전채널제외 숨김·해제=다시 업로드필요)·**이미지 포함 XLSX(대표A1/상세B1 실검사 6컬럼·jpg→png)**·**박스재고/재고금액 임계값 필터**·**다운로드 XLSX(코드 텍스트 서식)**. 이미지 egress 배포 확인 OK(사용자). **L4 핸드오프 = 후순위(사용자 2026-06-15: 일괄 업로드 가능 채널 프로세스 완비 후 재논의 — 미장착 채널 多, 지금 만들 단계 아님)** — (스마트스토어·ESM 입력폼 prefill: 관리코드·박스모드·합포장(product_attributes)·과세디폴트 + 이미지URL / 6채널 CSV). 상세 workflows/upload-monitor.md.
- (백로그) Phase 3 나머지 템플릿 이관 — 사용자 실물 파일 제공 대기.
- (백로그) 온누리 빈 G셀 회귀 fixture/pytest.

_갱신: 2026-06-12 (ESM(G마켓) 모니터+다중파일+가격변경(append), 8채널 모니터/7채널 가격변경. B=사이트상품번호·seq_col순번·jeong없음. core → Reboot 필요)_

_갱신: 2026-06-12 (기준마진율 편집 추가 — 현재 마진율→기준, 전 채널 공통, baseline 라이브read 즉시반영. ADR 0016. core+page → Reboot)_

_갱신: 2026-06-12 (기준마진율 새 기준 인라인 편집(data_editor) — offset 라디오 제거, 기본값=현재·직접 수정. page만 → Reboot)_

_갱신: 2026-06-12 (upload-monitor(업로드감시) 신규 워크플로우 설계확정·미구현 — base 정체 collapse·키=상품코드·재고금액 우선·L4 등록 인계. ADR 0017)_

_갱신: 2026-06-12 (intelligence-layer 신규 워크플로우 설계확정 — 이력엔진+두뇌, 데이터 카탈로그 9종, 정산진실=매출자료·택배=송장. 첫 브릭=수정로그 적재. ADR 0018)_

_갱신: 2026-06-15 (systemmap.json 신설 — 지도+로드맵 단일 진실원천. 스키마 계약·권한 경계(JSON=상태/로드맵/연결 정본·.md=디테일/서사)·갱신 트리거·검증3종. ADR 0019. 렌더러=outputs/system-map.html, 인앱 페이지 예정)_

_갱신: 2026-06-15 (intelligence-layer 첫 브릭 — 수정로그 가격이력 적재 완료. 2,567건(매입2009/매출558)·**1년 롤링(3년 소급 불가 정정)**·dedup키 중복0. work-automation-data:history/price_changes.parquet + core/intelligence/price_history.py(파서+dedup적재+역재생). 다음=역재생 앵커 확정. ADR 0018)_

_갱신: 2026-06-15 (intelligence-layer 역재생 결선 — 수정로그 '매입단가' 앵커=product_master 낱개[8] 확정(95.4%). current_purchase_price+as_of_value 실증 완료(as-of 매입가). 1a 완료, 다음=1b 상품관리 스냅샷. ADR 0018)_

_갱신: 2026-06-15 (intelligence-layer 1b 상품관리 재고 스냅샷 적립 완료 — 업로드 훅·stock_history.py·dedup 멱등·전이탐지. core→Reboot. 다음=두뇌① 마진 침식)_

_갱신: 2026-06-15 (두뇌① 마진 침식 v1 — 채널 baseline·최근3개월 매입인상∩미달·8채널 통합·권장가. 신규 8_마진침식.py+margin_erosion.py. intelligence-layer status→진행중. Reboot 필요)_

_갱신: 2026-06-15 (EasyAdmin 주문 적재 1차 — 2026 3~5월 25,821행·PII제거·송장그룹·발주일기준. core orders.py. 다음 Jan-Feb로 2026 완료. velocity→두뇌①정렬·③A/B·P2)_

_갱신: 2026-06-15 (EasyAdmin 주문 2026 적재 완료 — 1~5월 51,641행. 정확도 함정 기록(매출자료≠EasyAdmin, velocity 월/주). 다음 2025 백필)_

_갱신: 2026-06-15 (★세션 핸드오프 — EasyAdmin 주문 2026 적재(51,641행)+판매가 신뢰도 3중 검증 완료. 알리/식봄/올웨이즈 전부 해명·수수료 가정 정확. 재개점=velocity 활용 갈림길(두뇌①가중/P2/③A/B/2025백필). 보정=세트 판매가 백로그)_

_갱신: 2026-06-15 (velocity 갈림길 해소 — 사용자 확정 순서 P2 송장실배분(최우선)→2025 주문백필→두뇌③ A/B, velocity 가중 후순위. systemmap.json 정본 갱신)_

_갱신: 2026-06-15 (P2 송장 실배분 완료 — EA 송장그룹 박스배분÷매출낱개 강도 + 00-12 정합, 대시보드 온라인마진 실측 교체. core ship_alloc.py·⚠️Reboot. 단위=매출낱개≠EA판매단위. 다음=2025 백필)_

_갱신: 2026-06-15 (upload-monitor L4 등록 핸드오프 후순위 — 채널 일괄업로드 프로세스 완비 후 재논의. systemmap next→later)_

_갱신: 2026-06-15 (EasyAdmin 주문 2025 하반기 백필 — 7~12월 70,455행·발주일 기준 클린·PII0·멱등. <tr> 스트리밍 파싱(86MB·컨테이너). 누적 122K행. 다음=2025 상반기)_

_갱신: 2026-06-15 (EasyAdmin 주문 과거 백필 완료 — 통파일 .xlsx 2023-03~2025-06 276,777행·헤더명 매핑(Source.Name 시프트). 전 기간 2023-03~2026-05·398,873행. 2023 여름 갭. 다음=두뇌③ A/B)_

_갱신: 2026-06-15 (데이터현황 페이지 1단계 — 통합 데이터 관리, 시계열 누적 자료 적재 범위/갭 한눈에. core coverage.py(디렉토리목록만)+2_데이터현황.py+nav. 재고스냅샷=현황만, 매입/발주=예정. ⚠️Reboot. 다음=2단계 업로드)_

_갱신: 2026-06-15 (데이터현황 후속 — 가격이력 타임라인 포함(single 1파일 range read)·x축 YYYY-MM. 2단계 업로드=나중에 일괄(매입현황 등 적재 후) 결정. 다음=두뇌③)_

_갱신: 2026-06-15 (유형별매입현황 전기간 적재 — 통파일 72컬럼 헤더명 매핑·53파티션 2022-01~2026-05·65,999행·합계액=진실·PII0·멱등. core purchases.py(orders 동형). 거래처코드 2025+ 편중(리드타임 과거 위주)·2C/입고신호 전기간. 다음=두뇌③ A/B)_

_갱신: 2026-06-15 (로드맵 재배열 ADR 0020 — backbone 완성→신호결합. 두뇌① 강화(2C+velocity) next1·두뇌② 승격 next2·두뇌③ planned·상품360카드 신규. 착수=두뇌① 강화)_

_갱신: 2026-06-15 (두뇌① 강화 완료 — 3렌즈(이미침식/곧침식2C/실판매이상)+velocity 월손실액. margin_erosion.py+5함수·8_마진침식.py 3탭. ⚠️Reboot. 다음=두뇌②)_

_갱신: 2026-06-15 (두뇌① 탭D 당일 점검 — 당일 천년경영 output+송장출력+master 3파일로 당일 실현마진 이상치 즉시 탐지. 매출=실제기입단가(net)·택배=채널flat×실박스(송장)×물류량. core daily_margin.py·8_마진침식 4탭. 실파일0615 조인100%·택배정합diff0·이상28. ⚠️Reboot. 다음=두뇌②)_

_갱신: 2026-06-15 (탭D 정정 — 택배 실송장 단위 배분[채널 물류량 비례배분 과다계상 버그, 사용자 지적]·해소기 강화. 이상 28→9. ⚠️Reboot)_

_갱신: 2026-06-15 (두뇌② 재고 지능 v1 — 현재고(최종재고 낱개)÷소진율(매출 전채널)=소진예측일·매입 입고주기 리드타임 proxy로 재발주. 4구간(품절임박/곧재발주/충분/사장재고). 신규 stockout.py+9_재고지능.py. 매출 base 직조인(합성코드 한계 없음)·택배비/음수재고 처리. ⚠️Reboot. 다음=두뇌③ A/B)_

_갱신: 2026-06-16 (탭D 택배 배분 합포 2시나리오 정확화 — ① 250/355 H열 콤마 다품목 전체추출(둘째 품목 누락 버그) ② 175~200ml 30개입 수령자 그룹 ceil(팩/3) 물리합포(reference/hapo_175_190.csv 60종 관리코드). 거짓 역마진 해소. ⚠️core→Reboot. 다음=master+0616 이상치 before/after 사용자 확인 → 두뇌③)_

_갱신: 2026-06-16 (채널 내 고객키/합포박스키 설계 탐색 — ADR 0021. 채널별 PII 프로파일(수령자3종 100%·안심번호 채널 G마켓/옥션/쿠팡 전화불가)·★시기별 마스킹 급변(2026-03 51%→04 0.5%→05 0%)·robust 키(보이는 최소공통분모, 사용자 동의). reference/hapo·orders 재처리로 비-PII 해시키 박제 계획. **미구현 — 다음 세션 과거 통파일 받아 진행**(받은 파일=최근 3개월·과거 아님). 상세 logs/2026-06-16-customer-key-design.md·workflows/intelligence-layer.md §5.7)_

_갱신: 2026-06-16 (cheonnyeon 박스코드 이상 탐지 검수 장치 — 전체 시트 잔류 행 중 영문코드/`[낱개`태그 비차단 경고 + 소분목록 등록 유도. 소분누락→박스 오업로드 재발 방지. core detect_box_anomalies·page 표시·test. ⚠️core→Reboot 1회)_

_갱신: 2026-06-16 (채널 내 고객키·합포박스키 적재 완료 ADR 0021 — 통파일+2023여름 .xls로 39개월 430,592행 재처리·키 박제. robust 검증(이름끝1자·전화뒤4·안심채널 전화제외)·재구매 교차월 병합 실증·합포박스키 55K 송장묶음·2023여름 갭 백필 동시 완료. orders.py 키생성 정합100%·솔트=st.secrets 등록 필요. ⚠️core→Reboot. 다음=ship_alloc 합포박스키 연동(수치변동·사용자확인 후))_

_갱신: 2026-06-16 (ship_alloc 합포박스키 연동 완료 — 175~200 물리합포 ceil(팩/3)·합포 가능품목 제한(블랭킷 swap 금지·B2B 과대병합 방지). 채널총 불변·합포품목 택배 -3.8% 교정. ship_alloc hapo_codes 인자+대시보드 연동. ⚠️core→Reboot. 다음=두뇌③ A/B)_

_갱신: 2026-06-16 (두뇌③ 채널 가격 A/B v1 서술 완료 — 신규 '가격 A/B' 페이지(10_가격AB.py)+core channel_compare.py. 관리코드→채널별 실현마진(순이익÷매입가)·낱개이익·판매량·정산단가(net)·EA노출가(gross)·실측/추정 택배 비교. 채널택배 00-12 정합 검증. 다음=탄력성. ⚠️Reboot)_

_갱신: 2026-06-16 (다음 타깃=상품 360도 카드[사용자 선택]·두뇌③ 탄력성 후순위. 빌드는 다음 세션(통합 작업 大·컨텍스트). systemmap next 재우선)_

_갱신: 2026-06-16 (상품 360도 카드 v1 — 신규 11_상품360.py·page-only. 관리코드 1개 통합 뷰: 채널 등재/현재가/목표마진역산 + 채널별 실판매 + 매입가추이(실입고+수정로그) + 재고소진. 조회전용. 다음=탄력성)_

_갱신: 2026-06-16 (두뇌③ 탄력성 v1 — 마진율별 판매량. 레버=마진율·18개월·산점도+구간평균. page-only. 행사/품절/forward 안 함(사용자). 두뇌 3종+상품360 전부 v1 완성. 다음=사용자 선택)_

_갱신: 2026-06-16 (1c 진짜 리드타임 폐기 — 두뇌② 입고주기 cadence=확정. dashboard 물류량 차트·알리 가격변경도 로드맵 삭제. ADR 0022·systemmap m)_

_갱신: 2026-06-16 (데일리 대시보드 v1 — 당일점검 탭D 독립 페이지 승격+세션 자동 인계(재업로드 불요)·수동 갱신. 마진침식 3탭. 신규 0b+daily_inbox.py. ADR 0023·systemmap n. 새 core→Reboot 1회)_

_갱신: 2026-06-16 (데일리 대시보드 품절 알림판 — 발주 품절목록 자동등록·박스재고>0 재입고 입고로그+자동삭제·수동삭제·영속. core stockout_board.py. ADR 0024·systemmap o. Reboot 1회)_

_갱신: 2026-06-16 (유형별매입현황 2026-06(1~15일) 적재 — 개별 export 742행, buyin 54파티션·66,741행. 합계액 정합100%·거래처 78% 보존(거래처관리코드 alias). 품절목록 E/F/G·두뇌② 6월 입고 반영)_

_세션 클로즈: 2026-06-16 (품절 알림판+품절목록 cadence(E/F/G 1년)+매입현황 6월 적재+알림판 cadence 표시. core 4종 변경→Reboot 1회 대기. 다음=데일리 확장판)_

_갱신: 2026-06-16 (시장지능 nadl 로컬 수집기 방향 확정 — 클라우드 지오펜스로 KR 머신 수집→push. ADR 0025·systemmap 2026-06-16s. 막힘=행사 샘플 대기)_

_갱신: 2026-06-16 (시장지능 nadl 로컬 수집기 = 다음 세션 최우선. 막힘=행사 샘플 페이지 대기)_

_갱신: 2026-06-17 (데일리 대시보드 확장판① — 채널별 요약(당일 매출·마진율) + 가격 변동 알림(전체 상품 ±N% 매입가/판매가, 1b 스냅샷 연속 비교 detect_price_changes). 0b page + core stock_history. ⚠️ core→Reboot 1회. forward 적립이라 가격 이력 2026-06-15~ 누적. 다음=확장판② 후보 or 시장지능 nadl)_

_갱신: 2026-06-17 (데일리 확장판② — 이상치 표 권장가(채널기준·판매가) + 체크박스 선택→단일채널 가격변경 시트 다운로드(cmm 빌더 재사용·알리 미지원·listing 최신 의존). page-only Reboot 불요 예상. 다음=실사용 확인/추가 인사이트)_

_갱신: 2026-06-17 (가격 변동 알림에 박스재고 컬럼 + 인상 빨강/인하 파랑 색상. product_master '박스' 라이브·XLSX 포함. page-only)_

_세션 클로즈: 2026-06-17 (데일리 대시보드 확장판 + 채널 가격변경 연동 + 버그픽스). 완료: ①채널별 요약(당일 매출·마진율 groupby) ②가격 변동 알림(1b 스냅샷 ±N% 매입가/판매가·detect_price_changes·박스재고 컬럼·인상 빨강/인하 파랑) ③이상치→권장가(채널기준·매입가 기준 역산이라 listing 미등재도 항상 표시·_reco_from_master)+체크박스 단일채널 가격변경 시트 다운로드(cmm 빌더 재사용). 픽스: 스마트스토어 가격변경 미지원 오판(_supports_price_change)·Styler.applymap→.map(pandas 3.x 제거, pitfalls 등재). **전부 page-only 최신분=재배포 자동반영.** 신규 core=stock_history.detect_price_changes(확장판①)만 — 화면상 이미 활성(가격 변동 알림 렌더 확인), 안 보이면 Reboot 1회. 제약: 가격변경 시트 생성은 listing 필요(미등재 상품은 권장가 표시까지)·쿠팡/스마트스토어 raw .xlsx('전체 교체') 필요·알리 가격변경 미지원. ⚠️ 이 세션 중 app repo에 동일 PAT의 외부 커밋 1건(00:14 박스재고+색상) 관측 — **동시 세션 가능성, 0b 편집 전 최신 SHA 확인**. 다음=데일리 추가 인사이트(요약 메트릭 인하 아이콘 색 통일 등 잔손질) 또는 시장지능 nadl(★★ 최우선·행사 샘플 대기).)

_갱신: 2026-06-17 (데일리 이상치 표 **이중검수** — listing마진+판정(일시적/구조적/없음). 당일 미달이라도 listing 정상이면 '일시적'(쿠폰·실박스 택배), listing도 미달이면 '구조적'. 당일 vs listing 마진 기저 차이(배송비 수입·실박스 택배)는 설계상 의도 — 판정으로 해소. page-only·Reboot 불요. 사용자 실사용 확인 대기)_

_갱신: 2026-06-17 (fix — 데일리 ESM 행 현재가/권장가/판정/가격변경 누락. cmm ESM 키 'esm' vs daily 'ESM' 불일치 → 0b _cmm_key 대소문자 보정. page-only. ★잔여: cmm ESM 키 통일은 별건 미적용)_

_세션 클로즈: 2026-06-17 (데일리 대시보드 이상치 표 이중검수 + ESM 버그 fix + 인박스 휘발 질문 규명). 완료: ① **이중검수**(listing마진+판정: ⚠️ listing도 미달=구조적 / listing 정상=일시적 / 없음). 당일 vs listing 마진 **기저 차이 규명**(당일=매출net에 배송비 수입 미포함+실박스 택배 순비용 / listing=정산액에 배송비×0.967 수입+실택배비2700) — 권장가<현재가가 버그 아닌 이유. _reco_lookup(buffer) 4-tuple. 커밋 2a71a08. ② **ESM 채널키 버그 fix**: cmm CHANNEL_CONFIG ESM 키 'esm'(소문자) vs daily SHEET_TO_CMM 'ESM'(대문자) 불일치 → ESM 행만 현재가/권장가/판정/가격변경 누락. 0b `_cmm_key` 대소문자 무시 보정(_cmm_listing·_reco_from_master·_do_price_change). 커밋 29990bc. ③ 인박스 탭 유지 질문 = **세션 메모리라 탭 넘김엔 유지되는 게 정상**(PII 무관, 0b에 삭제코드 없음 확인) — 비워진 건 이번 세션 잦은 재배포로 세션 초기화된 탓. **버그 아님, 코드 변경 없음.** **전부 page-only → 재배포 자동반영·Reboot 불요.** 사용자 실사용 확인 대기(ESM 행 정상화·판정 컬럼). ★ 잔여: (a) cmm ESM 키 'esm'→'ESM' 통일은 별건 미적용(Reboot+셀렉트박스 영향 검증 필요—cross-module 잠복지뢰) (b) 인박스 리부트/새세션 영속(비-PII 결과만 저장)은 사용자가 탭 유지만 원해 보류. 다음 한 수=변동 없음 — ★★ 시장지능 nadl 로컬 수집기(행사 샘플 대기) 또는 데일리 추가 인사이트. 로그 logs/2026-06/: daily-dashboard-dual-check·daily-esm-channel-key-fix)_

_갱신: 2026-06-17 (cashnote-register 신설 — 캐시노트 KCD 등록 채널 셋업. 양식 42열·합포N→P열·자체카테고리53종·수수료6%. reference cashnote_category_food.csv + cashnote_bulk_template.xlsx(app repo). 챗 네이티브·코드무변경·첫 배치 대기)_

_갱신: 2026-06-17 (cashnote-register 1차 실업로드 77/87 성공 — ✅openpyxl 저장본·고시값 비움 정상(zip수술 불요). 실패 10건 단일원인=**검색어(H) 상품명 통짜 길이초과**(캐시노트 H=쉼표구분·각≤20자·최대10개) → 쉼표 토큰화로 10건 재업로드 파일. 카테고리 전건·AA 품목별(가공식품21/생활화학37) 적용분. 잔여: raw12 이름·피죤유연제/물티슈 군 임시)_

_갱신: 2026-06-17 (cashnote-register 완료 — 1차 87건 업로드 전건 성공(77+재업로드10). 정본 통합 재작성(workflows/cashnote-register.md end-to-end). 검증: openpyxl 수용·고시/정가/과세 비움 정상·H 쉼표토큰화 필수·AA 품목별. status live)_

_갱신: 2026-06-17 (데일리 대시보드 확장판③ 신규 업로드 대상 — 최근 N일(기본7) 재고 새로 생긴 상품(입고전이∪신규등재) ∩ 8채널 전부 미업로드 ∩ 재고>0 → 신규 업로드 후보. 품절 알림판 다음(나감↔들어옴 대칭). 신규 core stock_history.detect_new_stock(직전결측=신규등재 surfacing·baseline floor seed제외) + upload_monitor.build_gap_table 재사용(중복0·키=상품코드·업로드감시의 '최근 입고' 서브셋). 최근매입일=매입현황 cadence(월1회 적재라 보조·재고 신호는 박스재고 양수전환이 daily-fresh). 골든: 실스냅샷 4일(6/14 seed~6/17) 최근7일 입고22+신규등재1=23 ∩ 전채널미업로드264 → 8건. 커밋 stock_history 8845a7a6·0b 71ff2a88. **page 0b=재배포 자동반영·core stock_history 신규함수→안 보이면 Reboot 1회.** 사용자 실사용 확인 대기. 로그 logs/2026-06/2026-06-17-daily-new-upload-alert.md)_

_갱신: 2026-06-18 (시장지능 nadl 로컬 수집기 ✅운영중 — 구조 B 라이브 검증. 로컬 fetcher(ps_page 동적·저속) raw push → GitHub Actions(nadl-parse) 파싱 → market/nadl/prices_{date}.parquet. 첫 실행 606행/21p(개당가 599·박스가 606·dedup). 파서=클라우드 repo(nadl 변경시 직접 수정). work-automation-data: scripts/nadl_parse.py·nadl_fetch.ps1·.github/workflows/nadl.yml. ⚠️주1회 상시화 전 data 전용 PAT+작업스케줄러. 다음=개당가↔관리코드 매칭→두뇌① 시장대비 권장가. systemmap nadl planned→done·meta 2026-06-18a. 로그 2026-06-18-nadl-collector-build.md)_

_세션 클로즈: 2026-06-18 (시장지능 nadl 수집기 구조 B 라이브 완료·**운영중**. 로컬 fetcher 경로=`C:\claudeworkautolocal\nadl` (nadl_fetch.ps1 + run_nadl.bat). 운영=**수동 더블클릭(run_nadl.bat)**·토큰 `setx NADL_PAT`(가급적 work-automation-data Contents 전용 PAT)·자동 스케줄은 신뢰 쌓인 뒤로 보류(schtasks 한 줄 준비됨). bat은 %~dp0로 동일폴더 ps1 실행·**ASCII+CRLF 필수**(한글/LF는 cmd 파싱 깨짐). 흐름: 더블클릭→raw+마커 push(work-automation-data:market/nadl/raw/{date}, runs/latest.json)→Actions `nadl-parse` 파싱→`market/nadl/prices_{date}.parquet`(첫날 606행/21p·행사상품 ps_ctid=01320000). ⚠️ 채팅에 평문 노출된 넓은 PAT 폐기+프로젝트지식 사본 교체 권장. **다음 한 수=nadl 개당가↔관리코드 매칭→두뇌① 시장대비 권장가**(product_master↔nadl 상품명/규격 조인, 한 덩어리 작업). 로그 logs/2026-06/2026-06-18-nadl-collector-build.md)_

_갱신: 2026-06-18 (시장지능 nadl 개당가↔관리코드 매칭 v1 — 신규 core market_nadl.py + 페이지 12_시장가매칭.py(조회/매칭/매칭본 3탭). 모델 v2=박스 하드게이트(용량∧팩수·nadl 마트납품 박스단위→박스 다르면 다른 상품)+글자 bigram(띄어쓰기·어순 무시)+브랜드 가중(±0.15). top3 사람확정·자동없음 안함(점수=힌트)·중복등록 복수선택·직접입력·없음. 매핑=데이터repo nadl_map.csv(ps_goid 키·다음 수집 유지). 대화 검증 21건 top3 recall 16/16·1위 15~16/16. ⚠️신규 core(market_nadl)→재배포 후 Reboot 1회(page 12·nav=자동반영). 사용자 실사용 확인 대기·모델은 실사용 루프로 정교화. systemmap 2026-06-18b(매칭 done+시장대비권장가 planned). **다음 한 수=두뇌① 시장대비 권장가**(매핑 관리코드에 nadl 개당가 결합: 시장여유·포지션·시장기반 권장가→상품360 '시장대비'+전체스캔, 매핑 누적 후). 로그 logs/2026-06/2026-06-18-nadl-matching.md)_

_갱신: 2026-06-18 (시장가 매칭 UX/일괄 — ① 규격줄 본문크기 ② **저신뢰 일괄 '없음' 버튼**(최고점수<0.3·후보없음, 진짜매칭 최저0.38이라 안전 → 검토큐 606→146 축소) ③ 매핑관리 상태필터로 '없음'도 삭제=재검토 복귀. 전부 page-only·Reboot 불요. 모델은 실사용 루프로 정교화)_

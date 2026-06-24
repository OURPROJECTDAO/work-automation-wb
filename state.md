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
| sikbom-register (식봄 일괄등록) | — | 운영중 (1차 41건 실업로드 성공·검증완료) | workflows/sikbom-register.md |
| channel-margin-monitor (채널 가격·마진 모니터) | — | 운영중 (8채널 모니터 / 7채널 가격변경) | workflows/channel-margin-monitor.md |
| upload-monitor (업로드감시) | — | 운영중(업로드제외 등록/해제, L4 대기) | workflows/upload-monitor.md |
| intelligence-layer (지능 레이어·이력엔진+두뇌) | — | 진행중 (1a·1b·두뇌①·주문 39개월·판매가검증·P2·매입현황·탭D·두뇌②·고객키/합포박스키 적재·**ship_alloc 합포 ceil(팩/3) 교정**·**두뇌③ A/B v1**(서술+마진율별판매량 탄력성)·**상품360카드 v1** 완료) 두뇌3종+통합카드 완성·다음=사용자선택 | workflows/intelligence-layer.md |
| daily-dashboard (데일리 대시보드) | — | 진행중 (당일점검+세션인계+품절알림판+채널요약+가격변동알림+이상치→가격변경시트) | workflows/daily-dashboard.md |
| sikbom-event-planning (식봄 행사기획) | — | 운영중 (챗·1차 2026-07 기획전) | workflows/sikbom-event-planning.md |
| margin-optimizer (기준마진율 최적화·두뇌④) | app/pages/13_기준마진율최적화.py | 운영중 (노브 전부+운영 UX — 베이스·4분면·측정루프·⑧·⑦·②회전·평어화·가격제한제외·KPI동적·항상적용) | workflows/margin-optimizer.md |
| ui-design (전 페이지 UI 디자인·횡단) | — | 진행중 (Phase A·랜딩·B-1 데일리) | workflows/ui-design.md |

## 완료된 Phase
- Phase 0: 코드 repo 스캐폴딩. 2026-06-01.
- Phase 1: openmarket_merge 8단계 + pytest. 2026-06-01.
- Phase 2: Streamlit 앱 + Community Cloud 배포 + 기준데이터 관리 UI. 2026-06-01.
- Phase 3 (진행 중): 4종 완료 (onnuri-order, logistics-order, cheonnyeon-upload, invoice-fill). 나머지 템플릿 대기.
- Phase 4 (운영 최소): 대시보드 — 데이터계층+저장어댑터+3개년 적재(313K행)+최소 페이지(매출 집계)+증분 업로더([데이터 추가] 탭) 배포. 차트/물류량/이익률/거래처그룹 점진추가. 2026-06-08. (decisions/0006)

## 막힌 것 / 이슈
- 없음. (B2 인프라 완료 — repo·PAT R/W·st.secrets 검증됨 2026-06-08.)

## 다음 한 수
- **★ UI 디자인 Phase A 라이브 (2026-06-19, ADR 0028).** 전 페이지+사이드바+랜딩 프로화 1단계. **전역 2파일**: `.streamlit/config.toml`(인디고#3B5BDB·Pretendard·라운드/테두리, 19페이지 자동 상속) + `core/ui.py`(inject_css 전역 CSS: st.metric→카드·버튼/탭 폴리시·브랜드·KPI카드·핀필·▲빨강▼파랑 + 헬퍼 page_header/kpi_row/status_pill/delta_html). 진입점 inject_css 1회+사이드바 브랜드+네비 그룹명'분석·지능'. 커밋 config 168e203·ui e166707·app 6006b28. ⚠️ **재배포+Reboot 1회**(폰트·새 코어). **사용자 체감 확인 대기.** 함정=st.dataframe 캔버스라 CSS불가(Phase B 색표는 Styler/HTML 우회). 다음=체감 OK면 Phase B(데일리부터 헬퍼 적용). 정본 workflows/ui-design.md·로그 2026-06-19-ui-design-phase-a.md.
- **★★ 세션 클로즈 (2026-06-19): 두뇌④ 노브 완성 + 운영 UX + 가격제한 제외 + baseline 백필.** 이번 세션: ⑦매출목표(월매출<100만→나들까지 절반)+나들floor·②회전markdown(소진예측>180일→−2%p캡 자동복귀)·**사유/액션 전부 평어화**(올림·내림·낮게유지·재고정리내림·가격테스트·_MOVE/_DOWN 상수)·상단 설명서+wf §0 한눈에로직·**기록 후 st.rerun 이어서 진행**(필터유지·mo_recent 즉시숨김)·**'함께 변경' 토글 제거→항상 적용**·**baseline 백필 106건**(토글 누락분, 6 미스=낱개/소분류)·**작업목록 4분류**(메인=가격조정가능+변화 / 🔒가격제한=margin_floor 마진민감 48코드 / 🔴변화없음=가격외요인 / 가격테스트)·**KPI 채널+검색 동적**·UI wide·채널칩·8관리채널 스코프. status=live. ★core변경(⑦②평어)=Reboot 1회(스샷상 반영됨)·이후 page-only=재배포만. 원장 141건/baseline 106적용·측정은 7월초 6월매출+30일커버리지 후. 잔여=cmm직접prefill·margin_floor 원가하한클램프·미스6건·ESM키통일. 정본 wf §0·§13~22·로그 2026-06-19-margin-optimizer-{sales-target,turnover-markdown,baseline-backfill,session-close}.
- **★★ 기준마진율 최적화(두뇌④) v0 라이브 + 운영보강 (2026-06-19, ADR 0026·0027).** P×C 권장 기준마진율 작업목록 — 베이스=순이익누적85% proven 순이익가중평균·볼륨×(마진vs베이스) 4분면·절반스텝·🟢🟡🔴·관망(비중<1% 실험큐, 2회 무반응 park). **45일 억제**(결정원장 read로 최근 결정 셀 숨김). **기록 + 기준마진율 변경 통합** — 변경 시 **현 타깃 + Δ 가산**(cmm 노출가-target ↔ 두뇌④ 매출자료-realized 정합, ADR 0027 — 절대 기입 시 방향 역전). 표에 기준마진율(현 타깃) 컬럼·권장변화 ▲빨강/▼파랑(한국식)·월매출. 택배비 2,700 고정·나들 제외. **결정원장 history/decisions.parquet**(Gate3) seed. 데이터 토대 전부 보유(매출자료·ship_alloc·orders·두뇌②·nadl). **다음 = 측정 루프**(원장 측정후·결과 채움→유지/되돌림 자동) → ⑧시즌 제외 → **⑦ 상품 매출목표 라벨(미착수·출처 sales_target.csv 포맷 선결)** → ②회전·나들 floor. 정본 workflows/margin-optimizer.md(§14)·로그 2026-06-19-margin-optimizer-ops.md.
- **★ 식봄 일괄등록 운영중·end-to-end 완료(2026-06-18).** 식봄 최초 상품 일괄등록. 신규 워크플로우 sikbom-register + reference: sikbom_category.csv(266 카테고리 정본·2축매트릭스 평탄화)·sikbom_bulk_template.xlsx(빈양식)·sikbom_bulk_golden_41.xlsx(검증본). **1차 41건(74→판매중지 디듑33) 실업로드 성공**·openpyxl 수용 확인(zip수술 불요). 이미지 41건 폴더 zip 완료(**관리코드로 gi.esmplus A1/B1 다운로드→상품코드 A로 _1/_d1 리네임**). 표준 흐름=판매중지 디듑→양식 생성→업로드→이미지 폴더 zip. **펜딩 없음**(차기 배치는 업로드감시 출력만 받으면 반복). 상세 workflows/sikbom-register.md·로그 2026-06-18-sikbom-register-{setup,dedup,golden,images}.md.
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

_세션 클로즈: 2026-06-18 (시장가 매칭 v1 — nadl 개당가↔관리코드). 완료: ① 대화창 21건 실매칭으로 **매칭 모델 v2 확정**(박스 하드게이트 용량∧팩수[nadl=마트납품 박스단위→박스 다르면 다른 상품] + 글자 bigram[띄어쓰기·어순 무시] + 브랜드 가중±0.15. top3 recall 16/16·1위 15~16/16) ② 신규 core `market_nadl.py`(로드+모델+매핑 R/W+매칭본 결합) ③ 신규 페이지 `12_시장가매칭.py`(조회/매칭/매칭본 3탭·top3 사람확정·복수등록·직접입력·없음) ④ 매핑=데이터repo `nadl_map.csv`(ps_goid 키) ⑤ 실사용 UX: 규격줄 본문크기·**저신뢰 일괄없음 버튼(최고<0.3·후보없음→검토큐 606→146)**·매핑관리 상태필터(없음 되돌리기). ⚠️ **신규 core(market_nadl)→재배포 후 Reboot app 1회**(이후 page 수정분은 자동반영·Reboot 불요). 현재 사용자 실매칭 진행 중(146건 큐). **모델은 실사용 루프로 정교화**(top3 빗나간 케이스→브랜드사전·게이트·가중 보강). **다음 한 수=두뇌① 시장대비 권장가**(매핑 누적 후: 매핑 관리코드에 nadl 개당가 결합 → 시장여유[시장−매입]·우리 포지션[권장가−시장]·시장기반 권장가 → 상품360 '시장대비' 섹션 + 전체 스캔). 로그 logs/2026-06/2026-06-18-nadl-matching.md · systemmap 2026-06-18b(매칭 done+시장대비권장가 planned))_

_갱신: 2026-06-18 (천년경영 — 리테일앤인사이트 분배(리테일전체/리테일낱개 신규시트·H=F/D·수수료없음) + 제이티유통(기존매핑) + **선택 입력 ④ 추가 판매처 매출통계 병합**(ERP "판매처상품매출통계" HTML/xlsx export → parse_sales_stats → 발주자료 행에 병합·여러개 가능). 빈 erp코드는 옵션추가항목1 단일코드 보정·묶음(2코드+)은 skipped 경고. 출력 27→29시트. run() 5-tuple(+merge_info). 실파일 검증 11행/1스킵·리테일8행·end-to-end 29시트. core 2d2c4dd·page 1fd4d48·test f6399bb. **⚠️ core(cheonnyeon_upload)→재배포 후 Reboot 1회**. 사용자 실사용 확인 대기. 로그 logs/2026-06/2026-06-18-cheonnyeon-retail-jt-stats-merge.md)

_갱신: 2026-06-18 (천년경영 후속 — ① 배민·스스주문 **선택화**(발주자료만으로 실행. open_*(None)→None·process_*(None)→{}·run baemin/sss 기본 None·page if f_baeju. 미업로드 시 스마트스토어/배민상회 G=선결제비 폴백) ② 추가 매출통계 ④ 입력칸 **제거**(코어 parse_sales_stats/stats_files 휴면 보존). 제이티·리테일은 발주자료에 섞어 올림. 회귀 test_optional_shipping_none. core 17b95d9·page a00ff58·test 7c3edef. ⚠️core→Reboot 1회)

_갱신: 2026-06-18 (sikbom-event-planning 신규 워크플로우 — 식봄 행사기획. 판매중 리스트+product_master 원가 조인→MD 카테고리/타겟단가 매칭→식봄 정산식 마진→행사가(min(현재가,타겟)) 제안. channel-margin-monitor 정산식·4-tier 재사용. 챗 네이티브·내부공유 xlsx 산출. 1차 7품목 확정. systemmap 노드 추가)_

_갱신: 2026-06-18 (로드맵 프루닝 — intel 나중 '알림 배너'(스냅샷 diff: 입고·품절·침식) 항목 삭제. 데일리 대시보드로 이미 실현(품절 알림판=품절·가격 변동 알림=침식/가격·신규 업로드 대상=입고). '데이터현황 2단계(업로드)'만 유지. systemmap meta 2026-06-18f·intel.md §5.6 B·roadmap later 묶음 동반 정리. 검토결과=다른 예정/나중 전건은 미구현→유지)_

_갱신: 2026-06-18 (이력 1d 완료 — channel-margin-monitor listing 갱신 커밋 시 채널 가격을 날짜본으로 적립(snapshots/listing_YYYY-MM.parquet·9컬럼·dedup 멱등·forward). 신규 core listing_history.py(stock_history 1b 동형·detect_listing_price_changes) + 6_채널마진모니터 _accumulate_listing 훅(비차단 toast·_data_secret). 두뇌③ A/B 가격변경 전후 토대. ⚠️ 신규 core import→Reboot 1회. 커밋 코어 620f0a2·page dd34ab7. systemmap 1d planned→done(produces 박제)·meta 2026-06-18g. 다음=1e 행사 로깅(forward) or 두뇌③ A/B 전후 결선 or 시장대비 권장가(매핑 누적 후))_

_갱신: 2026-06-18 (로드맵 프루닝 — upload-monitor '재고금액×예상마진 우선순위(두뇌② 결합)' 항목 삭제(사용자 불요 판단). systemmap meta 2026-06-18h)_

_세션 클로즈: 2026-06-18 (로드맵 프루닝 + 이력 1d 완료 + 다음=1e 확정). 완료: ① 로드맵 감사·프루닝 2건 삭제(intel '알림 배너'=데일리 대시보드로 실현 / upload-monitor '재고금액×예상마진'=사용자 불요) ② **이력 1d listing 가격 날짜본 스냅샷 ✅**(신규 core listing_history.py=stock_history 1b 동형: snapshot_from_recs·ingest_listing_snapshot 월파티션 snapshots/listing_YYYY-MM.parquet·dedup (스냅샷일자·채널·상품번호) keep=last 멱등·detect_listing_price_changes 채널×상품번호 0%제외; 6_채널마진모니터 _accumulate_listing 훅=listing 커밋(전체교체/신규추가) 직후 비차단 toast 적립·_data_secret [data] pat/repo·forward). 커밋 코어 620f0a2·page dd34ab7. **리부트 완료(사용자)** — cmm '상품관리 갱신' 1회 시 toast '📚 listing 가격 스냅샷 적립' 확인 + 둘째 갱신부터 가격변경 탐지(forward 누적). 두뇌③ A/B 가격변경 전후의 빠진 다리 확보. ⚠️ 미검증=실제 cmm 갱신 1회 후 적립 toast/parquet 생성(사용자 다음 갱신 시 자연 확인). **다음 한 수=이력 1e 행사 로깅(forward·기획전 참여 결정 前 선제 셋업, 사용자 확정 2026-06-18)** — 가격변경/행사 이벤트 기록 테이블 신설(백필 불가·지금부터). 설계 미정(다음 세션 제안): 행사 로그 스키마(채널·행사명·기간·대상 관리코드·유형·할인율·비고)·저장(data repo history/events·forward·비-PII)·입력 UI(전용 페이지 or 데일리 섹션·stockout_board 패턴)·두뇌③ 준실험 교란 보정 소비. ★1d 가격변경은 snapshot diff로 이미 커버 → 1e는 **행사(쿠폰/노출/번들 — 가격불변인데 판매 교란)** 중심. 차순위=두뇌③ A/B 전후 결선(1d 이력 쌓인 뒤)·시장대비 권장가(시장가 매칭 누적 후). systemmap meta 2026-06-18h. 로그 logs/2026-06/: roadmap-prune-alert-banner·listing-history-1d)_

_갱신: 2026-06-18 (sikbom-register 신설 — 식봄 일괄등록 최초 셋업. 양식 상품_대량등록 29열·r8·수수료7%·배송비명 L규칙·카테고리명 그대로·sikbom_category.csv 266(2축매트릭스 평탄화)·이미지 phase2. 1차 74건 생성·검증·실업로드 대기. 비고 검색확정. systemmap 노드 추가)_

_갱신: 2026-06-18 (sikbom-register 운영중 — 1차 41건(74→판매중지 디듑33) 실업로드 성공. openpyxl 저장본 식봄 수용 확인(zip수술 불요). 빈 양식 reference/sikbom_bulk_template.xlsx + 골든 sikbom_bulk_golden_41.xlsx app repo 박제. 다음=이미지 phase2(상품코드 매칭))_

_세션 클로즈: 2026-06-18 (sikbom-register 신설·end-to-end 운영중 — 식봄 최초 상품 일괄등록). 완료: ① 카테고리 정리 reference/sikbom_category.csv(원본 양식 '상품 카테고리' **2축 블록 매트릭스→평탄 1차/2차/3차**·367→사용자 큐레이션 266) ② 양식 분석·전용값(상품 대량 등록 29열·r8·수수료7%·마진=스마트스토어 baseline(없으면10%)·판매가 공통식(2500/내림)·**배송비명 L=N==1?'유료배송(수량별)':'수량별 배송비 N'**[N=박스합포/낱개합포×박스내품·식봄센터 사전등록 의존]·카테고리명 그대로 B/C/D·과세 y·키워드 ≤15자/10개/한영숫자만·이미지 양식外) ③ 1차 74건 생성→검토 워크시트(정제명·카테고리 제안 정본100%·비고19건 검색/이미지 확정: 비스더블랙=캔커피·맛기름=향미유 참기름·스파크=세탁세제·밤감로자=밤통조림·호니베어=파이필링잼·피죤=섬유유연제2입) ④ **판매중지 다운로드 디듑**(상품코드 환원[낱개PC·박스관리코드·소분 변환코드→원코드]·446건 대조→33제거[낱개32+소분1: 백설튀김가루 박스08-45↔소분PD1KG5EA-08-45]→41) ⑤ **41건 실업로드 성공**(사용자 확인·openpyxl 수용·zip수술 불요) ⑥ 골든 박제 app repo reference/(sikbom_bulk_template.xlsx 빈양식·sikbom_bulk_golden_41.xlsx 검증본) ⑦ **이미지 phase2**(상품코드 폴더 zip·**찾기=관리코드/저장=상품코드A** — 낱개는 상이라 리네임 실질·82장 전건 성공·식봄이미지_41건.zip). systemmap sikbom-register **live**·meta 2026-06-18j. 로그 logs/2026-06/2026-06-18-sikbom-register-{setup,dedup,golden,images}.md. **다음 한 수=변동 없음** — 시장대비 권장가(두뇌① 시장결합·매핑 누적 후) 또는 이력 1e 행사 로깅(systemmap planned). 식봄 등록=펜딩 없음(차기 배치는 업로드감시 출력 받아 표준 흐름 반복).)

_갱신: 2026-06-19 (margin-optimizer(기준마진율 최적화·두뇌④) 신규 워크플로우 설계확정·미구현 — 인터뷰로 정의 도출. 베이스=proven채널 순이익가중평균·4분면·절반스텝·노브4종·라벨로스터. ADR 0026·systemmap 2026-06-19a)_

_갱신: 2026-06-19 (margin-optimizer 두뇌④ **v0 구현·라이브** — 권장 기준마진율 작업목록 + Gate3 결정원장(history/decisions.parquet seed). proven=월순이익 run-rate 누적85%·경계포함, 15-04 수작업 일치. ★**Reboot 필요**. 다음=측정루프→시즌라벨→cmm prefill. systemmap 2026-06-19b·로그 build)_

_갱신: 2026-06-19 (두뇌④ v0 운영보강·마진정합 — 택배2700·나들제외·45일억제·UI(월매출·코드·▲▼한국식)·기록+기준마진율 변경=타깃+Δ(ADR 0027)·기준마진율 컬럼. ⑦ 매출목표 로드맵 later. systemmap 2026-06-19c·ADR 0027·로그 ops)_

_갱신: 2026-06-19 (UI 디자인 Phase A 라이브 — 전역 테마(config.toml 인디고+Pretendard)+core/ui.py(CSS·헬퍼)+진입점 로고/그룹명. ADR 0028·systemmap backlog. 재배포+Reboot 1회·체감 확인 대기. 다음=Phase B)_

_갱신: 2026-06-19 (UI Phase C 시작 — 랜딩(지도·로드맵) 팔레트 리스킨: 크림+테라코타→near-white+인디고·상태색 통일·두뇌 인디고 분리·중복 st.title 제거. 기능 보존·page-only 자동반영. 커밋 dae597f. 다음=Phase B(데일리 헬퍼) or Phase C 잔여(오늘 할 일 요약))_

_갱신: 2026-06-19 (UI Phase B-1 데일리 — page_header+section_head(인디고 액센트바)·중복 divider 제거·toolkit에 section_head 추가. 이상치 표/metric/Styler 보존. core/ui.py 40fd855·데일리 3355a94. ⚠️ section_head 신규→Reboot 1회(이후 같은 헬퍼 페이지는 page-only). 다음=두뇌④·마진모니터·상품360 배치)_

_갱신: 2026-06-19 (데일리 품절 알림판 수제표 행 구분선 — keyed 컨테이너 스코프 CSS hairline(#ECEEF2). 타 표 무영향·로직 무변경·page-only. 커밋 62fc5cb)_

_세션 클로즈: 2026-06-19 (UI 디자인 — Phase A·랜딩 리스킨·B-1 데일리 출하, 나머지 로드맵·필요 시). 완료: ① **Phase A 전역 기반** — `.streamlit/config.toml`(인디고 #3B5BDB·Pretendard·라운드/테두리, 19페이지 자동 상속) + `core/ui.py`(inject_css 전역 CSS[st.metric→카드·버튼/탭 폴리시·핀필·▲빨강▼파랑] + 헬퍼 page_header·kpi_row·status_pill·delta_html·**section_head**) + 진입점 inject_css·사이드바 브랜드·네비 그룹명'분석·지능'. ② **Phase C 랜딩**(지도·로드맵) 팔레트 리스킨 — 크림+테라코타→near-white+인디고·상태색 앱 통일·두뇌 인디고 분리·중복 st.title 제거(기능/JS 보존·토큰만). ③ **B-1 데일리 대시보드** — page_header+section_head(인디고 액센트바)·중복 divider 제거·**품절 알림판 수제표 행 구분선**(keyed 컨테이너 `st.container(key="sb_board")` 스코프 CSS·타 표 무영향). 이상치 표(체크박스 선택형)·metric(이미 카드)·기존 Styler 보존. 커밋(app): config 168e203·ui e166707/40fd855·streamlit_app 6006b28·landing dae597f·daily 3355a94/62fc5cb. ADR 0028·workflows/ui-design.md·systemmap backlog. ⚠️ **재배포 + Reboot 1회**(폰트 + core/ui.py 신규 import/section_head) — 아직이면 1회. 이후 page-only는 자동반영. **잔여=로드맵·필요 시**: Phase B 나머지 페이지(두뇌④·채널마진모니터·상품360·마진침식·재고지능·가격AB·유틸 — page_header+section_head 같은 패턴, page-only·Reboot 불요) · Phase C 랜딩 '오늘 할 일' 요약 점프 · 데일리 4메트릭→kpi_row 승급(옵션). **프로젝트 기능 다음 한 수=변동 없음** — 두뇌④ 측정 루프 / 시장대비 권장가(매핑 누적 후). 로그 logs/2026-06/: ui-design-phase-a · ui-design-phase-c-landing · ui-design-phase-b1-daily)_

_세션 클로즈: 2026-06-19 (두뇌④ 측정 루프 = Gate 3 닫기 구현). 완료: 결정 원장의 pending 결정을 **결정일(ts) 이후 실적**으로 측정 → 개선/악화/무변화 판정 → 유지/되돌림. **사용자 확정**: 측정창 **30일**·되돌림=**baseline Δ 역가산 자동 원복**(승인 후). ① core margin_optimizer: MEASURE_MIN_DAYS=30·RESP_BAND=.10·`_verdict`·`measure`(ts 이후 거래만 월 run-rate·동일 마진정의·ready=경과≥30∧post>0). ② core decision_log: `update()` in-place 갱신(측정/조치 공용·스키마 무변경 18컬럼). ③ page 13 **탭 구조**(작업목록/측정 결과)·`build_prod` 공용 캐시 분리·`_apply_baseline` 모듈레벨 승격·측정 결과 탭(KPI→pending·ready 라이브표+[측정 확정]→measured표+[유지로 닫기]/[되돌림 baseline −Δ 원복·payload 미리보기]). 45일 억제 pending만. **되돌림=상대 역가산**(현 타깃+(before−applied)·ADR 0027 철학·기록만은 종료만). status pending→measured→closed/reverted(forward·비-PII). 판정=제안(행사·시즌·품절 미보정·사람 최종). 커밋 mo 39767b4·dl 650de01·page 25e45d2. 검증 합성 4건 스모크 전건 일치·ast 3파일 OK·원장 0행(forward seed→결정 누적+30일 후 실측 발생). ⚠️ **재배포(1~2분) + Reboot 1회 필요**(기존 import 모듈에 함수 추가→sys.modules 캐시; 페이지는 새 core 함수 참조라 Reboot 없으면 AttributeError). 검증 대기(사용자): 결정 기록→30일 후 측정 결과 탭 등장→측정 확정→유지/되돌림(되돌림 시 baseline 원복 cmm 반영). **다음 한 수=⑧ 시즌(명절세트) 라벨 제외**(월순이익 부풀림) → ⑦ 매출목표 라벨(sales_target.csv 포맷 선결) → ② 회전 markdown·나들 floor. 정본 workflows/margin-optimizer.md §15·systemmap 2026-06-19f·로그 2026-06-19-margin-optimizer-measure-loop.md)

_갱신: 2026-06-19 (두뇌④ 측정 루프 하드닝 — 매출자료 익월초 적재 갭 정합. ready=벽시계30일이 아니라 **적재 커버리지**(적재 최신거래일−ts≥30일)·run-rate **일수 정규화**(÷측정일수/30.4, 달력월 개수 아님) → 월말 결정+부분월 적재의 거짓 악화 해소. 신규 컬럼 측정일수·페이지 표시·대기 안내. 검증 4케이스(월말+완결=개선·월말+부분월=측정대기·오늘결정=대기·매출0=악화). 첫 실측=결정 누적+적재 30일분 후(현 5월말→6월분 7월초 적재돼야 시작). ⚠️ core 변경분에 포함→Reboot 1회. 커밋 mo 8834b7e·page 2bb0f5e. 로그 2026-06-19-margin-optimizer-measure-loop-coverage-fix.md)

_갱신: 2026-06-19 (두뇌④ ⑧ 시즌 제외 완료 — 선물세트(product_attributes 식품음료 분류 65종) build_prod에서 작업목록/측정 제외. 명절 스파이크(설13억·추석29억)가 활성개월 run-rate 부풀려 임팩트 상위 점령하던 노이즈 해소. page-only·Reboot 불요. 다음=⑦ 매출목표 라벨(sales_target.csv 포맷 선결). 커밋 page b7fcadb·로그 season-exclude)

_갱신: 2026-06-19 (두뇌④ ⑦ 매출목표+나들 floor(나) — best 관리채널 월매출<100만=미달 → 고마진/베이스근처/proven은 **나들 마진까지 절반스텝 인하**·나들 마진 없으면 −1%p·저마진은 🔴 사람판단. 원안 'best(나들포함) 따라가기'는 나들=바닥 무한인하라 폐기, 100만 절대 floor만 채택((나): 표시+자동제안, 측정 데이터 어차피 쌓임). 나들 floor anchor=build_prod가 나들 제외 전 1패스로 nadl_map 계산. core recommend_code(nadl_margin)·worklist(nadl_map)·TARGET_FLOOR 100만·TEST_CAP −1%p·목표 컬럼. 검증 합성 전건. ⚠️ core 변경→Reboot 1회(측정루프·하드닝·⑧·⑦ 묶어 1회). 다음=② 회전 markdown. 커밋 mo 277d295·page 2ca2a2d·로그 sales-target)

_세션 클로즈: 2026-06-19 (두뇌④ — 측정 루프부터 노브 전부 완성). 이번 세션 5종: ① 측정 루프(Gate3·결정일 이후 실적으로 효과측정→유지/되돌림) ② 측정 하드닝(커버리지 게이트+일수정규화, 익월초 적재 갭의 거짓악화 차단) ③ ⑧ 시즌(선물세트 65종·product_attributes) 작업목록/측정 제외 ④ ⑦ 매출목표(best 관리채널 월매출<100만→나들 마진까지 절반스텝·저마진🔴) + 나들 floor anchor ⑤ ② 회전 markdown(소진예측일>180일→램프 −2%p캡 청산·단방향·자동복귀·저마진🔴). **두뇌④ 설계 노브 전부 구현 → status 운영중.** ⚠️ **재배포+Reboot 1회**(core margin_optimizer/decision_log 변경 묶음). 결정원장 현재 0행(forward)·실측은 결정 누적+적재 30일분 후(6월분 7월초 적재돼야 시작). 잔여(나이스투해브)=cmm 편집창 직접 prefill('기준마진율도 함께 변경' 토글이 baseline 직접 write로 갈음 중)·margin_floor 제조원가 하한 명시 클램프. 커밋 mo 527ebd6·page 82c8c3d 외. 로그 logs/2026-06/: margin-optimizer-{measure-loop,measure-loop-coverage-fix,season-exclude,sales-target,turnover-markdown}. 다음 한 수=리부트 후 실데이터 점검 또는 사용자 선택)

_갱신: 2026-06-19 (invoice-fill 올웨이즈 송장 셀 서식 @→일반(General) 복귀 — invoice_cell_format 키 제거(값 int+General). 골든 20260619배송 5/5. 올웨이즈 요구 서식 변경. 커밋 1e1cd34. core지만 설정 dict 변경=보통 자동반영·안 보이면 Reboot 1회)

_세션 클로즈: 2026-06-22 (데일리 대시보드 가독성·맥락 보강 + 전역 풀폭). ①가격변동 알림 매입가 전용(b594bdf) ②상단 메트릭 잘림 해소+채널요약 콤마+택배 박스개수(7d0fefe) ③이상치 표 **최근 적재 2개월 정산 매출** 컬럼(추세·노이즈0·실적재월 자동롤·신규 cache _recent_month_sales·import store/cc)(b7b0d34) ④금액 콤마(localized·선택그리드라 Styler불가)+**월마진%**(gross 택배전·추세용)(db7eb50) ⑤금액 정수화(택배 송장배분發 소수 제거)(24be59e) ⑥**전 페이지 전역 풀폭**(core/ui.py .block-container max-width 1180px→none·데일리 임시 override 제거)(ui 5e11c40·0b f9141d4). ★**Reboot 1회 필요**=⑥ ui.py core 변경(폭 적용)·①~⑤ page-only 자동반영. 검증=8채널 매칭·52-55. ESM 추세·gross>net 일관. **미결: 6월 영업이익현황 7월초 [데이터추가] 수동 적재**(월매출 추세·두뇌④ 측정 갱신·자동누적 아님). 다음=두뇌④ 측정루프(6월 적재 후)·시장대비 권장가. 정본 workflows/daily-dashboard.md·ui-design.md·로그 2026-06-22-*)_


_세션 클로즈: 2026-06-22b (채널마진모니터 재고 필터 + 두뇌④ 3% 하한 clamp). ① **채널마진모니터** "재고 0" 체크박스 → **"재고 N개 이상" 숫자입력**(0=전체·NaN 자동제외·filter_sig 동기). page-only 자동반영. 커밋 56d1a1e. ② **두뇌④ 3% 절대 하한(MIN_SELL_MARGIN=0.03)** — 사용자 확정 "어떤 경우에도 3% 미만 판매 불가". 최초 hold+hide 구현(a53fcdc) → 사용자 정정 "3%까진 내리되 그 밑은 막기" → **clamp로 재구현**: 권장<3%면 현재>3%는 **3%까지만 내려 노출**(인하 액션 유지·사유 부기), 이미 3% 이하라 인하 불가면 **유지·작업목록 제외**. 전 경로(베이스·⑦매출목표·②회전·hold-low·실험큐) 합류 직후 1블록·나들<3%도 3%에서 막음(나들 예외 없음). 클램프 후 미세(<0.3%p)=MIN_DELTA 흡수·큰변동(>3%p)=BIG_MOVE 🔴 자연처리. 검증 합성 6케이스 전건(회전4.5→3.0 노출·⑦나들5→3.0 노출·현재2% 숨김·m3.1% 미세컷·8%→4.2 🔴·정상11→9). 커밋 core aa0cb9d·page bb8f224·정본 6efb1bf. **⚠️ core 변경 → Reboot app 1회 필요**(이후 page-only 자동). 정본 workflows/margin-optimizer.md §23·로그 logs/2026-06/2026-06-22-cmm-stock-filter·margin-optimizer-min-floor(-clamp). 다음 한 수=변동 없음 — 두뇌④ 측정 루프(6월 매출 7월초 적재 후)·시장대비 권장가(매핑 누적 후). 잔여(기존)=cmm prefill·margin_floor 원가하한 클램프._

_갱신: 2026-06-22 (두뇌④ ⑦ 매출목표 미달 임계 TARGET_FLOOR 100만→50만 — 사용자 '100만은 너무 하드'. 임계만·로직 동일·사유 문구 동적 자동반영. 기록된 결정은 소급 안 함. core f75e07b·page 349ed70·정본 eb21691. ⚠️ core 상수 → Reboot 1회(3% 하한과 함께). 로그 2026-06-22-margin-optimizer-target-floor-50)_

_세션 클로즈: 2026-06-22c (채널마진모니터 전월매출 2컬럼(이채널·전체)). ① 표 맨 끝 **전월매출(이채널)+전월매출(전체)** — 적재 최신월 매출자료(천년경영 정산)·**박스/낱개/소분 통일**. **전체=내 관리 8채널 합**(나들·B2B 제외·_CH_TO_SANGHO 전부, 사용자 정정 — '전 거래처' 아님). ② core **canonical_code**(신규·원박스 정규화: 소분→원코드·PC낱개→상품코드행 관리코드·박스/합포→자기자신, resolve_code 매핑 재사용) + page **_load_prev_sales**(store 파티션1개·_data_secret)·**_CH_TO_SANGHO**(8채널→상호명, **쿠팡=윙배송+로켓 합산**). ③ ★핵심: **매출자료 관리코드=전부 박스코드**(낱개·합포·소분 0건 실증)→listing만 정규화로 join. **같은 canonical 여러 행=같은 매출값**(세로 합산 금지·행별 참고)·매출 없으면 빈칸. ★**베이스(%)는 성능 우려로 사용자 보류**(두뇌④ 동일값=18개월+주문38만+ship_alloc 첫 로딩 십수 초). 검증: canonical(낱개 PC005900→274-245-10-03·소분 BT10EA-25-40-02→25-40-02)·전 채널 매칭·ast OK. ⚠️ **core canonical_code 신규 → Reboot 1회**(이후 page-only). 커밋 core 9c265d12·page 4aee8eb0·정본 wf 13e5757d. **+ 기준마진율 설정 UX 안정화**(체크박스 stale 해소 — 메인표 key `cmm_tblver` 버전카운터 저장 시 선택 강제 초기화 + 기준마진율 설정 인라인화(2단계→1단계), 두뇌④ mo_tblver 패턴. page-only. 커밋 13b33e56). **+ 제한 상품 등록/해제 UI**(표 선택→제한내용 입력=margin_floor.csv 등록·비움=해제·전 채널 공통·두뇌④ load_locked 공용. core parse_floor_dict·update_floor_csv·compute_listing floor_override 즉시반영. 골든=BOM/CRLF/타코드 보존. 커밋 core f8726dcd·page 18af7eb4). **+ 필터 다수**(제한 제외 fca6791f · **상품명 키워드 제외(쉼표)·기준 초과만(탐지>0)·전월매출(이채널) 범위 ≥/≤** 6ba74160 · 전부 page-only·filter_sig 동기). **세션 완료(2026-06-22c).** ⚠️ **재배포 후 Reboot app 1회** 필요 — 이번 세션 core 변경 묶음(canonical_code·parse_floor_dict·update_floor_csv·compute_listing floor_override). 한 번의 Reboot에 5개 기능 전부 반영(전월매출·기준마진율 UX·제한 등록/해제·필터들). 전부 **사용자 실사용 미검증**(Reboot 후 확인 대기). 다음 한 수=변동 없음 — 두뇌④ 측정 루프(6월 매출 7월초 [데이터추가] 적재 후)·시장대비 권장가(매핑 누적 후). 로그 2026-06-22-cmm-{prev-month-sales,baseline-edit-ux,floor-register,filters})_

_갱신: 2026-06-23 (식봄 행사기획 2차 사례 — MD 관리코드 직접 지정·과자10+컨츄리타임. 재확인 결과 7건 등재(박스4·PC낱개3)·메밀칩4 미등재. 현재 등재가가 이미 식봄 기준마진 이하(7.0~7.7%)→행사가=현재가 유지(사용자 확정)·메밀칩4 제외. 학습=① listing_sikbom 스냅샷 stale 주의(meta.updated_at 확인·사용자 갱신 직후 재fetch) ② 식봄 등재 유닛 PC낱개(개당)/박스별 매입가·판매가 단위 일치. 산출 xlsx 2시트(분석 라이브수식+식봄 공식양식 실 상품no/정가 기입). ⚠️86-66-05-0211 재고-15. 정본 workflows/sikbom-event-planning.md·로그 2026-06-23-sikbom-event-2nd-snacks.md)_

_갱신: 2026-06-23 (sikbom-register 2차 배치 — 행사기획 2차 미등재 메밀칩 4건을 일괄등록 양식으로 준비(낱개 모드). ★입력 경로=행사 매칭 미등재분에서 직접(업로드감시 미경유·첫 사례). PC005912/004212/005875/004291·판매가1,700~1,800·배송비명 수량별 배송비 10/8·카테고리 스낵.안주류/일반스낵.강냉이.씨리얼/일반스낵·과세y. 양식 생성·검증 완료·업로드 대기. 전제=배송비명 10·8 식봄센터 사전등록 확인·이미지 phase2. 산출 식봄_일괄등록_메밀칩4건.xlsx. 정본 workflows/sikbom-register.md §11·로그 2026-06-23-sikbom-register-meomilchip4.md)_

_갱신: 2026-06-23 (sikbom-register 3차 — 꽈배기 2건 업로드시트만(낱개·과세·같은 카테고리). ★67-64-01 부재→67-74-01(흑당) 추정 대체(67-74 참깨 페어·확인대기). 배송비명 수량별 배송비 16·판매가5,000·마진 baseline0→10%디폴트. 산출 식봄_일괄등록_꽈배기2건_v2.xlsx·로그 2026-06-23-sikbom-register-kkwabaegi2.md)_

_세션 클로즈: 2026-06-23 (식봄 행사기획 2차 + 미등재분 등록 인계 + 이미지). 이번 세션 흐름 = 행사 매칭 → 미등재분 일괄등록 → 이미지, 한 줄기로 연결. ① **식봄 행사기획 2차**(과자10+컨츄리타임1·MD 관리코드 직접 지정·타겟 없음). ★listing 06-18 스냅샷 stale→사용자 식봄 갱신 후 재fetch(06-23 14:01·586행). **7건 등재**(박스4·PC낱개3)·**메밀칩4 미등재**. 등재 유닛별 마진(박스/낱개)·현재가 7.0~7.7%=식봄 기준마진 이하라 **행사가=현재가 유지**(사용자 확정)·메밀칩4 제외. 산출 식봄_과자행사가_제안_분석.xlsx(분석 라이브수식+식봄 공식양식). ⚠️86-66-05-0211 재고-15. ② **sikbom-register 2차**(미등재 메밀칩4·낱개·과세). ★입력경로=행사 미등재분 직접(업로드감시 미경유·첫 사례). PC005912/004212/005875/004291·배송비명 수량별 배송비 10/8·카테고리 스낵.안주류/일반스낵.강냉이.씨리얼/일반스낵. 산출 식봄_일괄등록_메밀칩4건.xlsx. ③ **메밀칩 이미지 phase2** 3/4 zip(식봄이미지_메밀칩3건.zip). **65-54 제외**=gi.esmplus 미존재(65-54-01=명가찹쌀누룽지 오매칭). ★학습=소스폴더≠관리코드 시 대표 육안확인 필수. ④ **sikbom-register 3차**(꽈배기 2건·낱개·과세·업로드시트만). ★67-64-01 product_master 부재→67-74-01(흑당) 추정 대체(67-74 참깨 페어·확인대기). 배송비명 수량별 배송비 16·판매가5,000·마진 baseline0→10%디폴트. 산출 식봄_일괄등록_꽈배기2건_v2.xlsx. ⑤ **꽈배기 이미지 phase2** 2건 zip(식봄이미지_꽈배기2건.zip). 참깨·흑당 md5 동일=참깨+흑당 공용 브랜드컷(양쪽 표시·오매칭 아님). **펜딩(사용자측)**: (a) 식봄 행사 7건=공식양식 우측에 옮겨 제출(컨츄리타임 재입고) (b) 메밀칩4·꽈배기2 업로드 전 배송비명 사전등록 확인(10·8·16)+꽈배기 67-64-01 정정 확인+(선택)판매중지 디듑 (c) 65-54·흑당단독 이미지=호스트 올라오면 보충. **다음 한 수=변동 없음** — 두뇌④ 측정 루프(6월 영업이익현황 7월초 [데이터추가] 적재 후)·시장대비 권장가(매핑 누적 후). 로그 logs/2026-06/2026-06-23-: sikbom-event-2nd-snacks·sikbom-register-meomilchip4(+images)·sikbom-register-kkwabaegi2(+images). 정본 workflows/sikbom-event-planning.md·sikbom-register.md)_

_갱신: 2026-06-24 (식봄 행사기획 3차 — 행사가 단가 인하여력 검토 13품목(현마진 6.3~8.6%·식봄기준8% 이하 대부분·여력=현재가−3%하한 100~700원). ★식봄(foodspring) 경쟁가 GraphQL 크롤링 실증 — 지오펜스 없음·게스트세션+JS번들 raw 쿼리텍스트 POST 200·salePrice/appliedCoupon/vendor/stock 수신·즉시할인20%=마켓보로 부담 정산무관. 명가꽈배기=우리 5000 최저(8.6%). nadl동형 KR로컬 정례화 가능·미착수. 산출 식봄_7월_행사가_인하여력_분석.xlsx 2탭. 정본 workflows/sikbom-event-planning.md §3차·크롤링·로그 2026-06-24-sikbom-event-3rd-pricedown-graphql.md)_

_갱신: 2026-06-24 (식봄 행사기획 3차 후속 — 전 13품목 식봄 최저가 조사(꽈배기 외 11품목 추가 크롤). 규칙=우리 최저면 유지·경쟁 더 싸고 매칭시 마진≥3%면 매칭. **결과 전건 우리(태동유통) 최저 또는 동일규격 단독 → 내릴 품목 0·현재가 유지.** 경쟁 존재 3건(레몬에이드/꽈배기 참깨/흑당)도 우리가 더 쌈. 시트 탭 추가 식봄_최저가_조사(140수식 0오류). 학습=규격 다중품목은 동일규격 필터 후 비교. 식봄 단가 추가인하=경쟁 아닌 양보영역(3%하한·인하여력 참조))_

_갱신: 2026-06-24 (식봄 통조림 3건 박스→낱개 전환(668293/486842/486836)·hapo 0.833(5/6) 엔트리 제거 커밋 cc3545f3·N→1. ★식봄 경쟁가 운영형태 확정 ADR 0029 — **채팅 네이티브 ad-hoc + 재사용 스크립트 tools/sikbom_price_lookup.py**(세션·GraphQL·파싱·정산마진 코드화=토큰0, 판단(같은상품/규격매칭)=AI). nadl(정적카탈로그·페이지/스냅샷)과 본질 분리(식봄=라이브마켓·판매자별 이름상이·우리도 판매자). 페이지 안 만듦·xlsx 요청시만. 학습=대용량 저가캔 낱개전환 시 실비택배로 실현마진 급락→3%하한 클램프. 로그 sikbom-canned-box-to-single-hapo-remove)_

_세션 클로즈: 2026-06-24 (식봄 행사기획 3차 + 식봄 GraphQL 경쟁가 크롤링 capability 확립). 이번 세션 한 줄기: ① **행사가 인하여력 분석**(13품목 현마진 6.3~8.6%·대부분 식봄기준8% 이하·여력=현재가−3%하한 100~700원, xlsx 행사가_마진분석) ② **식봄 GraphQL 경쟁가 크롤링 실증**(지오펜스X·게스트세션+JS번들 raw 쿼리텍스트 POST 200·salePrice/coupon/vendor/stock·즉시할인20%=마켓보로 부담 정산무관) ③ **전 13품목 최저가 조사 = 전건 우리(태동) 최저/단독→내릴 품목 0**(경쟁 존재 3건도 우리가 더 쌈, xlsx 식봄_최저가_조사) ④ **통조림 3건(668293/486842/486836) 박스→낱개 전환**: 새 양식 시도→사용자가 기존 listing 직접 낱개 변경→**hapo 0.833(5/6) 엔트리 제거**(app reference, 커밋 cc3545f3·N→1) ⑤ **운영형태 확정 ADR 0029** — 식봄 경쟁가=**채팅 네이티브 ad-hoc + 재사용 스크립트 tools/sikbom_price_lookup.py**(세션·GraphQL·파싱·정산마진 코드화=토큰0 / 판단(같은상품·규격매칭)=AI). nadl(정적카탈로그·페이지)과 본질 분리·페이지 안 만듦·xlsx 요청시만. **코드 변경 0 → app Reboot 불필요**(hapo는 reference라 cmm 캐시/재배포 후 반영). 학습=대용량 저가캔 낱개전환 시 실비택배2700로 실현마진 급락→3%하한 클램프 필수. 정본 workflows/sikbom-event-planning.md·ADR 0029·tools/sikbom_price_lookup.py·로그 2026-06-24-sikbom-event-3rd-pricedown-graphql·sikbom-canned-box-to-single-hapo-remove. **다음 한 수=변동 없음** — 두뇌④ 측정 루프(6월 영업이익현황 7월초 [데이터추가] 적재 후)·시장대비 권장가(매핑 누적 후))_

_갱신: 2026-06-24 (식봄 행사기획 4차 — 통조림군 10품목 식봄 경쟁가 조사. 전건 우리(태동) 최저/동급최저 → 실인하 2건만: 994258 12,100→12,000(동률최저 6.1%)·486836 10,600→10,500(단독최저 4.6%) 매칭 인하. 산출 식봄_가격변경_행사가_2건.xlsx(상품 일괄수정 양식, 사용자 직접 업로드). 박스 2건(466061/466031)=경쟁 낱개캔뿐·낱개매칭시 마진붕괴라 유지·라리(486842) 재고0+역마진 제외. 코드변경0·Reboot불요. 정본 workflows/sikbom-event-planning.md 4차·로그 2026-06-24-sikbom-event-4th-canned-pricematch.md)_

_세션 클로즈: 2026-06-24b (식봄 행사기획 4·5차 + 쿠팡 무료배송 마진 관찰). 흐름: 통조림10 경쟁가 조사(4차)→2건 매칭 인하 시트→과자13 합쳐 MD 제출 양식+내부 재고마진(5차). ① **4차** 통조림 10품목 식봄 GraphQL 경쟁가 — 전건 우리(태동) 최저/동급최저, 실인하 2건만(994258 12,100→12,000·486836 10,600→10,500 매칭, 시트 식봄_가격변경_행사가_2건.xlsx). 박스 2건(466061/466031)=낱개매칭시 마진붕괴 유지·라리(486842) 재고0+역마진 제외. ② **5차** MD 제출용 = 통조림 최저가7 + 과자13(2·3차 크롤본 전건 우리최저) 통합. 산출 `식봄_7월_기획전_종합_프로모션_리스트.xlsx`(원본2시트+새시트 '3.통조림·과자(태동)' 판매자 H:O·원가/마진 미포함) + `내부공유_식봄7월_통조림과자_재고마진.xlsx`(매입가·재고·라이브수식 마진 4.3~9.3%·recalc0오류). ⚠️ 레몬에이드(994220) 재고-15 재입고 필수·청양마요90g/게맛살240g/삼아/DOLE 재고 얇음. ③ **쿠팡 무료배송 마진 관찰**(11-75-05): 택배비무료 적용건은 실택배비2700 미차감 → 마진 1.75%(차감)→25.1%(미차감). 단건이라 코드규칙화 보류·cmm.md 노트. **코드 변경 0**(reference/template/xlsx 산출만)→app Reboot 불필요. 잔여(기존)=두뇌④ 측정루프(6월 영업이익현황 7월초 적재 후)·시장대비 권장가. 정본 workflows/sikbom-event-planning.md 4·5차·channel-margin-monitor.md·로그 2026-06-24-sikbom-event-{4th-canned-pricematch,5th-md-submission})_

_갱신: 2026-06-24 (데이터현황(연동 데이터 관리) 적재 범위 일자까지 표시 — coverage monthly에 date_col(매출 거래일자·주문 발주일·재고 스냅샷일자·매입 기준일) + 첫/마지막 파티션 read해 first_day/last_day. 페이지 범위 컬럼·캡션 일자 폴백. 갭·타임라인은 월 유지. 골든 실데이터 매출 2023-01-01~2026-05-31 등 전건 확인. ⚠️ core coverage→Reboot 1회. 커밋 coverage a418e6b·page e344a98)_

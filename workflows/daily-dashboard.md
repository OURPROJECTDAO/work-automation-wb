# 워크플로우: daily-dashboard (데일리 대시보드)

> 이 기능을 건드리기 전 이 파일을 읽는다. 전역 함정 pitfalls.md, 설계근거 decisions/0023, 연계 intelligence-layer.md §6①·daily_margin.

## 요약
- **매일 반복 업무 산출물로 당일 인사이트를 즉시 보는 곳.** v1 = 당일 마진 점검(구 마진침식 탭D 승격) + **파일 자동 인계**.
- 사용자 비전: "마진침식→당일 점검의 **확장판**" — 당일 점검은 천년경영업로드 output·송장출력·상품관리 기반이므로 그 토대 위에 데일리 인사이트를 더 얹는다.
- 페이지: `app/pages/0b_데일리대시보드.py` (네비 첫 그룹, **지도·로드맵 바로 아래**). 세션 인계 = `core/intelligence/daily_inbox.py`.
- 계산 본체 = `core/intelligence/daily_margin.py`(탭D와 공유·무변경). 마진침식은 3탭으로 축소(탭D 제거).

## v1 — 당일 마진 점검 (탭D 로직 그대로)
- 매출 = 천년경영 output **실제기입단가×수량**(net·수수료적용) · 원가 = master **매입단가(낱개)×낱개수량** · 택배 = 채널 flat × **실제 물리박스**(합포 2시나리오: 250/355 H열 다품목 + 175~200ml 30개입 수령자 ceil(팩/3)).
- 이상 = 역마진 OR 마진율 < 채널 baseline − buffer. 조기 트립와이어(정산 진실=매출자료 월정산).
- 입력 3종: ① 천년경영 output(YYMMDD.xlsx) ② 송장출력(★★송장MMDD.xlsx) ③ 상품관리(master).

## ★ 파일 자동 인계 (ADR 0023) — 핵심
- **상품관리(master)** = reference `product_master.csv` 라이브 read(이미 자동·연동데이터관리에서 매일 갱신). 인계 불요.
- **천년경영 output · 송장출력** = 같은 세션의 이전 워크플로우(파일처리)에서 자동 인계:
  - 파일처리 **오픈마켓 합포 실행** → `invoice_bytes`(★★송장) 생성 시 `daily_inbox.push(SLOT_INVOICE)`.
  - 파일처리 **천년경영 업로드 실행** → `out`(output) 생성 시 `daily_inbox.push(SLOT_CHEONNYEON)`.
- 데일리 대시보드는 인박스에서 기본 사용 → **재업로드 불요**. 슬롯별 **수동 갱신 업로더**(override·"그 시점 파일로", 업로드 시 인박스에도 push).
- ★ **인박스 = 세션(st.session_state)·휘발성·in-memory.** 송장출력에 PII(수령자·주소·송장번호)가 있어 **디스크/repo 미저장**(전역 보안 규칙). → 같은 작업 세션이면 자동, **리부트/새 세션이면 인박스 비워짐 → 수동 업로드**. (cross-session은 후순위·비-PII 처리본만 영속 검토)
- 단일 진실원천(슬롯 키) = `daily_inbox.SLOT_CHEONNYEON`/`SLOT_INVOICE` — 생산처(1_파일처리)·소비처(0b) 공유로 키 드리프트 방지.

## 품절 알림판 (ADR 0024) — 발주 품절목록 → 재입고 자동/수동 해제
- **무엇**: 매일 발주작업(품절목록)에 뜬 상품을 알림판에 띄워놓고, 상품관리 갱신 후 **박스재고가 양수로 들어오면 입고로그 남기고 자동 삭제**. 안 들어오면 "MM월DD일부터 N일째 품절" 유지. 수동 1클릭 삭제(로그 없음).
- **저장(영속·비-PII)**: private data repo — `history/stockout_board.json`(현재 알림판 {관리코드:{상품명,since,발주수량,seed현재고}}) + `history/restock_log.csv`(입고로그 append: 관리코드·상품명·품절시작일·입고일·품절일수·입고시박스재고). 세션 휘발 아님(인박스와 다름).
- **등록(seeding)**: 발주서출력업무 **Phase2 품절목록 생성 시 자동**(1_파일처리 `_seed_stockout_board(stockout_df)`). 품절목록 컬럼=관리코드·상품명·발주수량·현재고(run_phase2가 rename). 없는 코드만 추가·**품절시작일=그날**(이미 있으면 유지). 전건.
- **재입고 reconcile**: 데일리 대시보드 열 때 알림판 각 항목의 **현재 박스재고**(product_master '박스' 컬럼, 라이브)를 확인 → **> 0(양수)** 이면 회복 → 입고로그 append + 알림판 제거. (현 품절건 박스재고 다 음수라 양수 전환이 깔끔한 신호·사용자 확정. 0=재고없음→유지.) `🔄 상품관리 다시 읽기` 버튼=cache clear(최신 product_master 반영).
- **수동 삭제**: 항목별 🗑 버튼 1클릭 제거(입고로그 안 남김·사용자 확정).
- **★ 박스재고 = product_master '박스' 컬럼**(박스내품 아님). 품절목록 현재고 = 박스재고 − 발주수량(박스단위) — 즉 품절목록은 "오늘 발주 대비 부족"이라 절대 0 아님. 회복 신호는 박스재고 양수 전환.
- **알림판 표시 컬럼(2026-06-16 추가)**: 관리코드·상품명·품절(MM월DD일부터 N일째)·현재박스재고에 더해 **최근입고일·평균매입주기·입고횟수(1년)** 표시(품절목록 E/F/G와 동일, 발주일 기준 1년·매입현황 cadence). 0b `_buyin_cadence()`(data repo 최근 13개월 파티션·`cadence_by_code(months=12)`·ttl30분) → `board_to_frame(..., cadence=...)`. 보기 편하게 한 화면에서 "이 품절건 마지막 입고·보통 며칠마다·1년간 몇 번" 확인.
- core: `core/intelligence/stockout_board.py` (read/write_board·read/append_log·seed_from_stockout·reconcile·manual_remove·board_to_frame). 페이지: 0b 상단 섹션.

## 채널별 요약 + 가격 변동 알림 (확장판①, 2026-06-17)
- **채널별 요약(당일)**: 당일 마진 점검 `ddf`를 채널 groupby → 매출(net)·원가·택배·마진·마진율(Σ마진÷Σ매출)·품목수. 메트릭 아래·이상치 표 위. page-only(daily_margin 재사용·새 의존 없음).
- **가격 변동 알림(±N%)**: 1b 스냅샷(`stock_history`) 연속 비교로 **매입단가·매출단가** ±N%(기본 2%·1~20% 슬라이더) 변동 탐지 → 구분(매입가/판매가)·방향(인상/인하)·전일가→금일가·변동률·변동일. 최근 N일(기본 7) 윈도우·구분 필터·XLSX. 품절 알림판 자매(품절 board 뒤·당일 마진 앞). **박스재고 컬럼**(product_master '박스'·품절 알림판 공유·None='—')·**색상**(▲ 인상 빨강#d11 / ▼ 인하 파랑#1565c0, Styler 텍스트색)·XLSX 박스재고 포함. (요약 메트릭 라벨은 CSS 색 불가→표만 색상.)
  - core `stock_history.detect_price_changes(snaps, threshold, fields)` — `detect_transitions`(재고) 자매. 상품코드별 연속 스냅샷 shift 비교·**직전 결측(신규 등재)/직전 0이하 제외**·구분·방향·변동률(%). 페이지 `_price_changes(days, threshold)`(data repo 최근 3개월 파티션·ttl30분·🔄 cache clear).
  - ★ 1b 스냅샷 **forward 적립(2026-06-15~)** → 가격 이력 현재 얕음, 상품관리 업로드일마다 누적. 업로드 sparse여도 "직전 기록 대비"라 자동 대응.
  - ★ 분모 주의: 채널 마진율 = Σ마진÷Σ매출(net) — 당일 마진 점검(이익÷매출)과 동일. 실현마진(÷매입가)인 두뇌③/상품360과 분모 다름.

## 이상치 → 권장가 + 채널 가격변경 시트 연결 (확장판②, 2026-06-17)
- **권장가 컬럼**: 당일 마진 점검 표(이상치/전체)에 **현재가·권장가(채널기준)** 추가. 권장가 = 채널 기준마진율 달성 **판매가**(cmm `compute`의 '권장가', 판매가 기준만). 출처=그 채널 listing(channel-margin-monitor 저장본) `compute_listing`(baseline 라이브 override). 1관리코드↔다listing이면 min~max 범위 표시.
- **체크박스 → 채널 가격변경 시트**: 표를 `st.dataframe(on_select="rerun", selection_mode="multi-row")` 선택형으로. 선택 행 채널이 **2종+/0종 → "한 채널만 가능" 경고**(표가 채널 혼재라 시트는 채널별). **단일 채널** → 그 채널 listing을 선택 관리코드로 필터해 pids 추출 → cmm 빌더 그대로 호출 → 그 채널 양식 다운로드. (채널마진모니터에서 그 상품 골라 내보내는 것과 동일 산출물)
- core 신규 없음 — cmm 재사용. 페이지 헬퍼: `_cmm_listing`(cached·listing→compute_listing)·`_reco_lookup`·`_gen_price_form`(append/filter/smartstore 디스패치)·`_do_price_change`(단일채널 가드+다운로드).
- **이중검수(2026-06-17)**: 표에 `listing마진`·`판정` 컬럼. 당일 미달이라도 **listing(compute_listing) 마진이 기준 이상이면 '일시적'**(쿠폰·실박스 택배 등 — 가격 손댈 필요 없음), **listing도 미달이면 '구조적'**(가격조정). `_reco_lookup(pairs, buffer)`가 listing 마진율/미달(마진율<기준−buffer, 당일과 동일 규칙) 집계 → 4-tuple. page-only.
- **★ 함정: 당일 vs listing 마진 기저 다름**. 당일=매출(net)에 **배송비 수입 미포함** + 택배 실박스×2700 **순비용**. listing=정산액에 **배송비×0.967 수입 가산** + 실택배비 2700. 그래서 당일 미달인데 listing은 건강(권장가<현재가) 가능 — 버그 아님(설계). '구조적' 과다 시 **listing 배송비 stale 의심**(무료배송인데 기본배송비 3000 잔존 → listing 마진 과대).
- **제약**: ① 알리=가격변경 양식 없음(안내) ② 쿠팡·스마트스토어=raw `.xlsx`('전체 교체') 필요 ③ **현재가**만 listing 최신 의존(미등재=빈칸) — **권장가는 product_master 매입가 기준 역산이라 항상 표시**(listing에 있으면 실 N·실 배송비로 정확, 없으면 N=1·채널기본 배송비 추정). ④ 가격변경 **시트 생성**은 여전히 listing 필요(미등재 상품은 변경 대상 행이 없어 시트 불가).

## 신규 업로드 대상 (확장판③, 2026-06-17)
- **무엇**: 최근 N일(기본 7) **재고가 새로 들어왔는데(입고·신규등재) 아직 8채널 어디에도 안 올라간** 상품 → 신규 업로드 후보. 품절 알림판 **바로 다음**(품절=나감 ↔ 신규입고=들어옴 대칭).
- **신호 = 재고 ∩ 채널미등록**:
  - 재고: `stock_history.detect_new_stock(snaps, since)` (신규 core) — **입고 전이**(직전 ≤0→양수, detect_transitions와 동일) **∪ 신규 등재**(스냅샷 최초 등장 + 양수). detect_transitions(입고)·detect_price_changes는 *직전 결측(신규 등재)을 일부러 제외* → 그 케이스를 뒤집어 surfacing한 게 신규등재. **상품코드별 최신 이벤트 1건.**
  - ★ **baseline floor**: forward 적립(2026-06-15~)이라 **최초 스냅샷일(seed)에 처음 뜬 코드는 신규 제외**(그날=기존 catalog). 그 이후 처음 뜬 것만 진짜 신규. 입고 전이는 직전값 있어야 잡혀 seed 자동 제외.
  - 채널 미등록: `upload_monitor.build_gap_table` **재사용**(중복 0·키=상품코드). **전채널 미업로드 = 모든 채널 ∈ {업로드필요, 업로드제외} & ≥1 업로드필요**. build_gap_table이 비판매 제외(반품/파렛트·exclude.csv)·채널별 skip·재고>0 노이즈컷까지 처리.
- **= 업로드감시의 '최근 입고' 서브셋**. 업로드감시=전수 감사(가서 봐야 함·재고∩미업로드 전량), 데일리=오늘 새로 들어온 것만 트리거(작게).
- **표**: 관리코드(공백이면 (상품코드) 폴백)·상품명·박스재고·유형(입고/신규등재)·이벤트일·**최근매입일**·올릴채널수. XLSX·🔄·N 슬라이더. page `_new_uploads(days)`(read_all_snapshots→detect_new_stock→build_gap_table 교집합·cache 30분).
- **★ 제약**: ① **최근매입일 = 매입현황 cadence(`_buyin_cadence`)인데 월1회 적재** → 당일 막 들어온 매입은 늦게 반영(보조 표시용). **재고 신호는 상품관리 박스재고 양수 전환이라 daily-fresh**(상품관리 매일 갱신). ② listing/product_master 미등재·stale 한계는 업로드감시와 동일 상속. ③ baseline floor는 적립 며칠이면 안정. ④ 매입현황(purchases)을 신호로 안 씀(timing 느림) — 어디까지나 1b 재고 스냅샷 기반.

## 코드
- `app/pages/0b_데일리대시보드.py` — 인박스 상태 표시 + 슬롯 수동 갱신(`_slot_ui`) + 당일 마진 표/메트릭/XLSX. 헬퍼(_master_lookup·_pc_lookup·_hapo_codes·_baseline_dict·_to_xlsx)는 8_마진침식과 동형(현재 복제).
- `core/intelligence/daily_inbox.py` — push/get + 슬롯 상수. (st.session_state를 인자로 받음 — core는 streamlit 비의존)
- `core/workflows/channel_margin_monitor.py` (cmm) — 권장가(compute_listing)·가격변경 빌더 재사용(이상치→시트 연결).
- `core/workflows/upload_monitor.py` (um) — `load_references`·`build_gap_table`·`CHANNEL_KEYS`·`ST_NEED_UP/ST_SKIP_CH` 재사용(신규 업로드 대상 전채널 미등록 판정·중복 0).
- `core/intelligence/stock_history.py` — `detect_price_changes`(가격 변동 알림)·`detect_new_stock`(신규 업로드 대상 재고 신호). 둘 다 1b 스냅샷 연속 비교·detect_transitions 자매.
- `core/intelligence/daily_margin.py` — parse_invoice_shipping·parse_cheonnyeon_sales·compute_daily_margin (변경 없음).
- 생산 훅: `app/pages/1_파일처리.py` (tab_basic 오픈마켓·tab_cy 천년경영) — `import core.intelligence.daily_inbox as _inbox` + 결과 생성 직후 push.
- 네비: `app/streamlit_app.py` 첫 그룹, 지도·로드맵 다음.

## 전용 함정
- **송장출력 = ★★송장(오픈마켓 generate_invoice_xlsx) = 탭D 검증(0615) 그 형식**: 10열 위치(상태·관리번호·발주일·**판매처[3]**·주문번호·**수령자[5]·주소[6]·상품명[7]**·택배사·**송장번호[9]**). 송장번호 그룹키 필수(없으면 박스 그룹 0).
- **인박스 휘발성**: 자동 인계는 *같은 세션* 한정. 사용자가 다른 기기/새 탭/리부트면 비어 있음 → 수동 업로더 안내. (영속 아님을 UI에 명시)
- daily_margin은 `read_only=True` 금지(천년경영 dim 오독·전역 pitfalls). 인박스 bytes는 BytesIO로 파싱(parse 함수가 bytes/파일객체 모두 수용).
- 새 core 모듈(daily_inbox) 첫 배포 → 안 보이면 Reboot app 1회(모듈캐시·pitfalls).

## 관련 로그 / 결정
- decisions/0023-daily-dashboard-handoff.md (당일점검 승격 + 세션 인박스 자동 인계)
- logs/2026-06/2026-06-16-daily-dashboard-v1.md
- intelligence-layer.md §6①(탭D 원설계·daily_margin) · logs/2026-06-15-daily-margin-tabd.md · 2026-06-16-daily-margin-hapo-shipping.md

_갱신: 2026-06-16 (신규 — 당일 점검 탭D를 독립 페이지로 승격 + 천년경영/송장출력 세션 자동 인계(재업로드 불요)·수동 갱신 override. 상품관리=reference 라이브. ADR 0023)_

_갱신: 2026-06-16 (품절 알림판 추가 — 발주 품절목록 자동 등록·박스재고>0 재입고 입고로그+자동삭제·수동삭제·영속(stockout_board.json/restock_log.csv). ADR 0024. 새 core→Reboot 1회)_

_갱신: 2026-06-16 (품절 알림판에 최근입고일·평균매입주기·입고횟수(1년) 컬럼 추가 — 매입현황 cadence(최근13개월·1년윈도우)·board_to_frame cadence 인자. core→Reboot)_

_갱신: 2026-06-17 (확장판① — 채널별 요약(당일 매출·마진율) + 가격 변동 알림(1b 스냅샷 ±N% 매입가/판매가·detect_price_changes). core stock_history→Reboot 1회)_

_갱신: 2026-06-17 (확장판② — 이상치 표 권장가(채널기준·판매가) 컬럼 + 체크박스 선택→단일채널 가격변경 시트 다운로드. cmm 빌더 재사용·page-only. 알리 미지원·쿠팡/스마트스토어 raw 필요·listing 최신 의존)_

_갱신: 2026-06-17 (fix — 스마트스토어 가격변경 미지원 오판 수정. `_supports_price_change`(price_form 또는 즉시할인 cols·consolidate 아님=bulk). 알리만 미지원. _gen_price_form pf=None 허용. page-only)_

_갱신: 2026-06-17 (fix — 권장가 항상 표시. listing 미등재여도 product_master 매입가 기준 역산(_reco_from_master, cmm 공식 동일·N=1·채널기본 배송비). 현재가만 listing 의존. page-only)_

_갱신: 2026-06-17 (가격 변동 알림 — 박스재고 컬럼 추가 + 인상 빨강/인하 파랑 색상(Styler ▲▼). XLSX 박스재고 포함. page-only)_

_갱신: 2026-06-17 (fix — Styler.applymap→.map. pandas 3.x(Streamlit Cloud)에서 applymap 제거 AttributeError 해소. 전역 함정 pitfalls 등재)_

_갱신: 2026-06-17 (이상치 표 이중검수 — listing마진+판정(일시적/구조적/없음). 당일 vs listing 마진 기저 차이(배송비 수입·실박스 택배) 함정 기록. page-only·Reboot 불요)_

_갱신: 2026-06-17 (fix — ESM 행만 현재가/권장가/판정/가격변경 누락 버그. 원인=cmm ESM 키 'esm'(소문자) vs SHEET_TO_CMM 'ESM'(대문자) 불일치. 0b _cmm_key 대소문자 무시 보정 3곳. page-only)_

_갱신: 2026-06-17 (확장판③ 신규 업로드 대상 — 최근 입고·신규등재 ∩ 8채널 전부 미업로드 ∩ 재고>0. 신규 core stock_history.detect_new_stock(입고전이∪신규등재·baseline floor·detect_transitions 자매) + upload_monitor.build_gap_table 재사용(중복0·업로드감시 최근입고 서브셋). 최근매입일=cadence(월1회 보조). 골든 8건. page 0b+core→Reboot 1회)_

_갱신: 2026-06-22 (가격 변동 알림 — **매입가 전용**. 판매가 불요(사용자) → 구분 멀티셀렉트 토글 제거·매입가 고정 필터·표 '구분' 컬럼 제거. core detect_price_changes 무변경(둘 다 탐지·page에서 매입가만 필터, 판매가 복귀는 1줄). 커밋 b594bdf·page-only·Reboot 불요)_

_갱신: 2026-06-22 (가독성 — ① 상단 4메트릭 매출/마진 잘림 해소(st.columns [3,3,2,2]로 매출·마진 넓게+이 페이지 CSS stMetricValue 1.55rem·nowrap) ② 채널별 요약 콤마(NumberColumn→Styler {:,.0f}, 가격변동 표와 동일 패턴) ③ **택배=박스개수**(택배비÷2700, 사용자요청 40500→15·캡션 실제박스수와 정합). 커밋 7d0fefe·page-only·Reboot 불요)_

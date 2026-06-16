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

## 코드
- `app/pages/0b_데일리대시보드.py` — 인박스 상태 표시 + 슬롯 수동 갱신(`_slot_ui`) + 당일 마진 표/메트릭/XLSX. 헬퍼(_master_lookup·_pc_lookup·_hapo_codes·_baseline_dict·_to_xlsx)는 8_마진침식과 동형(현재 복제).
- `core/intelligence/daily_inbox.py` — push/get + 슬롯 상수. (st.session_state를 인자로 받음 — core는 streamlit 비의존)
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

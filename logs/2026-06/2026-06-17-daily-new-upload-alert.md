# 2026-06-17 데일리 대시보드 확장판③ — 신규 업로드 대상

## 무엇
데일리 대시보드(0b)에 **"신규 업로드 대상"** 섹션 추가(품절 알림판 바로 다음). 최근 N일(기본 7) **재고가 새로 들어왔는데(입고·신규등재) 아직 8채널 어디에도 안 올라간** 상품을 매일 콕 집어 표시 → 신규 업로드 후보.

## 왜
사용자 실무 니즈: "그 코드로 온라인에 올라간 채널이 없는데 매입이 새로 들어왔다 → 신규 업로드 해야 하는 것." 업로드감시(업로드감시 = 전수 감사·박스재고∩채널미업로드 264건)는 가서 봐야 함. 데일리엔 **그중 '최근 새로 들어온' 시의성 있는 서브셋(8건)** 만 트리거.

## 변경
- **core `stock_history.detect_new_stock(snaps, since=None, in_stock_threshold=0.0)`** (신규) — 입고 전이(≤thr→양수, detect_transitions와 동일) **∪ 신규 등재**(최초 등장+양수). detect_transitions/detect_price_changes가 *직전 결측(신규 등재)을 제외*하는 그 케이스를 뒤집어 surfacing. ★ **baseline floor**: 최초 스냅샷일(seed)에 처음 뜬 코드는 신규 제외(forward 적립 6/15~ — 그날=기존 catalog). 입고 전이는 직전값 있어야 잡혀 seed 자동 제외. 상품코드별 최신 이벤트 1건. 반환 상품코드·관리코드·이벤트일·금일재고·유형(입고/신규등재). 커밋 8845a7a6.
- **page 0b** — import `upload_monitor as um`. `_new_uploads(days)`(cache 30분): `read_all_snapshots`→`detect_new_stock(since=today−N)` ∩ **`um.build_gap_table`의 전채널 미업로드**(모든 채널 ∈{업로드필요,업로드제외} & ≥1 업로드필요) ∩ 재고>0. 채널 미등록·비판매제외(반품/파렛트·exclude.csv)·채널별 skip 전부 build_gap_table 재사용(중복 0·키=상품코드). 섹션: N 슬라이더·🔄·표(관리코드·상품명·박스재고·유형·이벤트일·최근매입일·올릴채널수)·XLSX. 최근매입일=`_buyin_cadence` 재사용. 커밋 71ff2a88.

## 검증
- detect_new_stock ast OK + 실 import 골든: 실 스냅샷 **4일(6/14 seed·6/15·6/16·6/17)** 최근7일 → 입고 22 + 신규등재 1 = **23건**, baseline(6/14) 코드 미혼입, since=None/빈입력 방어 OK.
- 전체 조인 골든(build_gap_table 동등): 전채널 미업로드(재고>0) **264건** 중 최근7일 신규 ∩ = **8건**(전부 올릴채널수=8). 신규등재 1건=에이스 델리시아스케이퍼(005944·관리코드 공백→(상품코드) 폴백). 입고 7건(스프라이트슬림·오토미 등). product_master/listing 대조 정상.

## 다음·상태
- ✅ **page 0b 최신분 = 재배포 자동반영. core stock_history 신규 함수 추가 → 안 보이면 Reboot app 1회**(detect_new_stock import 모듈 캐시). 사용자 실사용 확인 대기.
- 제약(상속): 최근매입일=매입현황 월1회 적재라 당일 매입은 늦게 반영(재고 신호=상품관리 박스재고 양수 전환이 daily-fresh). listing/product_master 미등재·stale 한계는 업로드감시와 동일. baseline floor는 6/15~ 적립 며칠이면 안정.
- 다음 한 수 변동 없음 — ★★ 시장지능 nadl 로컬 수집기(행사 샘플 대기) 또는 데일리 추가 인사이트.

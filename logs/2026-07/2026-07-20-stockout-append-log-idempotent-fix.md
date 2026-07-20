# 2026-07-20 — 품절 알림판 재입고 자동처리 멱등화 + PUT 재시도 (HTTPError 픽스)

## 무엇
데일리 대시보드 "🔄 상품관리 다시 읽기(재입고 반영)"에서 `urllib.error.HTTPError`(0b line 518 → `stockout_board.append_log` PUT). 사용자 보고. core `stockout_board.py`의 append_log를 멱등화하고, append_log/write_board PUT에 재시도를 넣고, 이미 오염된 restock_log 중복 2행을 정리.

## 왜 (근본 원인)
**GitHub raw(contents API raw) read-after-write 지연으로 인한 재입고 중복 처리 → 짧은 시간 반복 PUT → GitHub 409/403.**

- 데일리 대시보드는 위젯 상호작용마다 스크립트 전체 rerun. 품절 알림판 블록(`if _board and _box_stock`)은 페이지 로드마다 자동으로 reconcile→append_log→write_board 를 돌린다.
- `read_board`/`read_log`는 CDN 캐싱된 raw 라 방금 write 한 걸 몇 초~수십초 stale 하게 읽는다 → **같은 재입고 건이 rerun 사이 반복 판정**.
- 물증: 7/20 `restock_log.csv` 에 `31-50 코카콜라`·`31-17-03 스프라이트`가 **각 2번** 완전동일 중복(113=115, 114=116). 커밋 히스토리도 `restock +2`가 01:03:37·01:03:48 **11초 간격 2회**. 그런데 board 는 01:03:44 에 **정상 1회만** 재입고 2건 삭제 → read_board stale 로 지운 board 가 다시 읽혀 로그만 중복된 것.
- 7/15 낱개/소분 reconcile 픽스로 재입고 자동삭제가 **실제로 작동**하기 시작하면서(전엔 조회 미매칭으로 영구 미작동) 이 race 가 처음 드러남.

## 변경
- **core/intelligence/stockout_board.py** (커밋 app `b5254b82`):
  - `_put_retry(pat, repo, path, content_bytes, msg, max_attempts=4)` 신설 — 매 시도 직전 fresh sha 재취득, PUT 이 409/422/403/429 면 `1.5×(n+1)`초 backoff 후 재시도(append_log·write_board 공용).
  - `append_log` **멱등화** — 커밋 직전 최신 로그 재확인해 `(관리코드, 입고일)` 이미 있는 rows skip, 실제 추가분만 PUT 하고 **fresh list return**(기존 호출부는 반환 무시라 호환).
  - `write_board` → `_put_retry` 사용.
  - `import time` 추가.
- **work-automation-data: history/restock_log.csv** (커밋 data `f8a4c3ec`): 완전동일 중복 2행 제거(keep first) 117→115. 제거분 = 31-50·31-17-03 의 2026-07-20 중복분(각 1행). 정당한 과거 재입고(입고일 다름)는 전부 보존.

## 검증
- `ast.parse` OK. base64/time 사용 확인.
- 멱등 필터 실데이터 스모크(내 PAT, PUT 없이): 실제 restock_log(117행) existing 로 오늘 이미 로그된 31-50/31-17-03 은 skip, 신규 코드만 통과 — 통과.
- restock_log dedup 117→115, 제거되는 2행이 정확히 31-50·31-17-03(2026-07-20)임을 출력으로 확인 후 커밋.
- 현재 board 19건은 재입고 대상(원코드 박스재고>0)이 **0건**(전부 ≤0 또는 미등록) — 즉 앱을 지금 열면 append_log 자체가 호출되지 않아 당장 재발은 없고, **다음 재입고 시점부터 근본 픽스가 적용**됨.

## 다음 / 상태
- ⚠️ **재배포 + Reboot app 1회 필요** (core stockout_board.py 함수 시그니처/신규 함수 변경 — 페이지는 새 core 참조라 Reboot 없으면 AttributeError 가능). 사용자 실사용 확인 대기(다음 재입고 때 중복 없이 1회 처리·HTTPError 소거).
- 정확한 HTTPError code 는 Streamlit Cloud 'Manage app' 로그로만 확정 가능하나(409/403 추정), 근본 원인은 데이터 물증(중복 로그·11초 2커밋)으로 확정. 처방은 code 무관 동일.
- 전역 함정 pitfalls.md 신설 — 같은 계열 data repo 영속 훅(stock_history·listing_history·decision_log)도 자동 rerun write 경로면 동일 처방(append 멱등·PUT 재시도·훅 게이팅) 점검 대상.
- 기존 다음 한 수 불변: 두뇌④ 측정 개시(7월 데이터 적재 후)·로켓그로스 8/1·시장대비 권장가.

커밋: app `b5254b82`(stockout_board.py) · data `f8a4c3ec`(restock_log.csv) · wb `d6edd1c2`(daily-dashboard.md) · wb `9606ec0c`(pitfalls.md).

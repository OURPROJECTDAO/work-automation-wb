# 2026-06-16 — 데일리 대시보드 품절 알림판 (발주 품절목록 → 재입고 reconcile)

## 무엇
발주 품절목록 상품을 데일리 대시보드 알림판에 자동 등록 → 상품관리 갱신 후 박스재고>0 재입고 시 입고로그 남기고 자동삭제(+수동 1클릭 삭제·로그없음), 미입고면 "MM월DD일부터 N일째 품절" 유지.

## 왜
매일 발주작업이 품절목록을 내는데, 보충 여부를 추적·알림하는 보드가 없었음. 사용자 요청.

## 변경 (코드 — app repo)
- 신규 `core/intelligence/stockout_board.py`(c5d4534) — read/write_board(json)·read/append_log(csv)·seed_from_stockout·reconcile(박스재고>0)·manual_remove·board_to_frame. data repo history/stockout_board.json + restock_log.csv 영속(비-PII).
- 수정 `app/pages/0b_데일리대시보드.py`(425dca9) — 상단 '🚨 품절 알림판' 섹션: reconcile(입고로그+자동삭제)·표(MM월DD일부터 N일째·현재박스재고)·🗑 수동삭제·🔄 다시읽기(cache clear)·입고로그 expander. `_box_stock_lookup`('박스' 컬럼).
- 수정 `app/pages/1_파일처리.py`(2afd28d) — 발주 Phase2 품절목록 생성 시 `_seed_stockout_board` 자동 등록 훅(run/retry 2곳)+import.

## 검증
- 실물 대조: 물류팀_0616.xlsx 품절목록 = 관리코드·상품명·발주수량·현재고(5건). run_phase2가 stockout.columns를 이 친화명으로 rename(코드 확인) → order_stockout_df 컬럼 일치. product_master 5개 품절코드 '박스'(박스재고) 다 음수(-19~-1027) → 양수 전환=깔끔한 재입고 신호 확인. 품절목록 현재고=박스재고−발주수량 검증(-19−39=-58).
- 코드 3종 ast.parse 통과(편집 anchor assert).
- 재입고 기준=박스재고>0(detect_transitions '0이하↔양수' 일치)·seeding=Phase2 전건 자동·수동삭제=로그없음 (사용자 확정).

## 다음 · 상태
- 상태: 배포 커밋 완료. **새 core(stockout_board) 첫 배포 → 알림판 안 보이면 Reboot app 1회.** 실사용(발주→등록·상품관리갱신→재입고 자동삭제) 사용자 확인 대기.
- KB: systemmap daily-dashboard 노드 갱신(품절 알림판 done·meta o)·edge logistics→daily·workflows/daily-dashboard.md 섹션·state·ADR 0024.
- 다음 한 수 = 확장판(추가 데일리 인사이트 — 사용자와 설계).

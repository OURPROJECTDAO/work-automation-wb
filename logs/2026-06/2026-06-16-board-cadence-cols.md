# 2026-06-16 — 품절 알림판에 최근입고/평균주기/입고횟수(1년) 표시

## 무엇
데일리 대시보드 품절 알림판 표에 품절목록 E/F/G(최근입고일·평균매입주기·입고횟수 1년)를 같이 표시. 보기 편하게.

## 변경 (코드)
- `core/intelligence/stockout_board.board_to_frame`(32404e9) — `cadence=None` 인자 추가, 최근입고일·평균매입주기·입고횟수(1년) 3컬럼 병합(NFC 매칭·날짜 YYYY-MM-DD·평균 round·코드 없으면 빈칸).
- `app/pages/0b_데일리대시보드.py`(f8a5c59) — `_buyin_cadence()`(data repo 최근 13개월 파티션·cadence_by_code months=12·ttl30분, now=KST naive) + import `_buy` + board_to_frame에 cadence 주입 + 알림판 표 8컬럼(최근입고·평균주기·입고(1년) 추가)·캡션 갱신.

## 검증
- end-to-end: 최근13개월 buyin cadence(1169코드) + 5 품절코드 board_to_frame → 컬럼 정상 채움. 6월 적재 반영돼 최근입고일 06-08~06-15(31-03-05 3일/140회·31-04-02 5일/79회 등). 코드 없는 항목 빈칸 처리 OK.

## 다음 · 상태
- 상태: 커밋 완료. **core(stockout_board) → Reboot app 1회.** 데일리 대시보드 품절 알림판에서 E/F/G 표시 사용자 확인 대기.
- 성능: 알림판은 매 render마다 buyin cadence 필요 → 최근 13개월만 로드(54파티션 read_all 대신)·ttl30분 캐시. 🔄 버튼=cache clear.
- KB: systemmap daily-dashboard consumes+buyin asset consumer(meta r)·workflows/daily-dashboard.md.

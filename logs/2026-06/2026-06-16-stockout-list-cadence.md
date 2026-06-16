# 2026-06-16 — 품절목록 E/F (최근입고일·평균매입주기, 물류팀 파일)

## 무엇
물류팀 파일 생성(generate_result_xlsx)의 품절목록 시트에 E열 "최근 입고일", F열 "평균매입주기(일)" 추가. 출처=매입현황(buyin) cadence. 대시보드 아님(사용자 명시).

## 왜
발주 담당이 품절 상품의 마지막 입고일·보통 입고주기를 한눈에 보고 발주 판단. "데이터 있잖아"(매입현황 입고일).

## 변경 (코드 — app repo)
- `core/intelligence/purchases.py`(416dfd6) — `cadence_by_code(buyin)` 추가: 실입고(합계액>0&수량>0)·입고일 distinct·관리코드별 {최근입고일, 평균주기(연속 입고일 간격 평균 일), 입고횟수}. 입고 1회면 평균주기 None.
- `core/workflows/logistics_order.py`(4454fa1) — generate_result_xlsx `cadence=None` 인자 + 품절목록 헤더 6열(E 최근입고일·F 평균매입주기(일))·행 렌더(NFC 매칭·날짜 YYYY-MM-DD·평균 round)·border 1..6·E/F 너비. `import unicodedata` 추가.
- `app/pages/1_파일처리.py`(449f5aa) — `_buyin_cadence()`(data repo read_all 캐시 ttl30분) + `import _buy` + `generate_result_xlsx(..., cadence=_buyin_cadence())`.

## 검증
- 실데이터 65,999행(2022-01~2026-05) cadence_by_code → 1800 관리코드. 0616 품절 5건 전부 산출: 39-91-01(19일·83회·~05-18)·39-91(16일·101회)·31-04-02(8일·202회·~05-27)·31-03-02(26일·62회)·31-03-05(4일·364회·~05-29). 합리적.
- 코드 3종 ast.parse 통과(편집 anchor assert).

## 다음 · 상태
- 상태: 배포 커밋 완료. **core(logistics_order·purchases) 수정 → Reboot app 1회.** 발주 실행→물류팀 파일 품절목록 E/F 사용자 확인 대기.
- ⚠️ 최근입고일=적재된 매입현황 기준(~2026-05). 당월 입고는 그 달 매입현황 적재 후 반영.
- KB: systemmap logistics-order consumes+buyin asset consumer·line(meta p)·workflows/logistics-order.md 섹션.

# 2026-06-22 cmm 재고 필터 변경 (재고 0 → 재고 N개 이상)

## 무엇
채널마진모니터(app/pages/6_채널마진모니터.py) 필터 행의 "재고 0" 체크박스를
"재고 N개 이상" 숫자 입력(number_input)으로 교체.

## 왜
사용자 요청 — 재고 0만 보는 토글보다, 임계 개수 이상 재고 상품을 골라보는 게 실용적.

## 변경
- f2 슬롯: only_zero 체크박스 → min_stock = number_input(min 0·value 0·step 1, 0=전체).
- 필터: `if only_zero: 재고==0` → `if min_stock>0: 재고.fillna(-1) >= min_stock`
  (0=무필터·전체 표시 / NaN(미매칭)은 양수 임계에선 자동 제외).
- filter_sig 위젯리셋 키의 only_zero → min_stock 교체(놓쳤다 잡음).

## 검증
ast.parse OK. only_zero 잔존 0(3곳 전부 min_stock 정합: 입력·필터·filter_sig).
커밋 56d1a1e.

## 다음·상태
완료. page-only → 재배포 자동반영·Reboot 불필요. 사용자 실사용 확인 대기.
워크플로우 정본(channel-margin-monitor.md) 미수정 — 필터 디테일은 페이지 레벨이라 불요.
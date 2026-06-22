# 2026-06-22 두뇌④ 3% 하한 — clamp 정정

## 무엇
앞선 3% 하한 구현(hold+hide)을 사용자 의도대로 clamp 방식으로 정정.

## 사용자 정정
"3%까진 내리되 그 밑은 막기가 내가 의도한 부분. 이미 3%인 거는 어차피 인하를 할 수가
없으니 결정쪽에서 빼기."
→ 권장이 3% 미만이면 (a) 현재>3%면 3%까지만 내려 그대로 노출(인하 살림), (b) 이미 3% 이하면
인하 불가라 작업목록 제외. (앞 구현은 (a)도 통째 유지·숨김이라 인하 기회 손실 → 정정)

## 변경
- core margin_optimizer.py recommend_code 하한 블록:
  if target<0.03: m>0.03 → target=0.03(액션/플래그 유지·사유 부기) / else → A_HOLD,target=m(제외).
  커밋 (정정).
- page 13 설명서 + workflows/margin-optimizer.md §23·안전장치·§1 clamp 문구.

## 검증
ast 2파일 OK. 합성 6케이스:
- 회전 360일 쿠팡 4.5%→(2.5%)→clamp 3.0 노출 ✓
- ⑦ 나들0.5% 알리 5%→(2.75%)→clamp 3.0 내림 노출 ✓
- 현재 2% → 유지·작업목록 제외 ✓
- m3.1%→3%(Δ0.1%p) → MIN_DELTA 미세컷 유지·숨김 ✓
- ⑦ 8%→4.2%(≥3%·Δ3.75%p) → 🔴 노출 ✓
- 정상 11%→9% → 노출 ✓

## 다음·상태
완료. ⚠️ core 변경 → Reboot app 1회.
정본 workflows/margin-optimizer.md §23(clamp). 잔여(기존)=cmm prefill·margin_floor 원가하한 클램프.
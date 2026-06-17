# 2026-06-17 — (fix) 권장가 항상 표시(매입가 기준 역산, listing 불요)

## 무엇 / 왜
데일리 이상치 표에서 listing 미등재 상품(예 ESM 일부)의 권장가가 None. 사용자 지적: 권장가는 **매입가(product_master) 기준 역산**이므로 listing 최신성과 무관하게 어떤 경우에도 표시돼야 함(현재가만 listing 의존).

## 변경 (app repo, page-only)
- `app/pages/0b_데일리대시보드.py`:
  - `_cmm_refs()`(cached cmm.load_references) + `_reco_from_master(channel, code, refs, bdict)` — cmm compute 권장가 공식 그대로: `((base×N + 2700)/(1−기준마진) − 배송비×0.967)/(1−수수료)` 100원 올림. **N=1·배송비=채널 ship_fee_const(기본0) 추정**(배민 등 상품별 수수료는 commission_add+0.045 대략치). resolve_code 미매칭/기준 미설정이면 None.
  - `_reco_lookup(pairs)` — listing에 권장가 있으면 그 값(실 N·실 배송비=가격변경 시트와 동일), 없으면 `_reco_from_master` 폴백. 현재가는 listing만(미등재 None).
  - 표 호출을 channels set → (채널,관리코드) pairs로, 캡션 정정.

## 검증
- 폴백 공식 = cmm compute(L650-652) 바이트 동일(매입가=base×1, ship=real_ship 2700, settle 0.967, rate 1−comm). listing N=1 상품은 폴백==정확값.
- listing 있는 행=정확(실 N), 없는 행=매입가 기준 추정으로 항상 표시. ast.parse 통과(anchor assert ×3).

## 다음 · 상태
- 상태: 커밋 완료. page-only → 재배포 후 반영. ESM 등 미등재 행도 권장가 표시 확인 대기.
- 주의: 가격변경 **시트 생성**은 여전히 listing 필요(미등재 상품은 변경 대상 행 없음). 권장가는 표시·참고용. N>1 합포 listing 상품이 미등재면 폴백 N=1이라 실제 팩가와 차이 가능(추정).

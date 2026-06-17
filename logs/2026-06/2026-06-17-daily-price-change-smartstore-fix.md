# 2026-06-17 — (fix) 데일리 가격변경 연결: 스마트스토어 미지원 오판 수정

## 무엇 / 왜
데일리 이상치에서 스마트스토어 행 선택 시 "스마트스토어는 가격변경 양식이 아직 없습니다" 오표시(사용자 보고·스크린샷). 스마트스토어는 **price_form 키가 없고** cmm에서 **else 분기(bulk·원본 filter)**로 처리되는데, `_do_price_change`가 `if not pf`(price_form 없음)를 미지원으로 잘못 판단.

## 변경 (app repo, page-only)
- `app/pages/0b_데일리대시보드.py`:
  - 신규 `_supports_price_change(cfg)` — `price_form` 있으면 True, 없어도 **cols에 '즉시할인' 있고 consolidate 아니면**(=스마트스토어형 bulk) True. 알리(consolidate·cols/price_form 없음)만 False.
  - `_do_price_change`: 가드를 `if not pf` → `if not _supports_price_change(cfg)`.
  - `_gen_price_form`: `mode = (pf or {}).get("mode")` (pf=None 스마트스토어 → else bulk 분기 정상 진입, AttributeError 방지).

## 검증
- CHANNEL_CONFIG 대조: 스마트스토어 cols에 '즉시할인'(58) 보유·price_form 없음·consolidate 없음 → 지원 True. 알리 consolidate·cols 없음 → False. 식봄/캐시노트/배민/쿠팡/올웨이즈/ESM price_form → True.
- 스마트스토어 dispatch=else → compute_new_prices + build_bulk_price_xlsx(raw 필요, '전체 교체'). ast.parse 통과.

## 다음 · 상태
- 상태: 커밋 완료. page-only → 재배포 후 반영(Reboot 불요). 스마트스토어 선택→bulk 시트(raw listing_smartstore.xlsx 필요) 사용자 확인 대기.
- 참고: ESM 등 일부 행 현재가/권장가 None = 그 관리코드가 채널 저장 listing에 없음(미등재/갱신 필요)·미매칭 — 버그 아님(listing 최신화로 해소).

# 2026-06-11 channel-margin-monitor: 캐시노트 할인전단가(H) 가짜 정가 생성

## 무엇
캐시노트 가격변경 양식 H(할인 전 단가)를 listing 정가 보존이 아니라 **무늬용 가짜 정가로 매번 생성**: 권장가 × (1 + 랜덤 0.20~0.30), 100원 반올림, 항상 판매가 초과. 채널 옵션 `jeong_fake`.

## 왜 (사용자 설명)
- 캐시노트 할인 전 단가(O/H열)는 **가짜(무늬) 가격** — 실제 판매가는 판매 단가(N/G). H는 할인율(%) 표기용 취소선 가격일 뿐.
- 모니터/마진/권장가는 **판매단가(N)만** 사용(확인됨 — 정가는 마진식에 미포함). 따라서 가격변경 시 H는 보존이 아니라 권장가 기준으로 그럴듯한 할인 보이게 새로 생성.
- **일부 채널만** 이렇게 — 식봄은 실제 정가 유지.

## 변경 (work-automation-app)
- `core/workflows/channel_margin_monitor.py` (→03fb7e5)
  - `import random`.
  - 캐시노트 price_form에 `jeong_fake{min_pct0.20,max_pct0.30,round100}`.
  - `build_append_items`: jeong_field 처리에 분기 — jeong_fake 있으면 `round(price×(1+uniform(min,max))/unit)×unit`(≤price면 price+unit), 없으면 기존 max(정가,price) 보존(식봄).

## 검증
- 표본 8건: H 모두 G의 +20~30% 범위·100원 단위·>G, 행마다 % 상이 ✅.
- 식봄 회귀: jeong_fake 없음 → D(정가)=max(실제정가,판매가) 보존(12000) ✅.
- ast.parse OK.

## 다음 / 상태
- 운영 가능. ⚠️ **core 수정 → Reboot app 1회**. (앞서 '전체 교체'로 OFR/SKU 채운 listing과 함께 사용.)
- 향후 다른 채널도 할인전단가 무늬면 jeong_fake만 추가하면 됨.

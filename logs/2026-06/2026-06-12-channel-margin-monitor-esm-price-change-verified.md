# 2026-06-12 channel-margin-monitor: ESM 가격변경 실업로드 성공 확인

## 무엇
ESM 가격변경 양식('(ESM)양식', B=사이트상품번호·C=권장가)을 ESM Plus에 실제 업로드 → **성공 사용자 확인**.

## 왜
직전 구현(logs/2026-06-12-channel-margin-monitor-esm-price-change) 시 미해결로 남긴 "ESM 실업로드 inlineStr 허용 여부 미검증" 항목 종결.

## 결과
- openpyxl `build_price_form_append` 저장(inlineStr)을 **ESM Plus 업로더가 허용** — 쿠팡식 네이티브 zip 수술 불요.
- 패턴 확인: 식봄·캐시노트·배민·올웨이즈와 동일(openpyxl append 저장 정상). 엄격 업로더 거부는 **쿠팡만** 예외(전역 pitfalls 그대로 유효).

## 변경
- 코드 변경 없음(검증만). KB: workflows/channel-margin-monitor.md·state.md 의 "실업로드 미검증" → "성공 사용자 확인(2026-06-12)"로 정리(인라인 반영 완료).

## 다음·상태
- ESM = 모니터+가격변경 완전 동작 확정. 8채널 모니터 / 7채널 가격변경(알리만 가격변경 미구현).
- 향후: 알리 가격변경(다중시트 양식 별도) or 추가 채널.

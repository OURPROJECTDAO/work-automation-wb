# 2026-06-22 전 페이지 본문 폭 풀기(full-width 디폴트)

## 무엇/왜
`core/ui.py` 전역 CSS `.block-container{max-width:1180px}`가 layout="wide"인데도 전 페이지 본문을 1180px로 캡 → 사용자: 전 페이지 디폴트를 양옆 꽉차게. `max-width:1180px → none`(레이아웃 wide 풀폭, 스트림릿 기본 좌우 패딩만 유지).

## 변경
- `core/ui.py` (28행): `.block-container ... max-width: 1180px;` → `max-width: none;`. 커밋 5e11c40.
- `app/pages/0b_데일리대시보드.py`: 지난번 데일리 전용 page-scoped override(`<style>.block-container{max-width:none}</style>`) 제거 — 전역화로 중복. 커밋 f9141d4.

## 다음·상태
- ★ **core/ui.py = core 모듈 → Reboot app 1회 필요**(inject_css 문자열 sys.modules 캐시). Reboot 전엔 폭 변화 미반영.
- 사용자 체감 확인 대기. 텍스트 위주 페이지(지도로드맵 등)가 너무 휑하면 특정 페이지만 캡 재부여 가능(요청 시).

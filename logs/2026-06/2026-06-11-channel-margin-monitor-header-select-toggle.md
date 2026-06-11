# 2026-06-11 channel-margin-monitor — 전체선택/해제 버튼 제거(헤더 체크박스로 통합)

## 무엇
선택 영역의 '전체 선택'/'전체 해제' 버튼 2개 제거. st.data_editor 선택(CheckboxColumn) **컬럼 헤더 체크박스가 이미 전체 선택/해제** 기능 → 중복이라 버튼 삭제(사용자 지적).

## 변경 (page만, Reboot 불필요)
- s1/s2 버튼 + `cmm_nonce` 세션/리시드 로직 제거. editor key=`cmm_ed_{key}_{filter_sig}`(nonce 제거).
- 헤더 체크박스 토글 결과는 기존 reconciliation(`checked_now = edited[선택]==True` → `sel = (sel-view_pids)|checked_now`)이 그대로 흡수 → 화면 밖 선택 유지·필터 넘어 지속 동일.
- ast OK, 커밋 200.

## 다음 / 상태
- page-only 자동 반영. 헤더 체크박스로 현재 필터/검색 결과 전체 선택·해제.

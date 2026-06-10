# 2026-06-10 대시보드 — 그룹 거래처 전체 선택/해제 토글

## 무엇
전체 선택 버튼을 토글로: 누를 때마다 전체 선택 ↔ 전체 해제. 라벨은 다음 동작 표시(전체 선택 상태면 '전체 해제', 반대면 '전체 선택').

## 왜 / 함정
data_editor는 키에 편집상태(edited_rows)를 누적 → 단순 `pop(key)`+rerun은 입력 디폴트(포함=True)로만 복원돼 '전체 해제' 불가. 또 토글 후 stale edits가 다음 토글을 오염.

## 변경 (app/pages/3_대시보드.py, commit 위)
- `st.session_state['dash_store_bulk']`(True/False, 초기 True) + `dash_store_ver`(키 버스터).
- 버튼 클릭 → bulk 반전 + ver+1 + rerun. 입력 DF `포함=bulk`로 세팅, data_editor 키=`dash_store_pick_{ver}` → 매 토글 fresh 재초기화(stale edits 폐기).
- 토글 사이 개별 체크/해제는 해당 ver 키에 보존, 입력 bulk 위에 적용.

## 검증
- ast.parse OK. 페이지 .py 자동반영.

## 다음 / 상태
- 완료. 잔여 점진: 물류량 노출 · 이익/물류량 콤보.

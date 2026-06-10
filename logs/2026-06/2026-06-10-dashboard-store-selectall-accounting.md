# 2026-06-10 대시보드 — 그룹 거래처 전체선택 버튼 + 매출열 accounting 포맷

## 무엇
📊 대시보드 '그룹 내 거래처 선택' 표에 ①전체 선택 버튼 ②매출 열 천단위 콤마(accounting) 추가.

## 변경 (app/pages/3_대시보드.py, commit 4a185efd)
- 전체 선택: data_editor(key=dash_store_pick) 위에 버튼 — 클릭 시 `st.session_state.pop('dash_store_pick')` + `st.rerun()` → 편집상태 초기화로 전 행 포함=True 복원(입력 DF 디폴트가 True).
- 매출 열 `format="%d"` → `format="accounting"`(콤마 구분). 같은 표 거래처 열 다음 1곳만 변경(👥/🏷 탭의 동일 매출열은 유지).

## 검증
- ast.parse OK. 페이지 .py라 자동반영(Reboot 불필요). requirements streamlit>=1.36, 배포본 최신이라 accounting 지원(localized 이미 사용 중).

## 다음 / 상태
- 완료. (전체 해제 버튼은 미추가 — 요청 시 대칭 추가 가능.)
- 대시보드 점진 후보 잔여: 물류량(수량÷박스내품) 노출 · 이익/물류량 콤보.

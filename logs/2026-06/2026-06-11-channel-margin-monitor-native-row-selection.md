# 2026-06-11 channel-margin-monitor — 선택 UI를 st.dataframe 네이티브 다중행선택으로 교체

## 무엇
표 선택을 **st.data_editor + CheckboxColumn + 수동 reconciliation** → **st.dataframe 네이티브 다중행 선택**(`on_select="rerun"`, `selection_mode="multi-row"`)으로 교체.

## 왜
- data_editor의 CheckboxColumn **헤더 체크박스가 (배포 Streamlit에서) 전체선택을 안 함** + 수동 reconciliation이 개별 체크까지 꼬여 선택 자체가 작동 안 함(사용자 보고).
- st.dataframe 다중행 선택은 **헤더 전체선택 체크박스 + 개별 선택을 네이티브 제공**(공식 패턴, ≥1.35). 읽기전용이라 edit-state 충돌 없음.

## 변경 (page만, Reboot 불필요)
- `event = st.dataframe(view_reset[DISPLAY], on_select="rerun", selection_mode="multi-row", key=f"cmm_df_{key}_{filter_sig}", column_config=...)`. `sel_rows = event.selection.rows`(위치 인덱스) → `sel_pids = view_reset.iloc[sel_rows]["상품번호"]`.
- '선택' 데이터컬럼/CheckboxColumn·전체선택 버튼·nonce·세션 선택집합·reconciliation 전부 제거. 다운스트림 `sel`→`sel_pids`.
- 선택은 **현재 필터/검색 화면 기준**(key에 filter_sig 포함 → 필터·검색 바뀌면 리셋). 화면 밖 누적 지속은 포기(단순·안정 우선).

## 검증
- API 공식 확인: `st.dataframe(on_select, selection_mode="multi-row")` + `event.selection.rows`(위치, `.iloc`로 조회). ast OK, 커밋 200.

## 전용 함정 / 상태
- ⚠️ **st.dataframe 다중행 선택은 사용자가 컬럼 정렬하면 선택 리셋됨**(공식 경고). 정렬 후엔 재선택 필요. 필터링은 우리 검색/필터 사용 권장.
- data_editor CheckboxColumn 헤더 체크박스 전체선택은 신뢰 불가 → 다중행선택엔 st.dataframe 네이티브가 정답.
- page-only 자동 반영.

# 2026-06-12 channel-margin-monitor: 표 선택 인덱스 stale IndexError 수정

## 무엇
모니터 페이지에서 가격변경 중 `IndexError: positional indexers are out-of-bounds` 크래시(6_채널마진모니터.py line 361, `view_reset.iloc[sel_rows]`).

## 원인
`st.dataframe(on_select="rerun", selection_mode="multi-row")`의 `event.selection.rows`는 표의 **위치 인덱스**. 위젯 key(`filter_sig`)가 필터 입력값만 반영하고 **행 수를 안 봐서**, 선택해둔 상태로 rerun이 일어나 필터 결과 행 수가 줄면(기준마진율 편집으로 '미달만' 행 감소·데이터 갱신 등) 위젯이 옛 선택 위치를 복원 → 지금 표에 그 행이 없어 `iloc` 범위 초과. 가격 데이터와 무관(선택 상태 ↔ 데이터 불일치).

## 변경 (page만)
- `app/pages/6_채널마진모니터.py`:
  - 선택 인덱스 클램프: `sel_rows = [i for i in event.selection.rows if 0 <= i < len(view_reset)]`.
  - `filter_sig`에 `len(view_reset)` 포함 → 행 수 변동 시 위젯 key 변경(어긋난 선택 복원 방지).

## 검증
- ast.parse OK. 페이지 변경 → 자동 재배포로 반영(core 무변경, Reboot 불요).

## 다음·상태
- 전역 패턴 기록: patterns.md(Streamlit). 동일 패턴 쓰는 다른 페이지(대시보드 등)도 같은 클램프 권장.
- 미검증: 재배포 후 사용자 재현 시나리오(선택→필터/편집→정상) 확인.

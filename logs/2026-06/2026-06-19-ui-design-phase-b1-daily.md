# 2026-06-19 · UI Phase B-1 (데일리 대시보드 톤)

## 무엇
Phase B 첫 페이지 = 데일리 대시보드. 패턴 세터로 톤 확정.

## 변경 (app repo)
- `core/ui.py` 확장 — `section_head(title, icon, tag)` 추가(인디고 액센트 바 + 제목 + 선택 mono 태그) + 섹션헤드/eyebrow CSS + JetBrains Mono @import. (40fd855)
- `0b_데일리대시보드.py` — `from core import ui`; `st.title`→`ui.page_header(icon="📅")`; 4개 섹션 `st.subheader`→`ui.section_head`(품절 알림판·신규 업로드 대상·가격 변동 알림·당일 마진 점검) + 중복 `st.divider()` 3개 제거. (3355a94)

## 보존(의도)
- 이상치 표 = `on_select` 체크박스 선택형(인터랙티브) → **네이티브 유지**(st.dataframe 캔버스라 CSS 불가). 가격변경 시트 다운로드 로직 무변경.
- st.metric 4종 = Phase A 전역 CSS로 이미 카드화 → 그대로.
- 가격변동/신규업로드 표 = 기존 Styler 유지.

## 검증
- 6개 치환 전건 count==1 + ast.parse PASS(core/ui.py·daily).

## 다음 · 상태
- ⚠️ `section_head` **신규 함수**라 **Reboot 1회** 필요(이후 같은 헬퍼 쓰는 Phase B 페이지는 page-only·Reboot 불요). daily는 page-only지만 새 헬퍼 의존 → 이번 Reboot에 포함.
- 사용자 체감 확인 대기. OK면 같은 패턴(page_header+section_head)으로 두뇌④·채널마진모니터·상품360 배치 적용.
- 더 pop 원하면 당일 마진 4메트릭 → ui.kpi_row(인디고 카드·mono)로 승급 가능(후속).

## 후속(2026-06-19)
- 품절 알림판(수제 st.columns 표) 행 구분선 추가 — keyed 컨테이너 `st.container(key="sb_board")` + 스코프 CSS(`.st-key-sb_board [data-testid="stHorizontalBlock"]` border-bottom #ECEEF2). 다른 표·컬럼 무영향. 데이터/🗑/로직 무변경. page-only(Reboot 불요). 커밋 62fc5cb.

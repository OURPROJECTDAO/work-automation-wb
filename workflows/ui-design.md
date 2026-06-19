# ui-design (전 페이지 UI 디자인) — 워크플로우

> 횡단 작업(파이프라인 노드 아님). 전 페이지 + 사이드바 + 랜딩의 시각 일관성·프로페셔널화.
> 정본 코드 = `.streamlit/config.toml`(전역 테마) + `core/ui.py`(전역 CSS·헬퍼).

## 요약
stock Streamlit("딱 봐도 Streamlit") → 절제된 인디고 액센트 + Pretendard + 카드/핀필 폴리시.
원칙(공식 가이드 일치): **색·폰트·라운드·테두리 = config.toml**(전역 자동 상속), **CSS는 보강만**.

## 전역이 되는 구조 (per-page 복붙 아님)
- `config.toml [theme]` → 19개 전 페이지 + 사이드바 자동 상속. 손댈 페이지 0.
- `streamlit_app.py`가 `pg.run()` 직전 `inject_css()` 1회 → 엔트리는 매 페이지 로드마다
  먼저 실행 → **CSS도 한 곳에서 전 페이지 적용**.
- 컴포넌트 헬퍼(`page_header`·`kpi_row`·`status_pill`·`delta_html`)는 그 패턴 쓰는 페이지에서 선택 호출.

## 디자인 토큰 (config.toml ↔ core/ui.py 동일 유지)
- primary(액센트) `#3B5BDB` 인디고 · 배경 `#FBFBFD` · 사이드바/보조 `#F4F6F9` · 텍스트 `#181B22` · 테두리 `#E6E8EC` · radius `0.5rem`
- 폰트 = Pretendard (`font = "Pretendard:<jsDelivr CDN css>"`)
- 시맨틱(한국식): 인상/상승 = 빨강 `#E03131` `.ui-up ▲` · 인하/하락 = 파랑 `#1971C2` `.ui-down ▼`
- 상태 🟢`#2F9E44` 🟡`#F08C00` 🔴`#E03131` → `.ui-pill g|y|r`

## 단계 계획
- **Phase 0** 토큰 확정 (목업 출발점·인디고 확정) — ✅
- **Phase A** 기반 ✅ **(2026-06-19 라이브)** — config.toml 테마 확장 + `core/ui.py`(전역 CSS·헬퍼) + 진입점 `inject_css` + 사이드바 브랜드 + 네비 그룹명("분석·지능"). 커밋 config 168e203·ui e166707·app 6006b28.
- **Phase B** 페이지 폴리시(헬퍼 적용, 우선순위순) — 데일리 대시보드 → 기준마진율 최적화 → 채널마진모니터 → 상품360 → 마진침식·재고지능·가격AB → 유틸 페이지(헤더/버튼/메시지 일관). **미착수.**
- **Phase C** 랜딩 = 지도·로드맵 강화(상단 "오늘 할 일" 요약 + 점프). 별도 홈 신설 안 함. **미착수.**
- **Phase D** copy/빈화면/에러 보이스 일관·라이트 QA·KB 마감. **미착수.**

## 전용 함정 (Streamlit CSS 한계)
- **st.dataframe = 캔버스(glide-data-grid)** → 내부 셀/헤더는 CSS로 못 바꿈. 색/핀필 표가 필요하면
  ① Styler + `st.table`(HTML·스타일 가능, 상호작용 없음) ② HTML 렌더(조회전용) ③ 테마 색만 자동 추종.
  data_editor/선택 상호작용이 필요한 표는 네이티브 유지 + 컬럼 `column_config`로 최선.
- CSS 셀렉터는 `data-testid`(stMetric/stMetricValue/stSidebar/stTabs) 우선 — 클래스명보다 안정. 빗나가도 무해하게 degrade.
- 커스텀 컴포넌트(카드·핀필·델타)는 `st.markdown(unsafe_allow_html=True)` HTML로 직접 렌더 = DOM 안 싸움.
- `[[theme.fontFaces]]`/`font` URL 변경은 **서버 재시작(Reboot) 필요**(색은 라이브 반영).
- Plotly/Altair 차트는 테마 색 자동 추종 — Phase B에서 실확인.

## 검증/재배포
- config.toml + core/ui.py(신규 import) 둘 다 전역 → **재배포(1~2분) + Reboot 1회**(폰트+새 코어).
- 되돌리기: 테마=1파일 되돌림, CSS=가산식(헬퍼 미사용 시 무영향).
- 체크 매트릭스: 버튼(primary 대비)·st.metric 카드·탭·dataframe(테마색)·차트·사이드바·라이트.

## 관련 로그/결정
- ADR 0028 (UI 디자인 방향·전역 2파일 구조)
- logs/2026-06/2026-06-19-ui-design-phase-a.md

# ADR 0028 — 전 페이지 UI 디자인 방향 (테마 + 헬퍼, 전역 2파일)

날짜: 2026-06-19
상태: 채택 (Phase A 라이브)

## 맥락
앱이 기능(두뇌①~④·8채널·시장지능)은 풍부하나 외형이 100% stock Streamlit("딱 봐도 Streamlit"). 사용자: 편의성 말고 디자인면에서 프로페셔널하게. 요구 = **전 페이지 + 랜딩 일관 적용**.

## 결정
1. **색·폰트·라운드·테두리는 `.streamlit/config.toml [theme]`** (공식 가이드 일치 — native theming은 안 깨지고 유지보수 쉬움). CSS는 보강만.
2. **전역 2파일 구조**: config.toml(테마, 19페이지 자동 상속) + `core/ui.py`(전역 CSS·헬퍼). 진입점 `streamlit_app.py`가 `pg.run()` 직전 `inject_css()` 1회 → CSS도 전 페이지 1곳 적용. per-page 복붙 안 함.
3. **액센트 = 인디고 `#3B5BDB`**(현 matplotlib 기본 `#1f77b4`의 다듬은 버전). 폰트 = Pretendard(CDN). 한국식 ▲빨강 ▼파랑·🟢🟡🔴 핀필.
4. **랜딩 = 지도·로드맵 강화**(별도 홈 신설 안 함 — 중복 방지).
5. 단계: Phase A 기반(테마+헬퍼+로고) → B 페이지 폴리시 → C 랜딩 → D 마감/QA.

## 대안·기각
- **CSS로 테마**(색/폰트까지) → 기각: Streamlit 업데이트에 깨짐·유지보수 비용. config.toml이 정석.
- **완전 커스텀 레이아웃/애니메이션** → 기각: Streamlit 천장 밖(커스텀 컴포넌트/프레임워크 교체). 내부 운영툴엔 과투자.
- **새 클러스터로 systemmap 노드화** → 기각: UI는 횡단(파이프라인 노드 아님) + 렌더러 enum 위험. systemmap `backlog`에 횡단 항목으로 기재.

## 결과
- 되돌리기 쉬움(테마 1파일·CSS 가산식). 재배포+Reboot 1회(폰트·새 코어).
- 함정: st.dataframe=캔버스 → CSS 불가(Styler/HTML 우회). workflows/ui-design.md §전용 함정.

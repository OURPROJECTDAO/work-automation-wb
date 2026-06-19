# 2026-06-19 · UI 디자인 Phase A (전역 테마 + 헬퍼 + 로고)

## 무엇
stock Streamlit → 프로페셔널 외형 1단계. 전 페이지·사이드바·랜딩 일괄.

## 왜
기능은 풍부한데 외형이 공장 기본값. 사용자 요청 = 편의성 말고 디자인, 전 범위. 진행 방향=Phase A 먼저 박고 체감(사용자 선택)·액센트=인디고(목업 그대로).

## 변경 (app repo)
- `.streamlit/config.toml` [theme] 확장 — base light·primary `#3B5BDB`(인디고)·배경 `#FBFBFD`·보조 `#F4F6F9`·텍스트 `#181B22`·테두리 `#E6E8EC`·radius `0.5rem`·**font Pretendard(jsDelivr CDN)**. (168e203)
- `core/ui.py` 신설 — `inject_css()`(전역 CSS: st.metric→카드·버튼/탭/간격 폴리시·브랜드·KPI카드·핀필·▲▼) + 헬퍼 `page_header`·`kpi_row`·`status_pill`·`delta_html`. 토큰 config와 동일. (e166707)
- `app/streamlit_app.py` — `inject_css()` 1회 + 사이드바 브랜드(.ui-brand) + 네비 마지막 그룹명 `" "`→`"분석·지능"`. (6006b28)

## 검증
- `ast.parse` core/ui.py·streamlit_app.py PASS. 헬퍼 문자열 스모크(status_pill/delta_html) 출력 정상.
- 전역 구조: 엔트리가 매 로드 먼저 실행 → inject_css 전 페이지 적용. 테마는 config로 자동 상속.

## 다음 · 상태
- ⚠️ **재배포(1~2분) + Reboot 1회** 필요(폰트 변경 + 신규 코어 import). **사용자 체감 확인 대기.**
- 확인 포인트: 사이드바 브랜드·인디고 버튼·Pretendard 적용·st.metric 카드화·"분석·지능" 그룹명.
- 함정 기록(workflows/ui-design.md): st.dataframe=캔버스라 CSS 불가 → Phase B 색표는 Styler/HTML 우회.
- 다음 = 체감 OK면 **Phase B**(데일리 대시보드부터 헬퍼 적용). 색/방향 코멘트 있으면 Phase A 미세조정.

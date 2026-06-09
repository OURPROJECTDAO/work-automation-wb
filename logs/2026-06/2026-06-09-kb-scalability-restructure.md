# 2026-06-09 KB 확장성 개선 — patterns 분리 · pitfalls 슬림 · state 상태 단일원천

## 무엇
에이전트 관점 점검에서 나온 3개 약점 중 나머지 2개 적용(manifest는 직전 로그). pitfalls를 프로토콜/환경(상시) vs 상황별(patterns)로 이분화, state 인덱스 상태를 통제어휘+포인터로 슬림. ADR 0010.

## 왜
상시읽기 세트(캐치업 22KB) 중 pitfalls 11.2KB가 유일하게 무한정 큼. Streamlit/Excel 상황 한정 항목은 매 세션 필요치 않음. 상태 3중 기록은 드리프트원(ESM 카테고리표 사례).

## 변경
- patterns.md 신설: pitfalls의 Streamlit/앱(서버시각KST·nav·st.stop·download_button rerun·dataframe정렬·data_editor) + Excel포맷(마켓 HTML-.xls·OLE2 CompDoc·암호 xlsx) 섹션을 ##→### 강등해 두 그룹으로 이전.
- pitfalls.md 슬림: GitHub API·인코딩·Drive·보안·작업규율·한국어/NFC만 유지 + 상단에 patterns/manifest 포인터.
- state.md 워크플로우 인덱스: 상태=통제어휘(운영중/진행중/이슈/개념doc)+doc링크. 상세 상태는 각 doc 단일 소유.
- INDEX.md 파일맵에 patterns.md 등록, pitfalls 설명 갱신.

## 검증
- pitfalls 섹션 분할은 ## 헤더 기준 프로그램적 라우팅(재타이핑 0). keep/→st/→xl 분류 출력 확인.
- 세 파일 재조회로 반영 확인(이 로그 후).

## 다음 / 상태
- 신규 교훈 라우팅 규율: 프로토콜/환경→pitfalls · 앱/포맷 거동→patterns · 자산연결→manifest · 워크플로우 전용→workflows.
- 점검 3제안(manifest·patterns·state) 모두 적용 완료.

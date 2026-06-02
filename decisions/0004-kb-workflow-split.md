# 0004 — KB 구조 재편: 워크플로우별 파일 분리

## 맥락
세션마다 캐치업으로 INDEX + state + pitfalls + roadmap 4개를 항상 읽는다.
이 중 pitfalls.md·state.md가 워크플로우 추가마다 단조 증가하는 구조였다.
- pitfalls.md에 전역 함정(API/인코딩/Drive/보안/Streamlit)과 워크플로우 전용 함정(VBA 버그·정렬·온누리·발주서출력)이 섞여 있었음.
- state.md의 "완료 Phase"가 워크플로우별 상세를 누적.
업무의 1/10 미만 이관 상태(워크플로우 ~20개+ 예상)에서 그대로 두면, 매 세션 무관한 함정 N-1개를 읽고 1개를 찾는 신호 대 잡음 악화.
로그(logs/)는 이미 날짜 폴더 + append-only + drill-down이라 확장성 문제 없음 — 병목은 "항상 읽는 파일"이었다.

## 검토한 대안
- A. 현행 유지: 단순하나 항상-읽기 셋이 선형 증가.
- B. 워크플로우별 파일 분리(workflows/<name>.md): 항상-읽기 셋 일정, 작업 시 1개 추가 읽기.
- C. 전역 함정까지 잘게 쪼개기(github.md·encoding.md…): 과설계. 전역은 천천히 plateau.

## 결정 (B)
- workflows/<name>.md 신설: 요약 · 핵심 로직/수식 · 전용 함정 · 골든/fixture 위치 · 관련 로그 링크.
- pitfalls.md = 전역/공통만. (마켓 .xls·한국어 NFC 등 여러 업무 공통 데이터-포맷 함정은 전역 유지.)
- state.md = 슬림 워크플로우 인덱스(이름·Phase·한 줄 상태·파일 링크) + 인프라 + 막힌 것.
- INDEX.md 읽기/쓰기 규칙 갱신 + 부트로더 프롬프트 갱신(캐치업에 "건드릴 workflows/<name>.md 추가 읽기", 쓰기에 "전용 지식은 workflows/로").

## 근거
- 분리 비용이 가장 싼 시점(워크플로우 2~3개). 15개에서 하면 비싸고 이미 아픔.
- 항상-읽기 셋을 워크플로우 수와 무관하게 일정화 → 토큰·신호대잡음 둘 다 개선.
- 에이전트 인계 시 해당 업무 파일 1개만 읽으면 됨.

## 결과 / 영향
- 마이그레이션: openmarket-merge / onnuri-order / logistics-order 3개 파일 생성, pitfalls·state 재작성, roadmap·INDEX 갱신.
- 워크플로우 전용 함정 3블록(VBA FasterCopyRows·상품명 줄바꿈·합포 정렬 → openmarket / 온누리 / 발주서출력)을 각 파일로 이동. 전역 함정은 손실 없이 보존.
- 신규 워크플로우 추가 규칙: workflows/<name>.md 생성 + state 인덱스 한 줄.

_2026-06-02_

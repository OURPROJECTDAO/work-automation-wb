# 로그: KB 구조 재편 — 워크플로우별 파일 분리

## 무엇
세션 캐치업(항상 읽기) 부하를 워크플로우 수와 무관하게 일정화하기 위해 KB를 재구조화.

## 왜
업무 1/10 미만 이관 상태에서 pitfalls.md·state.md가 워크플로우 추가마다 선형 증가.
전역 함정과 전용 함정이 섞여 매 세션 무관한 내용을 다 읽는 신호 대 잡음 악화 예상.
분리가 가장 싼 시점(워크플로우 2~3개)에 선제 정리. (decisions/0004)

## 변경 (KB repo)
- 신규: workflows/openmarket-merge.md, workflows/onnuri-order.md, workflows/logistics-order.md.
  - 각 파일 = 요약 · 핵심 로직/수식 · 전용 함정 · 골든/fixture 위치 · 관련 로그 링크.
- pitfalls.md 재작성: 전역/공통만 남김(GitHub API·인코딩·Drive·보안·작업규율·한국어·마켓 .xls·Streamlit). 워크플로우 전용 3블록(VBA FasterCopyRows·상품명 줄바꿈·합포 정렬, 온누리, 발주서출력) 제거 → workflows/로 이동.
- state.md 재작성: 슬림 워크플로우 인덱스(표) + 인프라 + 막힌 것 + 다음 한 수.
- INDEX.md 갱신: 파일 지도에 workflows/ 추가, 읽기/쓰기 규칙 갱신.
- roadmap.md 갱신: "KB 구조 확장성" 나중 → 완료 이동.
- decisions/0004-kb-workflow-split.md 신규.

## 검증
- 전역 함정 8개 섹션 전부 pitfalls.md에 보존(손실 없음).
- 전용 함정: openmarket 3블록 / 온누리 / 발주서출력 → 각 workflows 파일에 1:1 이전.
- 재읽기로 6개 파일 내용 대조 예정(쓰기 후).

## 다음·상태
- 부트로더 프롬프트 갱신본을 사용자에게 전달 → 사용자가 프로젝트 지식 프롬프트 교체.
  (캐치업: "건드릴 workflows/<name>.md 1개 추가 읽기" / 종료: "전용 지식은 workflows/<name>.md, 신규 워크플로우는 파일 생성 + state 인덱스 한 줄".)
- 기능 코드(work-automation-app) 변경 없음. KB-only 재구성.

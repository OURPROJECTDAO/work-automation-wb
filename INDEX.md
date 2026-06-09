# 업무 자동화 프로젝트 — KB INDEX

## 이 프로젝트
회사 발주 업무를 엑셀 템플릿 + 정제 파이프라인(현 VBA → 점진 Python 이관)으로 처리하는 시스템을 자동화·발전시키는 프로젝트.
- 기억(KB) 저장소 = GitHub `OURPROJECTDAO/work-automation-wb` (main, 고정 파일명).
- 코드 저장소 = GitHub `OURPROJECTDAO/work-automation-app` (main, public).
- 엑셀 작업물(템플릿/원본/정제본) = Google Drive `업무자동화-KB/templates·inputs·outputs`.

## 파일 지도 (고정 경로 — 제자리 갱신)
- INDEX.md — 이 맵 + 읽기/쓰기 규칙
- state.md — 현재 상태 + **워크플로우 인덱스** (작게, 항상 읽음)
- pitfalls.md — **전역/공통** 함정만 (작업 전 필독, 항상 읽음)
- roadmap.md — 백로그 / 우선순위 (항상 읽음)
- plan.md — 구현 청사진 (아키텍처 + 단계별 계획, 필요 시)
- **workflows/<name>.md — 워크플로우별 지식**(요약·핵심로직/수식·전용 함정·골든/fixture·관련 로그). 그 업무 건드릴 때만 읽음.
- logs/YYYY-MM/*.md — 작업 로그 (append-only, 1작업단위 1건)
- decisions/NNNN-*.md — ADR (append-only)

현재 워크플로우: openmarket-merge · onnuri-order · logistics-order · cheonnyeon-upload · invoice-fill · dashboard · product-registration-common(공통) · smartstore-register · easyadmin-register · esm-register (state.md 인덱스 참조).

## 읽기 규칙 (세션 시작 — 한 번에)
- PAT는 프로젝트 지식 파일에서 읽는다(절대 repo에 두지 않음).
- bash 한 번으로 **INDEX.md + state.md + pitfalls.md + roadmap.md** 를 contents API(raw)로 받는다:
  Accept: application/vnd.github.raw 헤더 → base64 아닌 raw 텍스트 직행(UTF-8).
- 이 4개는 워크플로우 수와 무관하게 일정(전역만). 특정 업무를 건드릴 때 그 **workflows/<name>.md** 1개를 추가로 읽는다.
- 그다음 필요한 것만 drill-down(해당 log/decision). 전부 읽지 말 것.

## 쓰기 규칙 (제자리 갱신 가능)
- 로그: logs/YYYY-MM/ 에 새 파일(append). 작업단위마다 1건: 무엇/왜/변경/검증/다음·상태.
- **워크플로우 전용** 지식·함정·상태 → 해당 `workflows/<name>.md` 에 (pitfalls/state 아님). 항상 전체 내용으로 덮어씀.
- **전역/공통** 함정만 pitfalls.md. state.md는 슬림 인덱스(워크플로우 한 줄 상태)만.
- state/pitfalls/roadmap/INDEX/workflows: 고정 경로 그대로 덮어쓴다(항상 전체 내용으로). 바뀔 때만.
- 새 워크플로우 추가 시: ① workflows/<name>.md 생성, ② state.md 인덱스에 한 줄 추가.
- 쓰기 = contents API PUT. 신규=sha 없이, 기존=현재 sha를 GET 후 PUT(안 하면 409/422). content는 base64.

## 검증 (최고 ROI)
- 변경 전 실물(템플릿/VBA/데이터) 재확인 → 변경 후 대조. KB는 길잡이지 진실의 원천 아님.

## 안전
- 부수효과·되돌릴 수 없는 동작(발송·삭제·결제·권한·외부쓰기)은 정확한 payload 보여주고 승인.
- KB에 비밀·PII 금지(고객정보·자격증명·계좌·주문자정보). 식별자(주문번호/참조ID)만. PAT도 repo·KB에 금지.

_갱신: 2026-06-09 (esm-register 추가 — ESM/G마켓)_

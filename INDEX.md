# 업무 자동화 프로젝트 — KB INDEX

## 이 프로젝트
회사 발주 업무를 엑셀 템플릿 + 정제 파이프라인(현 VBA → 점진 Python 이관 검토)으로 처리하는 시스템을 자동화·발전시키는 프로젝트.
- 기억(KB) 저장소 = GitHub `OURPROJECTDAO/work-automation-wb` (main, 고정 파일명).
- 엑셀 작업물(템플릿/원본/정제본) = Google Drive `업무자동화-KB/templates·inputs·outputs`.

## 파일 지도 (고정 경로 — 제자리 갱신)
- INDEX.md — 이 맵 + 읽기/쓰기 규칙
- state.md — 현재 상태 (작게)
- pitfalls.md — 재시도 금지 함정 (작업 전 필독)
- roadmap.md — 백로그 / 우선순위
- logs/YYYY-MM/*.md — 작업 로그 (append-only, 1작업단위 1건)
- decisions/NNNN-*.md — ADR (append-only)

## 읽기 규칙 (세션 시작 — 한 번에)
- PAT는 프로젝트 지식 파일에서 읽는다(절대 repo에 두지 않음).
- bash 한 번으로 INDEX.md + state.md + pitfalls.md 를 contents API(raw)로 받는다:
  Accept: application/vnd.github.raw 헤더 → base64 아닌 raw 텍스트 직행(UTF-8).
- 그다음 필요한 것만 drill-down(해당 log/decision). 전부 읽지 말 것.

## 쓰기 규칙 (제자리 갱신 가능)
- 로그: logs/YYYY-MM/ 에 새 파일(append). 작업단위마다 1건: 무엇/왜/변경/검증/다음·상태.
- state/pitfalls/roadmap/INDEX: 고정 경로 그대로 덮어쓴다(항상 전체 내용으로). 바뀔 때만.
- 쓰기 = contents API PUT. 신규=sha 없이, 기존=현재 sha를 GET 후 PUT(안 하면 409/422). content는 base64.

## 검증 (최고 ROI)
- 변경 전 실물(템플릿/VBA/데이터) 재확인 → 변경 후 대조. KB는 길잡이지 진실의 원천 아님.

## 안전
- 부수효과·되돌릴 수 없는 동작(발송·삭제·결제·권한·외부쓰기)은 정확한 payload 보여주고 승인.
- KB에 비밀·PII 금지(고객정보·자격증명·계좌·주문자정보). 식별자(주문번호/참조ID)만. PAT도 repo·KB에 금지.

_갱신: 2026-05-31 (KB를 GitHub로 이관. Drive는 엑셀 작업물 전용)_

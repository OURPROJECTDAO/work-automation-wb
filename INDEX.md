# 업무 자동화 프로젝트 — KB INDEX

## 이 프로젝트
회사 발주 업무를 엑셀 템플릿 + 정제 파이프라인(현 VBA → 점진 Python 이관)으로 처리하는 시스템을 자동화·발전시키는 프로젝트.
- 기억(KB) 저장소 = GitHub `OURPROJECTDAO/work-automation-wb` (main, 고정 파일명).
- 코드 저장소 = GitHub `OURPROJECTDAO/work-automation-app` (main, public).
- 엑셀 작업물(템플릿/원본/정제본) = Google Drive `업무자동화-KB/templates·inputs·outputs`.

## 파일 지도 (고정 경로 — 제자리 갱신)
- INDEX.md — 이 맵 + 읽기/쓰기 규칙
- state.md — 현재 상태 + **워크플로우 인덱스** (작게, 항상 읽음)
- pitfalls.md — **프로토콜·환경·공통 데이터위생** 함정 (항상 읽음, 슬림)
- patterns.md — **상황별 패턴**(Streamlit 앱 / Excel 파싱). 그 종류 작업할 때만 읽음
- roadmap.md — 백로그 / 우선순위 (항상 읽음)
- **systemmap.json — 지도+로드맵 구조화 정본**(노드 status·한 줄·로드맵 항목·edges·asset→소비처). 렌더러(HTML/인앱)가 읽음. 항상 읽음 (ADR 0019).
- manifest.md — **연결 맵**(공유 자산→소비자 역색인·워크플로우 의존·등록채널 자산위치). 공유 reference/체인 건드릴 때 읽음(상시 아님)
- plan.md — 구현 청사진 (아키텍처 + 단계별 계획, 필요 시)
- **workflows/<name>.md — 워크플로우별 지식**(요약·핵심로직/수식·전용 함정·골든/fixture·관련 로그). 그 업무 건드릴 때만 읽음.
- logs/YYYY-MM/*.md — 작업 로그 (append-only, 1작업단위 1건)
- decisions/NNNN-*.md — ADR (append-only)

현재 워크플로우: openmarket-merge · onnuri-order · logistics-order · cheonnyeon-upload · invoice-fill · dashboard · product-registration-common(공통) · smartstore-register · easyadmin-register · esm-register · cashnote-register · sikbom-register · channel-margin-monitor · upload-monitor · intelligence-layer(지능레이어) · daily-dashboard(데일리 대시보드) · sikbom-event-planning(식봄 행사기획) · margin-optimizer(기준마진율 최적화·두뇌④) · ui-design(전 페이지 UI·횡단) (state.md 인덱스 참조).

## 읽기 규칙 (세션 시작 — 한 번에)
- PAT는 프로젝트 지식 파일에서 읽는다(절대 repo에 두지 않음).
- bash 한 번으로 **INDEX.md + state.md + pitfalls.md + roadmap.md + systemmap.json** 을 contents API(raw)로 받는다:
  Accept: application/vnd.github.raw 헤더 → base64 아닌 raw 텍스트 직행(UTF-8).
- 이 5개는 워크플로우 수와 무관하게 일정(전역만). 특정 업무를 건드릴 때 그 **workflows/<name>.md** 1개를 추가로 읽는다.
- 그다음 필요한 것만 drill-down(해당 log/decision). 전부 읽지 말 것.

## 쓰기 규칙 (제자리 갱신 가능)
- 로그: logs/YYYY-MM/ 에 새 파일(append). 작업단위마다 1건: 무엇/왜/변경/검증/다음·상태.
- **워크플로우 전용** 지식·함정·상태 → 해당 `workflows/<name>.md` 에 (pitfalls/state 아님). 항상 전체 내용으로 덮어씀.
- **전역/공통** 함정만 pitfalls.md. state.md는 슬림 인덱스(워크플로우 한 줄 상태)만.
- state/pitfalls/roadmap/INDEX/workflows: 고정 경로 그대로 덮어쓴다(항상 전체 내용으로). 바뀔 때만.
- 새 워크플로우 추가 시: ① workflows/<name>.md 생성, ② state.md 인덱스에 한 줄 추가, ③ systemmap.json 노드 추가.
- **systemmap.json 갱신(ADR 0019)**: 노드 status 변화·로드맵 항목 완료/추가/재우선·공유자산/소비처 추가·새 체인/상속(edges)·새 워크플로우 → 같은 작업단위에 systemmap.json 갱신 + meta.updated(KST). **상태·로드맵·연결=JSON 정본, 깊은 디테일=workflows/.md, 서사=state.md/manifest.md**(같은 사실 양쪽 기재 금지). PUT 전 검증 3종: json 파싱·필수키/enum·참조 해소. enum(status/tier/cluster) 변경 시 렌더러 동반 수정.
- 쓰기 = contents API PUT. 신규=sha 없이, 기존=현재 sha를 GET 후 PUT(안 하면 409/422). content는 base64.

## 검증 (최고 ROI)
- 변경 전 실물(템플릿/VBA/데이터) 재확인 → 변경 후 대조. KB는 길잡이지 진실의 원천 아님.

## 안전
- 부수효과·되돌릴 수 없는 동작(발송·삭제·결제·권한·외부쓰기)은 정확한 payload 보여주고 승인.
- KB에 비밀·PII 금지(고객정보·자격증명·계좌·주문자정보). 식별자(주문번호/참조ID)만. PAT도 repo·KB에 금지.

_갱신: 2026-06-12 (intelligence-layer 워크플로우 추가 — 이력엔진+두뇌 설계확정; upload-monitor 이력 유지)_

_갱신: 2026-06-15 (systemmap.json 신설 — 지도+로드맵 구조화 정본. 캐치업 상시읽기 추가 + 갱신 규칙. ADR 0019)_

_갱신: 2026-06-16 (daily-dashboard 워크플로우 추가 — 당일점검 승격+세션 자동 인계. ADR 0023)_

_갱신: 2026-06-17 (cashnote-register 워크플로우 추가 — 캐시노트 KCD 일괄등록 채널 셋업)_

_갱신: 2026-06-18 (sikbom-event-planning 워크플로우 추가 — 식봄 행사기획. channel-margin-monitor 정산식 재사용·챗 네이티브)_

_갱신: 2026-06-18 (sikbom-register 워크플로우 추가 — 식봄 일괄등록 최초 셋업. 양식 분석·카테고리 평탄화 정본·1차 74건 생성)_

_갱신: 2026-06-19 (margin-optimizer 워크플로우 추가 — 기준마진율 최적화 두뇌④ 설계확정. ADR 0026)_

_갱신: 2026-06-19 (ui-design 워크플로우 추가 — 전 페이지 UI 디자인·횡단. Phase A 라이브. ADR 0028)_

_갱신: 2026-06-19 (margin-optimizer 두뇌④ 측정 루프 = Gate 3 닫기 구현 — 결정일 이후 실적으로 효과측정→유지/되돌림, 측정창 30일·되돌림 baseline −Δ 역가산. core measure/_verdict·decision_log.update·page 탭구조. Reboot 1회)_

_갱신: 2026-06-19 (margin-optimizer 두뇌④ 설계 노브 전부 완성 → 운영중: 측정 하드닝(커버리지 게이트+일수정규화)·⑧ 시즌(선물세트) 제외·⑦ 매출목표+나들 floor·② 회전 markdown. core+page·Reboot 1회. 정본 workflows/margin-optimizer.md §13~17)_

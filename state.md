# 현재 상태 (스냅샷)
> 워크플로우 상세 = workflows/<name>.md · 작업 이력 = logs/ · 백로그 = roadmap.md · 전역 함정 = pitfalls.md · 결정 = decisions/

## 운영 인프라
- KB 기억 시스템: GitHub OURPROJECTDAO/work-automation-wb (main).
- 코드 저장소: GitHub OURPROJECTDAO/work-automation-app (main, public).
- 엑셀 작업물: Google Drive 업무자동화-KB/templates·inputs·outputs.
- 웹 앱: Streamlit Community Cloud 배포·운영 중.

## 워크플로우 인덱스 (이관 완료 = 운영 중)
> 상태는 통제어휘(운영중/진행중/이슈/개념doc). **상세·검증·미해결·자산은 각 workflows/<name>.md**. 연결=manifest.md.

| 워크플로우 (내부명) | Phase | 상태 | 상세 |
|---|---|---|---|
| openmarket-merge (오픈마켓합포도서산간확인V7) | 1 | 운영중 | workflows/openmarket-merge.md |
| onnuri-order (온누리양식_발주서/제이티발주) | 3 | 운영중 | workflows/onnuri-order.md |
| logistics-order (발주서출력업무) | 3 | 운영중 | workflows/logistics-order.md |
| cheonnyeon-upload (천년경영업로드V15) | 3 | 운영중 | workflows/cheonnyeon-upload.md |
| invoice-fill (송장처리) | 3 | 운영중 (4채널) | workflows/invoice-fill.md |
| dashboard (영업이익현황) | 4 | 운영중 (이익률·물류량 점진) | workflows/dashboard.md |
| product-registration-common (등록 공통) | — | 개념doc | workflows/product-registration-common.md |
| smartstore-register (스마트스토어) | — | 운영중 (챗) | workflows/smartstore-register.md |
| easyadmin-register (이지어드민·정산채널) | — | 운영중 (챗) | workflows/easyadmin-register.md |
| esm-register (ESM=G마켓) | — | 운영중 (챗) | workflows/esm-register.md |

## 완료된 Phase
- Phase 0: 코드 repo 스캐폴딩. 2026-06-01.
- Phase 1: openmarket_merge 8단계 + pytest. 2026-06-01.
- Phase 2: Streamlit 앱 + Community Cloud 배포 + 기준데이터 관리 UI. 2026-06-01.
- Phase 3 (진행 중): 4종 완료 (onnuri-order, logistics-order, cheonnyeon-upload, invoice-fill). 나머지 템플릿 대기.
- Phase 4 (운영 최소): 대시보드 — 데이터계층+저장어댑터+3개년 적재(313K행)+최소 페이지(매출 집계)+증분 업로더([데이터 추가] 탭) 배포. 차트/물류량/이익률/거래처그룹 점진추가. 2026-06-08. (decisions/0006)

## 막힌 것 / 이슈
- 없음. (B2 인프라 완료 — repo·PAT R/W·st.secrets 검증됨 2026-06-08.)

## 다음 한 수
- **Phase 4 대시보드 점진 확장**: 매출집계·증분업로더·거래처그룹·구분분류·기간 날짜범위·일/월/연 추이·**이익 모드(택배비=ERP 00-12 라인, 3000/2500 보정 토글, 이익률=이익/매입가, 전체 거래처)** 배포 완료(decisions/0008). 다음 후보 — ① 물류량(수량÷박스내품) ② 이익/물류량 콤보(이중축). 상세 workflows/dashboard.md.
- core/ 신규 모듈을 페이지가 import → 첫 배포 후 Reboot app 필요(pitfalls 모듈캐시).
- **smartstore-register 운영 시작**(챗 네이티브, ADR 0009): 규칙·reference·캐시 KB화. 미해결 — 이미지확장자 자동검증·결정적 엔진/캐시 미구현. (reference csv·양식 app repo 커밋 완료) 상세 workflows/smartstore-register.md.
- (백로그) Phase 3 나머지 템플릿 이관 — 사용자 실물 파일 제공 대기.
- (백로그) 온누리 빈 G셀 회귀 fixture/pytest.

_갱신: 2026-06-09 (워크플로우 인덱스 상태 슬림화 — 통제어휘+포인터, 상세는 각 doc)_

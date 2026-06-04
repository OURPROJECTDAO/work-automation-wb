# 현재 상태 (스냅샷)
> 워크플로우 상세 = workflows/<name>.md · 작업 이력 = logs/ · 백로그 = roadmap.md · 전역 함정 = pitfalls.md · 결정 = decisions/

## 운영 인프라
- KB 기억 시스템: GitHub OURPROJECTDAO/work-automation-wb (main).
- 코드 저장소: GitHub OURPROJECTDAO/work-automation-app (main, public).
- 엑셀 작업물: Google Drive 업무자동화-KB/templates·inputs·outputs.
- 웹 앱: Streamlit Community Cloud 배포·운영 중.

## 워크플로우 인덱스 (이관 완료 = 운영 중)
| 워크플로우 | Phase | 상태 | 상세 |
|---|---|---|---|
| openmarket-merge (오픈마켓합포도서산간확인V7) | 1 | 운영 중 · 골든 5시트 PASS · 송장 단독파일(★★송장) 복원 | workflows/openmarket-merge.md |
| onnuri-order (온누리양식_발주서) | 3 | 운영 중 · 골든 15/15 | workflows/onnuri-order.md |
| logistics-order (발주서출력업무) | 3 | 운영 중 · 골든 4 passed · 프린트 디자인 | workflows/logistics-order.md |
| cheonnyeon-upload (천년경영업로드V15) | 3 | 운영 중 · 골든 27시트 0 불일치 · pytest 29 · logistics 체인 | workflows/cheonnyeon-upload.md |

## 완료된 Phase
- Phase 0: 코드 repo 스캐폴딩. 2026-06-01.
- Phase 1: openmarket_merge 8단계 + pytest. 2026-06-01.
- Phase 2: Streamlit 앱 + Community Cloud 배포 + 기준데이터 관리 UI. 2026-06-01.
- Phase 3 (진행 중): 3종 완료 (onnuri-order, logistics-order, cheonnyeon-upload). 나머지 템플릿 대기.

## 막힌 것 / 이슈
- 없음.

## 다음 한 수
- **천년경영업로드 배포 후 Streamlit Cloud Reboot 필요** (신규 import 모듈 — Manage app → ⋮ → Reboot).
- Phase 3 계속: 다음 이관 템플릿 — 사용자 실물 파일(.xlsm+입력+골든) 제공 대기.
- Phase 4: 대시보드 페이지.

_갱신: 2026-06-04 (cheonnyeon-upload 이관 완료 — logistics 체인·분류표 공유)_

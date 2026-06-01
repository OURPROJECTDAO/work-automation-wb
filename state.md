# 현재 상태 (스냅샷)
> 상세 = logs/ · 백로그 = roadmap.md · 함정 = pitfalls.md · 결정 = decisions/

## 운영 중
- KB 기억 시스템: GitHub OURPROJECTDAO/work-automation-wb (main).
- 코드 저장소: GitHub OURPROJECTDAO/work-automation-app (main). PAT 양측 허용.
- 엑셀 작업물: Google Drive 업무자동화-KB/templates·inputs·outputs.
  - templates/: 오픈마켓합포도서산간확인V7(작업전).xlsm
  - inputs/: 오픈마켓합포_입력_01.xls (820행, HTML-format .xls), 오픈마켓합포_골든_01.xlsm

## 진행 중
- Phase 0 완료: 코드 repo 스캐폴딩. 2026-06-01.
- **Phase 1 완료**: openmarket_merge.py 8단계 구현 + 골든 대조 pytest PASSED. 2026-06-01.

## 막힌 것 / 이슈
- 없음.

## 다음 한 수
- Phase 2: Streamlit 앱 골격 + Community Cloud 배포.
  - app/streamlit_app.py: 파일 업로드 → 워크플로우 선택 → 실행 → 다운로드.
  - Community Cloud 배포 + 뷰어 허용명단 설정.

_갱신: 2026-06-01 (Phase 1 완료)_

# 현재 상태 (스냅샷)
> 상세 = logs/ · 백로그 = roadmap.md · 함정 = pitfalls.md · 결정 = decisions/

## 운영 중
- KB 기억 시스템: GitHub OURPROJECTDAO/work-automation-wb (main).
- 코드 저장소: GitHub OURPROJECTDAO/work-automation-app (main). PAT 양측 허용.
- 엑셀 작업물: Google Drive 업무자동화-KB/templates·inputs·outputs.

## 진행 중
- Phase 0 완료: 코드 repo 스캐폴딩. 2026-06-01.
- Phase 1 완료: openmarket_merge.py 8단계 구현 + pytest PASSED + 합포확인 색상. 2026-06-01.
- **Phase 2 코드 완료**: Streamlit 앱 3페이지 작성 완료. Community Cloud 배포 대기.

## 막힌 것 / 이슈
- Community Cloud 배포 미완: 사용자가 직접 배포 설정 필요.
  (repo 연결 + GITHUB_PAT secret 입력)

## 다음 한 수
- Community Cloud 배포:
  1. streamlit.io/cloud → work-automation-app 연결
  2. Main file: app/streamlit_app.py
  3. Secrets에 GITHUB_PAT 입력
- 배포 후 기준 데이터 관리 페이지 실사용 검증.

_갱신: 2026-06-01 (Phase 2 코드 완료)_

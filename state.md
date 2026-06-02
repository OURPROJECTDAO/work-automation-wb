# 현재 상태 (스냅샷)
> 상세 = logs/ · 백로그 = roadmap.md · 함정 = pitfalls.md · 결정 = decisions/

## 운영 중
- KB 기억 시스템: GitHub OURPROJECTDAO/work-automation-wb (main).
- 코드 저장소: GitHub OURPROJECTDAO/work-automation-app (main, public).
- 엑셀 작업물: Google Drive 업무자동화-KB/templates·inputs·outputs.
- **웹 앱 운영 중**: Streamlit Community Cloud 배포 완료.

## 완료된 Phase
- Phase 0: 코드 repo 스캐폴딩. 2026-06-01.
- Phase 1: openmarket_merge.py 8단계 구현 + pytest PASSED. 2026-06-01.
- Phase 2: Streamlit 앱 3페이지 + Community Cloud 배포. 2026-06-01.
- Phase 3 (진행 중): 2종 완료.
  - 온누리양식_발주서: onnuri_order.py + 골든 15/15. 2026-06-01.
  - 발주서출력업무: logistics_order.py + UI 전체. 2026-06-02.
    Phase1(GATE A) + Phase2(GATE B) + 연동데이터관리 + 기준데이터관리 탭.

## 막힌 것 / 이슈
- product_master.csv 최초 업로드 필요 (연동데이터관리에서 사용자 수동).
- pytest 골든 대조 테스트 미작성.

## 다음 한 수
- 실 데이터로 Phase1/2 검증 → 버그 픽스.
- Phase 3 계속: 다음 템플릿.

_갱신: 2026-06-02 (Phase3 발주서출력업무 구현)_

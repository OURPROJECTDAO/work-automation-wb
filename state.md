# 현재 상태 (스냅샷)
> 상세 = logs/ · 백로그 = roadmap.md · 함정 = pitfalls.md · 결정 = decisions/

## 운영 중
- KB 기억 시스템: GitHub OURPROJECTDAO/work-automation-wb (main).
- 코드 저장소: GitHub OURPROJECTDAO/work-automation-app (main). PAT 양쪽 허용.
- 엑셀 작업물: Google Drive 업무자동화-KB/templates·inputs·outputs.
  - templates/: 오픈마켓합포도서산간확인V7(작업전).xlsm
  - inputs/: 오픈마켓합포_입력_01.xls (820행, HTML-format .xls), 오픈마켓합포_골든_01.xlsm

## 진행 중
- Phase 0 완료: 코드 repo 스캐폴딩 완료. 2026-06-01.
- Phase 1 착수 준비 완료: 입력+골든 파일 분석, io_excel.py HTML-xls 로더 추가.

## 막힌 것 / 이슈
- 없음.

## 다음 한 수
- Phase 1: openmarket_merge.py Step 8개 구현 + 골든 파일 대조 테스트.
  Step 순서: 0.병합셀정제 → 0.5.송장저장 → 1.합포찾기 → 2.정렬 → 3.색상 → 4.필터링 → 도서산간확인 → 미배송지확인
  골든 기준: 합포 282행 / 지역 13행 / 필터링 8행 / 미배송 0행

_갱신: 2026-06-01 (Phase 0 완료, Phase 1 착수 준비)_

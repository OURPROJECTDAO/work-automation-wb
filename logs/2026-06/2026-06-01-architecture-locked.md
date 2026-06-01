# 2026-06-01 자동화 시스템 아키텍처 확정

## 무엇
업무 자동화 시스템의 세부 아키텍처 확정(decisions/0002). 첫 템플릿(오픈마켓합포도서산간확인V7.xlsm) 실물 구조 분석.

## 왜
VBA 매크로 엑셀 → 원격/클라우드 시스템으로 발전. VBA 로직 점진 Python 이관.

## 변경
- decisions/0002 신규. roadmap.md / state.md 갱신.

## 검증 (실물 재확인)
- 첫 템플릿 xlsm 분석: 시트 10개, 매크로박스 버튼 8개(=실제 사용 매크로), 버튼↔VBA 매핑 확인.
  - 버튼 순서: 0.정제(ProcessMergedCells) → 0.5저장(SaveSheetToNewFile) → 1.합포(CopyDuplicatesToSummary) → 2.정렬(SortColumnBDescending) → 3.색상(HighlightColumnC) → 4.필터링(FilterAndCopyRows) / (번호없음) 도서산간(FasterCopyRows)·미배송(mbCopyRows).
  - 미사용 코드: OC_Module(버튼 없음, openclaw 경로 하드코딩 레거시) → 삭제 예정(Excel 수동, 파이썬 OLE 직접수정은 위험해 보류).
  - 참조 데이터 규모: 도서산간리스트 10,551행 / 필터링리스트 120건 / 미배송지리스트 30건.
- 규칙 확인: 버튼에 연결된 매크로 = 사용, 미연결 = 미사용 (모든 자동화 파일 공통).

## 다음 / 상태
- 다음 액션: 새 코드 repo(work-automation-app) 생성 + PAT 권한 2개 repo 확장.
- 그 후 템플릿 1종 Python 재구현 착수. 미완: repo·코드 아직 없음(아키텍처 설계만 완료).

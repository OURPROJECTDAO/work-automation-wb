# 로드맵 / 백로그

## 완료
- KB 기억 시스템 구축: Drive 테스트 → 캐치업 지연 발견 → GitHub 이관. 2026-05-31. (decisions/0001)
- 자동화 시스템 아키텍처 확정: Streamlit + Python 코어 + Community Cloud(무료), 코드 repo 분리. 2026-06-01. (decisions/0002)
- **Phase 1 완료**: 오픈마켓합포도서산간확인V7 Python 재구현 + pytest PASSED. 2026-06-01.
  - 참조 데이터(도서산간/필터링/미배송) csv 추출 → reference/
  - openmarket_merge.py 8단계 구현 (VBA 버그 재현 포함)
  - 골든 대조 테스트 5시트 전부 PASS

## 다음 (우선순위)
1. ~~새 코드 repo(work-automation-app) 생성 + PAT 권한 2개 repo로 확장.~~ ✅
2. ~~템플릿 1종(오픈마켓합포도서산간확인V7) 워크플로우를 Python으로 재구현.~~ ✅
3. **Streamlit 앱 골격 + Community Cloud 배포.**
   - app/streamlit_app.py: 업로드 → 워크플로우 선택 → 실행 → 다운로드.
   - Community Cloud 배포 + 뷰어 허용명단 설정.
4. 나머지 템플릿 1종씩 이관.
5. 대시보드 페이지(매출/현황 등 데이터 뷰).

## 나중
- 입력 자동 수집(스마트스토어/쿠팡/ESM API or 크롤링).
- 동료 접근(뷰어 허용명단 확대) / 리소스·통제 필요시 Railway 이전.

_갱신: 2026-06-01 (Phase 1 완료 표시)_

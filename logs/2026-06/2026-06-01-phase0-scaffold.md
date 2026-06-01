# 2026-06-01 Phase 0 완료 — 코드 repo 스캐폴딩

## 무엇
work-automation-app repo 생성 + PAT 확장 + 전체 골격 파일 19개 커밋.

## 변경 (work-automation-app)
- core/base.py: Workflow/Step 베이스, WorkflowContext, normalize_kr(NFC)
- core/io_excel.py: load_sheets, save_sheets, load_csv_ref(UTF-8-sig)
- core/workflows/registry.py: @register 데코레이터, get_workflow, list_workflows
- core/workflows/openmarket_merge.py: 8단계 Step 스캐폴딩 (Phase 1 구현 예정)
- reference/.gitkeep, tests/golden/.gitkeep, tests/fixtures/.gitkeep
- tests/test_openmarket_merge.py: 골든파일 대조 테스트 스캐폴딩 (skip 상태)
- app/streamlit_app.py, app/pages/1_파일처리.py, app/pages/2_대시보드.py
- requirements.txt, .gitignore, .streamlit/config.toml

## 함정 발견
- 한글 파일명(1_파일처리.py 등) → urllib.request가 URL ASCII 인코딩 실패.
  해결: urllib.parse.quote(segment)로 퍼센트 인코딩. pitfalls.md 추가.

## 다음 / 상태
- Phase 1 착수 조건: 사용자가 VBA 출력 결과물(골든 파일)과 입력 샘플을 제공.
- openmarket_merge.py Step 8개 구현 → 골든 대조 테스트 통과 목표.

# 2026-06-04 천년경영업로드 (cheonnyeon-upload) 이관

## 한 일
Phase 3 4번째 템플릿 `천년경영업로드자동화V15.xlsm` → Python(Streamlit) 이관 완료. 운영 배포 + 골든 검증 + KB 갱신.

## 핵심 결정 / 발견
- **logistics 체인 발견**: 입력 발주자료 = 발주서출력업무(logistics-order)가 산출하는 발주자료 아카이브 앞 7열. 멸치쇼핑 분류표 = `logistics_classification.csv` 재사용(골든 worksheet 215코드 100% 일치 검증). → 분류표 신규 업로드 불필요, 두 워크플로우가 체인. (decisions/0005)
- **신규 기준데이터 2종**: 배민상회 수수료율(781행)·소분목록(357행)을 골든 내장 시트에서 추출 → `reference/bm_commission.csv`·`sub_list.csv`.
- **스스주문 암호 1323**: 사용자가 암호 걸린 원본 그대로 업로드 → 앱이 msoffcrypto-tool로 복호화. `open_sss`는 평문도 자동 허용.
- 출력은 마켓 전체/낱개 27시트만 생성(원본 36시트 중 비파이프라인 시트 제외 — 업로드에 불필요).

## 검증
- raw 배민주문·스스주문(암호본) + 역산 발주자료로 **end-to-end 0 불일치** (27시트, H/J/K 계산값 직접 비교).
- 운영 `run()` API 경로(복호화 포함) 재검증 0 불일치. 출력 xlsx 40KB 정상.
- pytest 29 passed. fixtures는 PII 제거(슬림 컬럼만), 기준데이터 주입으로 결정적.

## 배포 (work-automation-app, 15파일)
- 신규: core/workflows/cheonnyeon_upload.py · reference/{bm_commission,sub_list}.csv · app/pages/2_기준데이터관리/4_천년경영업로드.py · tests/test_cheonnyeon_upload.py · tests/fixtures/cheonnyeon/(6) · tests/golden/cheonnyeon/golden_260604.xlsx
- 수정: requirements.txt(msoffcrypto-tool 추가) · app/streamlit_app.py(nav) · app/pages/1_파일처리.py(천년경영 탭)

## 상태 / 다음
- **상태**: 운영 중. 사용법 = 발주서출력업무 Phase1에서 발주자료 받고 → 천년경영 탭에 3파일(발주자료·배민주문·스스주문) 업로드 → {yymmdd}.xlsx 다운로드.
- **남은 일**: Streamlit Cloud **Reboot** 필요 — 신규 import 모듈(core/workflows/cheonnyeon_upload.py)은 자동 반영 안 됨(pitfalls: import 모듈 변경=리부트). Manage app → ⋮ → Reboot.
- 전용 함정·수식표는 workflows/cheonnyeon-upload.md.

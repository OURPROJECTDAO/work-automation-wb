# 로그: 발주서출력업무 구현 (Phase1/2 + Gate + UI)

## 무엇
발주서출력업무 워크플로우 전체 구현.

## 왜
사용자 요청. 물류팀프로그램v5_2 xlsm 16단계 VBA를 Python+Streamlit으로 재구현.

## 분석 단계 (구현 전)
- 골든 파일 대조로 16단계 파이프라인 전체 확정
- 셀나누기: HTML rowspan → NaN 감지 → 총수량/정산금액 ÷2
- 노이즈 행: HTML 서브테이블(품절경고) → 헤더 이전 행 전체 skip
- GATE A: 구분 미분류 코드 → 사용자 분류 → 분류표 자동 저장 → 재실행
- GATE B: 낱개 원코드 미매칭 → 낱개처리목록 수동 추가 후 재실행
- 병합셀: 필요 확정 → openpyxl로 A열(구분), B열(규격 연속그룹) 병합

## 변경 (work-automation-app)
- reference/logistics_classification.csv 신규 (1012행, 골든 xlsm 추출)
- reference/unit_list.csv 신규 (383행, 골든 xlsm 추출)
- reference/spec_master.csv 신규 (4366행, 골든 xlsm 추출)
- core/workflows/logistics_order.py 신규 (Phase1/2 파이프라인 + Excel 생성)
- app/pages/1_파일처리.py 수정 (발주서출력업무 탭 추가, Phase1/2 UI + GATE A/B)
- app/pages/2_기준데이터관리/3_발주서출력업무.py 신규 (분류표/낱개목록/규격파일 탭)
- app/pages/4_연동데이터관리.py 신규 (상품관리 업로드 + 타임스탬프)
- app/streamlit_app.py 수정 (연동데이터관리 섹션 추가)

## 검증
- 골든 파일 구조 대조 완료 (분석 단계)
- pytest 골든 대조 테스트: 미실행 (다음 단계)

## 다음·상태
- Streamlit 재배포 대기 (1~2분)
- 골든 대조 테스트 작성 필요 (tests/test_logistics_order.py)
- product_master.csv 최초 업로드 필요 (연동데이터관리에서 사용자 수동)
- 실 데이터로 Phase1/2 검증 후 pitfalls 추가

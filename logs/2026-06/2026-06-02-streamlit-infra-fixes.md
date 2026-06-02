# 로그: Streamlit 인프라 수정 2건 (nav 표시 + 모듈 캐시)

## 무엇
발주서출력업무 배포 중 발견한 Streamlit 인프라 이슈 2건 수정.

## 1. 연동데이터관리 사이드바 미표시
- 증상: streamlit_app.py에 등록했는데 "연동데이터관리" 섹션이 안 보임.
- 원인: 이름 있는 named section의 페이지는 pages/하위디렉토리/ 안에 있어야 표시됨. pages/ root에 직접 둔 4_연동데이터관리.py는 안 보임. (headerless 섹션 ""·" "은 root OK)
- 수정: pages/3_연동데이터관리/1_상품관리.py 로 이동(sys.path parent 4단계), streamlit_app.py에 _N 변수 추가. 구 파일 stub 처리.
- pitfalls 기록함.

## 2. import 모듈 변경 미반영
- 증상: "not enough values to unpack (expected 4, got 3)". 페이지(1_파일처리.py)는 새 버전인데 import된 logistics_order는 옛 버전(3-tuple) 캐시.
- 원인: Streamlit은 페이지 스크립트는 매번 재실행하지만 sys.modules에 캐시된 import 모듈은 안 갈아끼움.
- 해결: Manage app → Reboot app으로 프로세스 재시작. pitfalls 기록함.

## 변경 (work-automation-app)
- app/pages/3_연동데이터관리/1_상품관리.py 신규, app/pages/4_연동데이터관리.py stub.
- app/streamlit_app.py: _N 경로.

## 다음·상태
- 완료. 코드 수정 시 리부트 습관화 필요(특히 core/ 변경).

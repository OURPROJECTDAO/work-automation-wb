# 2026-09-17 이지어드민 취소주문 알리미 1차

- 무엇: 이지어드민 확장주문검색 취소건 → PC 알림(선택 카톡 나에게 보내기) 로컬 프로그램.
- 왜: 사용자 요청. 단톡방은 공식 API 불가·이지어드민 Open API는 유료라 제외 → 로컬 브라우저 자동화 + PC 알림.
- 변경: Claude in Chrome으로 화면 구조 읽기전용 조사(네트워크 조회는 사용자 거절 → 미실시, 조작 없음).
  date_type=cancel_date, order_cs_sel 4/5, jqGrid #grid1 컬럼 확인. ezcancel_alert.zip 산출
  (ezcancel_alert.py·config.json·install/login/test_run/register_task.bat·README). 앱·repo 코드 변경 0.
- 검증: py_compile·config JSON 파싱만. 실사이트 미실행. 현재 그리드 1건(G마켓 628500, 송장입력·1차 출력됨) 확인.
- 다음·상태: 사용자 PC 설치 → login.bat → test_run.bat 결과 확인. 실패 시 alert.log로 수정.
  미검증 = headless 세션 유지·검색 버튼 셀렉터·로드완료 대기·100건 페이지. 정본 workflows/easyadmin-cancel-alert.md.

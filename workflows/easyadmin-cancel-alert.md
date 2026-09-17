# easyadmin-cancel-alert (이지어드민 취소주문 알리미)

## 요약
이지어드민 확장주문검색2에서 신규 취소주문을 찾아 PC 알림(선택: 카톡 '나에게 보내기')으로 알림.
API 미사용(유료라 불가, 사용자 확정 2026-09-17) → 회사 PC 로컬 Playwright(nadl 수집기와 같은 로컬 실행 패턴).
배포물 = ezcancel_alert.zip (설치 폴더 권장 `C:\claudeworkautolocal\ezcancel`). 앱(Streamlit) 미탑재.

## 화면 구조 (2026-09-17 읽기전용 실측)
- URL `https://ga59.ezadmin.co.kr/template35.htm?template=DS00` (메인 document, 동일 폼이 iframe에도 중복)
- 폼 `myform`(127필드). 기간 기준 `select[name=date_type]` — **`cancel_date`=취소일** 옵션 존재(알림 기준으로 채택)
  · 날짜 `input[name=start_date|end_date]`(YYYY-MM-DD) · 시 `start_hour|end_hour`
- C/S `select[name=order_cs_sel]`: 0전체·1정상·10정상+교환·**2취소(배송전+배송후)**·3교환·**4배송전 취소·5배송후 취소**·6/7교환·8보류·9맞교환·11배송후교환C·13부분취소·12부분취소 제외
- 결과표 = jqGrid `#grid1`(url function.htm POST json, rowNum 100, 로딩표시 `#load_grid1`)
  colModel: rn,chk,seq(관리번호),shop_id(판매처),order_id,recv_name,name(상품명),p_options,qty,order_products_qty,supply_code,
  status,order_cs,collect_date(발주일),trans_no,trans_date,trans_date_pos,product_name(판매처상품명),supply_option,o_options,
  trans_no_print_seq(출력차수),order_name,cust_id,order_tel,order_mobile,…
- ★ status·order_cs 칸은 **텍스트 없이 아이콘 이미지**(status icon_06.gif=송장입력, order_cs icon_01.gif+S_cs.gif) →
  배송전/배송후 구분은 아이콘 해석 대신 **order_cs_sel 4·5로 따로 검색**해서 라벨 부여.
- 내부 호출(function.htm 파라미터)은 사용자 거절로 미조회 → 화면 조작(검색조건 설정+검색 버튼) 방식.

## 로직
- **검색조건(사용자 확정 2026-09-17)**: 발주일(`collect_date`) 오늘 포함 7일(lookback_days=6) × C/S `2`=취소(배송전+배송후) 1회 검색
  → getRowData(개인정보 컬럼 미수집) → 키 `관리번호` 신규만 알림. (초안의 취소일·CS 4/5 분리 검색은 폐기)
- 배송전/후 라벨 = `trans_date_pos`(배송일) 값 유무로 추정(아이콘 미해석). 발주 8일+ 지난 주문의 취소는 누락 → lookback 조정.
- seen.json 30일 보관, 첫 실행은 기록만. 평일 8~19시, 15분 스케줄(schtasks EZCancelAlert, pythonw).
- 배송전 취소 + 송장번호/출력차수 있음 → '⚠송장출력됨 → 출고 막기' 강조.
- 로그인 = 전용 크롬 프로필(chrome_profile) 수동 로그인 1회, 풀리면 알림. 비밀번호 미저장.
- 카톡 = 카카오 REST '나에게 보내기'(talk_message, 200자 분할·최대 5건, refresh_token 자동 갱신). 기본 off.

## 함정/미검증
- 실사이트 실행 미검증(컨테이너에선 문법만). 검증 대상: headless 로그인 유지 · 검색 버튼 텍스트 `검색(F2)` 클릭 · jqGridLoadComplete 이벤트(폴백=3초 후 #load_grid1 숨김) · 100건 초과 시 페이지 넘김(현재 경고만).
- 스크립트가 PC에 쓰는 파일(chrome_profile, kakao_token.json)은 비밀 — repo/KB 금지.

## 상태
진행중 — 1차 배포물 전달, 사용자 PC 설치·테스트 대기.

## v2 트레이 앱 (2026-09-17, 사용자 옵션 확정)
배포물 구성: `ezcore.py`(조회+상태) · `tray_app.py`(pystray+tkinter) · config.json · install/start/test_run/register_startup.bat.
구 `ezcancel_alert.py`·15분 schtasks(EZCancelAlert) 폐기 → 로그온 시 트레이 상주(EZCancelTray).
- **채택**: 긴급(배송전 취소+송장번호/출력차수) = **빨간 최상단 팝업**(소리 없음, 사용자 '어차피 안 들림') + 트레이 빨강 ·
  요약/건별 선택 · 알림 클릭=확장주문검색 URL · 조회주기 설정 · **처리함 체크 + 미처리 재알림**(기본 긴급만 30분) ·
  취소 목록 창(긴급 빨간 행·다중선택 처리/취소·CSV 내보내기·더블클릭=이지어드민) · 트레이 아이콘 · 상태 표시(색+툴팁 마지막 조회).
- **제외**: 카카오톡 전부 · 집중 조회('괜찮아'=불요로 해석) · 점심 일시정지 · 하루 마감 요약.
- 트레이 색: 초록 정상/주황 미처리/빨강 긴급/회색 조회중/검정 로그인·오류.
- 상태 `state.json`(관리번호 키: first_seen·done·done_at·urgent·last_alert). 첫 실행 건은 done='초기기록'.
  **이후 송장이 출력돼 긴급으로 바뀐 기존 건도 알림**(became). 처리 건만 keep_days 후 정리.
- 로그인 = 메뉴 '다시 로그인' → 헤드풀 창에서 사용자 로그인, 확장주문검색 셀렉터 감지 시 자동 종료(10분 제한).
- 구조: 브라우저 작업은 단일 워커 스레드(Playwright sync·프로필 동시 사용 방지), UI 갱신은 큐→tk 메인 스레드.
- 검증: py_compile + 상태 로직 단위(첫실행 기록만·신규·긴급전환·재알림 주기·처리) 통과. **실사이트/윈도우 GUI 미실행.**

## 로그인 함정 (2026-09-17 실사용 첫 보고)
- alert.log 에 조회 때마다 `비밀번호가 변경되었습니다. 다시 로그인해주시기 바랍니다.` 반복 + `잘못된 로그인 정보입니다.` 1회.
  → 조회 페이지가 **저장된 세션/자동로그인으로 옛 인증을 쓰다 거부**당하는 상태. 원인 후보: (a) 실제 비밀번호 변경 후 전용 프로필 쿠키 잔존
  (b) **같은 아이디를 평소 크롬과 공유 → 중복 로그인 차단으로 서로 끊음**(미확인). 권장 = 알리미 전용 조회권한 사용자 아이디.
- ★ **Playwright는 dialog 리스너가 없으면 확인창을 자동 '취소'** → v2 로그인 창에서 사용자가 이지어드민 확인창(예: 기존 접속 끊기)을 못 보고 로그인이 막힐 수 있었음.
  픽스: 로그인 모드는 dialog **accept + 기록**, 조회 모드는 **dismiss + 로그인 관련 문구면 즉시 LoginRequired(메시지 전달)**.
- 추가: 메뉴 '로그인 정보 초기화 후 로그인'(chrome_profile 삭제) · 로그인 필요 중엔 '지금 조회'도 차단(반복 시도로 계정 잠김 방지).
- ★★ **로그인해도 계속 로그인 요구(2026-09-17 2차 보고) — 추정 원인: Playwright persistent context 는 브라우저를 닫을 때 세션쿠키(만료 없음)를 버린다.**
  로그인 창(헤드풀)을 닫고 조회용 창(헤드리스)을 새로 띄우는 구조라 매번 로그아웃 상태였음. 픽스: 로그인/조회 성공 시 `ctx.cookies()` →
  `session.json` 저장, 다음 실행 `add_cookies` 복원 + 매 조회 후 재저장. 보조: 헤드리스 UA `HeadlessChrome` 차단 가능성 → 로그인 때 기록한 UA 사용.
  test_run.bat = 창 보임/숨김 2회 테스트(보임만 성공이면 UA/헤드리스 차단 → 설정 '크롬 창 숨기기' 해제로 우회). **실사이트 미검증.**

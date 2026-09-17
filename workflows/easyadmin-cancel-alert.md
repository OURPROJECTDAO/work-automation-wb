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

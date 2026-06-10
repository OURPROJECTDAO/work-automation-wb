# 2026-06-10 channel-margin-monitor — 코어 + 독립 페이지 구현

## 무엇
검증된 코어 로직 + 독립 Streamlit 페이지 구현·커밋. 스마트스토어 채널.

## 변경 (app repo 신규)
- `core/workflows/channel_margin_monitor.py` (e4bccf2c): CHANNEL_CONFIG(채널별 수수료·정산계수·실택배비·기준마진열·마진제한·다운로드 컬럼맵) + load_references(product_master·sobun·baseline·floor) + resolve_code(4-tier) + parse_download + compute + run.
- `app/pages/6_채널마진모니터.py` (c5bb291b): 채널선택 → .xlsx 업로드 → @st.cache_data run → KPI(총건수·평균마진·미달·제한·미설정·미매칭) + 필터(코드유형·마진미달·재고0·제한·미매칭) + 표(권장가/제한 합성열, percent/localized 서식) + CSV.

## 검증 (골든 705/706)
- 코어 end-to-end(실 다운로드 712행): 정산액 707/707, base매입단가 706/707, 마진율 705/706 골든 일치. 나머지=폐기한 3000/3700 분기(602+103) + 1건 매입단가 vintage(62000≠골든64000, product_master가 최신).
- 신식(2700 단일): 712건·평균마진 10.28%·마진미달 79·제한 37·미설정 9·미매칭 5. ast 양쪽 OK.
- 판매자바코드 N 분수(0.25·0.2…) float 처리 정상. PC낱개·소분 매입가/재고 정상. 합포(-CB-)는 이 다운로드 0건 — 로직만 검증.

## 다음 / 상태
- ⚠️ core import 모듈 신규 → **첫 배포 후 Reboot app 1회** 필요(페이지 인식).
- 배포·실사용 확인 후 상태 운영중 전환.
- 미해결: ① 미매칭 엣지 `(임박)…` 등 수기 접두 코드(현재 미매칭 표시) ② baseline↔product_master 조인 갭 ③ 마진제한 적용채널 세분화(현 전채널) ④ 합포 -CB- 실데이터 대조 추후 ⑤ sobun↔unit_list↔sub_list 통합.
- 타 채널: CHANNEL_CONFIG 한 세트 추가(수수료·기준마진열·다운로드 컬럼맵).


## 후속 (같은 날) — st.navigation 등록 누락 픽스
- 증상: Reboot 후에도 좌측 메뉴에 페이지 안 뜸(사용자 스크린샷).
- 원인: 이 앱은 pages/ 자동탐지가 아니라 `app/streamlit_app.py`의 명시적 `st.navigation()` 구조. 페이지 파일만 커밋하고 등록을 빠뜨림(patterns.md "pages/ root 파일 명시 등록 필수"를 적용 안 함).
- 픽스: streamlit_app.py 헤더없는 " " 섹션(대시보드 옆)에 `st.Page(_P/"6_채널마진모니터.py", title="채널마진모니터", icon="💹")` 추가. ast OK 커밋.
- streamlit_app.py는 진입 스크립트(import 모듈 아님) → 재배포(1~2분) 후 자동 반영, 추가 Reboot 불필요.
- 교훈(기존 함정 재확인): 새 페이지 추가 시 파일 생성 + **streamlit_app.py st.navigation 등록**이 한 세트. 단독 파일은 안 뜸.
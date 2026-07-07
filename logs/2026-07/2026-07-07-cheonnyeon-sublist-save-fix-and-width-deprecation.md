# 2026-07-07 — 천년경영업로드 소분목록 저장 폼화 + use_container_width→width 전역 교체

## 무엇
1. **기준데이터관리 → 천년경영업로드 → 소분목록(및 배민상회 수수료율) 저장이 "한 번에 안 되는" 버그 수정.**
   `app/pages/2_기준데이터관리/4_천년경영업로드.py`의 `_edit_with_search`가 `st.data_editor`(경합 지점) +
   `st.data_editor` 밖의 별도 `st.button`으로 구성돼 있었음. 사용자가 소분목록에 새 행을 추가하고 마지막
   셀(원코드 등)을 입력한 직후 바로 "저장" 버튼을 누르면, 그 마지막 셀 입력이 위젯 상태에 커밋되기 전에
   버튼 클릭 이벤트가 먼저 처리되어 **직전 상태로 커밋됨** → 사용자 입장에선 "저장이 한번에 안 되고
   두 번째 클릭에야 반영"되는 것처럼 보임. `st.data_editor` + 저장 버튼을 **`st.form`으로 묶어
   `st.form_submit_button`으로 교체** — 폼 제출은 모든 위젯 값을 한 번에 확정한 뒤 처리되므로 경합이 없어짐.
2. **`use_container_width` deprecation 경고 전역 제거.** Streamlit이 `use_container_width`를 `width`로
   교체(`True`→`width="stretch"`, `False`→`width="content"`) — 배포 로그에 매 요청마다 경고가 반복 출력됨.
   전체 저장소 grep 결과 **83건 전부 `use_container_width=True`**(False 사용례 없음) → 17개 페이지 파일
   전수 `width="stretch"`로 치환.

## 왜
- 소분목록 저장: 사용자가 반복 보고("계속 저장이 한번에 안 되거든"). 근본 원인 = Streamlit 위젯 상태
  확정 타이밍과 폼 밖 버튼의 경합(널리 알려진 Streamlit data_editor 패턴).
- width: 배포 로그에 매 상호작용마다 경고 라인이 찍혀 실질 에러와 섞임 — 지금 고치는 게 이후 로그
  가독성·차기 Streamlit 버전 대응에 유리(향후 `use_container_width` 완전 제거 대비).

## 변경
- `app/pages/2_기준데이터관리/4_천년경영업로드.py`: `_edit_with_search`가 `(result, submitted)` 튜플
  반환하도록 변경, 내부에 `st.form(key=f"form_{name}")` + `st.form_submit_button(save_label)` 도입.
  `_section`에서 별도 `st.button` 제거하고 `submitted` 플래그로 커밋 트리거. 이 파일 내 남은
  `use_container_width=True` 2건도 `width="stretch"`로 교체.
- 그 외 16개 페이지 파일(app/pages/ 전체) — `use_container_width=True` → `width="stretch"` 단순 치환
  (총 81건, 로직 변경 없음): 0b_데일리대시보드·10_가격AB·11_상품360·12_시장가매칭·13_기준마진율최적화·
  1_파일처리·2_기준데이터관리/{1_오픈마켓합포도서산간확인,2_온누리양식_발주서,3_발주서출력업무}·
  3_대시보드·3_연동데이터관리/{1_상품관리,2_데이터현황}·6_채널마진모니터·7_업로드감시·8_마진침식·9_재고지능.
- core/ 디렉토리는 무변경(grep 결과 use_container_width가 core/에는 없었음) — **전부 page-only 변경**.

## 검증
- `python3 -c "import ast; ast.parse(...)"` 전 17개 파일 통과.
- `python3 -m pytest tests/test_cheonnyeon_upload.py -q` → 36 passed (core 로직 무변경 확인, 페이지
  UI는 이 테스트 스위트 커버리지 밖이라 별도 pytest 없음 — 수기 로직 리뷰로 대체).
- GitHub API로 17개 파일 각각 fresh SHA GET 후 PUT 커밋 완료(전부 200 OK, 커밋 SHA 확보).

## 다음·상태
- **전부 page-only → Streamlit Cloud 자동 재배포(1~2분)만 필요, Reboot app 불필요**(신규 core import 없음).
- 사용자 실사용 확인 대기: (a) 소분목록에 새 행 추가 → 저장 버튼 1번 클릭으로 반영되는지
  (b) 배포 로그에서 `use_container_width` 경고가 더 안 뜨는지.
- 같은 `st.data_editor` + 별도 버튼 패턴이 다른 페이지에도 있을 수 있음(이번엔 리포트된 천년경영업로드
  범위만 수정) — 유사 증상 재보고 시 같은 폼화 패턴 적용.
- 다음 한 수(기존, 변동 없음): 두뇌④ 측정 루프 개시(결정원장 커버리지 충족 여부 확인) · 로켓그로스 8/1(7월분)
  · 시장대비 권장가(nadl 매핑 누적 후).

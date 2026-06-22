# 채널마진모니터 — 기준마진율 설정 UX 안정화(인라인 + 표 버전카운터)

## 무엇 / 증상
기준마진율 설정(현재→기준): 체크박스 선택→기준값 입력→저장 시 "위로 즉시 반영 + 체크박스 풀림"이
한번씩 작동 안 하고, 엉뚱한 값에 체크박스가 가 있는 불안정. 두뇌④는 같은 작업인데 깔끔 → 패턴 이식.

## 원인
- 메인 표 key = `cmm_df_{key}_{filter_sig}`(필터/검색/행수 hash). 저장 후 rerun으로 데이터 미세변동인데
  filter_sig 그대로면 positional 선택 인덱스 stale(엉뚱한 행 체크).
- 2단계 구조(버튼→session_state bl_{key}→data_editor): 선택 라이프사이클과 엇갈려 간헐 미작동.
- 두뇌④는 표 key=`mo_tbl_{mo_tblver}`(순수 버전카운터·기록 시 +1 강제초기화) + 선택→바로 아래 인라인.

## 변경 (page-only)
- 표 버전카운터 `cmm_tblver`(setdefault 0). 메인 표 key에 `_{cmm_tblver}` 추가 → 저장 시 +1로 선택 강제 초기화.
- 기준마진율 설정 인라인화(2단계→1단계): bl_{key}·여는 버튼 제거. 선택 있으면 즉시 propose_baseline→data_editor.
- 저장: update_baseline_csv→commit→clear→cmm_tblver+=1→st.rerun() → 즉시 반영+선택 풀림. 구 bl_{key} pop.

## 검증
- ast OK. 순수함수 시그니처 무변경. 동작은 두뇌④와 동일 메커니즘 → 사용자 실사용 확인. 커밋 page 13b33e56.

## 다음 / 상태
- page-only. 단 같은 세션 core canonical_code(전월매출) 때문에 Reboot 1회는 어차피 필요 — 함께 반영.

# 2026-06-08 대시보드 — 이익/매출 표 정렬 버그 수정

## 무엇
거래처 이익 표에서 송장 헤더 내림차순 클릭이 숫자가 아닌 문자열 순으로 정렬되던 문제 수정.

## 원인
st.dataframe에 숫자를 `f"{v:,.0f}"` 문자열로 변환해 넣어 dtype이 object → 헤더 클릭 정렬이 사전식.
첫 글자 기준(9>7>5>4>3>2>1)으로 정렬되어 962·916·5,625·27,999… 순으로 보임.

## 변경 (app/pages/3_대시보드.py)
- 매출/이익 표 모두 숫자 컬럼을 numeric(int 캐스팅)으로 유지하고, 표시 콤마는
  `st.column_config.NumberColumn(format="localized")`, 이익률은 `format="%.2f"`로 처리.
- 문자열 변환(map f-string) 제거. 기본 정렬(이익 desc)은 유지, 헤더 클릭 재정렬이 숫자 기준 동작.

## 검증
- ast.parse OK. 문자열 포맷 잔재 grep 0. 커밋 019460a6. pages/ 파일이라 Reboot 불필요.

## 다음 · 상태
- 운영. (streamlit>=1.36 unpinned → Cloud 최신 설치라 localized 포맷 지원.)

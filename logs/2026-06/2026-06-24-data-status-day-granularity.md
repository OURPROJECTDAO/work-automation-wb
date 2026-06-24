# 데이터현황(연동 데이터 관리) — 적재 범위 일자까지 표시

## 무엇
데이터 적재 현황 페이지(3_연동데이터관리/2_데이터현황.py)의 "범위"를 월(YYYY-MM)에서
일자(YYYY-MM-DD)까지 보이게 개선. 상단 메트릭 캡션 + 표 범위 컬럼 둘 다.

## 왜
사용자: "각각 2026-06 이런식으로 월은 있는데 일은 없어서, 일자까지 나오게."
기존 coverage는 파일명(sales_YYYY-MM.parquet)에서 월만 파싱 → 일 단위 정보 없음.

## 변경
- core/intelligence/coverage.py:
  - CATALOG monthly 4종에 date_col 추가 — 매출=거래일자·주문=발주일·재고=스냅샷일자·매입=기준일
    (가격이력 single은 기존 수정일자 그대로). 발주자료=예정(파일0).
  - 신규 _day_range(pat,repo,path,date_col): 파티션 1개 읽어 date_col (min,max) 'YYYY-MM-DD'.
    columns=[date_col]로 파싱 비용 최소화, 실패/공란이면 (None,None).
  - monthly 브랜치: 첫 달·마지막 달 파티션만 read해 first_day/last_day 산출
    (첫달==마지막달이면 1회만 read). first/last(YYYY-MM)는 갭·타임라인용으로 그대로 유지.
  - single 브랜치(가격이력): 기존 read에 first_day/last_day(%Y-%m-%d) 추가 산출.
  - rec에 first_day/last_day 키 신설(없으면 None).
- 페이지:
  - 메트릭 캡션(monthly·갭 없을 때) → first_day/last_day 우선, 폴백 first/last.
  - 표 "범위" 컬럼 → 동일 폴백 규칙.
  - 타임라인 차트·갭 컬럼은 무변경(월 단위 유지).

## 검증
- ast.parse 2파일 OK.
- 실데이터(work-automation-data) 골든 — coverage() 직접 실행:
  - 매출   2023-01-01 ~ 2026-05-31
  - 주문   2023-03-02 ~ 2026-05-29
  - 가격이력 2025-06-16 ~ 2026-05-29
  - 재고    2026-06-14 ~ 2026-06-24
  - 매입    2022-01-03 ~ 2026-06-15
  - 발주자료  — (파일0·예정)
  파티션 정합성 사전 확인: 각 파일 날짜가 그 달 안에 갇혀 있음 →
  첫 파일 min + 마지막 파일 max = 실제 전체 일자 범위 정확.

## 비용
- monthly 4종 × 첫·마지막 파티션 = 최대 7회 + 가격이력 1회 = 약 8회 file read.
  페이지 @st.cache_data(ttl=600)라 10분당 1회. 파티션 파일 작음(매출~176KB·주문~574KB·매입~52KB).

## 다음·상태
- ✅ 커밋 완료: coverage.py a418e6b · page e344a98.
- ⚠️ coverage.py = core import 모듈 → **재배포(1~2분) + Reboot app 1회** 필요
  (페이지가 새 함수/필드 참조, sys.modules 캐시). 페이지 단독은 자동반영이나 core 변경 묶여서 Reboot 권장.
- 사용자 실사용 확인 대기(Reboot 후 범위 컬럼 일자 표시).
- 프로젝트 다음 한 수=변동 없음 — 두뇌④ 측정 루프(6월 영업이익현황 7월초 적재 후)·시장대비 권장가.

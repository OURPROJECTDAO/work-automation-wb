# 워크플로우: 오픈마켓합포도서산간확인V7 (openmarket-merge)

> 이 워크플로우를 건드리기 전 이 파일을 읽는다. 전역 함정은 pitfalls.md.

## 요약
- 오픈마켓 발주 정제. HTML-xls 입력 → 5시트 멀티시트 xlsx 출력.
- 출력 시트: 송장출력 · 합포확인 · 지역확인 · 미배송지역확인 · 필터링확인.
- Phase 1 (최초 Python 이관 템플릿). 운영 중.
- 원본: 오픈마켓합포도서산간확인V7 xlsm (VBA 8단계).

## 코드 / 데이터
- `core/workflows/openmarket_merge.py` (8단계 + 색상 적용)
- 참조 데이터 (`reference/`, UTF-8-sig):
  - `dosan_list.csv` (10551행, 도서산간) — 대용량: curl 업로드 불가, Python urllib 사용.
  - `dosan_except_list.csv` (13행, 도서산간아님 — VBA 미사용)
  - `filter_list.csv` (120건, 필터링 키워드)
  - `undelivered_list.csv` (3행, 미배송지)
- 테스트: `tests/test_openmarket_merge.py`, `tests/conftest.py`(워크플로우 자동 등록)

## 8단계 파이프라인
1. StepLoadInput — HTML-xls 로드 + NFC 정규화
2. StepCopyDuplicates — 주소 중복 → 합포확인 (수령자→수취인명 rename)
3. StepSortByAddress — 주소 내림차순 정렬
4. StepColorGroups — 주소 그룹 경계 계산 → `ctx.meta['hapo_colors']` 저장
5. StepFilterProducts — 필터링리스트 상품명 키워드 매칭
6. StepDosanCheck — VBA B1 read 버그 재현(아래 함정)
7. StepUndeliveredCheck — 미배송지리스트 주소 매칭
8. `_save()` — 저장 후 openpyxl로 합포확인 배경색 적용
   - ColorIndex 36=연노랑(#FFFF99) ↔ 35=연초록(#CCFFCC), 그룹 바뀔 때마다 교대.

(plan.md §4에 VBA 매크로 ↔ Python 단계 매핑표.)

## 전용 함정
- **VBA FasterCopyRows B1 read 버그 (재현 필수)**: `ListSheet.Range("B1:B" & LastRowList)` — B1(헤더='주소')부터 읽음 → '주소' 자체가 키워드로 포함 → '(상세주소 없음)', '김승주소아과' 등이 도서산간으로 매칭됨. 도서산간아님 예외 로직은 VBA에 미구현(해당 시트는 데이터만 있고 미사용). Python 재현:
  `ds_kw = ['주소'] + [normalize_kr(k) for k in ds['주소'].tolist() if k.strip()]`
- **상품명 줄바꿈 인코딩**: 골든 xlsm은 `,_x000D_\n`(OOXML CRLF 인코딩), HTML-xls 원본은 `', '`(컴마+공백). 같은 데이터, 표현만 다름. 테스트 비교 시 골든 정규화 필요:
  `df['상품명'].str.replace(',_x000D_\n', ', ', regex=False)`
- **합포확인 정렬**: VBA SortColumnBDescending = xlPinYin 정렬(C열=주소 내림차순). Python `sort_values('주소', ascending=False)`와 그룹 내 행 순서가 다를 수 있음. 테스트 시 `check_like=True` 단독으로는 부족(index 기준 비교) → 송장번호 기준 정렬 후 `assert_frame_equal`.

## 검증 (골든 대조)
- pytest 5시트 전체 PASS:
  - 송장출력 820행, 합포확인 282행(+색상), 지역확인 13행, 미배송지역확인 0행, 필터링확인 8행.
- 테스트는 normalize + 송장번호 정렬 후 대조.

## 관련 로그 / 결정
- logs/2026-06/2026-06-01-phase1-impl.md (구현 + 함정 발견)
- plan.md §4 (단계 매핑), decisions/0002 (아키텍처)

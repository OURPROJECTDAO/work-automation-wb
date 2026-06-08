# 2026-06-08 Phase 4 대시보드 — 거래처 그룹 / 미분류 구분 분류 탭

## 무엇
대시보드(`app/pages/3_대시보드.py`)에 탭 2개 추가 + 대시보드 탭에 그룹 집계/필터 연동.
- **[👥 거래처 그룹]**: 상호명→그룹 배정. ① 검색→인라인 지정(data_editor) ② 목록 일괄 붙여넣기(NFC 매칭, 미매칭 리포트). 저장은 private repo `work-automation-data/groups/store_groups.csv`.
- **[🏷 구분 분류]**: 미분류 관리코드를 상품명·매출·건수와 함께 나열 → 음료/식품/선물세트 지정 → 멸치쇼핑 분류표(app repo `reference/logistics_classification.csv`)에 추가(기존 코드 덮어/신규 추가).
- **[📊 대시보드]**: 집계기준에 `그룹` 추가 + `그룹` 멀티선택 필터(미지정 포함). 매핑은 NFC 키로.

## 왜
거래처 그룹: 온/오프라인 등으로 묶어 채널 단위 매출 보기(로드맵 후보 ⑤).
구분 분류: 미분류(매출 비중 있음)를 사용자가 맥락 보고 분류 → 대시보드 구분 정확도↑. 0006의 "분류는 별도 UI" 방침을 "공유표 사용 + 대시보드 분류 도우미"로 변경(decisions/0007).

## 변경
- `core/dashboard/store.py`: `read_groups`/`write_groups` 추가(groups/store_groups.csv, 상호명,그룹). 기존 sha GET 후 PUT.
- `app/pages/3_대시보드.py`: 2탭 → 4탭. load_group_map(@st.cache_data, NFC키), _save_groups(canonical 상호명 보존·NFC dedup·빈값=해제), append_classification(app repo, GITHUB_PAT). 분류 저장 후 load_sales.clear(); 그룹 저장 후 load_group_map.clear().

## 데이터(초안 시드)
- 사용자 제공 `온라인거래처목록.xlsx`(15곳) → 전부 매출 마스터와 NFC 정확 매칭(미매칭 0) → groups/store_groups.csv 신규 커밋, 15곳 `온라인`.

## 검증
- ast.parse OK(store.py·대시보드). 분류 머지 로직(기존 덮어+신규) 스모크 OK.
- 마스터 현황 관측: **41개 월 파티션(2023-01~2026-05), 고유 거래처 1,041곳** (KB state는 29파티션/313K로 stale — 그새 사용자가 적재). 행수는 미합산.
- UI 동작은 배포 후 사용자 확인 예정.

## 다음·상태
- ⚠ **store.py(core 모듈) 변경 → 첫 배포 후 Reboot app 필요**(import 캐시). 대시보드 페이지는 자동반영이나 read_groups/write_groups는 리부트 전까지 옛 모듈.
- [구분 분류] 쓰기는 app repo라 `GITHUB_PAT` 시크릿 필요(발주 분류표 편집과 동일 PAT). [data] pat은 폴백.
- 분류 저장은 재배포(1~2분) 뒤 반영(load_sales는 로컬 reference csv를 읽으므로).
- 나머지 점진 후보: ① 멀티연도 월별 추이 차트 ② 이익률 KPI ③ 물류량(수량÷박스내품) ④ 이익/물류량 콤보.
- (정합화 backlog) state·dashboard.md의 파티션/행수 수치(29/313K)를 41파티션/2023-01 시작으로 차후 갱신.

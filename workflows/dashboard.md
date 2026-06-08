# 워크플로우: 대시보드 (dashboard, Phase 4)

> 이 기능을 건드리기 전 이 파일을 읽는다. 전역 함정은 pitfalls.md. 설계 근거 decisions/0006.

## 요약
- 영업이익현황(거래처별 매출, 트랜잭션 레벨) 3개년(~50만행) 파워BI 스타일 대시보드.
- ERP API 불가 → 사용자가 5월 양식 .xlsx 다운로드만 가능. 부트스트랩 1년치씩 + 일/주/월 증분.
- 데이터 계층 코어·저장 어댑터·3개년 부트스트랩·대시보드 최소버전+증분 업로더+거래처 그룹+구분 분류 탭 완료(2026-06-08). 차트/물류량/이익률 점진 확장.
- 4탭: 📊 대시보드(매출 KPI+구분/그룹/거래처/상품/관리코드 집계) · ➕ 데이터 추가 · 👥 거래처 그룹 · 🏷 구분 분류.

## 데이터 흐름
```
영업이익현황 xlsx 업로드
  → parse_sales()      합계행 제외·9컬럼 선별·타입·ym 파생 (calamine)
  → split_by_month()   YYYY-MM 파티션 분할
  → date_range_replace 중복: 파일 날짜구간 통째 교체(최근 우선)
  → 월별 parquet 누적  (저장소 = work-automation-data, private)
표시:
  → apply_categories() 구분 2단 분류 + 박스내품 조인 + 물류량(=수량÷박스내품)
  → @st.cache_data 1회 로드 → KPI/차트/슬라이서
```

## 입력 스키마 (영업이익현황, 23컬럼 A~W)
- 거래일자/상호명(거래처)/상품코드·관리코드·바코드/상품명/규격/단위/주매입처/메이커/상품분류/수량/단위원가·판매원가·판매단가·판매금액/판매이익/이익률/기준단가·박스단가/비고·상세비고/매입원가.
- **대시보드 보존 컬럼(KEEP_COLS, 9개)**: 거래일자·상호명·관리코드·상품명·규격·상품분류·수량·판매금액·판매이익. 나머지(빈컬럼/잡컬럼)는 버려 parquet 슬림 + PII 표면 축소.
- 상품분류(K)는 사실 브랜드(코카콜라/동서식품). 단위(H)·주매입처(I)·메이커(J)는 사실상 빈칸.

## 구분(식품/음료) 2단 분류 — 최종 규칙
1. **1차** = `logistics_classification.csv` (관리코드→구분: 음료/식품/선물세트). 발주서출력업무와 공유.
2. **2차 fallback** = `product_master.csv` 중분류명: `음료-B동`→음료, `통조림-C동`→식품.
3. 그 외(세제외-A동·잡화-S동·기타·미존재 "비식품") → **미분류**. 사용자 분류 전까지 미분류 유지(분류 UI는 추후 별도 논의).
- 카테고리 집합: 음료 / 식품 / 선물세트 / 미분류.

## 물류량
- `물류량 = 수량 ÷ 박스내품` (product_master 박스내품, 관리코드 조인).
- 박스내품 결측/0이면 **1.0으로 간주**(물류량=수량 그대로). 실거래 코드 99.7%가 박스내품 보유라 영향 미미.

## 중복 처리 = 날짜구간 교체 (decisions/0006 #4)
- 데이터에 전표/라인 고유ID 없음 → 행단위 dedup 불가.
- "파일이 다루는 날짜구간은 그 파일이 진실"(최근 다운로드 우선). new의 [min,max] 날짜를 master에서 지우고 new 삽입.
- ERP export가 연속 날짜구간이라는 전제. 월 파티션이라 건드린 달만 재기록.

## 성능 (실측, 5월 10,053행)
- parse(calamine) 0.78초/월. parquet 0.27MB/월·재로딩 0.02초. category dtype 1.0MB.
- 3개년 추정: 부트스트랩 파싱 ~28초(1회성), parquet ~10MB, 집계 <100ms.
- read_excel(openpyxl)은 50만행 65초/548MB → Community Cloud RAM 1GB 초과 위험. **xlsx 직접 집계 금지**, parquet 경유.

## 조인 커버리지 (5월 실파일, 784 고유 관리코드)
- 관리코드 조인키: product_master에 없는 코드 단 1개.
- 박스내품: 거래코드 99.7% 커버(결측 2개, 수량 0.02%).
- 구분: 1차 분류표 매출 87.6% → 2단 적용 후 미분류 5.5%(2차 fallback이 음료/식품 채움).
- 최종 구분별 매출(5월): 음료 73.5% / 식품 20.8% / 미분류 5.5% / 선물세트 0.1%.
- KPI: 매출 33.66억 / 이익 2.21억 / 이익률 6.55% / 물류량 ~21.6만.

## 저장소 (B2 — decisions/0006 갱신)
- **거래처 그룹 매핑** `groups/store_groups.csv`(상호명,그룹)도 같은 private repo. 상호명=영업정보라 public app repo 금지.
- **적재 현황(2026-06-08 확인)**: 41개 월 파티션 · **2023-01~2026-05 · 총 421,865행 · 고유 거래처 1,041곳**. (최초 3개년 부트스트랩 후 2023년치 추가 갱신 — 사용자 의도. load_master가 파티션을 동적 전수 로드하므로 앱은 자동 반영.)
- master(거래처 매출)는 **PII**(영업기밀) → public app repo 금지.
- **private repo `OURPROJECTDAO/work-automation-data`** 에 월별 parquet 보관. 앱이 `st.secrets`의 PAT로 R/W.
- (대안 기각/백업: B1 Drive+서비스계정 — GCP 셋업 부담. B3 세션보유 — 영속 없음.)
- ✅ repo 생성·PAT Contents R/W 권한·st.secrets 등록 완료(2026-06-08). PAT 읽기/쓰기/삭제 라이브 검증됨.
- ✅ **부트스트랩**(2026-06-08): 최초 3개년(2024~2026 = 29파티션/313,293행) 적재 후 2023년치 추가 → 현재 41파티션/421,865행(위 적재 현황).
  - 연도 KPI: 2023 313.8억/7.0%/562 · 2024 391.6억/6.4%/559 · 2025 378.3억/6.4%/540 · 2026(1~5월) 169.2억/6.6%/461.
  - 전체 구분: 음료 64.1% / 식품 21.9% / 선물세트 11.5% / 미분류 2.6%. master 메모리 61MB(category).
  - load_master 콜드 4.9초(29파티션 GitHub 순차 다운+합본) → @st.cache_data 세션 1회. 파티션 늘면 선형 증가 → 추후 합본 스냅샷/병렬 최적화 여지.
- Drive 큰 파일 적재 경로: download_file_content 결과가 커서 컨텍스트 초과 시 `/mnt/user-data/tool_results/*.json`에 저장됨 → 디스크에서 inner JSON `content`(base64) 디코딩→parse→ingest. 챗·컨텍스트 한계 둘 다 우회.
- 용량 여유: 월 파티션 ~0.2MB(parquet)·날짜구간 교체 → 작업트리 연 ~2.2MB 증가. GitHub 파일 하드차단 100MB·레포 권장<1GB 대비 runway 사실상 무제한. 단 잦은 binary 덮어쓰기는 .git 히스토리에 옛 blob 누적(우리 규모 수십 년 무방, 필요 시 git gc).

## 코드 / 데이터 / 테스트
- `core/dashboard/sales_data.py` — parse_sales·as_category·split_by_month·date_range_replace·make_classifier·make_box_lookup·apply_categories.
- `core/dashboard/store.py` — DataRepo R/W: list_partition_months·read_partition·write_partition·delete_partition·load_master·ingest(날짜구간 교체) + **read_groups·write_groups**(groups/store_groups.csv, 상호명→그룹). token/repo 인자(core는 app 모름, 페이지가 st.secrets 주입). secrets 키: `[data] pat / repo`.
- 기준데이터: `reference/logistics_classification.csv`(구분), `reference/product_master.csv`(중분류·박스내품).
- 테스트: `tests/test_sales_data.py` (8 passed). fixtures `tests/fixtures/dashboard/` (합성·PII 없음).
- ✅ **대시보드 페이지 최소버전**(`app/pages/3_대시보드.py`, 2026-06-08): 매출 KPI(총매출·건수·기간) + 연도/구분 필터 + 집계기준 선택(구분/거래처/상품/관리코드)별 매출 표(비중·CSV 다운). @st.cache_data(ttl 1h) load. 시크릿 `[data] pat/repo`(없으면 `GITHUB_PAT` 폴백), reference는 로컬 csv.
- ✅ 거래처 그룹 관리 탭([👥]) — 검색·인라인·일괄(NFC 매칭). 그룹맵=private repo groups/store_groups.csv. 전체 1,041곳 배정: 온라인 15 + 오프라인 1,026(2026-06-08, 온라인 외 전부 오프라인).
- ✅ 구분 분류 도우미 탭([🏷]) — 미분류 코드(상품명·매출·건수) → 음료/식품/선물세트 지정 → 공유 분류표 추가(decisions/0007).
- 추후 추가(점진): 멀티연도 월별 추이 차트·이익률 KPI·물류량(박스내품)·이익/물류량 콤보(이중축). (증분 업로더·거래처그룹·구분분류 ✅ 완료)
- requirements: pyarrow(parquet)·python-calamine 추가.

## 전용 함정
- **합계행**: 맨끝 1행 거래일자 NaT = 합계. 제외 안 하면 전 수치 2배. `df[df['거래일자'].notna()]`.
- **관리코드 NFC**: 출처 다른 데이터 NFD면 조인 실패. `unicodedata.normalize("NFC", ...)` 후 조인.
- **분류표는 발주 흐름 코드 위주**: logistics_classification은 발주서출력업무를 거친 코드 위주라 영업 데이터 꼬리가 빠짐 → 2차 fallback(product_master 중분류) 필요.
- **미분류 분류 = 공유표 + 대시보드 분류 도우미([🏷 구분 분류] 탭)** — decisions/0007. 코드별 수동 지정만(일괄 덤프 금지). 분류표에 추가는 발주 GATE A 트리거를 줄이기만 함(안 깨짐). 단 발주 안 거치는 코드 오분류 시 발주에서 GATE 없이 그 분류로 처리됨 주의. 분류 도우미는 app repo `reference/logistics_classification.csv`에 GITHUB_PAT으로 쓰기(발주 분류표 편집과 동일).
- **dict 분류맵 중복키**: 분류표에 동일 관리코드 중복 시 dict는 last-wins. 표준 검증 시 미세 차이 가능(수치 영향 미미).

## 관련 로그 / 결정
- decisions/0006-dashboard-data-layer.md (설계 + A/B 확정)
- decisions/0007-dashboard-shared-classification.md (미분류 분류 = 공유표 + 분류 도우미)
- logs/2026-06/2026-06-08-phase4-dashboard-design.md (큰 틀·목업)
- logs/2026-06/2026-06-08-phase4-dashboard-datalayer.md (조인검증·코어구현·커밋)
- logs/2026-06/2026-06-08-phase4-store-adapter.md (저장어댑터·B2 라이브검증·5월적재)
- logs/2026-06/2026-06-08-phase4-bootstrap-ingest.md (3개년 313K행 부트스트랩)
- logs/2026-06/2026-06-08-phase4-dashboard-minimal.md (최소버전 매출집계 페이지)
- logs/2026-06/2026-06-08-phase4-dashboard-uploader-tab.md (증분 업로더 [데이터 추가] 탭)
- logs/2026-06/2026-06-08-phase4-dashboard-group-classify.md (거래처 그룹·구분 분류 탭)

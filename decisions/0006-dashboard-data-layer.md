# 0006 — 대시보드(Phase 4) 데이터 계층·수집 아키텍처

## 맥락
거래처별 매출(영업이익현황) 3개년(~50만행) 대시보드. ERP API 연동 불가(API 문제). 사용자는 5월 샘플 양식(.xlsx, 23컬럼)으로 **다운로드만** 가능. 부트스트랩은 **1년치씩 분할** 제공 가능, 이후 일/주/월 수시 다운로드.

## 결정
1. **xlsx 직접 집계 금지 → parquet 변환 후 집계.**
   근거: 50만행 read_excel(openpyxl) 65초/548MB. Streamlit Community Cloud RAM 1GB/앱 공유 → 초과 위험. parquet 9MB/0.35초/58MB(category). 집계는 <100ms라 무관 — 병목은 계산이 아니라 xlsx 읽기·메모리.
2. **리더 = calamine**(openpyxl 대비 4배 빠름). 부트스트랩은 통제된 단발 작업이라 피크 649MB 허용. 한계 시 openpyxl read_only로 교체(1줄).
3. **저장 = 월별 parquet 파티션.** 증분이 건드린 월만 재기록.
4. **중복 처리 = 날짜구간 교체(date-range replace).** 데이터에 전표/라인 고유ID 없음 → 행단위 dedup 불가. "파일이 다루는 날짜구간은 그 파일이 진실"(최근 다운로드 우선). ERP export가 연속 날짜구간이라는 전제.
5. **거래처 그룹 = 앱 내 기준표(매핑).** export에 거래처 속성 없음 → 기준데이터관리 패턴으로 거래처→그룹 자유 배정. (옵션 A: export에 속성 컬럼 추가 — 사용자 불가 확인 → 기각)
6. **물류량 = 수량 ÷ 박스내품** (product_master.csv / unit_list.csv, 관리코드 조인).
7. **PII**: 거래처 매출은 영업기밀 → app repo(public) 금지. master는 Drive 또는 세션(미확정).

## 대안/기각
- xlsx 매 세션 직접 파싱 → 65초·메모리 폭주로 기각.
- 행단위 중복제거 → 고유ID 부재로 기각(날짜구간 교체로 대체).
- 거래처 속성 export 컬럼(옵션 A) → 사용자 불가 확인으로 기각.

## 상태
큰 틀 확정(2026-06-08). 미결: master 저장위치(Drive/세션), 식품/음료 매핑 소스 검증.

## 갱신 2026-06-08 — master 저장위치 확정: Google Drive (A)
- 사용자가 네이버 마이박스에 자료를 모아둠 → 연동 검토. **마이박스는 개인용 공개 API 미지원**(서드파티 연동 거의 없음). NCP Object Storage(S3 호환)는 별개의 기업용 유료라 제외.
- 프로젝트가 이미 Google Drive 연동(엑셀 작업물) 사용 중 → master(월별 parquet 파티션)도 **Google Drive** 보관 확정. 마이박스 → Drive 경유(다운로드/동기화).
- 결정 #7 미확정 해소. 세션 보유(B)는 백업안.


## 갱신 2026-06-08 (2) — 분류방식(A)·저장소(B2) 확정 + 실데이터 검증
- **검증(5월 실파일 10,053행)**: 관리코드 조인키 product_master 미존재 1개. 박스내품 거래코드 99.7% 커버. 구분 1차 분류표 매출 87.6%.
- **A 구분 = 2단 분류**: 1차 logistics_classification.csv(음료/식품/선물세트), 2차 product_master 중분류 fallback(음료-B동→음료, 통조림-C동→식품). 비식품(세제외/잡화)·미존재 → **미분류**(사용자 분류 전까지 유지, 분류 UI 추후). 최종 미분류 매출 5.5%.
- **B 저장소 = B2 확정**(0006 #7/갱신(1)의 Drive 대체): master=PII → **private repo `OURPROJECTDAO/work-automation-data`** + 앱 st.secrets PAT로 R/W. Drive(B1)는 GCP 서비스계정 셋업 부담, 세션보유(B3)는 영속 없음으로 기각. GitHub 인프라 재사용.
- **물류량** = 수량÷박스내품, 박스내품 결측/0 → 1.0 간주.
- 구현: core/dashboard/sales_data.py + 테스트 8 passed 커밋. 상세 workflows/dashboard.md.
# 2026-06-15 intelligence-layer — 데이터 적재 현황 페이지 1단계 (통합 데이터 관리)

## 무엇 / 왜
사용자 요청: 시계열로 누적되는 데이터(과거 포함)를 한 곳에서 통합 관리 — "어디~어디 적재 + 갭" 한눈에. §5.6 A 이력 적립 페이지의 1단계(현황 읽기전용).

## 분류 기준 (사용자 확정)
- 통합관리 대상 = **시계열 누적**(backbone work-automation-data 파티션): 매출·주문·가격이력·재고스냅샷·매입현황(예정)·발주자료(예정).
- 제외 = 현재상태 덮어쓰기: 상품관리(product_master)·채널 listing×8·기준/설정 reference.
- 미묘: **재고 스냅샷 = 상품관리 부산물(시계열)** → 현황 표시만, 업로드는 상품관리 탭 자동(사용자 확정).
- 매입현황·발주자료 = "예정(planned)"으로 노출(사용자 확정).

## 변경 (work-automation-app)
- `core/intelligence/coverage.py` (신규): CATALOG 6종(kind monthly/single · upload direct/auto/planned) + 디렉토리 목록만으로 범위·갭 산출(파일 read 0회) · next_month 헬퍼.
- `app/pages/3_연동데이터관리/2_데이터현황.py` (신규): 메트릭 카드 + plotly timeline(적재 파랑·갭 빨강) + 상세표. 읽기전용. _data_secret([data] 시크릿).
- `app/streamlit_app.py`: 연동데이터관리 그룹에 '데이터현황' Page 등록.

## 검증
- coverage() 실데이터: 매출 41개월(2023-01~2026-05 갭0)·주문 36개월(2023-03~2026-05 갭 2023여름)·가격이력 단일(80KB)·재고스냅샷 1(auto)·매입현황/발주자료 empty(planned). ast.parse 3파일 OK.
- API = 디렉토리 6회(파일 read 0) → 가벼움·@st.cache_data(600s).

## 다음 / 상태
- ⚠️ **core 신규 import(coverage) → 첫 배포 후 Reboot app 1회.**
- ✅ 1단계 현황(읽기전용) 배포. **다음 2단계=업로드 허브**(직접 적립=매출·주문·가격이력·매입현황). 주문=orders.py ingest 있어 최우선 쉬움. 메모리=월 1개(.xls read_html ~40MB)만 페이지서, 대량 백필은 컨테이너(pitfalls).
- 적립함수 현황: 매출=대시보드 sales_data 재사용·가격이력=price_history.py 있음·매입현황=신규 필요·발주자료=신규.

## 후속 (2026-06-15)
- fix: 가격이력(single)이 타임라인에 누락 → coverage가 **단일파일 수정일자 범위를 1파일 read**로 산출(2025-06~2026-05·1년 롤링). monthly는 여전히 디렉토리 목록만. 타임라인 포함.
- fix: x축 `Jan 2023` → `2023-01` (plotly tickformat `%Y-%m`).
- 결정(사용자): **2단계 업로드 = 나중에 일괄**. 매입현황·발주자료 등 적재 대상 자료를 다 backbone에 넣은 뒤 업로드 UI를 한 번에 구축(지금 주문만 붙이고 점진 X). 1단계 현황으로 마감.

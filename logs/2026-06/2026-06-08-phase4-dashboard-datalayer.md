# 2026-06-08 Phase 4 대시보드 — 조인 검증 + 데이터 계층 코어 구현·커밋

## 무엇
Phase 4 구현 착수. ① reference 조인 검증(실파일) → ② 데이터 계층 코어(sales_data) 구현·테스트·커밋. 분류방식(A)·저장소(B) 결정.

## 왜
설계(0006)는 확정됐으나 식품/음료 매핑·박스내품이 "잠정". 규율상 실데이터(5월 영업이익현황) 재확인 후 착수.

## 변경
- **work-automation-app**:
  - `core/dashboard/sales_data.py` 신설 — parse_sales(calamine·합계행 제외·9컬럼·ym), split_by_month, date_range_replace(날짜구간 교체), make_classifier(구분 2단), make_box_lookup(결측 fallback=1), apply_categories(구분·박스내품·물류량).
  - `tests/test_sales_data.py` 신설 + 합성 fixtures(PII 없음) → **8 passed**.
- **분류방식 결정(A)**: 음료/식품/선물세트/미분류. 1차=logistics_classification.csv, 2차 fallback=product_master 중분류(음료-B동→음료, 통조림-C동→식품). 비식품(세제외/잡화)·미존재 → 미분류, 사용자 분류 전까지 유지.
- **저장소 결정(B2)**: master=PII → private repo `work-automation-data` + 앱이 st.secrets PAT로 R/W. (0006 #7 갱신)

## 검증 (5월 실파일 10,053행)
- 합계행 제외 정확. KPI 모듈 경유 재현: 매출 33.66억·이익 2.21억·이익률 6.55%(KB와 일치).
- 조인: 관리코드 product_master 미존재 1개. 박스내품 거래코드 99.7% 커버(결측 수량 0.02%).
- 구분 최종: 음료 73.5% / 식품 20.8% / 미분류 5.5% / 선물세트 0.1%. 물류량 ~21.6만.
- 성능: parse 0.78초/월, parquet 0.27MB/월·재로딩 0.02초. 날짜구간 교체 단위테스트(행수 보존·금액델타 일치) PASS.

## 다음·상태
- **막힘(사용자 수동 필요)**: fine-grained PAT는 repo 생성 권한 없음(403). B2는 사용자가 ① private repo `OURPROJECTDAO/work-automation-data` 생성(README로 main 초기화) ② 기존 PAT에 그 repo Contents R/W 권한 추가 ③ Streamlit 앱 secrets에 PAT+repo 등록 필요.
- B2 인프라 올라오면: 저장 어댑터(work-automation-data parquet R/W, urllib+base64) → 부트스트랩 업로더 UI → 대시보드 페이지(`3_대시보드.py`, 현 플레이스홀더) + 거래처 그룹 관리 탭(④).
- 상세: workflows/dashboard.md.

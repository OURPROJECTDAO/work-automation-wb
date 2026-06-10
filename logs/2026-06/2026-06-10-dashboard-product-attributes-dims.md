# 2026-06-10 대시보드 — 브랜드·세분류·소매/도매 차원 (product_attributes 조인)

## 무엇
대시보드가 `reference/product_attributes.csv`를 관리코드로 조인 → 매출 모드 집계/피벗 차원에 **브랜드·세분류(최종분류)·소매/도매(b2b_b2c)** 추가. 식품음료(I)=구분 **3차 fallback**.

## 변경 (commit sales_data 0e0c88f7 · page baecc297)
- `core/dashboard/sales_data.py`: `make_classifier(cls,pm,food_map=None)` 3차 fallback 추가(1차 logistics_classification→2차 product_master 중분류→3차 product_attributes 식품음료). `make_attr_lookup(attr_df)` 신설(컬럼→{관리코드:값}, 빈값제외). `apply_categories(...,attr_df=None)` 확장(브랜드/최종분류/b2b_b2c category 컬럼, 미지정 채움).
- `app/pages/3_대시보드.py` load_sales: product_attributes 로드+조인, 식품음료 fallback classify, 브랜드/최종분류/b2b_b2c 컬럼 추가(category). CAT_DIMS·_dim_key에 브랜드/세분류/소매·도매 추가(매출 모드). 이익 모드 미적용(택배비 비배분).
- 구분 source는 logistics_classification 별도유지 — 식품음료는 연동(3차)만.

## 검증
- ast 양쪽 OK. 로직: 환타(31-47-11)→구분 음료(3차)·브랜드 코카콜라·세분류 탄산음료·b2b c. 동원참치→식품/동원참치/참치캔. 미존재→미분류·미지정. apply_categories 컬럼 정상.

## 다음 / 상태
- ⚠️ **Reboot app 필요**: sales_data.py는 core import 모듈(페이지가 import) → 첫 배포 후 Streamlit Cloud Reboot 1회.
- triage 나머지 640 채우면 미지정 더 축소. 화남 시바스케이퍼 최종분류 미지정.
- 잔여 점진: 물류량 노출·이익/물류량 콤보.

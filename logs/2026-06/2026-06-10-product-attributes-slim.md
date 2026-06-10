# 2026-06-10 product_attributes 속성 축소(슬림화) — 결정·반영

## 무엇
사용자 결정(ADR 0011): product_attributes는 **식품음료·합포수량·최종분류**만 유지. 브랜드·브랜드2·b2b_b2c·정제규격·합포그룹 폐기.

## 변경
- `reference/product_attributes.csv` 4컬럼 슬림화(1,134행, commit b3246887).
- `core/dashboard/sales_data.py`(d8919a78): `_ATTR_COLS=[최종분류,식품음료]`, apply_categories는 최종분류만 추가(+식품음료 구분 3차 fallback). 브랜드·b2b 컬럼 제거.
- `app/pages/3_대시보드.py`(66bcdb36): 로더에서 최종분류만 조인, CAT_DIMS·_dim_key에서 브랜드·소매/도매 제거(세분류만).
- triage_rest451.xlsx: 컬럼 축소(관리코드·상품명·매출·식품음료·최종분류·합포수량[작성]). 정제규격/브랜드/b2b 칸 제거.

## 검증
- ast 양쪽 OK. 슬림 attr로 apply_categories: out에 브랜드/b2b 없음, 최종분류만. 환타→음료(3차 fallback) 유지.

## 다음 / 상태
- ⚠️ Reboot app(sales_data core 모듈).
- 451: 사용자 합포수량 채워주면 product_attributes에 병합(식품음료·최종분류·합포수량). 189(최근1년 매출0) 제외.
- 폐기: 정제규격 정규화기, 브랜드 어휘, b2b 통일.

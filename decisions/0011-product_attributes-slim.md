# ADR 0011 — product_attributes 속성 범위 축소(식품음료·합포수량·최종분류만)

## 상태
채택 (2026-06-10)

## 맥락
합포데이터 기반 product_attributes.csv를 브랜드·b2b_b2c·정제규격까지 풀세트로 만들고 대시보드에 브랜드·소매/도매 차원까지 붙였으나, 유지비(분류 어휘 관리·정제규격 정규화·b2b 어휘 통일) 대비 효용이 낮다고 판단.

## 결정
product_attributes는 **식품음료·합포수량·최종분류** 3속성(+키 관리코드)만 유지. 브랜드·브랜드2·b2b_b2c·정제규격·합포그룹은 **폐기**(저장도 도출도 안 함).
- 대시보드 차원: 세분류(최종분류)만. 식품음료는 구분 **3차 fallback**로 계속 사용. 브랜드·소매/도매 차원 제거.
- 정제규격 정규화기(product_master 규격→숫자단위*숫자)는 폐기(향후 필요시 logs/2026-06-10-product-attributes-reference 인근 기록 참고).

## 결과
- `reference/product_attributes.csv` 4컬럼(관리코드·식품음료·합포수량·최종분류)로 슬림화(commit b3246887).
- sales_data.py(d8919a78)·3_대시보드.py(66bcdb36): 브랜드·b2b 차원 제거.
- triage_rest451: 사용자 작성칸 합포수량만(식품음료·최종분류 확인).
- ⚠️ sales_data.py(core) → 배포 후 Reboot app.

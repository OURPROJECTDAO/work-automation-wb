# retail-insight-pricing (리테일앤인사이트 가격책정)

> 챗 네이티브·앱 미탑재. 리테일앤인사이트(B2B 공급처) 요청 시 상품 가격표 산출. cmm 권장가 공식 오프라인 재현(식봄 행사기획·신규매입 가격책정과 동류). 전역 함정=pitfalls.md.

## 요약
- 리테일앤인사이트는 **baseline_margin/CHANNEL_CONFIG에 없는 비설정 채널.** 우리 공급 유닛=**박스(관리코드)**.
- 입력=스마트스토어 상품관리 최신 listing(우리 활성 상품 유니버스) + product_master + baseline_margin + 매입현황(품절 회전판정).
- 산출=내부공유 xlsx(상품명 ERP·규격·매입가·리테일판매가·마진율). 상대 제출용 양식은 요청 시 별도 변환.

## 파이프라인 (확정 2026-06-26)
1. 유니버스 = 스마트스토어 listing 코드 → `canonical_code`(박스 통일·PC낱개/소분→원박스) → dedup. 합포(-CB-)는 단일 관리코드 아님 → 제외.
2. 가용재고 필터:
   - 박스재고(product_master 박스)>0 → 포함.
   - 품절(박스재고=0) 중 **회전 도는 것만 구제** = 최근 실입고경과일 ≤ 90일(매입현황 합계액>0&수량>0) **그리고** 매출 소진>0(최근 4개월). 재입고 끊김(>90일·입고이력없음)은 제외.
3. 선물세트(product_attributes 식품음료=선물세트) 제외.
4. 기준마진율 체인 = **캐시노트 → 식봄 → 스마트스토어**. ★조회는 **canon 박스코드 + 원래 listing코드 양쪽** baseline_margin 행에서(아래 함정).
5. 가격공식 (택배비 있는 업체·B2B·수수료 2%):
   - 정산액 = 판매가 × (1−수수료)          (수수료 0.02, 배송비 수입 0)
   - 이익 = 정산액 − 매입가 − 실택배비(2,700)
   - 마진율 = 이익 / 정산액                (cmm 캐시노트 baseline 정의와 동일)
   - 판매가 = ⌈ (매입가+2,700)/(1−max(기준마진,0.03))/(1−수수료) ⌉   (100원 올림·3% 하한 클램프)
6. 단위=박스: 매입가=박스매입단가[9]·규격=규격[6]·상품명=product_master 상품명(ERP).

## 산출 서식
- xlsx 2시트: 메인(관리코드·상품명·규격·매입가·기준마진율·출처·리테일판매가·마진율·재고상태) + 제외내역(사유).
- **라이브 수식**: 판매가/마진율은 상단 가정셀(수수료·택배비·하한) 참조 수식. 매입가·기준마진율=파란 입력셀. recalc 0오류 필수.

## 전용 함정
- ★ **baseline_margin은 박스 관리코드뿐 아니라 원래 listing코드(PC낱개·소분)로도 키가 존재.** canon(박스)만 조회하면 PC낱개/소분 상품의 기준마진이 빈 것처럼 보임 → 캐시노트→식봄→스마트스토어 체인을 **canon + 원listing코드 양쪽**에서 돌릴 것. (2026-06-26: canon만 보면 99건 오탐, 양쪽 조회 시 562 캐시노트·1만 스마트스토어 fallback.)
- 품절 구제 임계 90일 = slow-moving-inventory 입고경과일 임계 재사용. 입고=합계액>0&수량>0.
- 매출자료 관리코드는 전부 박스코드 → listing만 canonical로 통일해 join(cmm 전월매출과 동일 원리).
- 리테일앤인사이트는 천년경영 분배(cheonnyeon-upload)에선 수수료없음·H=F/D였으나, 가격책정은 사용자 확정 **수수료 2%·택배비 2,700 적용**(B2B지만 택배비 부담 업체).

## 데이터 소스
- 스마트스토어 listing: app reference/listing_smartstore.csv(+meta) — 사용자 상품관리 갱신본.
- 매입가/재고/규격/상품명: app reference/product_master.csv.
- 기준마진: app reference/baseline_margin.csv(캐시노트·식봄·스마트스토어 열).
- 품절 회전: work-automation-data purchases/buyin_YYYY-MM.parquet(입고경과) + master/sales_YYYY-MM.parquet(소진).
- 코드해석: sobun.csv·product_master(canonical_code 4-tier).

## 로그
- logs/2026-06/2026-06-26-retail-insight-pricing.md (1차 내부공유본·공식 확정·baseline 양쪽키 학습)

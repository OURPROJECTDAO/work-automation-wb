# 2026-06-10 product_attributes.csv 정본 생성 (대시보드 고정 속성표)

## 무엇
합포데이터(첫 시트) 수동컬럼 + 미지정 triage 상위150을 병합해 app repo `reference/product_attributes.csv` 커밋(1,134코드, 85KB, commit 9e70026f).

## 왜
대시보드 브랜드별·세분류(최종분류)별 매출을 보려면 관리코드→속성 고정표가 repo에 영속 저장돼 매 실행 자동 로드돼야 함(매번 업로드 불가). product_master/logistics_classification와 동일 패턴.

## 변경
- 컬럼: 관리코드·합포·합포수량·식품음료·정제규격·최종분류·브랜드·브랜드2·b2b_b2c. PII 없음(상품 속성만) → public app repo.
- 병합: 합포데이터 1006 base + triage 150 overlay(신규 128 + 기존 22 채움) = 1,134코드. triage 값이 빈칸 채움/override.
- 정규화: b2b_b2c 어휘 통일 — 합포데이터 일반/업소 → b2c/b2b (업소=b2b 사용자 확정·대칭). 분포 b2c662/b2b221/미지정251.
- 빈칸(최종분류20·브랜드19·b2b251)은 그대로 → 대시보드에서 미지정 처리. (triage 나머지 640은 추후.)
- UTF-8-sig, 관리코드 NFC.

## 검증
- 식품음료·합포수량 1134/1134, 최종분류 1114, 브랜드 1115. 커밋 size 85232.

## 다음 / 상태
- ⏳ 대시보드 `apply_categories`에 이 표 조인 → 차원(브랜드·최종분류·b2b_b2c) 슬라이서/피벗 추가 + 식품음료를 구분 3차 fallback로.
- 별도유지+연동: 구분(음료/식품/선물세트) source는 logistics_classification 유지, 이 표 식품음료(I)는 3차 fallback로만 보강.
- master 합포데이터.xlsx(수식·드롭다운)는 사용자 작성용 → Google Drive(별도). 이 CSV가 거기서 뽑은 대시보드 정본.
- triage 나머지 640(갭 5%) 추후. 화남 시바스케이퍼(11-61-09-01) 최종분류 미지정.

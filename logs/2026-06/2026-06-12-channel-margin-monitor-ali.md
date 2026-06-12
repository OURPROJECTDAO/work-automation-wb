# 2026-06-12 channel-margin-monitor — 알리(AliExpress) 채널 추가 (모니터 + 자동 정제)

## 무엇
channel-margin-monitor에 **알리(AliExpress)** 모니터 추가. 7번째 채널. 핵심: **상품 정제(매크로 ALI상품매크로V2)를 parse 단계에서 자동화** — 별도 정제 업무 없이 원본 다운로드 그대로 태움.

## 왜
사용자가 "알리는 정제과정을 한 번 거친다"며 원본+매크로+골든 제공. 흐름: 원본(ALIPRODUCT.xlsx) → 매크로 정제 → 정제본 → 알리 골든. 정제를 별도 업무로 만들지 않고 자동화 요청.

## 매크로 정제 로직 (VBA 추출 — Module1 CopyDataFromAnotherWorkbook)
- ALIPRODUCT(AliExpress 대량등록 export) = **카테고리별 다중시트**(커피음료·탄산수…25개) + 각 `*_hide` 숨김시트 + `global_hide`(숨김) + 다단헤더(r1 그룹·**r2 라벨**·r3 옵션필수·r4~5 설명/예시).
- 매크로: **보이는 시트만**(xlSheetVisible — _hide/global_hide 자동 제외), "지침" 제외 → 각 시트 r2 라벨로 **id·*제품 이름·*제품 소매 가격·SKU 코드** 4컬럼 찾아 Sheet1에 이어붙임(startRow=5). Module2는 Sheet1 비우기(저장 Sub 아님). **숨은 저장/SaveAs 없음**(olevba 전수 확인).
- 정제본 = [알리상품번호·상품명·판매가·관리코드]. 골든은 이 정제본으로 마진 계산.

## 변경 (커밋: cmm 42d49e26 · page 8e9b577d)
- `core/workflows/channel_margin_monitor.py`:
  - **`_consolidate_parse(wb, cfg, con)` 신규**: 보이는 시트 순회(sheet_state=="visible"로 _hide/global_hide 제외)·skip_sheets 제외·header_row 라벨맵·data_start부터 labels 4종 추출·require_numeric_id로 예시'--' 제외. 배송비=ship_fee_const·즉시할인/포인트/정가/바코드 0/None.
  - `parse_download` 상단에 **`if cfg.get("consolidate"): return _consolidate_parse(...)`** 분기.
  - **알리 config**: commission 0.09 · ship_fee_const 0 · n_source "ref"(알리상품번호) · baseline_col 알리 · consolidate{header_row 2, data_start 5, skip_sheets[지침], require_numeric_id True, labels{상품번호:id, 상품명:*제품 이름, 판매가:*제품 소매 가격, 코드:SKU 코드}}. cols/sheet 미사용.
- `app/pages/6_채널마진모니터.py`: '신규만 추가' raw append를 **consolidate 채널은 스킵**(up_bytes 유지). append_rows_to_raw가 cfg['cols']['상품번호'] 참조 → 알리(cols 없음) KeyError 방지. CSV 머지(merge_listing)는 유지.

## 검증 (실데이터 run() — ALIPRODUCT 25시트 → 정제 322건 ↔ 골든 알리결과페이지 677행)
- 정제 재현: startRow=5+숫자ID필터 = 322건(예시'--' 25건 제거). 골든과 교집합 322·정제전용 0.
- **입력 전건 일치**: 관리코드(SKU코드) **322/322** · 상품명 **322/322** · 판매가(소매가) **322/322** · N(hapo 알리상품번호==골든N) **322/322**(골든 전체 677/677).
- 정산액==골든F **321/322**(1건 골든 중복ID 가격차 — last-write 아티팩트). base매입단가 314/320(비CB; 6 vintage). run: 322건·미매칭1·미설정3·마진미달15·제한34·평균마진율 10.1%.
- 수수료 **9%**(골든 F=판매가×0.91, 322/322·배송비 전건 0). baseline 알리 열 존재.

## 핵심 발견 (전용 함정 / 새 패턴)
- **알리 = 다중시트 정제형(consolidate)** — 단일시트 positional cols와 다른 새 parse 경로. 매크로(VBA)를 parse에 흡수.
- **숨김시트로 대상 구분**: `_hide`·`global_hide`는 openpyxl `ws.sheet_state!="visible"`로 제외(매크로 xlSheetVisible 동치). 보이는 카테고리 시트만 데이터.
- **다단헤더**: r2=필드라벨(id·*제품 이름·*제품 소매 가격·SKU 코드)·r5=예시('--'/'NKKE TEX 운동화'). data_start=5이나 require_numeric_id로 예시 제거(알리상품번호=16자리 숫자).
- 라벨 조회(positional 아님): 시트마다 컬럼 위치 달라도 안전. 관리코드=SKU코드(G), 상품명=*제품 이름(B 한글 클린), 판매가=*제품 소매 가격(E 텍스트 '13400.00'→_num).
- N=hapo(알리상품번호), 배송비0, 매입가 4-tier(SKU코드). 매입가 골든=base×N+700·실택배비3000 vs 우리 2700표준(의도적 차).

## 다음·상태
- **모니터 운영 가능. ⚠️ core+page 수정 → Reboot app 1회 필요.** listing은 첫 '상품관리 갱신(전체 교체)' 시 자동 생성(알리는 '전체 교체' 권장 — 주기적 전체 export). '신규만 추가'도 가능(CSV 머지로 카탈로그 누적, raw는 최신 유지).
- **미해결 — 알리 가격변경 미구현**: AliExpress 가격/재고 업로드도 동일 다중시트 양식(global_hide: excelActionType EXPORT·requestActionType newCustomPriceStock). 가격변경 양식 구조 확인 후 별도 추가.
- 7채널(스마트스토어·식봄·캐시노트·배민상회·쿠팡·올웨이즈·알리) 모니터. 가격변경은 6채널(알리 제외).

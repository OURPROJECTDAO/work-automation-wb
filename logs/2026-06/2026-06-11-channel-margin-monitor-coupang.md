# 2026-06-11 channel-margin-monitor: 쿠팡 채널 추가 (모니터 + 가격변경)

## 무엇
쿠팡 모니터 + 가격 일괄변경 한 번에. 신규 축: **가격변경 filter형**(다운로드 자체가 조회+변경요청 컬럼형). + `fake_jeong` 헬퍼 추출.

## 다운로드/골든 (price_inventory, 'data' 시트)
- r3=헤더, r4+=데이터. **키=옵션ID(C=3)** — 골든 조인키·hapo키(업체상품ID A는 multi-option, 499 ID에 2058 옵션). 코드=업체상품코드(F=6)·상품명=쿠팡노출상품명(G=7)·판매가=판매가격(J=10)·정가=할인율기준가(K=11). 즉시할인·포인트·바코드 없음.
- 정산: **수수료 12% 단일**(골든 G=판매가×0.88+배송비×0.967). **배송비 0**(골든 전건 0) → ship_fee_const 0. N=hapo(옵션ID). 4-tier 매입가. 실택배비 2700 표준(골든 3000/3700 미채택).
- 골든 매입가 fallback `RIGHT(관리코드,LEN-2)→재고기입 A→F`는 **미구현 불필요** — 접두붙은 코드는 이미 4-tier로 풀리고, 미매칭은 별개(아래).

## 변경 (work-automation-app)
- `core/workflows/channel_margin_monitor.py` (→628ef48)
  - CHANNEL_CONFIG['쿠팡']: commission 0.12 · ship_settle 0.967 · real_ship 2700 · **ship_fee_const 0** · baseline_col 쿠팡 · n_source "ref" · sheet data · header 3 · data 4 · cols{상품번호3(C 옵션ID),코드6(F),상품명7(G),판매가10(J),정가11(K)} · price_form{mode "filter", write{판매가16(P),정가17(Q)}}.
  - `fake_jeong(price, fake_cfg)` 헬퍼 추출(build_append_items가 호출) — 무늬용 가짜정가 표준 단일화.
  - `build_filter_price_xlsx(raw, rows, pids, cfg)`: 원본 다운로드에서 선택 옵션만 남기고 변경요청 컬럼 P=권장가·Q=가짜정가(FAKE_JEONG) 기입, R/S(판매상태/재고) 미기입, 미선택 삭제. 가짜정가 랜덤이라 **기입값 그대로 preview 반환**(미리보기-파일 일치).
- `app/pages/6_채널마진모니터.py` (→27a5bf8): 가격변경 버튼에 `mode=="filter"` 분기 — 저장된 원본(.xlsx)에서 build_filter, caption 별도. (append/filter/else(smartstore) 3분기.)

## 검증 (실데이터 골든 1989/1989)
- 모니터: 골든∩계산 1989/1989(옵션ID). 판매가 1989/1989·배송비(0) 1989/1989·**정산가(판매가×0.88) 1831/1831**·N(옵션ID) 1989/1989 일치. base 1815/1826(11 vintage). 미매칭 158(155건 관리코드 빈값)= **골든도 동일 미해결**(골든 매입가도 전건 NA) → 정상.
- 가격변경: 선택만 남김·P=권장가·Q=가짜(+20~30%)·R/S 공란·조회컬럼(J/K) 원본보존·**preview=파일 일치**. ast OK(core+page).

## 다음 / 상태
- 운영 가능. ⚠️ **core 수정 → Reboot app 1회**. 쿠팡 **'상품관리 갱신 → 전체 교체' 1회**(filter형은 저장된 원본 .xlsx에서 생성 — 미저장이면 안내 에러).
- 5채널(스마트스토어·식봄·캐시노트·배민상회·쿠팡) 모니터+가격변경 전부 운영. 다음: 알리.

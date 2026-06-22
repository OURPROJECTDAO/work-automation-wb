# 채널마진모니터 — 전월매출 2컬럼(이채널·전체) 추가 · 박스/낱개/소분 통일

## 무엇
6_채널마진모니터 표 맨 끝(권장가/제한 옆)에 **전월매출(이채널)** + **전월매출(전체)** 컬럼 추가.
가격 변경 의사결정 시 "이 상품이 이 채널/회사 전체로 전월에 얼마 팔렸나"를 바로 보게.

## 왜
권장가만 보고 가격을 바꾸면 판매 볼륨 맥락이 빠짐. 매출자료(천년경영 정산) 전월 실적을 옆에
띄워 "많이 파는 상품인지 / 이 채널에서 도는지"를 같이 보고 판단(사용자 요청).
★베이스(%)도 요청됐으나 **성능 우려로 사용자 보류**(두뇌④와 동일값 내려면 18개월 매출+주문
38만행+ship_alloc 실측이라 첫 로딩 십수 초). 전월매출만(파티션 1개=가벼움).

## 핵심 발견 (실데이터 검증)
- **매출자료(master/sales_*.parquet) 관리코드 = 박스코드 기준**. PC낱개·합포(-CB-)·소분 형태 **0건**
  (2026-05 10,053행 전수). 정산 시점에 이미 박스코드로 환원됨.
- 따라서 통일은 **listing 쪽만** 하면 됨 — listing 행 관리코드를 원박스로 정규화 → 매출자료(박스코드)와 join.
- 채널→매출자료 상호명: 1:1, 단 **쿠팡만 2개**(오픈마켓 쿠팡 (윙배송) + 쿠팡(로켓창고)) → 합산.

## 변경
- **core channel_margin_monitor.py `canonical_code(code, refs)`**(신규): 관리코드 원박스 정규화.
  소분→원코드 · PC낱개→그 상품코드 행의 관리코드 · 박스/합포/미매칭→자기자신. resolve_code 매핑 재사용.
- **page 6_채널마진모니터.py**:
  - `from core.dashboard import store` import.
  - `_load_refs()`(@cache): canonical용 reference 로드.
  - `_CH_TO_SANGHO`: 8채널키→매출자료 상호명(쿠팡=윙+로켓 리스트).
  - `_load_prev_sales()`(@cache): 적재 최신월 파티션(store.list_partition_months[-1]·read_partition)
    → (ym, {코드:전체매출}, {상호명:{코드:매출}}). _data_secret 재사용(data repo PAT).
  - df["전월매출"]/["전월매출(전체)"] = canonical로 lookup. DISPLAY·_col_config(prev_ym) 2컬럼.
- 매출 없으면 빈칸(None). **같은 canonical 여러 행(박스+낱개)은 같은 값** → 세로 합산 금지(행별 참고).

## 검증
- canonical_code 케이스: 박스 11-05-00→자기자신 · 낱개 PC005900→274-245-10-03 · 소분 BT10EA-25-40-02→25-40-02. ✅
- 채널→상호명 매핑 8채널 전부 매출자료에 존재(쿠팡 2상호명 OK).
- 배포 core import → 전 채널 전월매출 매칭(2026-05): 스마트259/식봄175/캐시125/알리114/쿠팡333/배민49/올86/ESM343 행 이채널매출 붙음, 전체매출은 더 많이(B2B 포함). 합리적.
- ast.parse OK. 커밋 core 9c265d12 · page 4aee8eb0.

## 다음 / 상태
- ✅ 운영 가능. ⚠️ **core canonical_code 신규 함수 → 페이지가 cmm.canonical_code 참조 → Reboot app 1회 필요**
  (안 하면 AttributeError). 전월매출 로더는 page-only지만 canonical 의존이라 Reboot 후 활성.
- "전월"=적재 최신월(현 2026-05, 6월분 7월초 적재되면 자동 6월로 롤).
- 베이스(%) 컬럼은 보류(성능). 추후 원하면 두뇌④ build_prod를 core 추출해 공용화 후 결합.
- data repo PAT(_data_secret) 없으면 두 컬럼 빈값(secrets [data] 필요 — 이미 1d listing 스냅샷에 쓰는 그 시크릿).

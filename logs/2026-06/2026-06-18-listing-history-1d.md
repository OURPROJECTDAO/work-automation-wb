# 2026-06-18 이력 1d — listing 가격 날짜본 스냅샷 적립

## 무엇
channel-margin-monitor '상품관리 갱신'(전체교체/신규추가)이 reference/listing_<key>.csv 를 덮어써 **채널 가격 역사 소실** → 커밋 직후 그 채널 listing 가격을 날짜본으로 private data repo에 적립. 1b(상품관리 재고 스냅샷·stock_history)와 완전 동형.

## 왜 (지금 만들 1순위 — forward-only 시급)
- cmm은 listing을 매 갱신 덮어쓰기만 → 매일 채널 가격 이력이 영구 소실 중. 1b 재고 스냅샷과 같은 "지금 안 모으면 못 되돌림" 자산.
- 두뇌③ 채널 가격 A/B는 현재 '서술'(현재 비교)만 — **가격변경 전후 효과(탄력성 인과)**는 listing 가격이 언제 얼마로 바뀌었는지 이력이 있어야 측정. 1d가 그 빠진 다리.
- 매핑 누적(시장가 매칭 146건 큐) 기다리는 세션에 병행 적합.

## 변경
- 신규 core `core/intelligence/listing_history.py`(stock_history 1b 동형):
  - `snapshot_from_recs(recs, channel, snap_date)` → 9컬럼(스냅샷일자·채널·상품번호·관리코드·판매가·정가·배송비·즉시할인·포인트)
  - GitHub R/W: read_listing_snapshots·list_listing_months·read_all_listing_snapshots·**ingest_listing_snapshot**(월 파티션 `snapshots/listing_YYYY-MM.parquet`·dedup키 (스냅샷일자·채널·상품번호) keep=last 멱등·base64 PUT)
  - **detect_listing_price_changes(snaps, threshold=0.0, fields=(판매가,정가))** — 채널×상품번호 연속 스냅샷 비교·threshold0=모든 실변동(0% 무변동 제외)·인상/인하. 두뇌③ A/B 전후 측정용.
  - 커밋 620f0a2.
- page `app/pages/6_채널마진모니터.py`:
  - import listing_history · `_data_secret()`([data] pat/repo 폴백·1b 훅 동형) · `_accumulate_listing(key, recs)`(비차단·toast·실패해도 listing 저장은 완료)
  - `if committed is not None:` 블록에서 `_accumulate_listing(key, committed)` 1회 호출(전체교체/신규추가 공통·committed는 커밋 시에만 set·재실행 멱등).
  - 커밋 dd34ab7.

## 검증
- core ast.parse OK + 합성 스모크: 공백 상품번호 제외·snapshot 9컬럼·**판매가 +10% 인상 1건 정확 탐지**(0% 무변동 제외)·dedup 멱등.
- page ast.parse OK·훅 호출/헬퍼 위치 확인.
- ★ 0% 무변동 버그 발견·수정: threshold=0이 rate.abs()>=0으로 무변동 포함 → `(rate != 0)` 가드 추가.

## 다음·상태
- 완료. **⚠️ 신규 core(listing_history) import → 재배포 후 Reboot app 1회** 필요(모듈캐시). Reboot 후 cmm '상품관리 갱신' 1회 실행 → toast '📚 listing 가격 스냅샷 적립' 확인. forward라 적립 시작일부터 누적(둘째 갱신부터 가격변경 탐지 가능).
- 다음 한 수 후보: ① 1e 행사 로깅(forward·식봄 2026-07 기획전 임박 시 그 행사부터) ② 두뇌③ A/B 가격변경 전후 결선(1d 이력 쌓인 뒤) ③ 시장대비 권장가(시장가 매칭 누적 후).

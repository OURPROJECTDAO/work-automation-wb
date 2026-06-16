# 2026-06-17 — 데일리 대시보드 확장판②: 이상치 → 채널 가격변경 시트 연결

## 무엇
당일 마진 점검 이상치 표에 (1) **권장가(채널 기준마진 달성 판매가)** 컬럼 + 현재가, (2) **체크박스 선택 → 단일 채널 가격변경 시트 다운로드**(cmm 빌더 재사용) 추가.

## 왜
이상치 보고 → 그 자리에서 기준마진 맞는 가격으로 일괄 변경 시트까지. 사용자: "기준에 맞는 판매가 보여주고, 채널 가격변경 시트랑 연결". 표는 채널 혼재라 시트는 채널별 → 단일채널 가드.

## 변경 (코드 — app repo, page-only)
- `app/pages/0b_데일리대시보드.py`:
  - import `core.workflows.channel_margin_monitor as cmm`.
  - `_cmm_listing(channel)` cached — listing_<key>.csv → csv_text_to_recs → compute_listing(baseline_override=라이브 baseline). `_cmm_baseline_text` cached.
  - `_reco_lookup(channels)` → {(채널,관리코드NFC):(권장가표시,현재가표시)}. 1관리코드 다listing이면 min~max 범위 문자열. **판매가 기준 권장가**(compute '권장가').
  - 이상치/전체 표: 현재가·권장가(채널기준) 컬럼 추가 + `st.dataframe(on_select="rerun", selection_mode="multi-row")` 체크박스 선택.
  - 선택 행 채널이 2종+/0종 → "한 채널만 가능" 경고. 단일 채널 → `_do_price_change` → `_gen_price_form`(mode append/filter/smartstore 디스패치, cmm.build_append_items+build_price_form_append / build_filter_price_xlsx / compute_new_prices+build_bulk_price_xlsx 그대로) → 다운로드+preview.
  - pids = 그 채널 listing rows 중 선택 관리코드인 상품번호(1관리코드→다listing 모두 포함).

## 검증
- cmm 시그니처 대조(코드 read): build_append_items(pf,rows,recs,pids)→(items,preview,skipped) · build_price_form_append(template_bytes,items,pf) · build_filter_price_xlsx(raw,rows,pids,cfg)→(bytes,prev,skipped,missing) · compute_new_prices(rows,recs,set)→(np,skipped) · build_bulk_price_xlsx(raw,np,cfg)→(bytes,kept,missing) · compute_listing(recs,channel,str(_REF),baseline_override=). 권장가/판매가/관리코드 키 compute 출력에 존재 확인.
- ast.parse 통과(anchor assert count==1 ×3).
- 채널명: daily SHEET_TO_CMM 값(스마트스토어·ESM·식봄·배민상회·올웨이즈·캐시노트·쿠팡·알리) == cmm CHANNEL_CONFIG 키. 알리=price_form 없음→"미지원" 안내.

## 다음 · 상태
- 상태: 배포 커밋 완료(page-only). **page-only이라 Reboot 불요 예상**(안 보이면 1회). 실사용 확인 대기.
- ⚠️ 권장가/현재가·시트 생성은 그 채널 listing(channel-margin-monitor 저장본) 의존 → 최신이어야 정확. 없으면 권장가 공백/안내. 쿠팡·스마트스토어는 raw .xlsx('전체 교체') 필요. 알리 미지원.
- KB: workflows/daily-dashboard.md 섹션·state·systemmap daily-dashboard(consumes listing_x8·roadmap done).

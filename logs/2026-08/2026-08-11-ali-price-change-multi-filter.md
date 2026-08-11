# 2026-08-11 — 알리(AliExpress) 가격 일괄변경 양식 추가 (multi_filter형)

## 무엇 / 왜
채널마진모니터에서 **알리만 가격 일괄변경이 미구현**이었다(2026-06-12 채널 추가 시 모니터만, 2026-06-16 로드맵에서 "당장 계획 없음"으로 폐기). 사용자 요청 = 알리도 상품 선택 → 가격 일괄변경 양식(.xlsx) 생성.

**착수 전 실측한 현재 동작**: 알리 config에 `price_form`이 없어 페이지가 마지막 `else`(스마트스토어 bulk)로 떨어지고, `build_bulk_price_xlsx`가 `cfg["cols"]`를 찾다가 **`KeyError: 'cols'`** — 즉 버튼을 누르면 양식이 아니라 트레이스백이 떴다. (알리는 consolidate 채널이라 `cols` 자체가 없음. 게다가 `compute_new_prices`는 없는 '즉시할인' 칸에 차액을 넣으려 해 값도 틀렸다.)

## 설계 판단
AliExpress는 **가격 수정도 신규 등록과 같은 대량등록 양식**(ALIPRODUCT, 카테고리별 다중시트)을 쓴다 → 별도 템플릿을 만들 게 아니라 **이미 저장해 둔 원본 raw(`reference/listing_ali.xlsx`)를 재사용**하는 게 정답. 쿠팡 `filter`형과 같은 발상이되 시트가 여러 개라 신규 모드 `multi_filter`로 분리.

**openpyxl 대신 zip 수술**을 택한 이유(쿠팡 사례와 이유는 다름): 이 양식은 `workbookProtection lockStructure="true"` + 시트별 `sheetProtection password` + `dataValidations`(OFFSET으로 `*_hide` 숨김시트 참조)를 갖고 있어 라운드트립이 이들을 변형/유실시킬 위험이 있다. (참고: 이 파일은 sharedStrings가 비어 있고 전 셀이 이미 `t="inlineStr"` — 쿠팡식 sharedStrings 정규화는 불필요.)

## 변경
- **core `channel_margin_monitor.py`** (커밋 `dfa72d70`)
  - `CHANNEL_CONFIG["알리"]`에 `price_form {mode:"multi_filter", price_label:"*제품 소매 가격", price_decimals:2}` 추가.
  - **`build_multi_filter_xlsx(raw, rows, pids, cfg)`** 신규 — 보이는 시트(숨김·skip_sheets 제외 = parse와 동일 기준)마다 ① `data_start` 이전 행과 **비숫자 id 예시행('--') 보존** ② 숫자 id 행 중 **선택분만 남기고 연속 재번호** ③ 가격 컬럼만 `'21200.00'` 텍스트로 교체. **컬럼은 헤더행(r2) 라벨 조회**로 찾는다(시트별 열 순서 상이 대비). 라벨이 없는 시트는 손대지 않음.
  - 헬퍼 `_sheet_parts`(workbook.xml 순서대로 [(시트명, 파트, state)]) · `_set_text_cell`(inlineStr 기입·스타일 `s=` 보존) 신규.
- **page `6_채널마진모니터.py`** (커밋 `c207b256`) — `multi_filter` 분기 + 안내 캡션. **`native_raw`에 multi_filter 포함** → 알리도 '신규만 추가' 비활성('전체 교체'만). 다중시트라 raw 병합이 불가능해 부분 export가 raw가 되면 가격변경 양식에서 나머지 상품이 통째로 누락되기 때문.
- **page `0b_데일리대시보드.py`** (커밋 `aa1ec33d`) — `_gen_price_form`에 `multi_filter`/`csv_filter` 분기 추가 + `_supports_price_change` 주석/안내 갱신. ★ 덤으로 **자사몰(카페24) 잠복 크래시 제거**: csv_filter는 분기가 없어 bulk 폴백으로 떨어져 `cols['즉시할인']` KeyError가 날 경로였다(데일리 이상치 → 가격변경 시트 생성 시).

## 검증 (실데이터 골든)
- listing_ali 312건 → 권장가 보유 308. **선택 16건**(권장가 없는 4건 포함) → 기입 12 · 제외 4 · 누락 0.
- **zip 파트 대조 59/59**: 변경분 = **보이는 시트 25개뿐**. 숨김 26개·styles·workbook.xml·[Content_Types] 전부 바이트 동일.
- **셀 단위 무손실**: 남긴 행은 **E(가격) 외 전 셀 원문 동일**, 스타일(`s="64"`)·행 속성(`ht`/`customHeight`) 보존, 행번호만 연속 재번호(예: 원본 r7·r36 → r6·r7).
- 선택 0건 시트(콜라 등)는 헤더 r1~5만 잔존(데이터 0행).
- **라운드트립 재파싱**(`parse_download` consolidate) **12/12**, 판매가 = 권장가 정확 반영. openpyxl `load_workbook` 로드도 정상.
- 세 파일 `ast.parse` 통과.

## 다음 / 상태
- ⚠️ **재배포 + Reboot app 1회 필요** — core(`channel_margin_monitor`)에 함수가 추가됐고 페이지가 그 새 함수를 참조한다(모듈 캐시 → Reboot 없으면 `AttributeError`).
- ⚠️ **알리 실업로드 미검증** — 알리 대량등록에 실제로 올려본 적 없음. 형식이 원본 export의 부분집합이라 구조적 위험은 낮지만, 첫 업로드 결과 확인 필요. 거부되면 다음 후보: ① 선택 0건 시트도 통째로 남길지/뺄지 ② 예시행('--') 제거 여부 ③ 가격 셀을 숫자형으로.
- 전제: 가격변경 양식은 **저장된 raw** 기준이므로 알리는 앞으로 '상품관리 갱신 → **전체 교체**'만 사용(신규만 추가는 비활성화됨). raw가 오래됐으면 선택 상품이 '누락'으로 보고된다.
- 로드맵상 "알리 가격변경"은 2026-06-16에 폐기 처리돼 있었음 → 이번에 구현으로 해소.

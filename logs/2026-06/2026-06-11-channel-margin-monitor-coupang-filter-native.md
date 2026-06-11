# 2026-06-11 channel-margin-monitor — 쿠팡 가격변경 filter 네이티브 zip 수술

## 무엇/왜
사용자 제보: 쿠팡 가격변경 양식 출력(실패본)이 쿠팡 업로더에서 **에러로 거부**, 골든본(성공)과 비교 요청. 두 파일 데이터(T2: row4, P=27700·Q=가짜정가)는 동일, **포맷만 차이**.
- 실패본 = openpyxl 3.1.5 산출: **전 셀 inlineStr**(`<is><t>`), sharedStrings.xml 없음, XML 선언 없음.
- 골든본 = 쿠팡 네이티브: **sharedStrings + `t="s"`**, P/Q = `t` 없는 숫자(`<c r="P4" s="2"><v>27700</v></c>`), mergeCells·phoneticPr·네임스페이스·XML선언 보존.
- 원인: `build_filter_price_xlsx`가 `load_workbook→wb.save()`로 라운드트립 → **openpyxl이 로드된 문자열 셀을 전부 inlineStr로 재직렬화**(실측 확인). 쿠팡 업로더(엄격 파서)가 inlineStr 거부.
- '전체 교체' 저장본 raw는 페이지 189행 `_commit_raw(key, up_bytes)`로 **업로드 바이트 그대로**(=네이티브) 저장돼 있음 → 원본은 네이티브인데 openpyxl 저장이 망가뜨린 것.

## 변경 (core/workflows/channel_margin_monitor.py)
- **build_filter_price_xlsx 전면 교체: openpyxl 저장 제거 → zip레벨 수술**(네이티브 포맷 보존).
  - 원본 sheet xml을 prefix/rows/suffix로 분리, 헤더행(r<data_start) 그대로, **선택 데이터행만 남겨 data_start부터 연속 재번호**, P(16)·Q(17)에 숫자 기입(`t` 없는 네이티브형, 기존 셀 스타일 보존). `<dimension>` 갱신. sharedStrings·styles·mergeCells·네임스페이스·XML선언 전부 원본 유지.
- **신규 헬퍼**: `_col_letter`·`_col_idx`·`_sheet_part`(workbook+rels로 시트 xml 해소, 폴백 첫 시트)·`_read_sst`·`_cell_in_row`·`_cell_text`(t="s"=sst조회/inlineStr/숫자/빈칸)·`_set_num_cell`(셀 숫자 기입·부재시 컬럼순 삽입)·`_renumber_row`. 키 해소 시 `_deflo`도 적용.

## 검증
- 합성 네이티브 raw(데이터 2건, P/Q 빈칸)로 end-to-end:
  - 1건 선택 → 출력: sharedStrings 보존·inlineStr 0·`t="s"` 존재·XML선언·mergeCells 보존, 미선택행 드롭, 행 1~4 연속, P4=권장가(`t`없는 숫자)·Q4=가짜정가, dimension A1:S4. openpyxl 재판독 정상(C4 옵션ID·P4·Q4).
  - 둘 다 선택 → 행 4·5 연속. 두번째만 선택 → 원래 r5가 r4로 당겨짐(재번호 정상). 권장가없음→skip, 원본없음→missing 동작 유지.
- **실제 골든 직접 대조**: 골든 P/Q 비운 단일행을 raw로 → 출력 row4가 **골든 row4와 완전 일치**(랜덤 Q값만 정규화 후 동일), **파트 목록 골든과 동일**(추가/누락 0). 바이트 레벨 네이티브 일치.
- ast.parse OK.

## 다음/상태
- **Reboot app 1회 필요**(core 수정).
- **전제: 쿠팡 raw가 네이티브여야 함**. '전체 교체'는 업로드 바이트 그대로 저장(네이티브) → OK. 단 **'신규만 추가'는 `append_rows_to_raw`가 openpyxl 저장 → raw가 inlineStr로 변질** → 그 raw로 만든 filter 출력도 inlineStr가 됨. **쿠팡은 '상품관리 갱신 → 전체 교체'를 사용**(신규만 추가 지양). (개선 후보: append도 zip 수술로 네이티브 보존.)
- 스마트스토어 bulk(build_bulk_price_xlsx)도 openpyxl 저장이라 inlineStr 산출이나 사용자 미제보(스마트스토어 업로더는 수용 추정). 필요 시 동일 수술 적용.

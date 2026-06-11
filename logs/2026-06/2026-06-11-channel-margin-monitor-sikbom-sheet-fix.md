# 2026-06-11 channel-margin-monitor — 식봄 시트명 KeyError 수정

## 무엇
parse_download 시트 선택을 `_pick_ws` 헬퍼로 교체(명시 시트 없거나 부재 시 첫 시트 폴백). 4곳(parse_download·build_bulk_price_xlsx·append_rows_to_raw×2) 일괄 적용.

## 왜
배포 후 식봄 '상품관리 갱신' 업로드 시 `KeyError: Worksheet 식봄붙여넣기 does not exist`. 분석 샘플은 '식봄붙여넣기' 탭(붙여넣기 가공본)이었으나 **실제 식봄 신규 다운로드의 시트명이 다름** → 하드코딩 `wb[cfg["sheet"]]` 가 크래시.

## 변경
- `core/workflows/channel_margin_monitor.py` (4968420): `_pick_ws(wb,cfg)` 추가 — cfg['sheet'] 있고 존재하면 그 시트, 아니면 첫 시트. 시트선택 4곳 교체. cfg['sheet']는 이제 '있으면 우선' 힌트.

## 검증
- ast.parse OK.
- 식봄 샘플: 명시시트 일치 485행 / 시트명 변경(불일치) 폴백 485행 동일. compute 통계 동일(미설정11·마진미달22·평균8.83%).

## 다음 · 상태
- **Reboot app 1회 필요**(core 수정). 리부트 후 식봄 상품관리 갱신 재시도.
- 단일시트 가정: 식봄 다운로드가 다중시트면(현재 아님) 첫 시트가 데이터 시트인지 재확인 필요. 그 경우 cfg['sheet']에 정확명 지정.

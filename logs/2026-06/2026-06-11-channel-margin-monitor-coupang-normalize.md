# 2026-06-11 channel-margin-monitor — 쿠팡 가격변경 수술 출력 sharedStrings 정규화 (네이티브 보장)

## 무엇
치유본 커밋 후에도 쿠팡 가격변경 출력이 여전히 inlineStr → 업로드 실패. 원인 = 앱이 가격변경 생성 시 **치유된 raw가 아니라 옛 오염 raw를 사용**(GitHub raw API/CDN 캐시 또는 미재배포). 사용자가 실패 파일을 엑셀 "값만 붙여넣기"로 정규화하니 업로드 성공(=골든) → 진짜 거부원인이 **inlineStr 확정**. 근본 해결: `build_filter_price_xlsx`가 raw 상태와 무관하게 **항상 sharedStrings로 출력**하도록 정규화 추가.

## 왜
- 실패 파일(티5실패) 데이터행 = `t="inlineStr"` s=11, sst uniqueCount 19(=옛 오염 raw 시그니처). 골든(티5골든, 값붙) = `t="s"` s=5, 행속성 spans/ht 有.
- 직전 raw 치유는 정확했으나(`reference/listing_coupang.xlsx` sst 5694) 앱이 옛 raw(sst 19)를 읽음 → 수술이 inlineStr 그대로 보존 → 출력 inlineStr.
- 즉 "raw가 네이티브여야 한다"는 전제가 캐시/배포 타이밍에 깨짐. 수술이 전제에 의존하는 한 취약.

## 변경 (core/workflows/channel_margin_monitor.py)
- 신규 헬퍼 `_inline_cells_to_shared(row_xml, sst_blocks, text2idx)`: 행의 inlineStr 셀을 `t="s"`+`<v>idx</v>`로 변환(스타일 s= 보존, 빈 inlineStr→빈 스타일셀), sst_blocks/text2idx in-place 확장.
- `build_filter_price_xlsx` 재작성:
  - 원본 sharedStrings.xml의 `<si>` verbatim 추출 + 텍스트→인덱스 맵.
  - 남긴 데이터행마다 `_inline_cells_to_shared` 적용(P/Q 숫자 기입 전).
  - 출력 시 sharedStrings.xml **재구성**(원본 `<sst>` 선언/네임스페이스 보존, count=시트 t=s 참조수·uniqueCount=si 개수) 후 zip에 기록(verbatim 복사 아님).
  - sst 파트 부재 시 생성 가드(쿠팡에선 미발생).
- 결과: 원본 raw가 inlineStr(오염·구 스냅샷·stale 캐시)이든 native든 **출력은 항상 sharedStrings** = 엑셀 '값만 붙여넣기' 동치. 직전 raw 치유·'신규만 추가' 가드는 유지(모니터 read 깨끗·재오염 방지)나 가격변경은 이제 그에 의존 안 함.

## 검증
- `ast.parse` OK.
- **회귀(핵심)**: **오염(inlineStr) raw 입력** → 출력 inlineStr **0**, t=s 81, sst uniqueCount 46(=헤더19+신규27), P/Q 숫자, A4/C4(옵션ID) 값 무손실, 행수 헤더3+선택4. **골든 네이티브 포맷 일치.**
- native(치유) raw 입력 → 동일하게 inlineStr 0·t=s 출력(기존 sst 참조, uniqueCount 5694 carry).
- 출력 openpyxl 재로드 값 정상.

## 다음 · 상태
- ✅ 완료. **⚠️ core 수정 → Reboot app 1회 필요** (그래야 새 수술 로직 반영).
- Reboot 후: 쿠팡 가격변경 재생성 → 네이티브 출력(새 다운로드 불필요). raw 캐시/오염과 무관하게 항상 성공.
- 스타일 s=11(출력) vs s=5(골든 엑셀정규화)·행 height 차이는 잔존하나 cosmetic — 거부원인은 inlineStr뿐(골든 대조로 확인). 업로드 실패 시 재검토.
- 미구현(불필요): 미참조 sst 가지치기(native raw 입력 시 전체 sst carry — 유효·업로드 무영향).

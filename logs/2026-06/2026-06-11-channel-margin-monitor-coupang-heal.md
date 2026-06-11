# 2026-06-11 channel-margin-monitor — 쿠팡 가격변경 raw inlineStr 오염 치유 + '신규만 추가' 가드

## 무엇
쿠팡 가격변경 출력(T4)이 골든과 달리 **데이터행이 inlineStr** → 쿠팡 업로더가 값을 못 읽음("양식은 맞는데 데이터 못잡음"). 근본 원인 = 저장 원본 `reference/listing_coupang.xlsx`가 이미 inlineStr 오염. 무손실 치유 커밋 + 재발 방지 가드.

## 왜
- 골든: 데이터행 문자열 셀 `t="s"`(sharedStrings, 네이티브). T4: 동일 셀 `inlineStr`.
- 엑셀로 열면 동일(=양식 맞음)이나 쿠팡 업로더(Apache POI 엄격형)는 inlineStr 값을 못 읽어 행 매칭 실패(=데이터 못잡음).
- 진단: `listing_coupang.xlsx` 데이터행 1,311개(row 4~1315) 전부 inlineStr(15셀/행), 헤더행(1~3)만 `t="s"`. 이건 **`append_rows_to_raw`(openpyxl load→save) = '신규만 추가' 버튼**의 지문. 과거 쿠팡에 '신규만 추가'를 쓴 게 raw를 통째 변질.
- 네이티브 수술 `build_filter_price_xlsx`는 정상(라이브 — T4 sharedStrings가 raw와 바이트 동일 = 수술이 raw sst verbatim 보존, openpyxl이면 재생성). 수술이 **오염된 원본을 충실히 보존**해 출력도 inlineStr이 된 것.

## 변경
1. **raw 치유** (`reference/listing_coupang.xlsx`, 데이터 repo 아님 — app repo reference):
   - inlineStr 셀 `<c r=.. s=.. t="inlineStr"><is><t>TEXT</t></is></c>` → `<c r=.. s=.. t="s"><v>IDX</v></c>` (스타일 `s=` 보존). 빈 inlineStr → 빈 스타일 셀 `<c r=.. s=../>`.
   - sharedStrings 재구성: 기존 19 si verbatim 보존(헤더 t=s 참조 인덱스 불변) + 신규 5,675 append → uniqueCount 5,694, count 18,306. 공백 텍스트는 `xml:space="preserve"`.
   - sheet1.xml + sharedStrings.xml만 교체, 나머지 파트 verbatim repack(styles·theme·workbook·mergeCells 등).
2. **가드** (`app/pages/6_채널마진모니터.py`): `native_raw = cfg["price_form"]["mode"]=="filter"` 면 '신규만 추가' 버튼 `disabled` + 안내 caption. filter형(쿠팡)은 '전체 교체'(업로드 바이트 verbatim)만 → raw 재오염 차단.

## 검증
- 치유본: 잔존 inlineStr **0** / t=s 18,306. 파트 목록 원본과 동일.
- 무손실: XML 파싱 7개 표본행 비어있지않은셀 불일치 **0**; openpyxl 전수 로드 비교 **24,985셀 불일치 0**, 차원 A1:S1315 동일.
- **엔드투엔드**: 치유본 + 실제 `build_filter_price_xlsx`(6 옵션ID 선택) → 출력 inlineStr **0**, 전 데이터행 t=s, P/Q 숫자(7200·8900), sharedStrings 존재, 행=헤더3+선택6. **골든 네이티브 포맷과 동일.**
- page6.py `ast.parse` OK.

## 다음 · 상태
- ✅ 완료. **Reboot app 불필요** — 치유본=런타임 reference, page .py=자동반영, 네이티브 수술=이미 라이브.
- 사용자: 쿠팡 가격변경을 **다시 생성만** 하면 네이티브 출력(새 다운로드 불필요). 이후 갱신은 반드시 '전체 교체'(가드로 신규만추가 비활성).
- 주의: 다른 filter형 채널 추가 시 동일 가드 자동 적용(price_form.mode=filter 감지). append형(식봄·캐시노트·배민)은 영향 없음.

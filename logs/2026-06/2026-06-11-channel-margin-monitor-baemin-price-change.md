# 2026-06-11 channel-margin-monitor: 배민상회 가격변경 양식

## 무엇
배민상회 가격 일괄변경 양식('(배민)양식') 생성 추가. 선택 상품 → 권장가로 변경판매가(J) 채우고, 변경소비자가(H)는 무늬용 가짜 — 현재 마크업 유지.

## 사용자 지정
- "변경 소비자가가 가짜가격" — 소비자가는 무늬용(판매가+마크업). 양식 실물 28행 분석: **(H−J) == (G−I) 전건**, 즉 변경소비자가 = 변경판매가 + (현재소비자가−현재판매가). 이 카탈로그는 소비자가=판매가+6000 균일이라 전부 +6000.
- 캐시노트식 랜덤(jeong_fake) 아님 → **gap 유지**(jeong_gap) 신규 모드.

## 변경 (work-automation-app)
- `core/workflows/channel_margin_monitor.py` (→9e5e7fc)
  - 배민상회 extra_cols += 옵션번호(R=18)·옵션명(U=21) — 양식 C/D용(다운로드에만 있음).
  - 배민상회 price_form: append, baemin_price_template.xlsx, '(배민)양식', data 2. cols A상품번호·B상품명·C옵션번호·D옵션명·E관리코드·G현재소비자가·H변경소비자가·I현재판매가·J변경판매가. source(현재소비자가←정가·현재판매가←판매가 등). price_field 변경판매가, jeong_field 변경소비자가, **jeong_gap True**.
  - `build_append_items` jeong 3모드: jeong_fake(랜덤) / **jeong_gap(권장가+(정가−판매가), 정가≤판매가면 권장가)** / 기본(max 실정가).
- `reference/baemin_price_template.xlsx` (→eca7ecd): 업로드 양식 그대로(빌드 시 예시행 제거).

## 검증
- 표본 6건: H=J+(정가−판매가) 전건 일치(마크업 0인 상품은 H=J). A·C·D·E·G·I·J 정상 기입, 예시행 제거.
- 옵션번호/옵션명/수수료raw listing 라운드트립 보존.
- 식봄(실정가)·캐시노트(랜덤)·배민상회(gap) 3모드 분기 합성 확인 PASS. ast OK.

## 다음 / 상태
- 운영 가능. ⚠️ **core 수정 → Reboot app 1회**. 배민상회 **'상품관리 갱신 → 전체 교체' 1회**(옵션번호/옵션명/수수료raw 채움 — 가드가 빈 경우 경고). 이후 선택→양식 생성→업로드.
- 4채널(스마트스토어·식봄·캐시노트·배민상회) 모니터+가격변경 전부 운영.

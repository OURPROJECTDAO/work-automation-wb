# 2026-06-11 channel-margin-monitor — 식봄 가격변경 양식(append)

## 무엇
식봄 가격 일괄변경을 '상품 일괄수정' 양식 append 방식으로 구현. 정가를 listing에 저장하도록 배선. 핵심: build_price_form_append + price_form cfg + 페이지 분기 + 템플릿 커밋.

## 왜
식봄 다운로드는 '다운로드 전용(수정·업로드 불가)' → 업로드는 별도 '상품 일괄수정' 양식. 스마트스토어처럼 다운로드에 덮어쓰는 filter 방식이 불가. 사용자 제공 양식(식봄_가격변경_양식.xlsx)에 선택 행만 채워 넣는 append 필요. "행 삭제 개념은 스마트스토어와 동일, E열은 n 고정"(사용자).

## 양식 구조 (실파일)
`(식봄)양식` 시트: r1~3 안내·r4~6 헤더/설명·r7+ 데이터. A상품no·B상품코드·C상품명·D정가·E수량별설정·F판매단가. 변경불가=A/B/C, 필수=D/E/F. D정가 ≥ F판매단가 제약.

## 변경
- `core/workflows/channel_margin_monitor.py` (ca608fb):
  - 식봄 cfg: cols에 정가=16 추가 + `price_form`(mode append·template sikbom_price_template.xlsx·sheet '(식봄)양식'·data_start 7·cols·fixed{5:'n'}).
  - `build_price_form_append(template,items,pf)`: 템플릿 데이터행 전부 제거 → 선택 행만 기입(A상품번호·B코드·C상품명·D정가=max(정가,판매단가)·E='n'·F판매단가=권장가). keep_last 초과 row_dimensions 정리(빈행 방지).
  - 정가 배선: parse_download(정가 _opt) · compute(row 정가) · LISTING_COLS '정가' · recs_to_csv/csv_text_to_recs 정가. 스마트스토어는 정가 col 없어 0(무영향).
- `reference/sikbom_price_template.xlsx` (75671ef): 사용자 제공 양식 그대로 커밋(예시행은 build가 제거).
- `app/pages/6_채널마진모니터.py` (0e77e15): 가격변경 버튼 분기 — cfg.price_form 있으면 append(템플릿 reference/에서 로드·새판매단가=권장가·정가 보존), 없으면 기존 filter. 미리보기/캡션 식봄용.

## 검증
- ast.parse OK(core·page). 정가 listing 라운드트립 보존(28400→28400). 스마트스토어 회귀 무영향.
- 식봄 양식 생성: 선택 5건 → 헤더 6행 보존 + 데이터 7~11행, A/B/C/D/E/F 정확. **정가≥판매단가 & E='n' 전부 충족**, 예시행(466427 등) 제거됨, max_row=11.

## 다음 · 상태 (세션 종료)
- **Reboot app 1회 필요**(이 세션 core 수정 누적: 식봄 채널·시트폴백·PC재고·정가/양식). 리부트 후 식봄 모니터+가격변경 사용 가능. 페이지 .py(컬럼 help·양식 분기)는 자동반영.
- **식봄 정가 보존하려면 식봄 '상품관리 갱신 → 전체 교체' 1회**(listing에 정가 채움). 안 하면 정가=판매단가 fallback.
- 식봄 가격변경 양식 정가 미세조정(정가>판매단가 마케팅 취소선 유지 정책)은 추후. 다음 채널=캐시노트/쿠팡/알리(다운로드 샘플+레시피).

# 2026-06-05 송장처리 — 채널 포맷/스키마 일반화 + 올웨이즈(.xlsx) 추가

## 무엇
invoice-fill 워크플로우를 채널별 포맷·스키마 설정 기반으로 일반화하고, 2번째 채널 **올웨이즈** 추가.

## 왜
올웨이즈 처리전 샘플(올웨이즈20260605배송.xlsx) 확인 결과 식봄과 양식이 크게 달라 한 줄 추가 불가:
- 포맷 .xlsx(식봄 .xls), 안내문 행 없음(식봄 r1 있음), match_col=주문아이디(UUID), 합포 주소=주소·수령인=수령인, 송장 컬럼='운송장번호'(식봄 '송장번호').

## 변경 (work-automation-app)
- `core/workflows/invoice_fill.py`:
  - CHANNEL_CONFIG 스키마 확장: format/courier_col/invoice_col/addr_col/recv_col/has_guide_row 추가. 식봄·올웨이즈 2채널 등록.
  - `parse_template(bytes,cfg)` 포맷 분기: `_parse_template_xls`(기존), `_parse_template_xlsx` 신규(안내문 없음, 빈행 미스킵=인덱스 정렬).
  - `write_template(orig_bytes,parsed,rows,keep,cfg)` 포맷 분기: `_write_template_xls`(xlwt, cfg 기반 invoice_col/courier_col), `_write_template_xlsx` 신규(openpyxl 원본 in-place 편집: 송장·택배사 기입 후 N/A 행 아래→위 delete_rows).
  - `find_consolidation_candidates(rows,cfg)`·`_recv(r,cfg)`: addr_col/recv_col 설정화.
- `app/pages/5_송장처리.py`: 업로더 type=cfg.format, parse_template(orig,cfg), 원본 bytes를 if_work에 저장(xlsx in-place 편집용), 합포 표시·na_rows를 cfg 컬럼 기반, 출력 확장자/MIME 포맷별.

## 검증 (로컬, 실파일+합성 마스터)
- **올웨이즈 e2e**: 실파일 13행 파싱 → 매칭3+합포1=keep4, N/A9 삭제. 되읽기: 운송장번호 전부 number('....0' float·int 모두 정수화), 택배사 전부 한진택배, 합포행 박스 송장 복사 확인, 원본 서식 보존(in-place).
- **식봄 회귀(.xls)**: 합성 .xls e2e — 안내문행·시트명 보존, 송장 number, 택배사 한진택배, N/A 삭제 정상.
- 두 파일 ast.parse 통과.

## 주의 / 다음
- import 모듈(invoice_fill.py) 변경 → **Streamlit Reboot 필요**. 페이지는 자동 반영.
- Reboot 후 실제 올웨이즈 처리전 + 당일 마스터로 재검증(사용자). 특히 **master_key 가정**(올웨이즈 주문아이디 ⟷ 마스터 주문번호): 0 매칭이면 마스터의 올웨이즈 주문아이디 보관 컬럼명 알려주면 cfg.master_key 수정.
- 올웨이즈 courier는 샘플상 한진택배 일괄. 다르면 cfg.courier 수정.
- (백로그) test_invoice_fill.py에 올웨이즈 xlsx 케이스 + N/O 타입 단언 추가.

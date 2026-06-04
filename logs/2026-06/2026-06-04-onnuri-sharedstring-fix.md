# 로그: 온누리양식_발주서 — sharedString → inlineStr 변환 버그픽스

## 무엇
제이티발주 출력 파일 헤더가 외부 사이트에서 인식 안 되는 버그 수정.

## 왜
사용자가 처리 결과를 외부 시스템에 업로드 시 헤더 인식 불가. 기대 형식 파일 제출.

## 근본 원인
openpyxl의 `load_workbook(file)` 후 `wb.save()` 실행 시,
원본의 sharedString 타입(`<c t="s"><v>인덱스</v></c>`) 셀이 모두
inlineStr 타입(`<c t="inlineStr"><is><t>한글엔티티</t></is></c>`)으로 변환됨.
- sharedStrings.xml 삭제됨
- 한글이 XML 엔티티(&#XXXXX;) 형태로 인코딩됨
- 일부 외부 시스템(JT 플랫폼 등)이 inlineStr 헤더 인식 불가

## 변경 (work-automation-app)
- `core/workflows/onnuri_order.py` `_save` 메서드 교체:
  - 기존: `shutil.copy2` + `openpyxl load_workbook(out).save()`
  - 신규: `zipfile`로 원본 xlsx 직접 열고 `sheet1.xml`의 합계 열만 패치
  - `_patch_column_values()` 함수 신규 추가 (정규식으로 셀 값만 교체)
  - `_col_num_to_letter()` 헬퍼 함수 추가 (1→A, 7→G 변환)
  - `shutil` import 제거, `zipfile·io·re` import 추가
  - `openpyxl.styles.Alignment` import 제거 (이제 사용 안 함)

## 검증
- zipfile 방식 처리 후 헤더 셀 전체 `t="s"` (sharedString) 유지 확인.
- sharedStrings.xml 존재 확인.
- 합계 열 값 정확히 교체됨 (99001→99001 등) 확인.
- 헤더 값 openpyxl로 재확인: `('NO', '발주일', '주문번호', ...)` 정상.
- 임포트 모듈 변경(io_excel 제거, 순수 stdlib) → Streamlit Reboot 필요.

## 주의
- `_load`는 여전히 openpyxl read_only → 영향 없음.
- 골든 15행 테스트는 파일 저장 방식 변경이므로 재검증 필요.

## 다음·상태
- 완료. Streamlit Reboot 후 실제 발주서 파일로 재검증 필요 (사용자).

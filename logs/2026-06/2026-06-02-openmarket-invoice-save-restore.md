# 로그: openmarket 송장출력 단독 저장 복원 (VBA SaveSheetToNewFile 유실)

## 무엇
오픈마켓합포도서산간확인 워크플로우에서, 정제 후 '송장출력' 시트를 별도
단일시트 xlsx(★★송장MMDD.xlsx)로 내보내는 단계를 복원.

## 왜
사용자 제보: 합포 송장 정제 후 "송장 파일을 저장"하는 과정이 웹 이관 중 유실된 듯.
원본 .xlsm VBA 실물 재확인으로 사실 확인:
- Module0p5.SaveSheetToNewFile() / OC_Module.OC_SaveSheetToNewFile()
  = '송장출력' 시트만 새 워크북에 ws.Copy → ★★송장MMDD.xlsx 로 SaveAs
  (운영 경로 C:\Users\user\Desktop\★발주자료today\송장\, 중복 시 _N).
- OC_ 시리즈(8단계 정리본)에 OC_SaveSheetToNewFile 포함 → 정식 단계였음.
Python 이관 시 _save()가 5시트 멀티시트 1개만 생성 → 송장 단독 저장 통째 누락.
KB 8단계에도 미기재(분석 단계에서 이 Sub가 누락 채집됨).

## 변경 (work-automation-app)
- core/workflows/openmarket_merge.py: `generate_invoice_xlsx(invoice_df)->bytes` 추가
  (io import). 송장출력 시트 통째 복사 → 단일시트 워크북. logistics generate_archive_xlsx와 동형.
- app/pages/1_파일처리.py: 기존 "결과 파일 다운로드" 버튼 뒤에
  "📥 송장 파일 다운로드 (★★송장)" download_button 추가. file_name=★★송장MMDD.xlsx.
- 커밋 579110c9 / 6f127816.

## 검증
- 라운드트립: 단일시트 '송장출력', 컬럼/행/값 손실 없음. 송장번호 앞자리0·상품명 컴마 보존.
- 멀티시트 결과의 송장출력 시트 미변경 → 기존 골든 5시트 테스트 영향 없음.

## 다음·상태
- import 모듈 변경 → Streamlit **Reboot app 필요**(사용자). 페이지(.py)는 자동반영.
- VBA `_N` 중복카운터는 웹 미적용(브라우저가 (1) 처리). 로컬 경로 C:\... 도 웹 무의미.
- (선택) 실 입력으로 송장 파일 = 골든 송장출력 820행 1:1 대조 테스트 추가 가능.

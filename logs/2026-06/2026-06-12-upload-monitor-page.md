# 2026-06-12 — upload-monitor 독립 페이지 배포

## 무엇
- `app/pages/7_업로드감시.py` 신규 + streamlit_app.py 네비 등록.

## 변경
- 페이지: KPI(감시대상·업로드필요 합집합·품절처리 합집합) + 채널별 미업로드/품절 건수표(channel_summary) + 필터(채널 selectbox·상태·검색) + 8채널 매트릭스 st.dataframe(multi-row 선택, 재고금액 desc, 채널키→라벨 헤더) + CSV 다운로드(선택/현재화면, utf-8-sig).
- 마진모니터 페이지 컨벤션 재사용(_REF·core import·on_select rerun·filter_sig 키·column_config localized·다운로드). 단 마진모니터=채널1개 선택형 vs 업로드감시=8채널 매트릭스(뷰 다름).
- 표시 컬럼에 **상품코드** 포함(비판매 제외목록 유지용 — 잡음행 다수가 관리코드 공백).
- 네비: 마지막 그룹(대시보드·채널마진모니터 옆)에 `7_업로드감시` 추가, icon 📦.

## 검증
- ast.parse OK. 페이지 pandas 로직 실데이터 스모크(st 없이): KPI 감시대상1001·업로드필요(합집합)748·품절처리99, channel_summary 8행, 채널필터(스마트스토어 362)·검색('부탄'3)·rename·CSV 전부 정상.

## 다음 · 상태
- **코어+페이지 배포. ⚠️ core 신규 모듈(upload_monitor.py) 첫 배포 → Reboot app 1회 필요.**
- 다음 = ⑤ L4 핸드오프(스마트스토어·ESM 입력폼 prefill / 6채널 CSV) + 비판매 제외목록 편집 UI.

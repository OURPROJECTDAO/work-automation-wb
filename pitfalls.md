# 알려진 함정 / 주의 (작업 전 필독 — 프로토콜·환경·공통 데이터위생)

> **항상 읽는 슬림 세트.** 여기엔 매 세션 환경 운영에 필요한 것만 둔다.
> 상황별 패턴은 분리 → **Streamlit 앱 작업 / Excel 파싱 시 `patterns.md`** 를 읽을 것.
> 공유 자산 바꾸기 전 영향범위 → `manifest.md`. 워크플로우 전용 함정 → `workflows/<name>.md`.

## ## GitHub contents API (KB 저장소)
- 기존 파일 덮어쓰기: 먼저 GET으로 현재 sha 받아 PUT에 포함. 안 하면 409/422. 신규 파일은 sha 불필요.
- 읽기는 Accept: application/vnd.github.raw 헤더 → base64 아닌 raw 텍스트 직행(UTF-8). 기본 JSON 응답의 content는 base64+줄바꿈이라 디코딩 필요.
- PUT의 content는 base64 인코딩(줄바꿈 없이).
- 한글 파일명 API 경로: urllib.request는 한글 URL을 ASCII로 못 보냄. urllib.parse.quote(segment)로 퍼센트 인코딩 필수 (app/pages/1_파일처리.py 등).
- 대용량 파일 업로드(예: 10551행 csv): curl 명령줄이 "Argument list too long" → Python urllib으로 업로드.
- PAT은 비밀: repo·KB·로그에 절대 안 적음. 프로젝트 지식 파일에만. 만료 시 그 파일만 갱신. fine-grained(work-automation-wb + work-automation-app, contents 읽기·쓰기).

## 인코딩
- 한글은 UTF-8. base64 디코딩 시 Latin-1 금지(모지바케). raw 헤더로 받으면 디코딩 자체가 불필요.
- 향후 커스텀 Worker 만들 때 atob() UTF-8 미디코딩 버그 주의.

## Google Drive (엑셀 작업물 전용 — KB 아님)
- 커넥터 update/delete 없음, 생성+읽기만. 엑셀은 템플릿=읽기전용·결과=날짜별 새 파일이라 무방. 삭제는 사용자 수동.
- 읽기는 download_file_content(base64→UTF-8). read_file_content는 마크다운 변형(미리보기용).
- 파일 생성 시 contentMimeType + disableConversionToGoogleType=true.

## 보안 (업무 도메인)
- KB에 PII·비밀 금지(고객정보·자격증명·계좌·주문자정보). 식별자(주문번호/참조ID)만.
- 부수효과·되돌릴 수 없는 동작(발송·삭제·결제·권한·외부쓰기)은 정확한 payload(무엇을 누구에게) 보여주고 승인.

## 작업 규율 (투자시스템에서 배움)
- 검증 단계화: 변경 전 실물(템플릿/VBA/데이터) 재확인 → 변경 후 대조. KB는 길잡이지 진실의 원천 아님. 최고 ROI.
- 1작업단위 1로그. 막힌 것·미완·실패도 로그 "다음/상태"에 정직하게(작업>로그 지연이 제일 위험).
- VBA→Python 이관 시 **메인 단계 외 별도 모듈에 숨은 저장 Sub(SaveAs/Workbooks.Add/SaveCopyAs)** 누락 주의. 메인 흐름만 분석하면 빠짐. olevba 전체 추출 후 SaveAs|Workbooks.Add 류 전역 grep으로 채집. (openmarket 송장 단독 저장 SaveSheetToNewFile이 최초 이관 때 통째 누락된 사례 — logs/2026-06-02-openmarket-invoice-save-restore)

## openpyxl 행 삭제 (전 워크플로우 공통)
- **`delete_rows`는 셀만 지우고 `ws.row_dimensions`(행 높이/서식)는 남긴다** → 빈 `<row>` 요소가 sheet XML에 잔존. openpyxl max_row로는 안 보여도 외부 파서(플랫폼 업로드 등)는 빈 상품행으로 인식. 행 삭제 후 마지막 유효행 초과 `row_dimensions` 키를 직접 삭제할 것. (channel-margin-monitor 가격변경 양식, logs/2026-06-11)

## 한국어 처리 (엑셀/앱 — 전 워크플로우 공통)
- 주소·상품명 매칭 전 NFC 정규화 필수(unicodedata.normalize("NFC", s)). 출처 다른 데이터가 NFD(자모 분리)면 같은 글자라도 부분일치 매칭 실패 → 도서산간/미배송 매칭 치명적.
- **숫자 ID 키 정규화 (전 워크플로우 공통)**: openpyxl은 정수 ID 셀(예 상품번호 46903)을 **float(46903.0)**로 읽음. str()/NFC만 하면 '46903.0' → CSV/reference의 '46903' 키와 매칭 실패(조용히 미매칭=기본값). 정수값 float은 int화 후 키로 쓸 것(`int(v) if isinstance(v,float) and v.is_integer() else v`). (channel-margin-monitor 캐시노트 N 전건 1 오류 사례, logs/2026-06-11-cashnote)
- reference csv는 UTF-8-sig(BOM)로 저장. Excel에서 직접 열어도 안 깨짐.
- 대시보드 차트: matplotlib는 한글 폰트 미설치 시 □□□. Plotly/Altair(브라우저 폰트) 권장.
- 정렬: VBA xlPinYin vs Python 코드포인트 정렬 차이 가능 → 골든 파일 대조로 확인.

_갱신: 2026-06-11 (숫자 ID 키 정규화 함정 추가 — 캐시노트 사례)_
